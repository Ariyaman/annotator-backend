import csv
from fastapi import FastAPI, Depends 
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session


from database import Base, engine, get_db
from src.router import user, article
from src.schemas.db_schemes import ArticleSchema

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

# TODO: Create a endpoint to set file in db
# @app.get("/test")
# def test(db: Session = Depends(get_db)):
#     file = open("title_synopsis_article2.csv", "r")

#     csvreader = csv.reader(file)

#     header = next(csvreader)

#     data = []

#     user_id = ""

#     for row in csvreader:
#         temp_data = ArticleSchema(
#             date = row[0],
#             article_id = row[1],
#             header = row[2],
#             sub_header = row[3],
#             news = row[4],
#             article_user = user_id
#         )

#         data.append(temp_data)
    
#     db.bulk_save_objects(data)

#     db.commit()

#     print("Done")
#     return {"OK!"}