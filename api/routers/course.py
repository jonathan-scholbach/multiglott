from fastapi import APIRouter


course_router = APIRouter(
    prefix="/courses",
)

@course_router.get("/")
def index_courses():
    return {"Hello": "World"}


@course_router.get("/{id}")
def fetch_course(id: int):
    pass


@course_router.post("/")
def create_course():
    pass


@course_router.put("/{id}")
def update_course():
    pass