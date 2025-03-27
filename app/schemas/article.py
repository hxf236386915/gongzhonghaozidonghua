from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ArticleBase(BaseModel):
    title: str
    content: str
    category_id: int
    status: str = "draft"

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[str] = None

class Article(ArticleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True