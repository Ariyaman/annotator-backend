from sqlalchemy.orm import Session

from src.schemas.db_schemes import ArticleSchema

#TODO add sort on the basis of status where the articles status false send it to top
def get_all_articles_service(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ArticleSchema).offset(skip).limit(limit).all()


def get_article_by_page_id_service(db: Session, page_id: int):
    return db.query(ArticleSchema).filter(ArticleSchema.page_id == page_id).first()

#TODO given an article id fetch status of that article

#TODO given an article id set the status of that article to true

#TODO given a page id get article id