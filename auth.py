from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import User
from hashlib import sha256


security = HTTPBasic()


def auth(
  credentials: HTTPBasicCredentials = Depends(security),
  db: Session = Depends(get_db),
):
  found_user = db.query(User).filter(User.username == credentials.username).first()

  if not found_user or sha256(credentials.password.encode("utf-8")).hexdigest() != found_user.password_hash:
    raise HTTPException(403, "Неверный логин или пароль")

  return found_user

