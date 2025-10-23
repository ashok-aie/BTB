from fastapi import FastAPI, Request, Depends
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from gtts import gTTS
from sqlalchemy.orm import Session
from sqlalchemy import text
from starlette.middleware.sessions import SessionMiddleware
from app.dependencies.auth import require_login, get_current_user
from app.routes import auth, quiz, spell_mastery
from app.db import database
from app.db.database import engine, get_db  # or wherever your engine is defined
from app import schemas, models
from app.schemas.word import WordSchema
import os
#from . import models, schemas, database

#app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "dev-key"))

app = FastAPI()
app.include_router(auth.router)
# Add a secret key for signing session cookies
app.add_middleware(SessionMiddleware, secret_key="supersecret123", max_age=3600)

# Mount templates
templates = Jinja2Templates(directory="app/templates")

# Include auth routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(quiz.router, tags=["quiz"])
app.include_router(spell_mastery.router)

# Login page
@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Landing page (after login)
@app.get("/landing")
def landing_page(request: Request, user: str = Depends(require_login)):
    return templates.TemplateResponse(
        "landing.html",
        {
            "request": request,
            "user": user
        }
    )

@app.get("/words/{word_id}", response_model=WordSchema)
def get_word(word_id: int, db: Session = Depends(get_db)):
    word = db.query(models.Word).filter(models.Word.id == word_id).first()
    if not word:
        return {"error": "Word not found"}
    return word

@app.get("/words/random", response_model=WordSchema)
def get_random_word(db: Session = Depends(get_db)):
    word = db.query(models.Word).order_by(models.func.random()).first()
    return word