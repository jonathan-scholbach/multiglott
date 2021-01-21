from csv import DictReader
from tempfile import SpooledTemporaryFile
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Session

from config import config
from db.database import Base
from db.models.db_model import DBModel
from db.models.vocab import Vocab
from privileges import Privilege, AccessConstricted
from utils.string_utils import slug_from_title


class Lesson(DBModel, Base, AccessConstricted):
    title = Column(String)
    slug = Column(String)

    course_id = Column(Integer, ForeignKey("course.id"))
    course = relationship("Course", foreign_keys=[course_id])
    vocabs = relationship("Vocab")

    @classmethod
    def from_csv(
        cls,
        db: Session,
        title: str,
        course_id: int,
        csv_file: SpooledTemporaryFile,
    ) -> "Lesson":
        slug = slug_from_title(title)

        csv_file.seek(0)
        lines = [
            line.decode("utf-8").replace(r"\n", "")
            for line in csv_file.readlines()
        ]

        entries = list(
            DictReader(
                lines,
                delimiter=";",
                fieldnames=["target", "source", "hint"],
            )
        )

        errors = [
            index
            for index, row in enumerate(entries)
            if row["target"] is None or row["source"] is None
        ]
        if errors:
            raise HTTPException(
                status_code=400,
                detail=f"csv file malformatted at row(s) {errors}.",
            )

        db_lesson = Lesson(title=title, slug=slug, course_id=course_id)

        db.add(db_lesson)
        db.commit()
        db.refresh(db_lesson)

        for entry in entries:
            source = list(map(lambda x: x.strip(), entry["source"].split("|")))
            target = list(map(lambda x: x.strip(), entry["target"].split("|")))
            hint = entry["hint"]
            vocab = Vocab(
                lesson_id=db_lesson.id, source=source, target=target, hint=hint
            )
            db.add(vocab)

        db.commit()
        db.refresh(db_lesson)

        return db_lesson

    def access_privileges(
        self, db: Session, user: Optional["User"] = None
    ) -> List["Privilege"]:
        if not user:
            return []

        return self.course.access_privileges(db=db, user=user)
