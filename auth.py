from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha256


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = "ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f" # password: 12345678


security = HTTPBasic()


def auth(credentials: HTTPBasicCredentials = Depends(security)):

  username = credentials.username
  password_hash = sha256(credentials.password.encode('utf-8')).hexdigest()

  if username != ADMIN_USERNAME or password_hash != ADMIN_PASSWORD_HASH:
    raise HTTPException(401, "Неверный логин или пароль")

