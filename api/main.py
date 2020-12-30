import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from config import config


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{config['POSTGRES_USER']}:{config['POSTGRES_PASSWORD']}"
    f"@{config['POSTGRES_HOST']}:{config['POSTGRES_PORT']}/{config['POSTGRES_DB']}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from routers import v1_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.include_router(v1_router)


@app.get("/")
async def root():
    return {"Hello, ": "World!"}


from models import User, Course

Base.metadata.create_all(bind=engine)
