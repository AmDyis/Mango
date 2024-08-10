from jikanpy import Jikan
from pprint import pprint

jikan = Jikan()

# Получение информации о конкретном аниме
anime_id = 1  # ID аниме, например, 1 — это "Cowboy Bebop"
anime = jikan.anime(anime_id)

# Извлечение данных с учетом возможного отсутствия некоторых полей
title = anime["data"].get("title", "Название неизвестно")
aired_from = anime["data"]["aired"].get("from", "Дата начала неизвестна")
aired_to = anime["data"]["aired"].get("to", "Дата окончания неизвестна")
episodes = anime["data"].get("episodes", "Количество эпизодов неизвестно")
duration = anime["data"].get("duration", "Продолжительность неизвестна")
genres = [genre.get("name", "Жанр неизвестен") for genre in anime["data"].get("genres", [])]
images_jpg = anime["data"]["images"]["jpg"].get("image_url", "Изображение отсутствует")
images_webp = anime["data"]["images"]["webp"].get("image_url", "Изображение отсутствует")
studios = [studio.get("name", "Студия неизвестна") for studio in anime["data"].get("studios", [])]
synopsis = anime["data"].get("synopsis", "Синопсис отсутствует")

# Дополнительные данные
anime_type = anime["data"].get("type", "Тип неизвестен")
status = anime["data"].get("status", "Статус неизвестен")
rating = anime["data"].get("score", "Рейтинг отсутствует")
age_rating = anime["data"].get("rating", "Возрастной рейтинг неизвестен")
source = anime["data"].get("source", "Источник неизвестен")
demographics = [demo.get("name", "Аудитория неизвестна") for demo in anime["data"].get("demographics", [])]
trailer_url = anime["data"]["trailer"].get("url", "Трейлер отсутствует")
mal_url = anime["data"].get("url", "URL MAL отсутствует")

# Вывод данных
pprint({
    "title": title,
    "aired_from": aired_from,
    "aired_to": aired_to,
    "episodes": episodes,
    "duration": duration,
    "genres": genres,
    "images_jpg": images_jpg,
    "images_webp": images_webp,
    "studios": studios,
    "synopsis": synopsis,
    "type": anime_type,
    "status": status,
    "rating": rating,
    "age_rating": age_rating,
    "source": source,
    "demographics": demographics,
    "trailer_url": trailer_url,
    "mal_url": mal_url
})
