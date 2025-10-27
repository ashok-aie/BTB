from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Word
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/vocab_mastery")
def vocab_mastery(request: Request, db: Session = Depends(get_db)):
    words_query = db.query(Word).all()

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
        "vocab_mastery.html",
        {"request": request, "words_selected": words, "total_words": total_words}
    )
