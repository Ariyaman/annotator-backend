from http import HTTPStatus
from http.client import NOT_FOUND
from re import S
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from database import get_db
from src.models.article import ArticleResponseBody
from src.models.statement import CreateStatement

from src.services.article import get_all_articles_service, get_article_by_id_service
from src.services.statement import create_statement_service, get_statements_by_article_id


router = APIRouter()


@router.get("/article/headers/{user_id}/{page}")
def get_article_headers(page: int, user_id: str, db: Session = Depends(get_db)):
    article_metadata = get_all_articles_service(db, user_id, (page - 1) * 10, 10)
    print(article_metadata[0].header)

    if(not article_metadata or article_metadata is None):
        return JSONResponse(jsonable_encoder({"msg": "Articles not found"}), HTTPStatus.NOT_FOUND)

    compact_result = []

    for article in article_metadata:
        temp_data = {
            "header": article.header,
            "sub_header": article.sub_header,
            "status": article.status,
            "article_id": article.article_id
        }

        compact_result.append(temp_data)

    return JSONResponse(jsonable_encoder({"page": compact_result}), HTTPStatus.OK)


@router.get("/article/{user_id}/{article_id}")
def get_article_by_id(article_id: int, user_id: str, db: Session = Depends(get_db)):
    article = get_article_by_id_service(db, article_id)

    if(article is None):
        return JSONResponse(jsonable_encoder({"msg": "Article does not exist"}), HTTPStatus.NOT_FOUND)

    auth: bool = article.user_fk == user_id
    statements = get_statements_by_article_id(db, article_id)

    if not statements:
        statements = {}
    elif auth == False:
        return JSONResponse(jsonable_encoder({
            "msg": "Unauthorized user"
        }), HTTPStatus.UNAUTHORIZED)
    else:
        temp_statement = {}
        emp_statements = []

        for i in statements:
            if(i.overall):
                temp_statement["overallAnger"] = i.anger
                temp_statement["overallContempt"] = i.contempt
                temp_statement["overallDisgust"] = i.disgust
                temp_statement["overallFear"] = i.fear
                temp_statement["overallHappiness"] = i.happiness
                temp_statement["overallNeutral"] = i.neutral
                temp_statement["overallSadness"] = i.sadness
                temp_statement["overallSentiment"] = i.sentiment
                temp_statement["overallSurprise"] = i.surprise
            else:
                minor_statement = {}
                minor_statement["anger"] = i.anger
                minor_statement["company"] = i.company
                minor_statement["contempt"] = i.contempt
                minor_statement["disgust"] = i.disgust
                minor_statement["fear"] = i.fear
                minor_statement["happiness"] = i.happiness
                minor_statement["neutral"] = i.neutral
                minor_statement["sadness"] = i.sadness
                minor_statement["sentence"] = i.sentence
                minor_statement["sentiment"] = i.sentiment
                minor_statement["surprise"] = i.surprise

                emp_statements.append(minor_statement)

        temp_statement["empStatements"] = emp_statements
        statements = temp_statement

    if(article is None):
        return JSONResponse(jsonable_encoder({
            "msg": "No articles found"
            }),
            HTTPStatus.NOT_FOUND
    )
    else:
        return JSONResponse(jsonable_encoder({
            "header": article.header,
            "sub_header": article.sub_header,
            "news": article.news,
            "statements": statements
            }),
            HTTPStatus.OK
        )


@router.post("/mark_article")
def mark_article(response: ArticleResponseBody, db: Session = Depends(get_db)):
    article = get_article_by_id_service(db, response.id)

    if(article.user_fk != response.user):
        return JSONResponse(jsonable_encoder({
            "msg": "User not authorized"
    }), HTTPStatus.UNAUTHORIZED)

    overall_statement = CreateStatement(
        anger=response.overallAnger,
        contempt=response.overallContempt,
        disgust=response.overallDisgust,
        fear=response.overallFear,
        happiness=response.overallHappiness,
        neutral=response.overallNeutral,
        sadness=response.overallSadness,
        sentiment=response.overallSentiment,
        surprise=response.overallSurprise,
        overall=True,
        article_fk=article.article_id
    )
    create_statement_service(db, overall_statement)

    for i in response.empStatements:
        minor_statement = CreateStatement(
            anger=i.anger,
            article_fk=article.article_id,
            company=i.company,
            contempt=i.contempt,
            disgust=i.disgust,
            fear=i.fear,
            happiness=i.happiness,
            neutral=i.neutral,
            overall=False,
            sadness=i.sadness,
            sentence=i.sentence,
            sentiment=i.sentinment,
            surprise=i.surprise
        )

        create_statement_service(db, minor_statement)

    return JSONResponse(jsonable_encoder({
        "msg": "Article marked"
    }), HTTPStatus.CREATED)
