from fastapi import FastAPI, Query, Path, HTTPException
from typing import Optional


app = FastAPI()


fake_items_db = [
  {"id": 1, "name": "iPhone 13", "price": 999.99, "category": "phone"},
  {"id": 2, "name": "Samsung Galaxy S21", "price": 899.99, "category": "phone"},
  {"id": 3, "name": "MacBook Pro", "price": 1999.99, "category": "laptop"},
  {"id": 4, "name": "Dell XPS 15", "price": 1499.99, "category": "laptop"},
  {"id": 5, "name": "AirPods Pro", "price": 249.99, "category": "accessories"},
  {"id": 6, "name": "Logitech Mouse", "price": 49.99, "category": "accessories"},
  {"id": 7, "name": "iPad Air", "price": 599.99, "category": "tablet"},
  {"id": 8, "name": "Samsung Tablet", "price": 349.99, "category": "tablet"},
  {"id": 9, "name": "Smart Watch", "price": 199.99, "category": "wearable"},
  {"id": 10, "name": "Fitbit", "price": 129.99, "category": "wearable"},
]


@app.get("/items/")
def get_goods_list(
  name: Optional[str] = Query(None, min_length=2, description="Фильтр по названию (минимум 2 символа)"),
  min_price: Optional[float] = Query(None, gt=0, description="Минимальная цена (положительное число)"),
  max_price: Optional[float] = Query(None, gt=0, description="Максимальная цена (должна быть > min_price)"),
  limit: Optional[int] = Query(10, le=100, description="Лимит товаров (максимум 100)")
):
  filtered_items = fake_items_db
  
  if name:
    filtered_items = [item for item in filtered_items if name.lower() in item["name"].lower()]
  
  if min_price is not None:
    filtered_items = [item for item in filtered_items if item["price"] >= min_price]
  
  if max_price is not None:
    if min_price is not None and max_price < min_price:
      raise HTTPException(
        status_code=400,
        detail="max_price должен быть больше min_price"
      )
    filtered_items = [item for item in filtered_items if item["price"] <= max_price]
  
  return filtered_items[:limit]


# @app.get("/items/{item_id}")
# def get_good_info(
#   item_id: int = Path(..., gt=0, description="ID товара (положительное число)")
# ):
#   result = None

#   for item in fake_items_db:
#     if item["id"] == item_id:
#       result = item
#       break

#   if not result:
#     raise HTTPException(
#       status_code=404,
#       detail="Товар не найден"
#     )
  
#   return result

