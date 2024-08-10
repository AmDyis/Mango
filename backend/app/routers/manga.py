#manga.py файл эндпоинт для работы с аниме
from fastapi import APIRouter, HTTPException
from api_parser import get_manga_by_id, get_manga_by_title

router = APIRouter()

@router.get("/manga/{manga_id_or_title}")
async def get_manga(manga_id_or_title: str):
    if manga_id_or_title.isdigit():  # Если это число, то ищем по ID
        manga_data = await get_manga_by_id(int(manga_id_or_title))
    else:  # Иначе ищем по названию
        manga_data = await get_manga_by_title(manga_id_or_title)

    if manga_data is None:
        raise HTTPException(status_code=404, detail="Manga not found")
    return manga_data