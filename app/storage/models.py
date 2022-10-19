from datetime import datetime

from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    ForeignKey,
    String,
    Boolean,
    DateTime,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship

from app.storage.base_class import BaseClass


class User(BaseClass):
    """User model."""

    id: int = Column(BigInteger, primary_key=True, index=True)
    telegram_id: int = Column(Integer, unique=True, index=True)
    name: str = Column(String)
    is_admin: bool = Column(Boolean, default=False)
    is_member: bool = Column(Boolean, default=False)
    state: int = Column(Integer, default=0)
    playlist = relationship("Playlist")


class Playlist(BaseClass):
    """Playlist model."""

    id: int = Column(Integer, primary_key=True, index=True)
    event_id: int = Column(Integer, ForeignKey("events.id"))
    telegram_id: int = Column(Integer, nullable=False)
    link: str = Column(String, unique=True, nullable=False)
    description: str = Column(String, nullable=True)


class Review(BaseClass):
    """Playlist review model."""

    id: int = Column(Integer, primary_key=True, index=True)
    author_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    playlist_id: int = Column(Integer, ForeignKey("playlists.id"), unique=False, nullable=False)
    event_id: int = Column(Integer, ForeignKey("events.id"), unique=False, nullable=False)
    round: int = Column(Integer, nullable=False)
    rating: int = Column(Integer, nullable=False)
    comment: int = Column(String, nullable=False)


class Event(BaseClass):
    """Event model."""

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False)
    description: str = Column(String, nullable=True)
    rules: str = Column(String, nullable=False)
    round_duration: int = Column(Integer, nullable=False)
    start_date: datetime = Column(DateTime, default=datetime.now())
    end_date: datetime = Column(DateTime, nullable=True)
    state: int = Column(Integer, default=0)
    members: list[int] = Column(MutableList.as_mutable(ARRAY(Integer)))
    round: int = Column(Integer, nullable=True)
    playlist_queue: dict[str, str] = Column(JSON)
