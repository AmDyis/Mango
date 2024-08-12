from fastapi import APIRouter, HTTPException
import aiohttp
import asyncio
from api_parser import fetch_data

JIKAN_API_BASE_URL = "https://api.jikan.moe/v4"

async def get_seasons():
    return await fetch_data('seasons')

router = APIRouter()

@router.get("/seasons")
async def seasons():
    seasons = await get_seasons()
    if seasons:
        return seasons
    raise HTTPException(status_code=404, detail="Seasons not found")