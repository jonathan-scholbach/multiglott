from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import (
    UserBase,
    Course as CourseSchema,
    UserSchema,
    UserWithPassword,
    UserWithAuthToken
)
from middleware.auth import get_current_user


me_routes = APIRouter(prefix="/me")


@me_routes.get("/", response_model=UserSchema)
def get_me(user: User = Depends(get_current_user)):
    return user


@me_routes.get("/courses", response_model=list)
def get_my_courses(user: User = Depends(get_current_user)):
    return [
        {
            "title": course.title,
            "id": course.id,
            "created_at": course.created_at,
            "target_language": course.target_language,
            "source_language": course.source_language,
        }
        for course in user.owned_courses
    ]