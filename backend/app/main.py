from fastapi import FastAPI, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
from routers.characters import router as characters_router
from routers.genres import router as genres_router
from routers.magazines import router as magazines_router
from routers.person import router as person_router
from routers.producers import router as producers_router
from routers.random import router as random_router
from routers.seasons import router as seasons_router
from routers.top import router as top_router
from routers.anime import router as anime_router
from routers.manga import router as manga_router
from routers.anime import get_anime
from routers.manga import get_manga
from routers.random import get_random_anime
from routers.characters import get_anime_characters
from routers.genres import get_anime_genres
from routers.person import get_person
from routers.producers import get_producers
from routers.seasons import get_seasons
from routers.top import get_top_anime

load_dotenv()

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    async with SessionLocal() as db:
        request.state.db = db
        response = await call_next(request)
    return response

# Include all routers
app.include_router(characters_router)
app.include_router(genres_router)
app.include_router(magazines_router)
app.include_router(person_router)
app.include_router(producers_router)
app.include_router(random_router)
app.include_router(seasons_router)  
app.include_router(top_router)
app.include_router(anime_router)
app.include_router(manga_router)

# Mount static files directory
app.mount("/static", StaticFiles(directory="../../frontend/static"), name="static")

# Template directory setup
templates = Jinja2Templates(directory="../../frontend/templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# # @app.get("/search")
# async def perform_search_anime(query: str):
#     # Вызов функции поиска аниме из вашего парсера
#     anime_data = await get_anime(query)
#     if anime_data is None:
#         raise HTTPException(status_code=404, detail="Anime not found")
#     return anime_data

@app.get("/random")
async def random_anime(request: Request):
    random_anime_data = await get_random_anime()
    if random_anime_data is None:
        raise HTTPException(status_code=404, detail="Random anime not found")
    return random_anime_data

@app.get("/characters")
async def characters_page(request: Request):
    # Получение данных для персонажей
    characters_data = await get_anime_characters()  # Замените на вашу функцию получения данных
    if characters_data is None:
        raise HTTPException(status_code=404, detail="Characters not found")
    return characters_data

@app.get("/genres")
async def genres_page(request: Request):
    # Получение данных для жанров
    genres_data = await get_anime_genres()  # Замените на вашу функцию получения данных
    if genres_data is None:
        raise HTTPException(status_code=404, detail="Genres not found")
    return genres_data

@app.get("/person")
async def person_page(request: Request):
    # Получение данных для персон
    person_data = await get_person()  # Замените на вашу функцию получения данных
    if person_data is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return person_data

@app.get("/producers")
async def producers_page(request: Request):
    # Получение данных для продюсеров
    producers_data = await get_producers()  # Замените на вашу функцию получения данных
    if producers_data is None:
        raise HTTPException(status_code=404, detail="Producers not found")
    return producers_data

@app.get("/seasons")
async def seasons_page(request: Request):
    # Получение данных для сезонных аниме
    seasons_data = await get_seasons()  # Замените на вашу функцию получения данных
    if seasons_data is None:
        raise HTTPException(status_code=404, detail="Seasons not found")
    return seasons_data

@app.get("/top")
async def top_page(request: Request):
    # Получение данных для топов
    top_data = await get_top_anime()  # Замените на вашу функцию получения данных
    if top_data is None:
        raise HTTPException(status_code=404, detail="Top data not found")
    return top_data

@app.get("/search")
async def search(request: Request, query: str):
    # Логика поиска аниме
    search_results = await get_anime(query)
    # Отладка: печатаем данные, которые передаются в шаблон
    print(search_results)
    
    return templates.TemplateResponse("search_result.html", {
        "request": request,
        "results": search_results,
        "query": query
    })
