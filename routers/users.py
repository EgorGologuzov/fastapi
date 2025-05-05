from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from pyd.users import UserCreate, UserReturn
from models import User
from hashlib import sha256


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/user", response_model=UserReturn)
def registration_new_user(create_data: UserCreate, db: Session = Depends(get_db)):

  found_user = db.query(User).filter(User.username == create_data.username).first()

  if found_user:
    raise HTTPException(400, "Пользователь с таким именен уже существует")
  
  new_user = User(**create_data.model_dump(exclude=["password"]), password_hash=sha256(create_data.password.encode("utf-8")).hexdigest())
  db.add(new_user)
  db.commit()

  return new_user

