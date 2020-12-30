from typing import Any, TypeVar

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declared_attr


Class = TypeVar("Class")


class DBBaseModel:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime)

    @classmethod
    def get(
        cls: Class,
        db: Session,
        value: Any,
        key: str = "id",
    ) -> Class:
        return db.query(cls).filter(getattr(cls, key) == value).first()

    def delete(self, db: Session) -> None:
        db.query(self.__class__).filter(self.__class__.id == self.id).delete()
        db.commit()
