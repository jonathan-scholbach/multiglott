from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from main import get_db
from models import Language

language_router = APIRouter(prefix="/languages")


@language_router.get("/")
def index_languages(db: Session = Depends(get_db)):
    return Language.index(db=db)
