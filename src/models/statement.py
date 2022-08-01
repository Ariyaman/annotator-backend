from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Statement(BaseModel):
    statment_id: Optional[UUID] = None
    emotion: str
    sentiment: str
    overall: bool
    sentence: Optional[str] = None
    company: Optional[str] = None
    article_fk: str
    user_fk: str


class CreateStatement(BaseModel):
    overall: bool
    emotion: str
    sentiment: str
    sentence: Optional[str] = None
    company: Optional[str] = None
    article_fk: str
    user_fk: str
