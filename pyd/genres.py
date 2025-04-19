from pydantic import BaseModel, Field


id_field = Field(..., gt=0, example=1)
name_field = Field(..., min_length=2, max_length=50, example="Боевик")
description_field = Field(None, min_length=2, max_length=200, example="Фильмы с динамичными сценами борьбы и погонями.")


class GenreReturn(BaseModel):
  id: int = id_field
  name: str = name_field
  description: str = description_field

  class Config:
    orm_mode = True


class GenreReturnShort(BaseModel):
  id: int = id_field
  name: str = name_field

  class Config:
    orm_mode = True


class GenreCreate(BaseModel):
  name: str = name_field
  description: str = description_field

  class Config:
    orm_mode = True

