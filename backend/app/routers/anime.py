#anime.py файл эндпоинт для работы с аниме

from fastapi import APIRouter, HTTPException, Query
from api_parser import get_anime_by_id, get_anime_by_title

router = APIRouter()

@router.get("/anime/{anime_id_or_title}")
async def get_anime(anime_id_or_title: str):
    if anime_id_or_title.isdigit():  # Если это число, то ищем по ID
        anime_data = await get_anime_by_id(int(anime_id_or_title))
    else:  # Иначе ищем по названию
        anime_data = await get_anime_by_title(anime_id_or_title)

    

    if anime_data is None:
        raise HTTPException(status_code=404, detail="Anime not found")
    return anime_data

@router.get("/search")
async def search_anime(query: str = Query(..., description="Search query")):
    # Поиск аниме по названию
    anime_data = await get_anime_by_title(query)
    if anime_data is None:
        raise HTTPException(status_code=404, detail="Anime not found")
    return anime_data
