from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Course, User, Language
from schemas.course import CourseCreate, CourseSubmit, Course as CourseSchema
from middleware.auth import get_current_user


course_routes = APIRouter(
    prefix="/courses",
)


@course_routes.get("/", response_model=List[CourseSchema])
def index_courses(db: Session = Depends(get_db)):
    return Course.index(db=db)


@course_routes.get("/{id}", response_model=CourseSchema)
def fetch_course(id: int):
    return Course.get(id)

@course_routes.post("/")
def create_course(
    course: CourseSubmit,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    target_language = Language.get_or_create(db=db, name=course.target_language)
    source_language = Language.get_or_create(db=db, name=course.source_language)
    
    Course.create(
        db=db,
        course=CourseCreate(
            target_language_id=target_language.id,
            source_language_id=source_language.id,
            title=course.title,
        ),
        author_id=user.id,
    )


@course_routes.put("/{id}")
def update_course():
    pass
