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

async def get_top_anime():
    return await fetch_data('top/anime')

async def get_top_manga():
    return await fetch_data('top/manga')

router = APIRouter()

@router.get("/top/anime")
async def top_anime():
    top_anime = await get_top_anime()
    if top_anime:
        return top_anime
    raise HTTPException(status_code=404, detail="Top anime not found")

@router.get("/top/manga")
async def top_manga():
    top_manga = await get_top_manga()
    if top_manga:
        return top_manga
    raise HTTPException(status_code=404, detail="Top manga not found")
