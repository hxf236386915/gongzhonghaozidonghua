from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import model_config, article, formatting
from app.db.database import engine
from app.models import model_config as model_config_models
from app.models import article as article_models
from app.models import formatting as formatting_models

# 创建数据库表
model_config_models.Base.metadata.create_all(bind=engine)
article_models.Base.metadata.create_all(bind=engine)
formatting_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="微信公众号自动化平台",
    description="支持文章自动生成、排版优化和定时发布功能的微信公众号自动化平台",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(
    model_config.router,
    prefix="/api/v1/model-configs",
    tags=["model-configs"]
)

app.include_router(
    article.router,
    prefix="/api/v1/articles",
    tags=["articles"]
)

app.include_router(
    formatting.router,
    prefix="/api/v1/formatting",
    tags=["formatting"]
) 