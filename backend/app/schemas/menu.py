from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MenuBase(BaseModel):
    name: str
    path: Optional[str] = None
    component: Optional[str] = None
    icon: Optional[str] = None
    type: Optional[str] = None
    permission: Optional[str] = None
    parent_id: Optional[int] = None
    level: Optional[int] = 1
    sort: Optional[int] = 0
    status: Optional[bool] = True

class MenuCreate(MenuBase):
    pass

class MenuUpdate(MenuBase):
    name: Optional[str] = None

class MenuResponse(MenuBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 