from pydantic_settings import BaseSettings
import os
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: postgresql://postgres.wxctkrgdnrjvangebnso:Tamaya1BtBeeAai@aws-1-us-east-2.pooler.supabase.com:6543/postgres?pgbouncer=true
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "../../.env")  # adjust path if needed
        extra = "ignore"

settings = Settings()
