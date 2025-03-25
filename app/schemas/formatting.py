from pydantic import BaseModel, HttpUrl
from typing import Dict, List, Optional, Union
from datetime import datetime

class FormattingRuleBase(BaseModel):
    rule_type: str
    rule_config: Dict
    priority: int = 0

class FormattingRuleCreate(FormattingRuleBase):
    template_id: int

class FormattingRuleUpdate(FormattingRuleBase):
    template_id: Optional[int] = None

class FormattingRule(FormattingRuleBase):
    id: int
    template_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class FormattingTemplateBase(BaseModel):
    name: str
    description: str
    css_styles: Dict
    html_structure: str
    is_default: bool = False

class FormattingTemplateCreate(FormattingTemplateBase):
    pass

class FormattingTemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    css_styles: Optional[Dict] = None
    html_structure: Optional[str] = None
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None

class FormattingTemplate(FormattingTemplateBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    rules: List[FormattingRule] = []

    class Config:
        orm_mode = True

class ImageUpload(BaseModel):
    url: Optional[HttpUrl]
    base64_data: Optional[str]
    position: str = "after"  # before, after, inline
    alignment: str = "center"  # left, center, right
    size: Dict[str, int] = {"width": 800, "height": 600}

class FormattedContent(BaseModel):
    html_content: str
    css_styles: Dict
    images: List[Dict] = [] 