from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Session

from database import Base
from schemas.user import UserBase


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    @classmethod
    def create(cls, db: Session, user: UserBase):
        created_at = datetime.now()
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = cls(
            email=user.email, 
            name=user.name, 
            password=fake_hashed_password, 
            created_at=created_at
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user
    
    @classmethod
    def delete(cls, db: Session, id: int):
        db.query(User).filter(User.id == id).delete()
        db.commit()
