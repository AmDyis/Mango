# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import crud, schemas, security
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select
import models, security
from schemas import TokenRefreshRequest

router = APIRouter()

@router.post("/register/", response_model=schemas.Token)
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    async with db.begin():  # Открываем транзакцию
        # Проверяем, существует ли уже пользователь с таким именем
        existing_user = await db.execute(
            select(models.User).filter(models.User.username == user.username)
        )
        existing_user = existing_user.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # Создаем нового пользователя
        user = await crud.create_user(db, user)
        
        # Генерируем токены
        access_token = security.create_access_token(data={"sub": user.username})
        refresh_token = security.create_refresh_token(data={"sub": user.username})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

@router.post("/login/", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = security.create_access_token(data={"sub": user.username, "is_admin": user.is_admin})
    refresh_token = security.create_refresh_token(data={"sub": user.username})
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh-token/", response_model=schemas.Token)
async def refresh_token(
    request: schemas.TokenRefreshRequest,
    db: AsyncSession = Depends(get_db)
):
    # Проверка refresh token
    user = await crud.get_user_by_refresh_token(db, request.refresh_token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Генерация новых токенов
    access_token = crud.create_access_token(data={"sub": user.username})
    refresh_token = crud.create_refresh_token(data={"sub": user.username})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}