from sqlalchemy.orm import Session

from src.schemas.db_schemes import Article


def get_all_articles(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(Article).filter(Article.user_fk == user_id).offset(skip).limit(limit).all()


def get_article_by_id(db: Session, article_id: int):
    return db.query(Article).filter(Article.article_id == article_id).first()
