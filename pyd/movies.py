from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from pyd.genres import GenreReturnShort


id_field: int = Field(..., gt=0, example=1)
title_field: str = Field(..., min_length=2, max_length=100, example="Название фильма")
year_field: int = Field(None, gt=1800, lt=2100, example=2010)
duration_field: int = Field(None, gt=0, example=127)
rating_field: float = Field(None, ge=0, le=10, example=7.8)
description_field: str = Field(None, min_length=2, max_length=500, example="Описание фильма")
poster_url_field: str = Field(None, min_length=2, max_length=200, example="https://example.com/poster.jpg")
create_at_field: datetime = Field(..., example=datetime.now())
genres_field: List[GenreReturnShort] = Field(None, example=[{ "id": 1, "name": "Боевик" }])
genre_ids_field: List[int] = Field(None, example=[1, 2])


class MovieReturn(BaseModel):
  id: int = id_field
  title: str = title_field
  year: int = year_field
  duration: int = duration_field
  rating: float = rating_field
  description: str = description_field
  poster_url: str = poster_url_field
  create_at: datetime = create_at_field
  genres: List[GenreReturnShort] = genres_field

  class Config:
    orm_mode = True


class MovieCreate(BaseModel):
  title: str = title_field
  year: int = year_field
  duration: int = duration_field
  rating: float = rating_field
  description: str = description_field
  poster_url: str = poster_url_field
  genre_ids: List[int] = genre_ids_field

  class Config:
    orm_mode = True


class MovieUpdate(BaseModel):
  title: str = title_field
  year: int = year_field
  duration: int = duration_field
  rating: float = rating_field
  description: str = description_field
  poster_url: str = poster_url_field
  genre_ids: List[int] = genre_ids_field

  class Config:
    orm_mode = True

