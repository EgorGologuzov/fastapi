from typing import Optional
from pydantic import BaseModel, Field


class ItemFields:
  id: int = Field(
    default=...,
    gt=0,
  )
  name: str = Field(
    default=...,
    min_length=2,
    max_length=100,
  )
  price: float = Field(
    default=...,
    gt=0,
  )
  description: Optional[str] = Field(
    default=None,
    max_length=500,
  )


# модели
class Item(BaseModel):
  id: int = ItemFields.id
  name: str = ItemFields.name
  price: float = ItemFields.price
  description: str = ItemFields.description

  class ItemCreate(BaseModel):
    name: str = ItemFields.name
    price: float = ItemFields.price
    description: str = ItemFields.description

    class Config:
      json_schema_extra = {
        "openapi_examples": {
          "normal": {
            "value": {
              "name": "Мой крутой товар",
              "price": 9999.9,
              "description": "Это очень крутой товар",
            },
          },
          "invalid": {
            "value": {
              "name": "1",
              "price": -1,
              "description": "1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
            },
          },
        }
      }

