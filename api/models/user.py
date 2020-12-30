import os
import secrets

from datetime import datetime
from typing import Any

from fastapi import HTTPException
from itsdangerous import URLSafeTimedSerializer
from passlib.hash import pbkdf2_sha256
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config import config
from schemas.user import UserBase
from .db_base_model import DBBaseModel
from database import Base
from mail import send_mail

class User(DBBaseModel, Base):
    __tablename__ = "users"

    name = Column(String, unique=True)
    email = Column(String, unique=True)

    password_hash = Column(String)

    confirmation_token = Column(String)
    confirmed = Column(Boolean, default=False)

    _auth_token = Column(String, nullable=True, default=None)

    @classmethod
    def create(cls, db: Session, user: UserBase) -> "User":
        if User.get(db=db, value=user.name, key="name"):
            raise HTTPException(
                status_code=422,
                detail=(
                    f"The name {user.name} is already in use. ",
                    f"Please pick a different user name.",
                )
            )

        if User.get(db=db, value=user.email, key="email"):
            raise HTTPException(
                status_code=422,
                detail=(
                    f"There is already an account linked to the email ",
                    f"{user.email}."
                )
            )

        db_user = cls(
            email=user.email,
            name=user.name,
            password_hash=User.hash_password(plaintext_password=user.password),
            created_at=datetime.now(),
            confirmation_token=User.create_confirmation_token(user.email),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def create_confirmation_token(email: str) -> str:
        serializer = URLSafeTimedSerializer(config["API_SECRET_KEY"])

        return serializer.dumps(email, salt=config["API_SECURITY_PASSWORD_SALT"])

    @staticmethod
    def confirmation_token(token: str, expiration: int = 3600):
        serializer = URLSafeTimedSerializer(config["API_SECRET_KEY"])
        try:
            email = serializer.loads(
                token, salt=config["API_SECURITY_PASSWORD_SALT"], max_age=expiration
            )
        except:
            return False

        return email

    @staticmethod
    def hash_password(plaintext_password: str) -> str:
        return pbkdf2_sha256.hash(plaintext_password)

    def verify_password(self, plaintext_password: str) -> bool:
        return pbkdf2_sha256.verify(plaintext_password, self.password_hash)

    @property
    def auth_token(self):
        if not self._auth_token:
            self._refresh_auth_token()

        return self._auth_token

    def _refresh_auth_token(self):
        new_token = secrets.token_hex(32)
        self._auth_token = new_token

    def send_confirmation_mail(self):
        href = f"{config['API_URL']}/{config['API_VERSION']}/users/confirm/{self.confirmation_token}"
        html_body = (
            "<html>\n"
            "\t<body>\n"
            f"\t\tPlease <a target='_blank' href={href}>confirm</a> your account on jargon.\n"
            "\t</body>\n"
            "</html>"
        )
        
        send_mail(
            sender_email="do-not-reply@jargon.org", 
            receiver_email=self.email,
            subject=f"Confirm your account on {config['API_DOMAIN']}",
            html_body=html_body
        )
