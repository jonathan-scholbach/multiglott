from contextlib import suppress
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from pydantic import BaseModel

from sqlalchemy.orm import Session

from config import config
from db.database import get_db
from db.models.user import User
from schemas.auth import Token, TokenData


ALGORITHM = "HS256"
TOKEN_VALIDITY_MINUTES = 60 * 24 * 7 * 31


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token", auto_error=False)


def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=TOKEN_VALIDITY_MINUTES),
    algorithm: str = ALGORITHM,
) -> "str":
    expire = datetime.utcnow() + expires_delta
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(
        data, config["API_SECRET_KEY"], algorithm=algorithm
    )

    return encoded_jwt


async def get_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> "User":
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(
            token, config["API_SECRET_KEY"], algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = User.get(db=db, value=token_data.username, key="email")

    if user is None:
        raise credentials_exception

    return user


async def get_verified_user(
    user: User = Depends(get_user),
) -> "User":
    if not user.verified:
        raise HTTPException(status_code=400, detail="User not verified.")
    return user


async def get_verified_user_or_none(
    token: str = Depends(oauth2_scheme), db=Depends(get_db)
) -> Optional["User"]:
    """Return verified user. If can't be identified, don't raise, return None."""

    with suppress(HTTPException):
        user = await get_user(token, db=db)
        if user.verified:
            return user

    return None
