from http import HTTPStatus
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from database import get_db
from src.models.article import ArticleResponseBody
from src.models.statement import CreateStatement

from src.services.article import get_all_articles_service, get_article_by_page_id_service
from src.services.statement import create_statement_service, get_statement_by_article_id


router = APIRouter()


@router.get("/article/headers/{page}")
def get_article_headers(page: int, db: Session = Depends(get_db)):
    article_metadata = get_all_articles_service(db, (page - 1) * 10, 10)

    if(not article_metadata or article_metadata is None):
        return JSONResponse(jsonable_encoder({"msg": "Articles not found"}), HTTPStatus.NOT_FOUND)

    compact_result = []

    for article in article_metadata:
        temp_data = {
            "header": article.header,
            "article_id": article.page_id,
        }

        compact_result.append(temp_data)

    return JSONResponse(jsonable_encoder({"page": compact_result}), HTTPStatus.OK)


@router.get("/article/{page_id}")
def get_article_by_page_id(page_id: int, db: Session = Depends(get_db)):
    article = get_article_by_page_id_service(db, page_id)

    if(article is None):
        return JSONResponse(jsonable_encoder({"msg": "Article does not exist"}), HTTPStatus.NOT_FOUND)

    return JSONResponse(jsonable_encoder({
        "header": article.header,
        "sub_header": article.sub_header,
        "news": article.news,
    }), HTTPStatus.OK)

#TODO given an article id mark status as true (integrate service)
#TODO set article id in place of page_id(response.id)
@router.post("/mark_article")
def mark_article(response: ArticleResponseBody, db: Session = Depends(get_db)):
    overall_statement = CreateStatement(
        overall = True,
        emotion = response.overallEmotion,
        sentiment = response.overallSentiment,
        article_fk = int(response.id),
        user_fk = response.user
    )

    create_statement_service(db, overall_statement)

    for i in response.empStatements:
        emp_statement = CreateStatement(
            overall=False,
            article_fk=int(response.id),
            company=i['company'],
            emotion=i['emotion'],
            sentence=i['sentence'],
            sentiment=i['sentiment'],
            user_fk=response.user
        )

        create_statement_service(db, emp_statement)

    return JSONResponse(jsonable_encoder({
        "msg": "Article marked"
    }), HTTPStatus.CREATED)

#TODO add an api and service to count the number of articles with false status
