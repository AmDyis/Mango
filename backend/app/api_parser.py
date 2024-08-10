# api_parser.py файл для прямого парсинга аниме и манги с Jikan API
import aiohttp
import asyncio

JIKAN_API_BASE_URL = "https://api.jikan.moe/v4"

async def fetch_data(endpoint, params=None):
    url = f"{JIKAN_API_BASE_URL}/{endpoint}"
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(url, params=params) as response:
                    if response.status == 429:  # Лимит запросов достигнут
                        print("Rate limit exceeded. Sleeping for 10 seconds...")
                        await asyncio.sleep(10)  # Подождать 10 секунд
                        continue
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientResponseError as e:
                print(f"Error fetching data: {e}")
                return None

async def get_anime_by_id(anime_id):
    return await fetch_data(f'anime/{anime_id}/full')

async def get_anime_by_title(title):
    data = await fetch_data('anime', params={'q': title, 'limit': 1})
    if data and 'data' in data and data['data']:
        anime_id = data['data'][0]['mal_id']
        return await get_anime_by_id(anime_id)
    return None

async def get_manga_by_id(manga_id):
    return await fetch_data(f'manga/{manga_id}/full')

async def get_manga_by_title(title):
    data = await fetch_data('manga', params={'q': title, 'limit': 1})
    if data and 'data' in data and data['data']:
        manga_id = data['data'][0]['mal_id']
        return await get_manga_by_id(manga_id)
    return None
