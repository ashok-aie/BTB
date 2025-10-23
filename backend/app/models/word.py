from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from zoneinfo import ZoneInfo

# EST/EDT timezone
eastern = ZoneInfo("America/New_York")

timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(eastern))

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
    grade_level = Column(String)
    bee_level = Column(String)
    lexical_level = Column(String)
    
class UserActivity(Base):
    __tablename__ = "user_activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # optional if tracking by user
    word_id = Column(Integer, ForeignKey("words.id"))
    user_input = Column(String)
    is_correct = Column(Boolean)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(eastern))

    # relationships
    user = relationship("User", back_populates="activities")
    word = relationship("Word")