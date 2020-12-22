from sqlalchemy import Column, Integer, String
from api.models import BaseModel


class Course(BaseModel):
    __tablename__ == "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String)
