from fastapi import APIRouter, HTTPException
import aiohttp
import asyncio
from api_parser import fetch_data

JIKAN_API_BASE_URL = "https://api.jikan.moe/v4"

async def get_person(person_id):
    return await fetch_data(f'people/{person_id}')

router = APIRouter()

@router.get("/people/{person_id}")
async def person(person_id: int):
    person = await get_person(person_id)
    if person:
        return person
    raise HTTPException(status_code=404, detail="Person not found")
