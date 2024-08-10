#database.py файл для настройки подключения к базе данных
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем URL базы данных из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in .env file")

# Создаем асинхронный движок базы данных
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем асинхронную сессию
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Функция для получения сессии базы данных
async def get_db():
    async with async_session() as session:
        yield session
