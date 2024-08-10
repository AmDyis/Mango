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

async def get_anime_genres():
    return await fetch_data('genres/anime')

async def get_manga_genres():
    return await fetch_data('genres/manga')

router = APIRouter()

@router.get("/genres/anime")
async def anime_genres():
    genres = await get_anime_genres()
    if genres:
        return genres
    raise HTTPException(status_code=404, detail="Anime genres not found")

@router.get("/genres/manga")
async def manga_genres():
    genres = await get_manga_genres()
    if genres:
        return genres
    raise HTTPException(status_code=404, detail="Manga genres not found")
