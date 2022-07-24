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


@router.get("/article/{user_id}/{article_id}")
def get_article_by_id(article_id: int, user_id: str, db: Session = Depends(get_db)):
    article = get_article_by_id_service(db, article_id)
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

        for i in range(0, statements.lenght):
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
