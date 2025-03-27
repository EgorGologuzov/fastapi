from fastapi import FastAPI, HTTPException, Query
import random
from math import sqrt


app = FastAPI()


@app.get("/about")
async def information_about_developer():
    return {
        "firstname": "Егор",
        "lastname": "Гологузов",
        "group": "Т-323901-НТ",
        "university": "НТИ (филиал УРФУ)",
        "email": "gologuzovegor@gmail.com"
    }


@app.get("/rnd")
async def random_integer_from_1_to_10():
    return {"randint": random.randint(1, 10)}


@app.post("/t_square")
async def calculate_perimeter_and_area_for_triangle_by_3_sides(
    a: float = Query(..., gt=0, description="Сторона A > 0"),
    b: float = Query(..., gt=0, description="Сторона B > 0"),
    c: float = Query(..., gt=0, description="Сторона C > 0"),
):
    if not (a + b > c and a + c > b and b + c > a):
        raise HTTPException(
            status_code=400,
            detail="Треугольник с такими сторонами не существует"
        )
    
    perimeter = a + b + c
    p = perimeter / 2
    area = sqrt(p * (p - a) * (p - b) * (p - c))
    
    return {"perimeter": perimeter, "area": area}

