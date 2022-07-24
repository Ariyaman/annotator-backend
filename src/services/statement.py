from uuid import uuid4
from sqlalchemy.orm import Session
from src.models.statement import CreateStatement

from src.schemas.db_schemes import ArticleSchema, StatementSchema


def get_statement_by_id(db: Session, statement_id: str):
    return db.query().filter(StatementSchema.statement_id == statement_id).first()


def create_statement_service(db: Session, statement: CreateStatement):
    statement_db = StatementSchema(
        statement_id=str(uuid4()),
        overall=statement.overall,
        anger=statement.anger,
        contempt=statement.contempt,
        disgust=statement.disgust,
        fear=statement.fear,
        happiness=statement.happiness,
        neutral=statement.happiness,
        sadness=statement.sadness,
        sentiment=statement.sentiment,
        surprise=statement.surprise,
        sentence=statement.sentence,
        company=statement.company,
        article_fk=statement.article_fk
    )

    db.add(statement_db)
    db.commit()
    db.refresh(statement_db)

    return statement_db


def get_statements_by_article_id(db: Session, article_id: int):
    article = db.query(ArticleSchema).filter(ArticleSchema.article_id == article_id).first()
    return article.statements_foreign


def delete_by_article_id(db: Session, article_id: int):
    statements = get_statements_by_article_id(db, article_id)

    map(lambda x: db.query(StatementSchema).filter(StatementSchema.statement_id == x.statement_id).delete(), statements)

    db.commit()
