import csv
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.models.word import Word

# Optional: create tables if they don't exist
#Word.metadata.create_all(bind=engine)

def load_words_from_csv(file_path: str):
    db: Session = SessionLocal()
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
            word = Word(
                word=row['word'],
                part_of_speech=row['part_of_speech'],
                language_origin=row['language_origin'],
                definition=row['definition'],
                example=row['example'],
                prefixes_suffixes=row['prefixes_suffixes'],
                root_word=row['root_word'],
                grade_level=row['grade_level'],
                bee_level=row['bee_level'],
                lexical_level=row['lexical_level']
            )
            db.add(word)
        db.commit()
    db.close()
    print(f"Loaded data from {file_path} successfully!")

if __name__ == "__main__":
    load_words_from_csv("/Users/ashok/Documents/AAI/LocalRepo/BTBee/backend/app/data/words.csv")
