from sqlalchemy import true, false
from sqlalchemy.orm import Session

from src.schemas.db_schemes import ArticleSchema


def get_all_articles_service(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(ArticleSchema).filter(ArticleSchema.user_id == user_id) \
        .order_by(ArticleSchema.status).offset(skip).limit(limit).all()


def get_article_by_page_id_service(db: Session, page_id: int):
    return db.query(ArticleSchema).filter(ArticleSchema.page_id == page_id).first()


def update_status_by_article_id_service(db: Session, article_id: int):
    db.query(ArticleSchema).filter(ArticleSchema.article_id == article_id).update({ArticleSchema.status: True})
    db.commit()


def count_articles_with_false_status_service(db: Session):
    return db.query(ArticleSchema).filter(ArticleSchema.status == False).count()
