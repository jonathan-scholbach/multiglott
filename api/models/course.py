from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base
from .db_base_model import DBBaseModel
from .language import Language


class Course(DBBaseModel, Base):
    title = Column(String)
    public = Column(Boolean, default=False)

    target_language_id = Column(Integer, ForeignKey("language.id"))
    target_language = relationship(
        "Language", foreign_keys=[target_language_id]
    )

    source_language_id = Column(Integer, ForeignKey("language.id"))
    source_language = relationship(
        "Language", foreign_keys=[source_language_id]
    )

    lessons = relationship("Lesson")


class Lesson(DBBaseModel, Base):
    name = Column(String)

    course_id = Column(Integer, ForeignKey("course.id"))


class Vocab(DBBaseModel, Base):
    source = Column(String)
    target = Column(String)

    lesson_id = Column(Integer, ForeignKey("lesson.id"))
