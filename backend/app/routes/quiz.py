from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.word import Word
from gtts import gTTS
import os
import random

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Step 1: Show form to pick number of words
@router.get("/spell-mastery", response_class=HTMLResponse)
def spell_mastery_start(request: Request):
    selected_words = random.sample(WORDS, k=min(10, len(WORDS)))
    #words = ["accommodate", "rhythm", "pharaoh", "necessary", "beautiful",
    #         "miscellaneous", "occurrence", "embarrass", "weird", "questionnaire"]
    return templates.TemplateResponse("spell_mastery.html", {"request": request, "words": selected_words})
    #return templates.TemplateResponse(
    #    "spell_mastery_start.html", {"request": request} )


# Step 2: Initialize quiz with chosen number of words
@router.post("/spell-mastery/start")
def spell_mastery_init(
    request: Request,
    num_words: int = Form(...),
    db: Session = Depends(get_db)
):
    all_words = db.query(Word).all()
    if not all_words:
        return {"error": "No words in DB"}

    num_words = min(num_words, len(all_words))
    quiz_words = random.sample(all_words, num_words)

    request.session = {
        "quiz_words": [w.id for w in quiz_words],
        "current_index": 0,
        "results": []
    }

    # Show first word
    return show_next_word(request, db)


# Helper to render next word
def show_next_word(request: Request, db: Session):
    quiz_words_ids = request.session.get("quiz_words", [])
    current_index = request.session.get("current_index", 0)
    results = request.session.get("results", [])

    if current_index >= len(quiz_words_ids):
        # Quiz complete
        return templates.TemplateResponse(
            "quiz_complete.html",
            {"request": request, "results": results, "db": db}
        )

    word_id = quiz_words_ids[current_index]
    word = db.query(Word).filter(Word.id == word_id).first()

    # Generate audio if missing
    audio_filename = f"temp_{word.word}.mp3"
    if not os.path.exists(audio_filename):
        tts = gTTS(text=word.word, lang='en')
        tts.save(audio_filename)

    return templates.TemplateResponse(
        "quiz.html",
        {
            "request": request,
            "word": word,
            "audio_url": f"/quiz/audio/{word.word}",
            "result": None,
            "quiz_complete": False
        }
    )


# Step 3: Submit answer and move to next word
@router.post("/spell-mastery/submit")
def submit_word(
    request: Request,
    word_id: int = Form(...),
    spelling: str = Form(...),
    db: Session = Depends(get_db)
):
    quiz_words_ids = request.session.get("quiz_words", [])
    current_index = request.session.get("current_index", 0)
    results = request.session.get("results", [])

    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        return {"error": "Word not found"}

    correct = word.word.lower() == spelling.strip().lower()
    results.append({"word_id": word.id, "correct": correct, "attempted_spelling": spelling})
    request.session["results"] = results
    request.session["current_index"] = current_index + 1

    return show_next_word(request, db)


# Serve audio
@router.get("/quiz/audio/{word_text}")
def serve_audio(word_text: str):
    filename = f"temp_{word_text}.mp3"
    if os.path.exists(filename):
        return FileResponse(filename, media_type="audio/mpeg")
    return {"error": "Audio not found"}


# Sample word dataset (you’ll later replace with DB)
WORDS = [
    {
        "word": "accommodate",
        "definition": "To provide lodging or sufficient space for.",
        "part_of_speech": "verb",
        "origin": "Latin",
        "difficulty": "medium",
        "example": "The hotel can accommodate up to 500 guests."
    },
    {
        "word": "rhythm",
        "definition": "A strong, regular repeated pattern of movement or sound.",
        "part_of_speech": "noun",
        "origin": "Greek",
        "difficulty": "hard",
        "example": "She moved in perfect rhythm with the music."
    },
    {
        "word": "beautiful",
        "definition": "Pleasing the senses or mind aesthetically.",
        "part_of_speech": "adjective",
        "origin": "French",
        "difficulty": "easy",
        "example": "The sunset was so beautiful that it took our breath away."
    },
]

