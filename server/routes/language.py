from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Language

language_routes = APIRouter(prefix="/languages")


@language_routes.get("/")
def index_languages(db: Session = Depends(get_db)):
    return Language.index(db=db)
