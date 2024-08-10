import aiohttp
import asyncio
import datetime
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import Base, Anime, Episode, Genre, Studio

load_dotenv()

# Подключение к базе данных и создание сессии
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

# Jikan API базовый URL
JIKAN_API_BASE_URL = "https://api.jikan.moe/v4"

async def get_data_from_jikan(endpoint, params=None):
    url = f"{JIKAN_API_BASE_URL}/{endpoint}"
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(url, params=params) as response:
                    if response.status == 429:  # Если лимит запросов достигнут
                        print("Rate limit exceeded. Sleeping for 10 seconds...")
                        await asyncio.sleep(10)  # Подождать 10 секунд
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

async def get_last_anime_id_from_db(session):
    result = await session.execute(select(Anime.id).order_by(Anime.id.desc()).limit(1))
    last_anime_in_db = result.scalar_one_or_none()
    return last_anime_in_db if last_anime_in_db is not None else 0

async def parse_anime():
    async with async_session() as session:
        last_anime_id_in_db = await get_last_anime_id_from_db(session)
        page = 1
        while True:
            anime_data = await get_data_from_jikan('anime', params={'page': page})
            if not anime_data or 'data' not in anime_data:
                break

            all_anime = anime_data['data']
            if not all_anime:
                break

            added_any_anime = False

            for anime in all_anime:
                # Пропускаем аниме, которое уже есть в базе данных
                if anime['mal_id'] <= last_anime_id_in_db:
                    continue

                # Проверяем, существует ли уже аниме в базе данных
                existing_anime = await session.execute(select(Anime).filter_by(id=anime['mal_id']))
                existing_anime = existing_anime.scalar_one_or_none()

                try:
                    genres = []
                    for genre in anime['genres']:
                        existing_genre = await session.execute(select(Genre).filter_by(name=genre['name']))
                        genre_entry = existing_genre.scalar_one_or_none()
                        if genre_entry is None:
                            genre_entry = Genre(name=genre['name'])
                            session.add(genre_entry)
                        genres.append(genre_entry)

                    studios = []
                    for studio in anime['studios']:
                        existing_studio = await session.execute(select(Studio).filter_by(name=studio['name']))
                        studio_entry = existing_studio.scalar_one_or_none()
                        if studio_entry is None:
                            studio_entry = Studio(name=studio['name'])
                            session.add(studio_entry)
                        studios.append(studio_entry)

                    episode_count = anime.get('episodes', 0)  # Получаем количество серий

                    if existing_anime:
                        # Обновляем существующую запись
                        existing_anime.title = anime['title']
                        existing_anime.synopsis = anime.get('synopsis', '')
                        existing_anime.release_date = datetime.datetime.strptime(anime['aired']['from'], '%Y-%m-%dT%H:%M:%S%z') if anime['aired']['from'] else None
                        existing_anime.score = anime.get('score', 0.0)
                        existing_anime.rank = anime.get('rank', None)
                        existing_anime.is_ongoing = anime['status'] == 'Currently Airing'
                        existing_anime.episode_count = episode_count
                        existing_anime.genres = genres
                        existing_anime.studios = studios
                    else:
                        # Создаем новую запись
                        anime_entry = Anime(
                            id=anime['mal_id'],
                            title=anime['title'],
                            synopsis=anime.get('synopsis', ''),
                            release_date=datetime.datetime.strptime(anime['aired']['from'], '%Y-%m-%dT%H:%M:%S%z') if anime['aired']['from'] else None,
                            score=anime.get('score', 0.0),
                            rank=anime.get('rank', None),
                            is_ongoing=anime['status'] == 'Currently Airing',
                            episode_count=episode_count,
                            genres=genres,
                            studios=studios
                        )
                        session.add(anime_entry)

                    print_data_info("Anime", {
                        "id": anime['mal_id'],
                        "title": anime['title'],
                        "synopsis": anime.get('synopsis', ''),
                        "release_date": anime['aired']['from'],
                        "score": anime.get('score', 0.0),
                        "rank": anime.get('rank', None),
                        "is_ongoing": anime['status'] == 'Currently Airing',
                        "episode_count": episode_count
                    })

                    added_any_anime = True

                except Exception as e:
                    print(f"Error processing anime {anime['mal_id']}: {e}")

            if not added_any_anime:
                break

            try:
                await session.commit()
            except Exception as e:
                print(f"Error committing transaction: {e}")
                await session.rollback()

            page += 1



# async def parse_episodes(anime_id):
#     episode_data = await get_data_from_jikan(f'anime/{anime_id}/episodes')
#     async with async_session() as session:
#         async with session.begin():
#             for episode in episode_data.get('data', []):
#                 episode_number = episode.get('episode_id')  # Убедитесь, что поле существует
#                 if episode_number is None:
#                     print(f"Warning: Episode {episode['title']} has no episode_number and will be skipped.")
#                     continue  # Пропустите запись, если номер эпизода отсутствует
#
#                 if await check_if_exists(session, Episode, episode['mal_id']):
#                     print(f"Episode with id {episode['mal_id']} already exists. Skipping...")
#                     continue
#
#                 episode_entry = Episode(
#                     id=episode['mal_id'],
#                     anime_id=anime_id,
#                     title=episode['title'],
#                     episode_number=episode_number,
#                     duration=episode.get('duration')
#                 )
#                 print_data_info("Episode", {
#                     "id": episode['mal_id'],
#                     "anime_id": anime_id,
#                     "title": episode['title'],
#                     "episode_number": episode_number,
#                     "duration": episode.get('duration')
#                 })
#                 session.add(episode_entry)
#             await session.commit()

# Основной запуск парсера
async def main():
    await create_tables()
    while True:
        await parse_anime()
        await asyncio.sleep(3600)  # Подождать 1 час перед следующей проверкой

if __name__ == "__main__":
    asyncio.run(main())

