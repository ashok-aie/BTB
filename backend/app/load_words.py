import csv
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.db.database import SessionLocal
from app.models.word import Word


def load_words_from_csv(file_path: str):
    db: Session = SessionLocal()
    try:
        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Build the insert statement with ON CONFLICT ... DO UPDATE
                stmt = insert(Word).values(
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

                # If the word already exists, update all fields
                update_dict = {
                    "part_of_speech": row['part_of_speech'],
                    "language_origin": row['language_origin'],
                    "definition": row['definition'],
                    "example": row['example'],
                    "prefixes_suffixes": row['prefixes_suffixes'],
                    "root_word": row['root_word'],
                    "grade_level": row['grade_level'],
                    "bee_level": row['bee_level'],
                    "lexical_level": row['lexical_level']
                }

                stmt = stmt.on_conflict_do_update(
                    index_elements=['word'],
                    set_=update_dict
                )

                db.execute(stmt)

            db.commit()
            print(f"✅ Loaded and updated data from {file_path} successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error loading words: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    load_words_from_csv("/Users/ashok/Documents/AAI/BTB-main/backend/app/data/word.csv")
    #/Users/ashok/Documents/AAI/BTB-main/backend/app/data
