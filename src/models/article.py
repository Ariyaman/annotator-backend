from typing import List
from pydantic import BaseModel

from src.models.statement import Statement


class Article(BaseModel):
    id: int
    header: str
    subheader: str
    article: str
    statements: list[Statement] = []
    user_id: str


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
