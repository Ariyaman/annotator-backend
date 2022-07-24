from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Statement(BaseModel):
    statment_id: Optional[UUID] = None
    anger: int
    contempt: int
    disgust: int
    fear: int
    happiness: int
    neutral: int
    sadness: int
    sentiment: int
    surprise: int
    overall: bool
    sentence: Optional[str] = None
    company: Optional[str] = None
    article_fk: str


class CreateStatement(BaseModel):
    anger: int
    contempt: int
    disgust: int
    fear: int
    happiness: int
    neutral: int
    sadness: int
    sentiment: int
    surprise: int
    overall: bool
    sentence: Optional[str] = None
    company: Optional[str] = None
