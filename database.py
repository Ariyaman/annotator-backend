from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_URL = "mysql+pymysql://doadmin:AVNS_J9Bp5lhLemduOjUZ8HI@annotator-db-do-user-12101645-0.b.db.ondigitalocean.com:25060/annotator"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()