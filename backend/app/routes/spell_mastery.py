# app/routes/spell_mastery.py
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func  
from pydantic import BaseModel
from app.dependencies.auth import require_login, get_current_user
from app.db.database import get_db
from app import models, schemas
from app.models import UserActivity, Word, User
from app.routes.word_service import fetch_spell_mastery_words
from app.schemas import user_activity
from gtts import gTTS
import os
import hashlib
import random
from datetime import datetime
from pytz import timezone
import logging
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/spell_mastery")
def spell_mastery(request: Request, grade_level: str = None, db: Session = Depends(get_db)):
    # Fetch all words (optional, for template)
    words_query = db.query(Word).all()
    words = [
        {
            "id": w.id,
            "word": w.word or "",
            "part_of_speech": w.part_of_speech or "",
            "language_origin": w.language_origin or "",
            "definition": w.definition or "",
            "example": w.example or "",
            "root_word": w.root_word or ""
        }
        for w in words_query
    ]
    
    # Fetch words for Spell Bee Mastery
    words_selected = fetch_spell_mastery_words(db, grade_level=grade_level)
    words_selected_dict = [
        {
            "id": w.id,
            "word": w.word or "",
            "part_of_speech": w.part_of_speech or "",
            "language_origin": w.language_origin or "",
            "definition": w.definition or "",
            "example": w.example or "",
            "root_word": w.root_word or ""
        } 
        for w in words_selected
    ]

    total_words = len(words)

    return templates.TemplateResponse(
        "spell_mastery.html",
        {
            "request": request,
            "words": words,
            "words_selected": words_selected_dict,
            "total_words": total_words
        }
    )

@router.get("/tts/")
def tts_audio(text: str):
    """
    Generate and return a gTTS audio file for any given word or text.
    """
    os.makedirs("app/static/audio", exist_ok=True)
    filename = hashlib.md5(text.encode()).hexdigest() + ".mp3"
    path = os.path.join("app/static/audio", filename)

    if not os.path.exists(path):
        tts = gTTS(text)
        tts.save(path)

    return FileResponse(path, media_type="audio/mpeg")


# ----------------------------
# Pydantic model for JSON input
# ----------------------------
class CheckWordRequest(BaseModel):
    word_id: int
    user_input: str
    user_id: int = 3  # default to 3

# US/Eastern timezone object
eastern = timezone("US/Eastern")

# -------------------------------
# Route to check user's spelling
# -------------------------------
@router.post("/spell_mastery/check")
def check_word(req: CheckWordRequest, db: Session = Depends(get_db)):
    """
    Checks the user's spelling against the correct word, stores
    the activity in the database, and returns the result.

    Request JSON format:
    {
        "word_id": 1,
        "user_input": "example",
        "user_id": 3
    }
    """

    # 1. Fetch the word object from DB
    word = db.query(Word).filter(Word.id == req.word_id).first()
    if not word:
        # If the word is not found, return an error
        return {"error": "Word not found"}

    # Normalize both strings for comparison
    correct_word = word.word.strip().lower()
    user_word = req.user_input.strip().lower()

    # 2. Compare spelling
    is_correct = correct_word == user_word

    # 2. Compare the user's input (case-insensitive) with the correct word
    #is_correct = req.user_input.strip().lower() == word.word.lower()
    print(is_correct)

    # 3. Create a new UserActivity record
    activity = UserActivity(
        user_id=req.user_id,
        word_id=word.id,
        user_input=req.user_input,
        is_correct=is_correct,
        timestamp=datetime.now(eastern)  # timezone-aware timestamp
    )

    # 4. Add the record to the DB session
    db.add(activity)

    # 5. Commit the session to save the record permanently
    db.commit()

    # 6. Refresh the instance to get auto-generated fields (e.g., id)
    db.refresh(activity)

    # 7. Return the result along with the activity ID
    return {
        "success": True,
        "is_correct": is_correct,
        "activity_id": activity.id
    }


@router.post("/user_activity")
def record_activity(activity: user_activity.UserActivitySchema, db: Session = Depends(get_db)):
    logger.info("POST /user_activity received: %s", activity)
    print("Received activity raw:", activity)  # debug

    try:
        # Convert Pydantic model to dict and exclude None so DB server_defaults are preserved
        activity_dict = activity.model_dump(exclude_none=True)
        logger.debug("activity dict: %s", activity_dict)
        print("Activity dict ->", activity_dict)  # debug

        # Basic existence checks to avoid FK errors
        user_exists = db.query(User).filter(User.id == activity_dict.get("user_id")).first()
        if not user_exists:
            logger.warning("User id %s not found", activity_dict.get("user_id"))
            raise HTTPException(status_code=400, detail="user_id not found")

        word_exists = db.query(Word).filter(Word.id == activity_dict.get("word_id")).first()
        if not word_exists:
            logger.warning("Word id %s not found", activity_dict.get("word_id"))
            raise HTTPException(status_code=400, detail="word_id not found")

        # Build and persist
        new_activity = models.UserActivity(**activity_dict)
        db.add(new_activity)
        db.commit()
        db.refresh(new_activity)

        logger.info("✅ Saved activity id: %s", new_activity.id)
        print("✅ Saved activity id:", new_activity.id)

        return {"status": "success", "activity_id": new_activity.id}

    except HTTPException:
        raise  # re-raise intentional HTTP errors unchanged
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("💥 SQLAlchemy error saving activity")
        raise HTTPException(status_code=500, detail=f"DB error: {e}")
    except Exception as e:
        db.rollback()
        logger.exception("💥 Unexpected error saving activity")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
