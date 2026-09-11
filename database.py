"""Clean database connection with ZERO mock data initialization."""

import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DB_URL = os.getenv("DATABASE_URL", "sqlite:///fluffflow.db")

engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if "sqlite" in DB_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FluffFlowDB")

def init_db() -> None:
    """Initialize clean database schema without pre-populated mock users."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Clean database schema created.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")

def get_db():
    """Context manager generator for DB sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
