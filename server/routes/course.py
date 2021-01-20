from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Course, User, Language, Lesson
from middleware.auth import get_verified_user
from schemas.course import CourseCreate, CourseSubmit, Course as CourseSchema
from schemas.lesson import Lesson as LessonSchema
from utils.string_utils import slug_from_title


course_routes = APIRouter(
    prefix="/courses",
)


@course_routes.get("/", response_model=List[CourseSchema])
def index_courses(db: Session = Depends(get_db)):
    return [
        {
            "id": course.id,
            "title": course.title,
            "slug": course.slug,
            "source_language": course.source_language.name,
            "target_language": course.target_language.name,
            "author_id": course.author_id,
        }
        for course in Course.index(db=db)
    ]


@course_routes.get(
    "/{course_slug}/lessons/{lesson_slug}", response_model=LessonSchema
)
def fetch_lesson(
    course_slug: str, lesson_slug: str, db: Session = Depends(get_db)
):
    course = Course.get(db=db, value=course_slug, key="slug")

    if not course:
        raise HTTPException(
            status_code=404, detail="Course with that slug not found."
        )

    lesson = list(
        filter(lambda lesson: lesson.slug == lesson_slug, course.lessons)
    )[0]

    if not lesson:
        raise HTTPException(
            status_code=404, detail="Lesson with that slug not found."
        )

    return {
        "id": lesson.id,
        "title": lesson.title,
        "slug": lesson.slug,
        "course_id": course.id,
    }


@course_routes.post("/find")
def find_course(
    key: Any = Body(...),
    value: Any = Body(...),
    related_models: List[str] = Body(...),
    db=Depends(get_db),
):
    course = Course.get(db=db, value=value, key=key)

    if not course:
        raise HTTPException(
            status_code=404, detail=f"Cannot find Course with {key} = {value}."
        )

    serialized_course = jsonable_encoder(course)

    serialized_course.update(
        {
            related_model: getattr(course, related_model)
            for related_model in related_models
        }
    )

    return serialized_course


@course_routes.post("/")
def create_course(
    course: CourseSubmit,
    db: Session = Depends(get_db),
    user: User = Depends(get_verified_user),
):
    target_language = Language.get_or_create(db=db, name=course.target_language)
    source_language = Language.get_or_create(db=db, name=course.source_language)

    Course.create(
        db=db,
        course=CourseCreate(
            target_language_id=target_language.id,
            source_language_id=source_language.id,
            title=course.title,
            slug=slug_from_title(course.title),
        ),
        author_id=user.id,
    )


@course_routes.put("/{id}")
def update_course():
    pass
