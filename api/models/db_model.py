from contextlib import suppress
from datetime import datetime
from typing import Any, Iterable, Optional, TypeVar

from fastapi import Depends
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declared_attr

from database import get_db


Class = TypeVar("Class")


class DBModel:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    @classmethod
    def get(
        cls: Class,
        db: Session,
        value: Any,
        key: str = "id",
    ) -> Optional[Class]:
        return db.query(cls).filter(getattr(cls, key) == value).first()

    @classmethod
    def fetch(
        cls: Class,
        db: Session,
        value: Any,
        key: str,
    ) -> Iterable[Class]:
        return db.query(cls).filter(getattr(cls, key) == value)

    @classmethod
    def index(
        cls: Class,
        db: Session,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> Iterable[Class]:
        query = db.query(cls).offset(offset)
        if limit:
            query = query.limit(limit)

        return query.all()

    def delete(
        self,
        db: Session,
    ) -> None:
        db.query(self.__class__).filter(self.__class__.id == self.id).delete()
        db.commit()

    def update(self, db: Session, **kwargs) -> "User":
        for key, val in kwargs.items():
            with suppress(AttributeError):
                setattr(self, key, val)

        self.updated_at = datetime.now()

        db.add(self)
        db.commit()

        return self
