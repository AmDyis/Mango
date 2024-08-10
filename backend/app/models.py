from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    ratings = relationship("Rating", back_populates="user")
    comments = relationship("Comment", back_populates="user")

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    entity_id = Column(Integer, nullable=False)  # ID аниме или манги
    entity_type = Column(String, nullable=False)  # "anime" или "manga"
    rating = Column(Float, nullable=False)
    user = relationship("User", back_populates="ratings")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    timestamp = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    entity_id = Column(Integer, nullable=False)  # ID аниме, манги, эпизода или главы
    entity_type = Column(String, nullable=False)  # "anime", "manga", "episode", "chapter"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="comments")
