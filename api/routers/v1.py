from fastapi import APIRouter

from .course import course_router
from .user import user_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(course_router)
v1_router.include_router(user_router)
