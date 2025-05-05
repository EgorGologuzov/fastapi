from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
  username: str = Field(example="Egor Gologuzov", min_length=3, max_length=60)
  password: str = Field(example="12345678", min_length=8, max_length=60)
  email: EmailStr | None = Field(None)


class UserReturn(BaseModel):
  id: int
  username: str = Field(example="Egor Gologuzov")
  email: EmailStr | None = Field(None, example="example@email.com")

