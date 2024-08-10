import aiohttp
import asyncio
import datetime
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import Base, Manga, Genre, MangaIssuer

load_dotenv()

# Подключение к базе данных и создание сессии
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Jikan API базовый URL
JIKAN_API_BASE_URL = "https://api.jikan.moe/v4"

async def get_data_from_jikan(endpoint, params=None):
    url = f"{JIKAN_API_BASE_URL}/{endpoint}"
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(url, params=params) as response:
                    if response.status == 429:
                        print("Rate limit exceeded. Sleeping for 10 seconds...")
                        await asyncio.sleep(10)
                        continue
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientResponseError as e:
                print(f"Error fetching data: {e}")
                return None

def print_data_info(data_type, data):
    print(f"\n{data_type} Data to be added:")
    for key, value in data.items():
        print(f"{key}: {value}")
    print("\n")

async def check_if_exists(session, model, identifier):
    result = await session.execute(select(model).filter_by(id=identifier))
    return result.scalar_one_or_none() is not None

async def get_last_manga_id_from_db(session):
    result = await session.execute(select(Manga.id).order_by(Manga.id.desc()).limit(1))
    last_manga_in_db = result.scalar_one_or_none()
    return last_manga_in_db if last_manga_in_db is not None else 0

async def parse_manga():
    async with async_session() as session:
        last_manga_id_in_db = await get_last_manga_id_from_db(session)
        page = 1
        while True:
            manga_data = await get_data_from_jikan('manga', params={'page': page})
            if not manga_data or 'data' not in manga_data:
                break

            all_manga = manga_data['data']
            if not all_manga:
                break

            # Флаг для определения, нужно ли продолжать цикл
            added_any_manga = False

            for manga in all_manga:
                if manga['mal_id'] <= last_manga_id_in_db:
                    continue

                # Проверка существования манги в базе данных
                if await check_if_exists(session, Manga, manga['mal_id']):
                    print(f"Manga with id {manga['mal_id']} already exists. Skipping...")
                    continue

                # Получаем или создаем жанры
                genres = []
                for genre in manga['genres']:
                    existing_genre = await session.execute(select(Genre).filter_by(name=genre['name']))
                    genre_entry = existing_genre.scalar_one_or_none()
                    if genre_entry is None:
                        genre_entry = Genre(name=genre['name'])
                        session.add(genre_entry)
                    genres.append(genre_entry)

                # Получаем или создаем издателей манги
                issuer = None
                if manga['serializations']:
                    issuer_name = manga['serializations'][0]['name']
                    existing_issuer = await session.execute(select(MangaIssuer).filter_by(name=issuer_name))
                    issuer = existing_issuer.scalar_one_or_none()
                    if issuer is None:
                        issuer = MangaIssuer(name=issuer_name)
                        session.add(issuer)

                # Создаем запись манги
                manga_entry = Manga(
                    id=manga['mal_id'],
                    title=manga['title'],
                    synopsis=manga.get('synopsis', ''),
                    release_date=datetime.datetime.strptime(manga['published']['from'], '%Y-%m-%dT%H:%M:%S%z')
                                 if manga['published']['from'] else None,
                    chapter_count=manga.get('chapters', 0),
                    score=manga.get('score', 0.0),
                    rank=manga.get('rank', None),
                    is_ongoing=manga['status'] == 'Publishing',
                    genres=genres,
                    issuer=issuer
                )

                # Вывод информации о манге
                print_data_info("Manga", {
                    "id": manga['mal_id'],
                    "title": manga['title'],
                    "synopsis": manga.get('synopsis', ''),
                    "release_date": manga['published']['from'],
                    "chapter_count": manga.get('chapters', 0),
                    "score": manga.get('score', 0.0),
                    "rank": manga.get('rank', None),
                    "is_ongoing": manga['status'] == 'Publishing',
                })

                session.add(manga_entry)
                added_any_manga = True

            if not added_any_manga:
                break

            await session.commit()
            page += 1

async def main():
    await create_tables()
    while True:
        await parse_manga()
        await asyncio.sleep(3600)  # Подождать 1 час перед следующей проверкой

if __name__ == "__main__":
    asyncio.run(main())
