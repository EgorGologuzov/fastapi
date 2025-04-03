from fastapi import FastAPI, HTTPException, Query, Path, Body
from typing import List, Optional
from pydantic import BaseModel, Field
from items import ITEMS
from models import Item


app = FastAPI()


# Эндпоинт 1
class GetItemsListParams(BaseModel):
  name: Optional[str] = Query(
    default=None,
    min_length=2,
    description="Фильтр по названию (минимум 2 символа)",
    openapi_examples={
      "normal": {"value": "iphone"},
      "invalid": {"value": "i"},
    })
  min_price: Optional[float] = Query(
    default=None,
    gt=0,
    description="Минимальная цена (положительное число)",
    openapi_examples={
      "normal": {"value": 200},
      "invalid": {"value": -1},
    })
  max_price: Optional[float] = Query(
    default=None,
    gt=0,
    description="Максимальная цена (должна быть > min_price)",
    openapi_examples={
      "normal": {"value": 1000},
      "invalid": {"value": -1},
    })
  skip: Optional[int] = Query(
    default=0,
    ge=0,
    description="Пропустить первые несколько товаров из выборки (положительное число)",
    openapi_examples={
      "normal": {"value": 3},
      "invalid": {"value": -1},
    })
  limit: Optional[int] = Query(
    default=10,
    le=100,
    description="Лимит товаров (максимум 100)",
    openapi_examples={
      "normal": {"value": 3},
      "invalid": {"value": 101},
    })


@app.get(
  path="/items/",
  response_model=List[Item],
  summary="Получить список товаров",
  description="Фильтрация по названию, цене и лимиту",
  tags=["Товары"],
)
def get_items_list(params: GetItemsListParams = Query()):
  name = params.name
  min_price = params.min_price
  max_price = params.max_price
  skip = params.skip
  limit = params.limit

  filtered_items = ITEMS

  if max_price and min_price and max_price < min_price:
    raise HTTPException(
      status_code=400,
      detail="max_price должен быть больше min_price"
    )
  
  if name:
    filtered_items = [item for item in filtered_items if name.lower() in item["name"].lower()]
  
  if min_price is not None:
    filtered_items = [item for item in filtered_items if item["price"] >= min_price]
  
  if max_price:
    filtered_items = [item for item in filtered_items if item["price"] <= max_price]
  
  return filtered_items[skip : skip + limit]


# Эндпоинт 2
@app.get(
  path="/items/{item_id}",
  response_model=Item,
  summary="Получить информацию о товаре",
  description="Поиск одного товара по id",
  tags=["Товары"],
)
def get_item_info(
  item_id: int = Path(
    default=...,
    gt=0,
    description="ID товара (положительное число)",
    openapi_examples={
      "normal": {"value": 1},
      "invalid": {"value": -1},
    }),
):
  item = next((item for item in ITEMS if item["id"] == item_id), None)

  if not item:
    raise HTTPException(
      status_code=404,
      detail="Товар не найден"
    )
  
  return item


# Эндпоинт 3
@app.post(
  path="/items/",
  response_model=Item,
  summary="Создать товар",
  description="Создание товара из пользовательских данных",
  tags=["Товары"],
)
def create_item(
  data: Item.ItemCreate = Body(
    default=...,
    openapi_examples=Item.ItemCreate.Config.json_schema_extra["openapi_examples"],
  )
):
  next_id = max(item["id"] for item in ITEMS) + 1

  new_item = {
    "id": next_id,
    "name": data.name,
    "price": data.price,
    "description": data.description,
  }

  ITEMS.append(new_item)

  return new_item

