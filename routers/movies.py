from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import Movie, Genre
from pyd.movies import MovieReturn, MovieCreate, MovieUpdate
from database import get_db
from fastapi import UploadFile, File
import imghdr
import os
import uuid
from settings import POSTERS_DIR


router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/", response_model=List[MovieReturn])
def get_all_movies(db: Session = Depends(get_db)):

  return db.query(Movie).all()


@router.get("/{movie_id}", response_model=MovieReturn)
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):

  movie = db.query(Movie).filter(Movie.id == movie_id).first()

  if not movie:
    raise HTTPException(404, "Фильм с таким id не найден")

  return movie


@router.post("/", response_model=MovieReturn)
def create_movie(create_data: MovieCreate, db: Session = Depends(get_db)):

    genres = db.query(Genre).filter(Genre.id.in_(create_data.genre_ids)).all()

    if len(genres) != len(create_data.genre_ids):
      raise HTTPException(400, "Фильм ссылается на несуществующий жанр(ы)")

    movie = Movie(**create_data.model_dump(exclude={"genre_ids"}))
    movie.genres = genres

    db.add(movie)
    db.commit()
    db.refresh(movie)

    return movie


@router.put("/{movie_id}", response_model=MovieReturn)
def update_movie(movie_id: int, update_data: MovieUpdate, db: Session = Depends(get_db)):
    
  movie = db.query(Movie).filter(Movie.id == movie_id).first()

  if not movie:
    raise HTTPException(404, "Фильм с таким id не найден")

  for field, value in update_data.model_dump(exclude={"genre_ids"}, exclude_unset=True).items():
    setattr(movie, field, value)

  if update_data.genre_ids:
    genres = db.query(Genre).filter(Genre.id.in_(update_data.genre_ids)).all()

    if len(genres) != len(update_data.genre_ids):
      raise HTTPException(400, "Фильм ссылается на несуществующий жанр(ы)")
    
    movie.genres = genres

  db.commit()
  db.refresh(movie)

  return movie


@router.delete("/{movie_id}", response_model=MovieReturn)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):

  movie = db.query(Movie).filter(Movie.id == movie_id).first()

  if not movie:
    raise HTTPException(404, "Фильм с таким id не найден")

  db.delete(movie)
  db.commit()

  return movie


@router.put("/{movie_id}/image", response_model=MovieReturn)
async def upload_movie_poster(movie_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
  
  # Проверяем наличие фильма в БД
  movie = db.query(Movie).filter(Movie.id == movie_id).first()

  if not movie:
    raise HTTPException(404, "Фильм с таким id не найден")
  
  # Проверяем, что файл - изображение
  content_type = imghdr.what(file.file)

  if not content_type:
    raise HTTPException(400, "Файл не является изображением")

  # Проверяем размер файла
  max_size_megabytes = 3
  file.file.seek(0, 2)
  file_size = file.file.tell()
  file.file.seek(0)

  if file_size > max_size_megabytes * 1024 * 1024:
    raise HTTPException(400, f"Файл слишком большой. Максимальный размер: {max_size_megabytes} Мб")

  # Генерируем уникальное имя файла
  file_ext = file.filename.split(".")[-1]
  file_name = f"{uuid.uuid4()}.{file_ext}"
  file_path = os.path.join(POSTERS_DIR, file_name)

  # Сохраняем файл
  with open(file_path, "wb") as buffer:
    buffer.write(await file.read())

  # Обновляем запись о фильме в БД
  movie.poster_url = f"/static/posters/{file_name}"
  db.commit()
  db.refresh(movie)

  return movie

