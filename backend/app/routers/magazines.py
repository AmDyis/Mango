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

async def get_magazines():
    return await fetch_data('magazines')

router = APIRouter()

@router.get("/magazines")
async def magazines():
    magazines = await get_magazines()
    if magazines:
        return magazines
    raise HTTPException(status_code=404, detail="Magazines not found")
