from typing import Optional

from fastapi import Depends
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship
from sqlalchemy.types import ARRAY

from db.database import Base
from db.models.db_model import DBModel
from db.models.user_vocab_progress import UserVocabProgress
from privileges import AccessConstricted


class Vocab(DBModel, Base, AccessConstricted):
    target = Column(ARRAY(String))
    source = Column(ARRAY(String))
    hint = Column(String, nullable=True, default=None)

    lesson_id = Column(Integer, ForeignKey("lesson.id"))
    lesson = relationship("Lesson", foreign_keys=[lesson_id])

    students = relationship(
        "User",
        secondary=UserVocabProgress.__table__,
        back_populates="vocabs",
    )

    def access_privileges(self, db: Session, user: Optional["User"]):
        return self.lesson.access_privileges(db=db, user=user)
