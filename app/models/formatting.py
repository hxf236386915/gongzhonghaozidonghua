from sqlalchemy import Column, Integer, String, JSON, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base

class FormattingTemplate(Base):
    __tablename__ = "formatting_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    css_styles = Column(JSON)  # 存储CSS样式配置
    html_structure = Column(Text)  # 存储HTML模板结构
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class FormattingRule(Base):
    __tablename__ = "formatting_rules"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("formatting_templates.id"))
    rule_type = Column(String)  # text, image, heading, list, etc.
    rule_config = Column(JSON)  # 存储规则的具体配置
    priority = Column(Integer)  # 规则优先级
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 