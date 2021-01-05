from typing import Optional

from pydantic import BaseModel


class CourseTorse(BaseModel):
    title: str

class Course(CourseTorse):
    id: Optional[int] = None
    source_language: str
    target_language: str


class CourseSubmit(CourseTorse):
    source_language: str
    target_language: str


class CourseCreate(CourseTorse):
    source_language_id: int
    target_language_id: int