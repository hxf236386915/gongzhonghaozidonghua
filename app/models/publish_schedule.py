from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.session import Base

class PublishStatus(str, enum.Enum):
    PENDING = "pending"
    PUBLISHED = "published"
    FAILED = "failed"

class PublishSchedule(Base):
    __tablename__ = "publish_schedules"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    account_id = Column(Integer, ForeignKey("official_accounts.id"))
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(String(20), default=PublishStatus.PENDING)
    error_message = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    article = relationship("Article", back_populates="publish_schedules")
    official_account = relationship("OfficialAccount", back_populates="publish_schedules") 