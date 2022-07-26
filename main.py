import csv
from fastapi import FastAPI, Depends 
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session


from database import Base, engine, get_db
from src.router import user, article
from src.schemas.db_schemes import HolderSchema

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router)
app.include_router(article.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return "Nothing to see here. Please do not break my back."

# TODO: Create a protected endpoint to get file

# @app.get("/test")
# def test(db: Session = Depends(get_db)):
#     file = open("title_synopsis_article.csv", "r")

#     csvreader = csv.reader(file)

#     header = next(csvreader)

#     data = []

#     for row in csvreader:
#         temp_data = HolderSchema(
#             header = row[0],
#             sub_header = row[1],
#             news = row[2]
#         )

#         data.append(temp_data)
    
#     db.bulk_save_objects(data)

#     db.commit()

#     print("Done")
#     return {"OK!"}