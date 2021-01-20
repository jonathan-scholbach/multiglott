from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.database import get_db
from db.models.user import User
from middleware.auth import create_access_token
from schemas.auth import Token


auth_routes = APIRouter(
    prefix="/auth",
)


@auth_routes.post("/token", response_model=Token)
def login(
    data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    email = data.username
    password = data.password

    user = User.get(db=db, value=email, key="email")
    if not user:
        raise HTTPException(
            status_code=401,
            detail="These credentials do not match our records.",
        )
    if not user.verify_password(plaintext_password=password):
        raise HTTPException(
            status_code=401,
            detail="These credentials do not match our records.",
        )

    access_token = create_access_token(data=dict(sub=email))

    return {"access_token": access_token, "token_type": "bearer"}
