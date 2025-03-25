from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.article import Article, ArticleCreate, ArticleUpdate, ArticleHistory
from app.services import article as article_service
from app.services import model_config as model_config_service
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=Article)
async def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    # 检查模型配置是否存在
    model_config = model_config_service.get_model_config(db, article.model_config_id)
    if not model_config:
        raise HTTPException(status_code=404, detail="Model configuration not found")
    
    # 创建文章
    db_article = article_service.create_article(db=db, article=article)
    
    # 生成内容
    content = await article_service.generate_content(
        model_config=model_config,
        prompt=f"请根据以下标题生成一篇文章：{article.title}"
    )
    
    # 更新文章内容
    db_article = article_service.update_article(
        db=db,
        article_id=db_article.id,
        article=ArticleUpdate(content=content)
    )
    
    return db_article

@router.get("/{article_id}", response_model=Article)
def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = article_service.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@router.get("/", response_model=List[Article])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    articles = article_service.get_articles(db, skip=skip, limit=limit)
    return articles

@router.put("/{article_id}", response_model=Article)
def update_article(article_id: int, article: ArticleUpdate, db: Session = Depends(get_db)):
    db_article = article_service.update_article(db, article_id=article_id, article=article)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@router.delete("/{article_id}", response_model=Article)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    db_article = article_service.delete_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@router.get("/{article_id}/history", response_model=List[ArticleHistory])
def read_article_history(article_id: int, db: Session = Depends(get_db)):
    # 检查文章是否存在
    db_article = article_service.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    
    history = article_service.get_article_history(db, article_id=article_id)
    return history 