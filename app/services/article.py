from sqlalchemy.orm import Session
import aiohttp
from app.models.article import Article, ArticleHistory
from app.models.model_config import ModelConfig
from app.schemas.article import ArticleCreate, ArticleUpdate
from app.core.security import decrypt_api_key

async def generate_content(model_config: ModelConfig, prompt: str) -> str:
    """调用大模型API生成内容"""
    api_key = decrypt_api_key(model_config.api_key)
    headers = {"Authorization": f"Bearer {api_key}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            model_config.endpoint,
            headers=headers,
            json={
                "model": model_config.model_name,
                "prompt": prompt,
                **model_config.parameters
            }
        ) as response:
            result = await response.json()
            return result.get("choices", [{}])[0].get("text", "")

def create_article(db: Session, article: ArticleCreate):
    db_article = Article(
        title=article.title,
        model_config_id=article.model_config_id,
        generation_params=article.generation_params,
        status="draft"
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def get_article(db: Session, article_id: int):
    return db.query(Article).filter(Article.id == article_id).first()

def get_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Article).offset(skip).limit(limit).all()

def update_article(db: Session, article_id: int, article: ArticleUpdate):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if db_article:
        # 如果内容发生变化，保存历史记录
        if article.content and article.content != db_article.content:
            history = ArticleHistory(
                article_id=article_id,
                content=db_article.content,
                generation_params=db_article.generation_params
            )
            db.add(history)
        
        update_data = article.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_article, key, value)
        db.commit()
        db.refresh(db_article)
    return db_article

def delete_article(db: Session, article_id: int):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if db_article:
        db.delete(db_article)
        db.commit()
    return db_article

def get_article_history(db: Session, article_id: int):
    return db.query(ArticleHistory).filter(
        ArticleHistory.article_id == article_id
    ).order_by(ArticleHistory.created_at.desc()).all() 