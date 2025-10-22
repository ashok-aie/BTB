# app/routes/spell_mastery.py
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from gtts import gTTS
import os
import hashlib

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

WORDS = [
    {
        "word": "benevolent",
        "part_of_speech": "adjective",
        "origin": "Latin",
        "definition": "well meaning and kindly",
        "example": "She gave a benevolent smile.",
        "difficulty": "Medium",
    },
    {
        "word": "gregarious",
        "part_of_speech": "adjective",
        "origin": "Latin",
        "definition": "fond of company; sociable",
        "example": "He was a popular and gregarious man.",
        "difficulty": "Medium",
    },
]


@router.get("/spell_mastery")
def spell_mastery(request: Request):
    return templates.TemplateResponse(
        "spell_mastery.html", {"request": request, "words": WORDS}
    )

@router.get("/tts/")
def tts_audio(text: str):
    """Generate gTTS pronunciation for any text (word or sentence)."""
    os.makedirs("app/static/audio", exist_ok=True)
    # Hash filename so we can cache different sentences
    filename = hashlib.md5(text.encode()).hexdigest() + ".mp3"
    path = os.path.join("app/static/audio", filename)

    if not os.path.exists(path):
        tts = gTTS(text)
        tts.save(path)

    return FileResponse(path, media_type="audio/mpeg")

