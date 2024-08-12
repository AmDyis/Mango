# app/crud.py

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import models, schemas, security
from typing import Optional
from security import get_password_hash
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Пользователь
async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        is_admin=user.is_admin,
        is_active=user.is_active,
        hashed_password=hashed_password
    )
    db.add(db_user)
    # Не используйте db.commit() или db.refresh() здесь, если транзакция уже обрабатывается в вызывающей функции
    return db_user


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[models.User]:
    stmt = select(models.User).filter(models.User.username == username)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_user(db: AsyncSession, user_id: int) -> Optional[models.User]:
    stmt = select(models.User).filter(models.User.id == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def update_user(db: AsyncSession, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    db_user = await get_user(db, user_id)
    if db_user:
        if user_update.password:
            db_user.hashed_password = security.get_password_hash(user_update.password)
        if user_update.username:
            db_user.username = user_update.username
        if user_update.email:
            db_user.email = user_update.email
        if user_update.is_active is not None:
            db_user.is_active = user_update.is_active
        if user_update.is_admin is not None:
            db_user.is_admin = user_update.is_admin
        await db.commit()
        await db.refresh(db_user)
        return db_user
    return None

async def delete_user(db: AsyncSession, user_id: int) -> Optional[models.User]:
    db_user = await get_user(db, user_id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
        return db_user
    return None

# Оценки
async def create_rating(db: AsyncSession, rating: schemas.RatingCreate, user_id: int, entity_id: int, entity_type: str) -> schemas.RatingResponse:
    db_rating = models.Rating(
        rating=rating.rating,
        user_id=user_id,
        entity_id=entity_id,
        entity_type=entity_type
    )
    db.add(db_rating)
    await db.commit()
    await db.refresh(db_rating)
    return db_rating

async def get_rating(db: AsyncSession, rating_id: int) -> Optional[models.Rating]:
    stmt = select(models.Rating).filter(models.Rating.id == rating_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_ratings_for_entity(db: AsyncSession, entity_id: int, entity_type: str) -> list[models.Rating]:
    stmt = select(models.Rating).filter(models.Rating.entity_id == entity_id, models.Rating.entity_type == entity_type)
    result = await db.execute(stmt)
    return result.scalars().all()

async def delete_rating(db: AsyncSession, rating_id: int) -> Optional[models.Rating]:
    db_rating = await get_rating(db, rating_id)
    if db_rating:
        await db.delete(db_rating)
        await db.commit()
        return db_rating
    return None

# Комментарии
async def create_comment(db: AsyncSession, comment: schemas.CommentCreate, user_id: int, entity_id: int, entity_type: str) -> schemas.CommentResponse:
    db_comment = models.Comment(
        content=comment.content,
        timestamp=comment.timestamp,
        user_id=user_id,
        entity_id=entity_id,
        entity_type=entity_type
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

async def get_comment(db: AsyncSession, comment_id: int) -> Optional[models.Comment]:
    stmt = select(models.Comment).filter(models.Comment.id == comment_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_comments_for_entity(db: AsyncSession, entity_id: int, entity_type: str) -> list[models.Comment]:
    stmt = select(models.Comment).filter(models.Comment.entity_id == entity_id, models.Comment.entity_type == entity_type)
    result = await db.execute(stmt)
    return result.scalars().all()

async def delete_comment(db: AsyncSession, comment_id: int) -> Optional[models.Comment]:
    db_comment = await get_comment(db, comment_id)
    if db_comment:
        await db.delete(db_comment)
        await db.commit()
        return db_comment
    return None

async def authenticate_user(db: AsyncSession, username: str, password: str) -> models.User:
    async with db as session:
        result = await session.execute(
            select(models.User).filter(models.User.username == username)
        )
        user = result.scalars().first()

        if user and pwd_context.verify(password, user.hashed_password):
            return user
        return None
    
async def get_user_by_refresh_token(db: AsyncSession, refresh_token: str):
    async with db as session:
        result = await session.execute(
            select(models.User).filter(models.User.refresh_token == refresh_token)
        )
        return result.scalars().first()