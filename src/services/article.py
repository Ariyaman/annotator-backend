from sqlalchemy.orm import Session

from src.schemas.db_schemes import ArticleSchema

def get_all_articles_service(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ArticleSchema).offset(skip).limit(limit).all()


def get_article_by_id_service(db: Session, page_id: int):
    return db.query(ArticleSchema).filter(ArticleSchema.page_id == page_id).first()

