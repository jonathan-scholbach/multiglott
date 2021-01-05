from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


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
    token: str = Field(alias="auth_token")

    class Config:
        orm_mode = True
