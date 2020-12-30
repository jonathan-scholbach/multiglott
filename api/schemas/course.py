from pydantic import BaseModel


class Course(BaseModel):
    id: int
    title: str
    source_language: str
    target_language: str
