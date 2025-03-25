from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base_class import Base

class InputType(str, enum.Enum):
    MANUAL = "manual"  # 在线编辑
    IMPORT = "import"  # 文件导入
    URL = "url"       # 链接获取

class ContentStatus(str, enum.Enum):
    DRAFT = "draft"       # 草稿
    GENERATING = "generating"  # 生成中
    COMPLETED = "completed"    # 已完成
    FAILED = "failed"         # 失败

class ChangeType(str, enum.Enum):
    CREATE = "create"     # 创建
    UPDATE = "update"     # 更新
    DELETE = "delete"     # 删除
    GENERATE = "generate" # 生成
    EVALUATE = "evaluate" # 评估

class ContentInput(Base):
    """内容输入模型"""
    __tablename__ = "content_inputs"

    id = Column(Integer, primary_key=True, index=True)
    input_type = Column(Enum(InputType))
    content = Column(Text)  # 原始内容
    source_url = Column(String)  # 链接来源
    file_path = Column(String)  # 导入文件路径
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联生成的内容
    generated_content = relationship("GeneratedContent", back_populates="input_content")

class ContentQuality(Base):
    """内容质量评估模型"""
    __tablename__ = "content_qualities"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("generated_contents.id"))
    readability_score = Column(Float)  # 可读性得分
    originality_score = Column(Float)  # 原创性得分
    relevance_score = Column(Float)  # 相关性得分
    overall_score = Column(Float)     # 总体得分
    tags = Column(JSON)               # 内容标签
    evaluation_time = Column(DateTime, default=datetime.utcnow)
    
    # 关联生成的内容
    content = relationship("GeneratedContent", back_populates="quality_assessment")

class ContentHistory(Base):
    """内容历史记录模型"""
    __tablename__ = "content_histories"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("generated_contents.id"))
    change_type = Column(Enum(ChangeType))
    previous_version = Column(JSON)  # 变更前的内容
    change_details = Column(JSON)    # 变更详情
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联生成的内容
    content = relationship("GeneratedContent", back_populates="history")

class GeneratedContent(Base):
    """生成的内容模型"""
    __tablename__ = "generated_contents"

    id = Column(Integer, primary_key=True, index=True)
    input_id = Column(Integer, ForeignKey("content_inputs.id"))
    title = Column(String)
    content = Column(Text)
    status = Column(Enum(ContentStatus), default=ContentStatus.DRAFT)
    model_name = Column(String)  # 使用的模型名称
    model_params = Column(JSON)  # 模型参数
    generation_time = Column(Float)  # 生成耗时
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    input_content = relationship("ContentInput", back_populates="generated_content")
    quality_assessment = relationship("ContentQuality", back_populates="content")
    history = relationship("ContentHistory", back_populates="content") 