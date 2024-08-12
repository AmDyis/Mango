from fastapi import APIRouter, HTTPException
import aiohttp
import asyncio
from api_parser import fetch_data

JIKAN_API_BASE_URL = "https://api.jikan.moe/v4"

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
