from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text, DateTime, Boolean, Table, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

# Промежуточные таблицы для связи "многие ко многим"
anime_genres = Table(
    'anime_genres', Base.metadata,
    Column('anime_id', Integer, ForeignKey('animes.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

manga_genres = Table(
    'manga_genres', Base.metadata,
    Column('manga_id', Integer, ForeignKey('mangas.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

anime_studios = Table(
    'anime_studios', Base.metadata,
    Column('anime_id', Integer, ForeignKey('animes.id'), primary_key=True),
    Column('studio_id', Integer, ForeignKey('studios.id'), primary_key=True)
)

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

class Anime(Base):
    __tablename__ = "animes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    synopsis = Column(Text)
    release_date = Column(TIMESTAMP(timezone=True))  # Измените здесь
    manga_name = Column(String, nullable=True)
    manga_id = Column(Integer, ForeignKey('mangas.id'), nullable=True)
    score = Column(Float, nullable=True)
    rank = Column(Float, nullable=True)
    is_ongoing = Column(Boolean, default=True)
    episode_count = Column(Integer, nullable=True)

    # Связи
    episodes = relationship("Episode", back_populates="anime")
    ratings = relationship("Rating", back_populates="anime")
    comments = relationship("Comment", back_populates="anime")
    genres = relationship("Genre", secondary=anime_genres, back_populates="animes")
    studios = relationship("Studio", secondary=anime_studios, back_populates="animes")
    images = relationship("Image", back_populates="anime")

class Episode(Base):
    __tablename__ = "episodes"
    id = Column(Integer, primary_key=True, index=True)
    anime_id = Column(Integer, ForeignKey("animes.id"), nullable=False)
    title = Column(String, index=True, nullable=False)
    episode_number = Column(Integer, nullable=False)
    duration = Column(Float, nullable=True)
    anime = relationship("Anime", back_populates="episodes")
    comments = relationship("Comment", back_populates="episode")
    images = relationship("Image", back_populates="episode")

class Manga(Base):
    __tablename__ = "mangas"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    synopsis = Column(Text)
    release_date = Column(TIMESTAMP(timezone=True))  # Измените здесь
    chapter_count = Column(Integer, nullable=True)
    score = Column(Float, nullable=True)
    rank = Column(Float, nullable=True)
    is_ongoing = Column(Boolean, default=True)
    issuer_id = Column(Integer, ForeignKey("issuers.id"), nullable=True)
    chapters = relationship("Chapter", back_populates="manga")
    ratings = relationship("Rating", back_populates="manga")
    comments = relationship("Comment", back_populates="manga")
    genres = relationship("Genre", secondary=manga_genres, back_populates="mangas")
    images = relationship("Image", back_populates="manga")
    issuer = relationship("MangaIssuer", back_populates="mangas")


class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True, index=True)
    manga_id = Column(Integer, ForeignKey("mangas.id"), nullable=False)
    title = Column(String, index=True, nullable=False)
    chapter_number = Column(Integer, nullable=False)
    page_count = Column(Integer, nullable=True)
    manga = relationship("Manga", back_populates="chapters")
    comments = relationship("Comment", back_populates="chapter")


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    anime_id = Column(Integer, ForeignKey("animes.id"), nullable=True)
    manga_id = Column(Integer, ForeignKey("mangas.id"), nullable=True)
    rating = Column(Float, nullable=False)
    user = relationship("User", back_populates="ratings")
    anime = relationship("Anime", back_populates="ratings")
    manga = relationship("Manga", back_populates="ratings")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    timestamp = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    episode_id = Column(Integer, ForeignKey('episodes.id'), nullable=True)
    manga_id = Column(Integer, ForeignKey('mangas.id'), nullable=True)
    anime_id = Column(Integer, ForeignKey('animes.id'), nullable=True)
    chapter_id = Column(Integer, ForeignKey('chapters.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Связи
    user = relationship("User", back_populates="comments")
    episode = relationship("Episode", back_populates="comments")
    manga = relationship("Manga", back_populates="comments")
    anime = relationship("Anime", back_populates="comments")
    chapter = relationship("Chapter", back_populates="comments")


class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    animes = relationship("Anime", secondary=anime_genres, back_populates="genres")
    mangas = relationship("Manga", secondary=manga_genres, back_populates="genres")


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True, nullable=False)
    episode_id = Column(Integer, ForeignKey("episodes.id"), nullable=True)
    manga_id = Column(Integer, ForeignKey("mangas.id"), nullable=True)
    anime_id = Column(Integer, ForeignKey("animes.id"), nullable=True)
    episode = relationship("Episode", back_populates="images")
    manga = relationship("Manga", back_populates="images")
    anime = relationship("Anime", back_populates="images")


class Studio(Base):
    __tablename__ = "studios"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    animes = relationship("Anime", secondary=anime_studios, back_populates="studios")


class MangaIssuer(Base):
    __tablename__ = "issuers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    mangas = relationship("Manga", back_populates="issuer")
