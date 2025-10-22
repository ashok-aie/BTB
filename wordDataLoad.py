import csv
from app.db.database import SessionLocal
from app.models.word import Word

db = SessionLocal()

with open("words.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        word_obj = Word(**row)
        db.add(word_obj)
db.commit()
db.close()
