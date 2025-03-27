from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.session import Base

class OfficialAccount(Base):
    __tablename__ = "official_accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    appid = Column(String(50), unique=True, nullable=False)
    app_secret = Column(String(100), nullable=False)
    access_token = Column(String(200))
    refresh_token = Column(String(200))
    expires_at = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    owner = relationship("User", back_populates="official_accounts")
    publish_schedules = relationship("PublishSchedule", back_populates="official_account") 