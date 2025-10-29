from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ---- Base schema shared across operations ----
class UserActivityBase(BaseModel):
    user_id: int
    word_id: int
    user_input: Optional[str] = None
    is_correct: bool

# ---- Schema for creating new activity ----
class UserActivityCreate(UserActivityBase):
    """Used for incoming POST requests to create an activity."""
    pass

# ---- Schema for reading activity data ----
class UserActivityRead(UserActivityBase):
    id: int
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True  # works with SQLAlchemy ORM models

# ---- (Optional) alias used by your route ----
UserActivitySchema = UserActivityCreate
