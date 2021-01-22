from contextlib import suppress
from datetime import datetime
from typing import Any, Dict, Iterable, Optional, TypeVar

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import Session
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.ext.declarative import declared_attr

from db.database import get_db
from utils.class_utils import properties


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
        for key, value in kwargs.items():
            try:
                prop = getattr(self.__class__, key).property
            except AttributeError:
                continue
            if key == "id" or type(prop) is RelationshipProperty:
                continue
            with suppress(AttributeError):
                setattr(self, key, value)

        db.commit()

    def serialized(self):
        """JSON-compatible dict of public attributes and properties."""
        dictionary = jsonable_encoder(self)
        dictionary.update(
            {
                prop: jsonable_encoder(getattr(self, prop))
                for prop in properties(self.__class__)
            }
        )

        return {
            key: value
            for key, value in dictionary.items()
            if not key.startswith("_")
        }
