from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserWithPassword(UserBase):
    password: str


class User(UserBase):
    id: int
    auth_token: str
    
    class Config:
        orm_mode = True


class AuthToken(BaseModel):
    token: str