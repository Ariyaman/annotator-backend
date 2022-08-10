from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Text, BigInteger, Date
from database import Base


class UserSchema(Base):
    __tablename__ = "users"

    user_id = Column(String(40), primary_key=True, index=True)
    name = Column(String(200), index=True)
    email = Column(String(200), unique=True, index=True)
    hashed_password = Column(String(100))
    gender = Column(String(20), index=True)
    role = Column(String(20), index=True)
    age = Column(Integer, index=True)
    profession = Column(String(50), index=True)


class ArticleSchema(Base):
    __tablename__ = "articles"

    article_id = Column(BigInteger, index=True, unique=True)
    page_id = Column(Integer, index=True, primary_key=True)
    date = Column(Date, index=True)
    header = Column(Text(length=300), index=False)
    sub_header = Column(Text(length=1000), index=False)
    news = Column(Text(length=33000), index=False)
    status = Column(Boolean, index=True, default=False)
    article_user = Column(String(40), ForeignKey("users.user_id"), index=True, nullable=False)


class StatementSchema(Base):
    __tablename__ = "statements"

    statement_id = Column(String(36), primary_key=True, index=True)
    overall = Column(Boolean, index=True)
    emotion = Column(String(20), index=True)
    sentiment = Column(String(20), index=True)
    sentence = Column(Text(length=2000), nullable=True, index=False)
    company = Column(String(200), nullable=True, index=True)
    article_fk = Column(BigInteger, ForeignKey("articles.article_id"), index=True, nullable=False)
    user_fk = Column(String(40), ForeignKey("users.user_id"), index=True)
