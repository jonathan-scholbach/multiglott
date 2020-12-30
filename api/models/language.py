from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from database import Base
from .db_base_model import DBBaseModel


class Language(DBBaseModel, Base):
    name = Column(String)
