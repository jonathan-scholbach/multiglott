from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base
from models.db_model import DBModel
from models.language import Language
from models.user import User
from schemas.course import CourseCreate


class Course(DBModel, Base):
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

    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship("User", foreign_keys=[author_id])

    lessons = relationship("Lesson")

    @classmethod
    def create(cls, db, course: CourseCreate, author_id: int):
        db_course = cls(
            title=course.title,
            target_language_id=course.target_language_id,
            source_language_id=course.source_language_id,
            author_id=author_id,
        )

        db.add(db_course)
        db.commit()
        db.refresh(db_course)

        return db_course


class Lesson(DBModel, Base):
    name = Column(String)

    course_id = Column(Integer, ForeignKey("course.id"))


class Vocab(DBModel, Base):
    source = Column(String)
    target = Column(String)

    lesson_id = Column(Integer, ForeignKey("lesson.id"))
