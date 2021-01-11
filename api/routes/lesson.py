import os
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Form
from sqlalchemy.orm import Session

from database import get_db
from models import Course, Lesson, User
from schemas.lesson import Lesson as LessonSchema
from middleware.auth import get_verified_user


lesson_routes = APIRouter(
    prefix="/lessons",
)


@lesson_routes.post("/")
def create_lesson(
    course_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_verified_user),
):
    title, _ = os.path.splitext(file.filename)
    title = title.replace("_", " ")

    course = Course.get(db=db, value=course_id)

    if not course:
        raise HTTPException(status_code=400, detail="Course not found.")

    if not course.author_id == user.id:
        raise HTTPException(
            status_code=401,
            detail="User lacks privilege to change this course.",
        )

    db_lesson = Lesson.from_csv(
        db=db, title=title, course_id=course.id, csv_file=file.file
    )

    return db_lesson
