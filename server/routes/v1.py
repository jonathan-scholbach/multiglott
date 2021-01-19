from fastapi import APIRouter

from .auth import auth_routes
from .course import course_routes
from .language import language_routes
from .lesson import lesson_routes
from .me import me_routes
from .privilege import privilege_routes
from .query import query_route
from .user import user_routes


v1_routes = APIRouter(prefix="/v1")

v1_routes.include_router(auth_routes)
v1_routes.include_router(course_routes)
v1_routes.include_router(language_routes)
v1_routes.include_router(lesson_routes)
v1_routes.include_router(me_routes)
v1_routes.include_router(privilege_routes)
v1_routes.include_router(query_route)
v1_routes.include_router(user_routes)
