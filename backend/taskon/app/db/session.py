from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
session_local = sessionmaker(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
