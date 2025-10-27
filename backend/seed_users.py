from app.db.database import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = [
    {"username": "Admin", "email": "admin@example.com", "password": "admin123"},
    {"username": "Ashok", "email": "ashok@example.com", "password": "password123"},
    {"username": "Ruthsika", "email": "ruthsika@example.com", "password": "password123"},
]

def seed():
    db = SessionLocal()
    try:
        for u in users:
            hashed_pw = pwd_context.hash(u["password"])
            db_user = User(username=u["username"], email=u["email"], hashed_password=hashed_pw)
            db.add(db_user)
        db.commit()
        print("Users added successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
