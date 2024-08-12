from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    is_admin: bool

class TokenRefreshRequest(BaseModel):
    refresh_token: str

# User schema
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False

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
    entity_id: int
    entity_type: str

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
    entity_id: int
    entity_type: str
    created_at: datetime

    class Config:
        orm_mode = True
