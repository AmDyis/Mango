from fastapi import APIRouter, HTTPException
import aiohttp
import asyncio
from api_parser import fetch_data

JIKAN_API_BASE_URL = "https://api.jikan.moe/v4"

async def get_magazines():
    return await fetch_data('magazines')

router = APIRouter()

@router.get("/magazines")
async def magazines():
    magazines = await get_magazines()
    if magazines:
        return magazines
    raise HTTPException(status_code=404, detail="Magazines not found")
