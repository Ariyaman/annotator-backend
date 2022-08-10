from typing import List
from pydantic import BaseModel


class Article(BaseModel):
    article_id: int
    page_id: int
    date: str
    header: str
    sub_header: str
    news: str
    status: bool
    article_user: str


class ArticleResponseBody(BaseModel):
    id: str
    overallEmotion: str
    overallSentiment: str
    empStatements: List
    user: str
