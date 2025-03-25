from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, Dict, Union
from datetime import datetime
from enum import Enum

class InputType(str, Enum):
    MANUAL = "manual"
    IMPORT = "import"
    URL = "url"

class ContentStatus(str, Enum):
    DRAFT = "draft"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"

class ChangeType(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    GENERATE = "generate"
    EVALUATE = "evaluate"

# 内容输入相关Schema
class ContentInputBase(BaseModel):
    input_type: InputType
    content: Optional[str] = None
    source_url: Optional[HttpUrl] = None
    file_path: Optional[str] = None

class ContentInputCreate(ContentInputBase):
    pass

class ContentInput(ContentInputBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 内容质量评估相关Schema
class ContentQualityBase(BaseModel):
    readability_score: float = Field(..., ge=0, le=100)
    originality_score: float = Field(..., ge=0, le=100)
    relevance_score: float = Field(..., ge=0, le=100)
    overall_score: float = Field(..., ge=0, le=100)
    tags: List[str]

class ContentQualityCreate(ContentQualityBase):
    content_id: int

class ContentQuality(ContentQualityBase):
    id: int
    evaluation_time: datetime

    class Config:
        orm_mode = True

# 内容历史记录相关Schema
class ContentHistoryBase(BaseModel):
    change_type: ChangeType
    previous_version: Optional[Dict]
    change_details: Dict

class ContentHistoryCreate(ContentHistoryBase):
    content_id: int

class ContentHistory(ContentHistoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# 生成内容相关Schema
class GeneratedContentBase(BaseModel):
    title: str
    content: str
    model_name: str
    model_params: Dict

class GeneratedContentCreate(GeneratedContentBase):
    input_id: int

class GeneratedContentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[ContentStatus] = None
    model_params: Optional[Dict] = None

class GeneratedContent(GeneratedContentBase):
    id: int
    status: ContentStatus
    generation_time: float
    created_at: datetime
    updated_at: datetime
    quality_assessment: Optional[ContentQuality]
    history: List[ContentHistory]

    class Config:
        orm_mode = True

# API响应Schema
class ContentResponse(BaseModel):
    input: ContentInput
    generated: GeneratedContent

class ContentListResponse(BaseModel):
    total: int
    items: List[ContentResponse]

class ContentQualityResponse(BaseModel):
    content_id: int
    quality: ContentQuality

class ContentHistoryResponse(BaseModel):
    content_id: int
    history: List[ContentHistory] 