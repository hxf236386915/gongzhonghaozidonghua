from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class ArticleStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    DELETED = "deleted"

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    content_html = Column(Text, nullable=True)
    status = Column(String(20), default=ArticleStatus.DRAFT)
    source_type = Column(String(50), nullable=True)  # markdown, word, link, etc.
    source_url = Column(String(500), nullable=True)
    cover_image = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    author_id = Column(Integer, nullable=True)
    category_id = Column(Integer, nullable=True)

class ArticleImage(Base):
    __tablename__ = "article_images"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    url = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

class ArticleCategory(Base):
    __tablename__ = "article_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now) 