import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.core.config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

try:
    # Create engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    # Test connection
    with engine.connect() as connection:
        connection.execute("SELECT 1")
    logger.info("✅ Successfully connected to the database.")
except OperationalError as e:
    logger.error(f"❌ Failed to connect to the database: {e}")

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
