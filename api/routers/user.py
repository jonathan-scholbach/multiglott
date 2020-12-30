from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from main import get_db
from models import User
from schemas import UserBase, UserSchema, AuthToken, UserWithPassword


user_router = APIRouter(prefix="/users")

@user_router.get("/", response_model=List[UserSchema])
def index_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@user_router.post("/", response_model=UserSchema)
def create_user(user: UserWithPassword, db: Session = Depends(get_db)):
    db_user = User.create(db, user)

    return db_user

@user_router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    id = int(id)
    return User.delete(db, id)

@user_router.get("/confirm/{token}", response_model=UserSchema)
def confirm_user(token: str, db: Session = Depends(get_db)):
    db_user = User.get(db=db, value=token, key="confirmation_token")
    db_user.confirmed = True
    db.add(db_user)
    db.commit()

    return db_user

@user_router.post("/login", response_model=UserSchema)
def login_user(user: UserWithPassword, db: Session = Depends(get_db)):
    exception = HTTPException(
        status_code=401, 
        detail="These credentials do not match our records"
    )
    db_user = User.get(db=db, value=user.email, key="email")
    if not db_user:
        raise exception

    if db_user.verify_password(user.password):
        return db_user
    else:
        raise exception
    
@user_router.get("/logout")
def logout_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = User.get(db=db, value=user.id)
    db_user.refresh_auth_token()

@user_router.get("/{email}", response_model=UserSchema)
def fetch_user(id: int, db: Session = Depends(get_db)):
    return User.get(db=db, value=user.email, key="email")
