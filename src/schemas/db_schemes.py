from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Text
from database import Base
from src.models.user import Roles
from sqlalchemy.orm import relationship


class UserSchema(Base):
    __tablename__ = "users"

    user_id = Column(String(200), primary_key=True, index=True)
    name = Column(String(200), index=True)
    email = Column(String(200), unique=True, index=True)
    hashed_password = Column(String(100))
    gender = Column(String(200), index=True)
    role = Column(String(200), index=True, default=Roles.superuser)
    age = Column(Integer, index=True)
    profession = Column(String(200), index=True)

    articles = relationship("Article", backref="users")


class ArticleSchema(Base):
    __tablename__ = "articles"

    article_id = Column(Integer, index=True, primary_key=True)
    header = Column(Text(2000), index=False)
    sub_header = Column(Text(4000), index=False)
    news = Column(Text(length=50000), index=False)
    user_fk = Column(String(200), ForeignKey(
        "users.user_id"), nullable=False, index=True)
    status = Column(Boolean, index=True, default=False)

    statements_foreign = relationship("Statement", backref="articles")


class StatementSchema(Base):
    __tablename__ = "statements"

    statement_id = Column(String(200), primary_key=True, index=True)
    overall = Column(Boolean, index=True)
    anger = Column(Integer, index=True)
    contempt = Column(Integer, index=True)
    disgust = Column(Integer, index=True)
    fear = Column(Integer, index=True)
    happiness = Column(Integer, index=True)
    neutral = Column(Integer, index=True)
    sadness = Column(Integer, index=True)
    sentiment = Column(Integer, index=True)
    surprise = Column(Integer, index=True)
    sentence = Column(Text(length=1000), nullable=True, index=False)
    company = Column(String(200), nullable=True, index=True)
    article_fk = Column(Integer, ForeignKey("articles.article_id"), index=True, nullable=False)
