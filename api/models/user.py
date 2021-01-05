import os
import secrets

from datetime import datetime
from typing import Any

from fastapi import Depends, HTTPException
from itsdangerous import URLSafeTimedSerializer
from passlib.hash import pbkdf2_sha256
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, relationship

from config import config
from database import Base
from mail import send_mail
from main import get_db
from models.db_model import DBModel
from schemas.user import UserBase


class User(DBModel, Base):
    name = Column(String, unique=True)
    email = Column(String, unique=True)

    password_hash = Column(String)

    verification_token = Column(String)
    verified = Column(Boolean, default=False)

    owned_courses = relationship("Course")

    @classmethod
    def create(cls, db: Session, user: UserBase) -> "User":
        if User.get(db=db, value=user.name, key="name"):
            raise HTTPException(
                status_code=422,
                detail=(
                    f"The name {user.name} is already in use. ",
                    f"Please pick a different user name.",
                ),
            )

        if User.get(db=db, value=user.email, key="email"):
            raise HTTPException(
                status_code=422,
                detail=(
                    f"There is already an account linked to the email ",
                    f"{user.email}.",
                ),
            )

        db_user = cls(
            email=user.email,
            name=user.name,
            password_hash=User.hash_password(plaintext_password=user.password),
            created_at=datetime.now(),
            verification_token=User.create_verification_token(user.email),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def create_verification_token(email: str) -> str:
        serializer = URLSafeTimedSerializer(config["API_SECRET_KEY"])

        return serializer.dumps(
            email, salt=config["API_SECURITY_PASSWORD_SALT"]
        )

    @staticmethod
    def verification_token(token: str) -> str:
        serializer = URLSafeTimedSerializer(config["API_SECRET_KEY"])
        try:
            email = serializer.loads(
                token, salt=config["API_SECURITY_PASSWORD_SALT"]
            )
        except:
            raise HTTPException(
                status_code=401, detail="Invalid Authentication Token."
            )

        return email

    @staticmethod
    def hash_password(plaintext_password: str) -> str:
        return pbkdf2_sha256.hash(plaintext_password)

    def verify_password(self, plaintext_password: str) -> bool:
        return pbkdf2_sha256.verify(plaintext_password, self.password_hash)

    def send_confirmation_mail(self):
        href = f"http://{config['API_URL']}/{config['API_VERSION']}/users/confirm/{self.verification_token}"
        html_body = f'\t\tPlease <a target="_blank" href="{href}">confirm</a> your account on jargon.\n'

        send_mail(
            sender_email="do-not-reply@jargon.org",
            receiver_email=self.email,
            subject=f"Confirm your account on {config['API_DOMAIN']}",
            html_body=html_body,
        )
