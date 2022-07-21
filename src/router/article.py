from http import HTTPStatus
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from database import get_db

from src.services.article import get_all_articles


router = APIRouter()


@router.get("/article_header/{user_id}/{page}")
def get_article_headers(page: int, user_id: str, db: Session = Depends(get_db)):
    article_metadata = get_all_articles(db, user_id, (page - 1) * 10, 10)

    if(not article_metadata or article_metadata is None):
        return JSONResponse(jsonable_encoder({"msg": "Articles not found"}), HTTPStatus.NOT_FOUND)

    compact_result = map(lambda article: jsonable_encoder({
        "header": article.header,
        "sub_header": article.sub_header[:50],
        "status": article.status
    }), article_metadata)

    return JSONResponse(jsonable_encoder({"page": compact_result}), HTTPStatus.OK)
