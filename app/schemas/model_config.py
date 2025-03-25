from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

class ModelConfigBase(BaseModel):
    model_name: str
    endpoint: str
    parameters: Dict = {}

class ModelConfigCreate(ModelConfigBase):
    api_key: str

class ModelConfigUpdate(ModelConfigBase):
    api_key: Optional[str] = None
    is_active: Optional[bool] = None

class ModelConfig(ModelConfigBase):
    id: int
    api_key: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True 