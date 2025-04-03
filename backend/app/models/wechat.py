from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class WechatAccount(Base):
    __tablename__ = "wechat_accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="公众号名称")
    appid = Column(String(50), unique=True, nullable=False, comment="AppID")
    appsecret = Column(String(100), nullable=False, comment="AppSecret")
    access_token = Column(String(512), nullable=True, comment="访问令牌")
    expires_in = Column(Integer, nullable=True, comment="令牌过期时间")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间") 