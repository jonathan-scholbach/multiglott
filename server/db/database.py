import os
from os.path import abspath, dirname
import sys

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server.config import config


Base = declarative_base()

if "DATABASE_URL" in config:
    DATABASE_URL = config["DATABASE_URL"]
else:
    DATABASE_URL = (
        f"postgresql://{config['POSTGRES_USER']}:{config['POSTGRES_PASSWORD']}"
        f"@{config['POSTGRES_HOST']}:{config['POSTGRES_PORT']}/{config['POSTGRES_DB']}"
    )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
