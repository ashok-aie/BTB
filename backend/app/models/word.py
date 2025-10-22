from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base

class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True)
    word = Column(String, unique=True, nullable=False)
    part_of_speech = Column(String)
    language_origin = Column(String)
    definition = Column(String)
    example = Column(String)
    prefixes_suffixes = Column(String)
    root_word = Column(String)
    complexity = Column(String)
    grade_level = Column(String)
    bee_level = Column(String)
    frequency = Column(Integer)
    lexical_level = Column(String)
    
class UserWordStats(Base):
    __tablename__ = "user_word_stats"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    word_id = Column(Integer, ForeignKey("words.id"))
    attempts = Column(Integer, default=0)
    correct = Column(Integer, default=0)
    incorrect = Column(Integer, default=0)