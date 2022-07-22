from http import HTTPStatus
from re import S
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from database import get_db

from src.services.article import get_all_articles_service, get_article_by_id_service
from src.services.statement import get_statements_by_article_id


router = APIRouter()


@router.get("/article/headers/{user_id}/{page}")
def get_article_headers(page: int, user_id: str, db: Session = Depends(get_db)):
    article_metadata = get_all_articles_service(db, user_id, (page - 1) * 10, 10)

    if(not article_metadata or article_metadata is None):
        return JSONResponse(jsonable_encoder({"msg": "Articles not found"}), HTTPStatus.NOT_FOUND)

    compact_result = map(lambda article: jsonable_encoder({
        "header": article.header,
        "sub_header": article.sub_header[:50],
        "status": article.status
    }), article_metadata)

    return JSONResponse(jsonable_encoder({"page": compact_result}), HTTPStatus.OK)


# @router.get("/article/{article_id}")
# def get_article_by_id(article_id: int, db: Session = Depends(get_db)):
#     article = get_article_by_id_service(db, article_id)
#     statements = get_statements_by_article_id(db, article_id)

#     if(article is None):
#         return JSONResponse(jsonable_encoder({
#             "msg": "No articles found"
#             }),
#             HTTPStatus.NOT_FOUND
#         )
