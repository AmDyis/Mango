import asyncio
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, get_db

async def test_connection():
    async with engine.connect() as conn:
        result = await conn.execute(select(1))
        print(result.fetchall())

# Запускаем тест
asyncio.run(test_connection())
