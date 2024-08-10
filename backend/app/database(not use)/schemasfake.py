from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schema
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    ratings: List['RatingResponse'] = []
    comments: List['CommentResponse'] = []

    class Config:
        orm_mode = True

# Anime schema
class AnimeBase(BaseModel):
    title: str
    synopsis: str
    release_date: datetime
    score: Optional[float] = None
    rank: Optional[float] = None
    is_ongoing: Optional[bool] = True
    trailer_url: Optional[str] = None
    episode_count: Optional[int] = None  # Добавлено поле для количества серий


class AnimeCreate(AnimeBase):
    pass

class AnimeUpdate(AnimeBase):
    episode_count: Optional[int] = None  # Добавлено поле для количества серий

class AnimeResponse(AnimeBase):
    id: int
    episode_count: Optional[int] = None  # Добавлено поле для количества серий
    episodes: List['EpisodeResponse'] = []
    ratings: List['RatingResponse'] = []
    comments: List['CommentResponse'] = []
    genres: List['GenreResponse'] = []
    images: List['ImageResponse'] = []
    studios: List['StudioResponse'] = []

    class Config:
        orm_mode = True

# Episode schema
class EpisodeBase(BaseModel):
    title: str
    episode_number: int
    duration: Optional[float] = None

class EpisodeCreate(EpisodeBase):
    pass

class EpisodeUpdate(EpisodeBase):
    pass

class EpisodeResponse(EpisodeBase):
    id: int
    anime_id: int
    comments: List['CommentResponse'] = []
    images: List['ImageResponse'] = []

    class Config:
        orm_mode = True

# Manga schema
class MangaBase(BaseModel):
    title: str
    synopsis: str
    release_date: datetime
    chapter_count: Optional[int] = None
    score: Optional[float] = None
    rank: Optional[float] = None
    is_ongoing: Optional[bool] = True

class MangaCreate(MangaBase):
    pass

class MangaUpdate(MangaBase):
    pass

class MangaResponse(MangaBase):
    id: int
    chapters: List['ChapterResponse'] = []
    ratings: List['RatingResponse'] = []
    comments: List['CommentResponse'] = []
    genres: List['GenreResponse'] = []
    images: List['ImageResponse'] = []
    issuer: Optional['MangaIssuerResponse'] = None

    class Config:
        orm_mode = True


# Chapter schema
class ChapterBase(BaseModel):
    title: str
    chapter_number: int
    page_count: Optional[int] = None

class ChapterCreate(ChapterBase):
    pass

class ChapterUpdate(ChapterBase):
    pass

class ChapterResponse(ChapterBase):
    id: int
    manga_id: int
    comments: List['CommentResponse'] = []

    class Config:
        orm_mode = True

# Rating schema
class RatingBase(BaseModel):
    rating: float

class RatingCreate(RatingBase):
    pass

class RatingUpdate(RatingBase):
    pass

class RatingResponse(RatingBase):
    id: int
    user_id: int
    anime_id: Optional[int] = None
    manga_id: Optional[int] = None

    class Config:
        orm_mode = True

# Comment schema
class CommentBase(BaseModel):
    content: str
    timestamp: float

class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    user_id: int
    episode_id: Optional[int] = None
    manga_id: Optional[int] = None
    anime_id: Optional[int] = None
    chapter_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True

# Genre schema
class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class GenreUpdate(GenreBase):
    pass

class GenreResponse(GenreBase):
    id: int

    class Config:
        orm_mode = True

# Image schema
class ImageBase(BaseModel):
    url: str

class ImageCreate(ImageBase):
    pass

class ImageUpdate(ImageBase):
    pass

class ImageResponse(ImageBase):
    id: int
    episode_id: Optional[int] = None
    manga_id: Optional[int] = None
    anime_id: Optional[int] = None

    class Config:
        orm_mode = True

# Studio schema
class StudioBase(BaseModel):
    name: str

class StudioCreate(StudioBase):
    pass

class StudioUpdate(StudioBase):
    pass

class StudioResponse(StudioBase):
    id: int

    class Config:
        orm_mode = True

# MangaIssuer schema
class MangaIssuerBase(BaseModel):
    name: str

class MangaIssuerCreate(MangaIssuerBase):
    pass

class MangaIssuerUpdate(MangaIssuerBase):
    pass

class MangaIssuerResponse(MangaIssuerBase):
    id: int

    class Config:
        orm_mode = True
