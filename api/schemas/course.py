from typing import List, Optional

from pydantic import BaseModel

from schemas.lesson import Lesson


class CourseTorso(BaseModel):
    title: str


class Course(CourseTorso):
    id: Optional[int] = None
    slug: str
    source_language: str
    target_language: str
    author_id: Optional[int]

    class Config:
        orm_mode = True


class CourseSubmit(CourseTorso):
    source_language: str
    target_language: str


class CourseCreate(CourseTorso):
    slug: str
    source_language_id: int
    target_language_id: int
