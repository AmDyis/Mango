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

async def get_random_anime():
    return await fetch_data('random/anime')

async def get_random_manga():
    return await fetch_data('random/anime')

router = APIRouter()

@router.get("/anime/random")
async def random_anime():
    anime = await get_random_anime()
    if anime:
        return anime
    raise HTTPException(status_code=404, detail="Random anime not found")

@router.get("/manga/random")
async def random_manga():
    manga = await get_random_manga()
    if manga:
        return manga
    raise HTTPException(status_code=404, detail="Random manga not found")
