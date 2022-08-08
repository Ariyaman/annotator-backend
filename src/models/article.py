from typing import List
from pydantic import BaseModel

from src.models.statement import Statement


class Article(BaseModel):
    article_id: int
    page_id: int
    date: str
    header: str
    sub_header: str
    news: str
    status: bool


class ArticleResponseBody(BaseModel):
    id: str
    overallEmotion: str
    overallSentiment: str
    empStatements: List
    user: str
