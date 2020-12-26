import hashlib
import os

from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import Session

from itsdangerous import URLSafeTimedSerializer

from config import config
from database import Base
from schemas.user import UserBase


def get_confirmation_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(config["SECRET_KEY"])

    return serializer.dumps(email, salt=config["SECURITY_PASSWORD_SALT"])


def confirm_token(token: str, expiration: int=3600):
    serializer = URLSafeTimedSerializer(config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token,
            salt=config["SECURITY_PASSWORD_SALT"],
            max_age=expiration
        )
    except:
        return False
    return email

def hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    salt = Column(String)
    confirmation_token = Column(String)
    confirmed = Column(Boolean, default=False)

    @classmethod
    def get(cls, db: Session, value: Any, key: str = "id", ) -> "User":
        return db.query(cls).filter(getattr(cls, key) == value).first()

    @classmethod
    def create(cls, db: Session, user: UserBase) -> "User":
        salt = os.urandom(32)
        hashed_password = hash_password(
            password=user.password, 
            salt=salt
        )
        db_user = cls(
            email=user.email,
            name=user.name,
            password=hashed_password,
            salt=salt,
            created_at=datetime.now(),
            confirmation_token=get_confirmation_token(user.email)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @classmethod
    def delete(cls, db: Session, id: int):
        db.query(User).filter(User.id == id).delete()
        db.commit()
