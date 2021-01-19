from typing import Any

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Session

from database import Base
from models.db_model import DBModel


class Language(DBModel, Base):
    name = Column(String, primary_key=True)

    @classmethod
    def get_or_create(cls, db: Session, name: str) -> "Language":
        language = cls.get(db=db, value=name, key="name")

        if not language:
            language = cls(name=name)
            db.add(language)
            db.commit()

        return language
