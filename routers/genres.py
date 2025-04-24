from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import Genre
from pyd.genres import GenreReturn, GenreCreate
from database import get_db
from auth import auth


router = APIRouter(prefix="/genres", tags=["genres"])


@router.get("/", response_model=List[GenreReturn])
def get_all_genres(db: Session = Depends(get_db)):
  
  return db.query(Genre).all()


@router.post("/", response_model=GenreReturn)
def create_genre(create_data: GenreCreate, db: Session = Depends(get_db), _ = Depends(auth)):
  
  existing_genre = db.query(Genre).filter(Genre.name == create_data.name).first()

  if existing_genre:
    raise HTTPException(400, "Жанр с таким названием уже существует")

  new_genre = Genre(**create_data.model_dump())
  db.add(new_genre)
  db.commit()
  db.refresh(new_genre)
  
  return new_genre
  


