from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from main import get_db
from models import User
from schemas import UserSchema, UserBase


user_router = APIRouter(
    prefix="/users",
)


@user_router.get("/", response_model=List[UserSchema])
def index_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@user_router.get("/{id}")
def fetch_user(id: int):
    pass


@user_router.post("/", response_model=UserSchema)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = User.create(db, user)

    return db_user


@user_router.put("/{id}")
def update_user():
    pass


@user_router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    id = int(id)
    return User.delete(db, id)


@user_router.get("/confirm/{token}")
def confirm_user(token: str, db: Session = Depends(get_db)):
    db_user = User.get(db=db, value=token, key="confirmation_token")
    db_user.confirmed = True
    db.add(db_user)
    db.commit()

    return db_user
