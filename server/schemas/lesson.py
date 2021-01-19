from pydantic import BaseModel


class Lesson(BaseModel):
    id: int
    title: str
    slug: str
    course_id: int

    class Config:
        orm_mode = True
