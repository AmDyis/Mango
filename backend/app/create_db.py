from sqlalchemy.ext.asyncio import create_async_engine
from models import Base
import os
from dotenv import load_dotenv
import asyncio

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем URL базы данных из переменных окружения
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Создание асинхронного движка SQLAlchemy
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Асинхронное создание всех таблиц в базе данных
async def create_db():
    async with engine.begin() as conn:
        # Создаем таблицы
        await conn.run_sync(Base.metadata.create_all)

# Запуск асинхронного создания базы данных
asyncio.run(create_db())
