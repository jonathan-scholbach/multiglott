from contextlib import suppress
from typing import List, Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Session
from sqlalchemy.types import ARRAY

from db.database import Base
from db.models.db_model import DBModel
from privileges import Privilege, AccessConstricted
from schemas.course import CourseCreate


class Course(DBModel, AccessConstricted, Base):
    PROPS_MAP = {"lesson_order": "_lesson_order"}

    title = Column(String, unique=True)
    slug = Column(String, unique=True)

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

    _lessons = relationship("Lesson")
    _lesson_order = Column(ARRAY(Integer), default=[])

    @classmethod
    def create(cls, db, course: CourseCreate, author_id: int) -> "Course":
        db_course = cls(
            title=course.title,
            slug=course.slug,
            target_language_id=course.target_language_id,
            source_language_id=course.source_language_id,
            author_id=author_id,
        )

        db.add(db_course)
        db.commit()
        db.refresh(db_course)

        return db_course

    @property
    def lesson_order(self):
        if not self._lesson_order:
            return [lesson.id for lesson in self._lessons]
        else:
            missing_lesson_ids = [
                lesson.id
                for lesson in self._lessons
                if lesson.id not in self._lesson_order
            ]

            return self._lesson_order + missing_lesson_ids

    @lesson_order.setter
    def lesson_order(self, value: List[int]) -> None:
        self._lesson_order = value

    @property
    def lessons(self):
        return sorted(
            self._lessons, key=lambda lesson: self.lesson_order.index(lesson.id)
        )

    def access_privileges(
        self, db: Session, user: Optional["User"] = None
    ) -> List["Privilege"]:
        privileges = [Privilege.CAN_READ]

        with suppress(AttributeError):
            if self.author_id == user.id:
                privileges += [Privilege.CAN_EDIT, Privilege.CAN_DELETE]

        return privileges
