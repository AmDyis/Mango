from fastapi import FastAPI, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv
from api_parser import (get_anime_by_title,
                        get_manga_by_title)
from routers import (
    characters,
    genres,
    magazines,
    person,
    producers,
    random,
    seasons,
    top,
    anime,
    manga,
    auth
)

load_dotenv()

app = FastAPI()


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        async with SessionLocal() as session:
            request.state.db = session
            response = await call_next(request)
            await session.commit()  # Убедитесь, что commit вызывается после обработки запроса
            return response

# Include all routers
app.include_router(characters.router)
app.include_router(genres.router)
app.include_router(magazines.router)
app.include_router(person.router)
app.include_router(producers.router)
app.include_router(random.router)
app.include_router(seasons.router)
app.include_router(top.router)
app.include_router(anime.router)
app.include_router(manga.router)
app.include_router(auth.router, tags=["auth"])

# Mount static files directory
app.mount("/static", StaticFiles(directory="../../frontend/static"), name="static")

templates = Jinja2Templates(directory="../../frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "anime_data": None})

@app.get("/search", response_class=HTMLResponse)
async def search_anime(request: Request, query: str):
    anime_data = await get_anime_by_title(query)
    return templates.TemplateResponse("index.html", {"request": request, "anime_data": anime_data})