from fastapi import FastAPI
from routers import genres, movies, users
from fastapi.staticfiles import StaticFiles
import os
from settings import POSTERS_DIR


app = FastAPI()


app.include_router(genres.router)
app.include_router(movies.router)
app.include_router(users.router)

# Создаем папку для хранения постеров
os.makedirs(POSTERS_DIR, exist_ok=True)

# Раздаем статику (для доступа к загруженным постерам)
app.mount("/static", StaticFiles(directory="static"), name="static")

