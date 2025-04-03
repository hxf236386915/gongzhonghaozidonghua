from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.article import Article, ArticleCategory, ArticleStatus

def init_article_data():
    db = SessionLocal()
    try:
        # 清除现有数据
        db.query(Article).delete()
        db.query(ArticleCategory).delete()
        
        # 创建文章分类
        categories = [
            ArticleCategory(
                name="技术文章",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            ArticleCategory(
                name="行业资讯",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            ArticleCategory(
                name="产品更新",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        db.add_all(categories)
        db.commit()

        # 创建测试文章
        articles = [
            Article(
                title="Python Web开发最佳实践",
                content="这是一篇关于Python Web开发的文章...",
                status=ArticleStatus.PUBLISHED,
                category_id=1,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Article(
                title="人工智能发展趋势",
                content="这是一篇关于AI发展的文章...",
                status=ArticleStatus.PUBLISHED,
                category_id=2,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Article(
                title="新功能预告",
                content="这是一篇关于产品更新的文章...",
                status=ArticleStatus.DRAFT,
                category_id=3,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        db.add_all(articles)
        db.commit()
        
        print("文章数据初始化成功")
    except Exception as e:
        print(f"文章数据初始化失败：{str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_article_data() 