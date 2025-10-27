from fastapi import FastAPI, Request, Depends, Form, APIRouter, Response
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from gtts import gTTS
from sqlalchemy.orm import Session
from sqlalchemy import text
from starlette.middleware.sessions import SessionMiddleware
from app.dependencies.auth import require_login, get_current_user
from app.routes import auth, quiz, spell_mastery, vocab_mastery, word_curing
from app.models import Word, UserActivity, User 
from app.db.database import engine, get_db 
from app import schemas, models
from app.schemas.word import WordSchema
import os
from app.routes.dashboard import get_dashboard_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
router = APIRouter()
app.include_router(auth.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Add a secret key for signing session cookies
app.add_middleware(SessionMiddleware, secret_key="supersecret123", max_age=3600)

# Mount templates
templates = Jinja2Templates(directory="app/templates")

# Include auth routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(quiz.router, tags=["quiz"])
app.include_router(spell_mastery.router)
app.include_router(vocab_mastery.router)
app.include_router(word_curing.router)


@app.get("/")
async def root():
    return RedirectResponse(url="/login")

# Landing page (after login)
@app.get("/landing")
def landing_page(request: Request, 
                 user = Depends(require_login), 
                 db: Session = Depends(get_db)):
    #user = get_current_user(request)
    # 👇 Check if user is actually a redirect response
    if isinstance(user, RedirectResponse):
        return user  # redirect to login if not authenticated

    user_id = user.get("id")
    username = user.get("username")

    dashboard_data = get_dashboard_data(db, user_id)

    return templates.TemplateResponse(
        "landing.html",
        {
            "request": request,
            "user": user,
            **dashboard_data  # expands all keys from get_dashboard_data()
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


@app.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("session")
    return response