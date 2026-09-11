"""Database models for FluffFlow v2.2 with Authentication."""

from datetime import datetime, date
from sqlalchemy import String, Integer, Float, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""
    pass

class User(Base):
    """User table storing authenticated user profiles and password hashes."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    current_streak: Mapped[int] = mapped_column(Integer, default=0)
    last_checkin_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    checkins: Mapped[list["FluffCheckin"]] = relationship("FluffCheckin", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(username='{self.username}', streak={self.current_streak})>"

class FluffCheckin(Base):
    """Log of daily emotional check-ins and drink recommendations."""
    __tablename__ = "fluff_checkins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    checkin_date: Mapped[date] = mapped_column(Date, default=date.today)
    
    mood: Mapped[str] = mapped_column(String(50), nullable=False)
    energy_level: Mapped[int] = mapped_column(Integer, nullable=False)
    weather_city: Mapped[str] = mapped_column(String(100), nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    weather_desc: Mapped[str] = mapped_column(String(100), nullable=False)
    
    drink_name: Mapped[str] = mapped_column(String(100), nullable=False)
    quote: Mapped[str] = mapped_column(Text, nullable=False)
    user_note: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="checkins")
