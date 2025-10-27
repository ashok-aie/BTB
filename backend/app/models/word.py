from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from zoneinfo import ZoneInfo

# EST/EDT timezone
eastern = ZoneInfo("America/New_York")

timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(eastern))

class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=True, nullable=False)
    part_of_speech = Column(String, nullable=False)
    language_origin = Column(String, nullable=False)
    definition = Column(String, nullable=False)
    example = Column(String, nullable=False)
    prefixes_suffixes = Column(String, nullable=False)
    root_word = Column(String, nullable=False)
    grade_level = Column(String, nullable=False)
    bee_level = Column(String, nullable=False)
    lexical_level = Column(String, nullable=False)
    
    activities = relationship("UserActivity", back_populates="word")

class UserActivity(Base):
    __tablename__ = "user_activities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    user_input = Column(String, nullable=True)
    is_correct = Column(Boolean, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="activities")
    word = relationship("Word", back_populates="activities")