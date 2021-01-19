from sqlalchemy import Column, ForeignKey, Integer, String, Table

from database import Base
from models.db_model import DBModel


class UserVocabProgress(DBModel, Base):
    __tablename__ = "user_vocab_progress"

    user_id = Column(Integer, ForeignKey("user.id"))
    vocab_id = Column(Integer, ForeignKey("vocab.id"))
    progress = Column(String, default="")
