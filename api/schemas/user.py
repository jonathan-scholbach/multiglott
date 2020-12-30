from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserWithPassword(UserBase):
    password: str

class UserWithAuthToken(User):
    auth_token: str

class AuthToken(BaseModel):
    token: str
