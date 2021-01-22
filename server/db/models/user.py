import os
import secrets

from datetime import datetime
from typing import Any, Iterable

from fastapi import Depends, HTTPException
from itsdangerous import URLSafeTimedSerializer
from passlib.hash import pbkdf2_sha256
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Table
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, relationship

from config import config

from ..database import Base, get_db

from .db_model import DBModel
from .lesson import Lesson
from .user_vocab_progress import UserVocabProgress
from .vocab import Vocab

from mail import send_mail

from schemas.user import UserBase


class User(DBModel, Base):
    name = Column(String, unique=True)
    email = Column(String, unique=True)

    password_hash = Column(String)

    verification_token = Column(String)
    verified = Column(Boolean, default=False)

    owned_courses = relationship("Course")
    vocabs = relationship(
        "Vocab",
        secondary=UserVocabProgress.__table__,
        back_populates="students",
        lazy="dynamic",
    )

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

    def send_confirmation_mail(self) -> None:
        href = (
            f"http://{config['API_URL']}/{config['API_VERSION']}/users/"
            f"confirm/{self.verification_token}"
        )
        html_body = (
            f'\t\tPlease <a target="_blank" href="{href}">confirm</a> '
            f'your account on {config["APP_NAME"]} by clicking the link.'
        )

        send_mail(
            sender_email=f"do-not-reply@{config['APP_NAME']}.org",
            receiver_email=self.email,
            subject=f"Confirm your account on {config['APP_NAME']}",
            html_body=html_body,
        )

    def next_vocab_in_lesson(
        self,
        lesson_id: int,
    ) -> "Vocab":
        db = next(get_db())
        vocabs_in_lesson = (
            db.query(Vocab).filter(Vocab.lesson_id == lesson_id).all()
        )

        return min(
            vocabs_in_lesson,
            key=lambda vocab: self.progress_percentage(
                db=db, vocab_id=vocab.id
            ),
        )

    def _raw_progress(
        self,
        db: Session,
        vocab_id: int,
        lookback: int = config["LOOKBACK"],
    ) -> str:
        progress_entry = (
            db.query(UserVocabProgress)
            .filter(UserVocabProgress.user_id == self.id)
            .filter(UserVocabProgress.vocab_id == vocab_id)
            .first()
        )

        if progress_entry:
            return progress_entry.progress

        return ""

    def progress_percentage(
        self,
        db: Session,
        vocab_id: int,
        lookback: int = config["LOOKBACK"],
    ) -> float:
        raw_progress = self._raw_progress(
            db=db, vocab_id=vocab_id, lookback=lookback
        )
        if not raw_progress:
            return 0

        return sum(int(x) for x in raw_progress[-lookback:]) / lookback

    def accomplishment(
        self,
        db: Session,
        lesson_id: int,
        lookback: int = config["LOOKBACK"],
    ) -> float:
        lesson = Lesson.get(db=db, value=lesson_id)

        if not lesson.vocabs:
            return 0

        return sum(
            self.progress_percentage(
                db=db, vocab_id=vocab.id, lookback=lookback
            )
            for vocab in lesson.vocabs
        ) / len(lesson.vocabs)
