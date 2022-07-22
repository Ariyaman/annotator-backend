from sqlalchemy.orm import Session

from src.schemas.db_schemes import ArticleSchema


def get_all_articles_service(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(ArticleSchema).filter(ArticleSchema.user_fk == user_id).offset(skip).limit(limit).all()


def get_article_by_id_service(db: Session, article_id: int):
    return db.query(ArticleSchema).filter(ArticleSchema.article_id == article_id).first()


def change_status_to_complete(db: Session, article_id: int):
    article = db.query(ArticleSchema).filter(ArticleSchema.article_id == article_id).first()

    article.status = True
    db.commit()
