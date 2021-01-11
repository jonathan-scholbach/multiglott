from fastapi import Depends
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship
from sqlalchemy.types import ARRAY

from database import Base
from models.db_model import DBModel
from models.user_vocab_progress import UserVocabProgress


class Vocab(DBModel, Base):
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
