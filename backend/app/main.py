from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from app.routes import auth, quiz, spell_mastery
from gtts import gTTS
#from app.routes import quiz
from app.db.database import engine  # or wherever your engine is defined
from sqlalchemy import text

app = FastAPI()

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
def landing_page(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/spell-mastery")
def spell_mastery_page(request: Request):
    return templates.TemplateResponse("spell_mastery.html", {"request": request})


@app.get("/test-db")
async def test_db_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return {"status": "success", "db_connected": True, "result": result.scalar()}
    except Exception as e:
        return {"status": "error", "db_connected": False, "error": str(e)}
    


