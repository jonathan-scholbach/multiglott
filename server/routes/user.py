from typing import List
from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import User
from schemas import UserBase, UserSchema, UserWithPassword, UserWithAuthToken
from middleware.auth import get_verified_user


user_routes = APIRouter(prefix="/users")


@user_routes.get("/me", response_model=UserSchema)
def read_users_me(user: User = Depends(get_verified_user)):
    return user


@user_routes.get("/", response_model=List[UserSchema])
def index_users(db: Session = Depends(get_db)):
    return User.index(db=db)


@user_routes.post("/", response_model=UserSchema)
def create_user(user: UserWithPassword, db: Session = Depends(get_db)):
    db_user = User.create(db, user)
    try:
        db_user.send_confirmation_mail()
    except Exception as e:
        db_user.delete(db=db)
        logger = getLogger("fastapi")
        logger.log(msg=e, level=40)
        raise HTTPException(
            status_code=501, detail="Failed to send confirmation email."
        )

    return db_user


@user_routes.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    id = int(id)
    return User.delete(db, id)


@user_routes.get("/confirm/{token}", response_model=UserSchema)
def confirm_user(token: str, db: Session = Depends(get_db)):
    email = User.verification_token(token=token)
    db_user = User.get(db=db, value=email, key="email")
    if db_user:
        db_user.verified = True
        db.add(db_user)
        db.commit()

        return db_user
    else:
        raise HTTPException(
            status_code=422, detail="cannot find user with this token."
        )


@user_routes.post("/login", response_model=UserWithAuthToken)
def login_user(user: UserWithPassword, db: Session = Depends(get_db)):
    exception = HTTPException(
        status_code=401, detail="These credentials do not match our records"
    )
    db_user = User.get(db=db, value=user.email, key="email")
    if not db_user:
        raise exception

    if db_user.verify_password(user.password):
        if db_user.verified:
            return db_user
        else:
            raise HTTPException(
                status_code=401,
                detail=(
                    "The email address of this user has not been verified ",
                    "yet. Please click the link in the confirmation email.",
                ),
            )
    else:
        raise exception


@user_routes.get("/logout")
def logout_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = User.get(db=db, value=user.id)
    db_user.refresh_auth_token()


@user_routes.get("/{email}", response_model=UserSchema)
def fetch_user(email: str, db: Session = Depends(get_db)):
    return User.get(db=db, value=email, key="email")
