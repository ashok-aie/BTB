# app/routes/spell_mastery.py
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func  
from pydantic import BaseModel
from app.dependencies.auth import require_login, get_current_user
from app.db.database import get_db
from app import models, schemas
from app.models import UserActivity, Word
from gtts import gTTS
import os
import hashlib
import random
from datetime import datetime
from pytz import timezone

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/spell_mastery")
def spell_mastery(request: Request, db: Session = Depends(get_db)):
    # Get a random word from the database
    words_query = db.query(Word).all()
    
        # Convert ORM objects to dict
    words = []
    for w in words_query:
        words.append({
             "id": w.id,
            "word": w.word or "",
            "part_of_speech": w.part_of_speech or "",
            "language_origin": w.language_origin or "",
            "definition": w.definition or "",
            "example": w.example or "",
            "root_word": w.root_word or ""
        })
    
    total_words = len(words)

    return templates.TemplateResponse(
        "spell_mastery.html",
        {
            "request": request,
            "words": words,
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

print('Hello')
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