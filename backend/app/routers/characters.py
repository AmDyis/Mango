from fastapi import APIRouter, HTTPException
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
                        await asyncio.sleep(10)
                        continue
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientResponseError as e:
                print(f"Error fetching data: {e}")
                return None

async def get_anime_characters(anime_id):
    return await fetch_data(f'anime/{anime_id}/characters')

async def get_manga_characters(manga_id):
    return await fetch_data(f'manga/{manga_id}/characters')

router = APIRouter()

@router.get("/anime/{anime_id}/characters")
async def anime_characters(anime_id: int):
    characters = await get_anime_characters(anime_id)
    if characters:
        return characters
    raise HTTPException(status_code=404, detail="Anime characters not found")

@router.get("/manga/{manga_id}/characters")
async def manga_characters(manga_id: int):
    characters = await get_manga_characters(manga_id)
    if characters:
        return characters
    raise HTTPException(status_code=404, detail="Manga characters not found")
