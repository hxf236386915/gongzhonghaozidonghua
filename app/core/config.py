from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # API配置
    API_V1_STR: str = "/api/v1"
    
    # OpenAI配置
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # 其他配置
    PROJECT_NAME: str = "微信公众号自动化平台"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 