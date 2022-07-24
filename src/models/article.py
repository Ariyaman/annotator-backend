from typing import List
from pydantic import BaseModel

from src.models.statement import Statement


class Article(BaseModel):
    article_id: int
    header: str
    sub_header: str
    article: str
    statements_foreign: list[Statement] = []
    user_fk: str
    status: bool


class ArticleResponseBody(BaseModel):
    id: int
    overallAnger: int
    overallContempt: int
    overallDisgust: int
    overallFear: int
    overallHappiness: int
    overallNeutral: int
    overallSadness: int
    overallSentiment: int
    overallSurprise: int
    empStatements: List
    user: str
