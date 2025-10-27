from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    DATABASE_DIRECT_URL: Optional[str] = None
    SECRET_KEY: Optional[str] = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        #env_file = os.path.join(os.path.dirname(__file__), "../../.env")
        env_file = ".env"
        extra = "ignore"

settings = Settings()
