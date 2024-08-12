from fastapi import APIRouter, HTTPException
import aiohttp
import asyncio
from api_parser import fetch_data

JIKAN_API_BASE_URL = "https://api.jikan.moe/v4"

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
