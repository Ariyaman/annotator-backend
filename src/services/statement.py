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
        emotion=statement.emotion,
        sentiment=statement.sentiment,
        sentence=statement.sentence,
        company=statement.company,
        article_fk=statement.article_fk,
        user_fk=statement.user_fk
    )

    db.add(statement_db)
    db.commit()
    db.refresh(statement_db)

    return statement_db


def get_statement_by_article_id(db: Session, article_id: int,):
    return db.query(StatementSchema).filter(StatementSchema.article_fk == article_id).all()


def get_statement_count_by_user_id_and_overall(db: Session, user_id: int, overall: bool):
    return db.query(StatementSchema) \
        .filter(StatementSchema.user_fk == user_id, StatementSchema.overall == overall) \
        .count()