from pydantic import BaseModel

from src.models.statement import Statement


class Article(BaseModel):
    id: int
    header: str
    subheader: str
    article: str
    statements: list[Statement] = []
    user_id: str
