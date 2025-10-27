import logging
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        logger.info("✅ Database connection successful.")
except Exception as e:
    logger.error(f"❌ Failed to connect to database: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
