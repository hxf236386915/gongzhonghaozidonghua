from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

class ArticleBase(BaseModel):
    title: str
    model_config_id: int
    generation_params: Dict = {}

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    generation_params: Optional[Dict] = None

class Article(ArticleBase):
    id: int
    content: Optional[str]
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class ArticleHistory(BaseModel):
    id: int
    article_id: int
    content: str
    generation_params: Dict
    created_at: datetime

    class Config:
        orm_mode = True 