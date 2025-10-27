from fastapi import APIRouter, Request, Form, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.db.database import get_db
from app.models import Word
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/word_curing")
def get_word_curing_page(request: Request, db: Session = Depends(get_db)):
    words = db.query(Word).all()
    return templates.TemplateResponse("word_curing.html", {"request": request, "words": words})

@router.post("/word_curing/add")
def add_or_update_word(
    request: Request,
    db: Session = Depends(get_db),
    word_id: int = Form(None),
    word: str = Form(...),
    definition: str = Form(""),
    part_of_speech: str = Form(""),
    language_origin: str = Form(""),
    example: str = Form(""),
    root_word: str = Form("")
):
    if word_id:
        # Update existing word
        existing_word = db.query(Word).filter(Word.id == word_id).first()
        if existing_word:
            existing_word.word = word
            existing_word.definition = definition
            existing_word.part_of_speech = part_of_speech
            existing_word.language_origin = language_origin
            existing_word.example = example
            existing_word.root_word = root_word
    else:
        # Add new word
        new_word = Word(
            word=word,
            definition=definition,
            part_of_speech=part_of_speech,
            language_origin=language_origin,
            example=example,
            root_word=root_word
        )
        db.add(new_word)
    db.commit()
    return RedirectResponse(url="/word_curing", status_code=303)
