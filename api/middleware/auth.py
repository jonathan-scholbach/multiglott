from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from pydantic import BaseModel

from sqlalchemy.orm import Session

from config import config
from database import get_db
from models.user import User
from schemas.auth import Token, TokenData


ALGORITHM = "HS256"
TOKEN_VALIDITY_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token", auto_error=False)


def create_access_token(
    data: dict, 
    expires_delta: timedelta = timedelta(minutes=TOKEN_VALIDITY_MINUTES),
    algorithm: str = ALGORITHM
):
    expire = datetime.utcnow() + expires_delta
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(
        data, config["API_SECRET_KEY"], algorithm=algorithm
    )

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, 
            config["API_SECRET_KEY"], 
            algorithms=[ALGORITHM]
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


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
):
    if not current_user.verified:
        raise HTTPException(status_code=400, detail="User not verified.")
    return current_user
