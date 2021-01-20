from contextlib import suppress
from typing import List, Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Session

from db.database import Base
from db.models.db_model import DBModel
from privileges import Privilege, AccessConstricted
from schemas.course import CourseCreate


class Course(DBModel, AccessConstricted, Base):
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

    lessons = relationship("Lesson")

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

    def access_privileges(
        self, db: Session, user: Optional["User"] = None
    ) -> List["Privilege"]:
        privileges = [Privilege.CAN_READ]

        with suppress(AttributeError):
            if self.author_id == user.id:
                privileges += [Privilege.CAN_EDIT, Privilege.CAN_DELETE]

        return privileges
