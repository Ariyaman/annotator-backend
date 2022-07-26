from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db

from src.schemas.db_schemes import HolderSchema


def get_all_articles_holder_service(db:Session = Depends(get_db)):
    return db.query(HolderSchema).all()