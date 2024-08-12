from fastapi import APIRouter, HTTPException
import aiohttp
import asyncio
from api_parser import fetch_data

JIKAN_API_BASE_URL = "https://api.jikan.moe/v4"

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
