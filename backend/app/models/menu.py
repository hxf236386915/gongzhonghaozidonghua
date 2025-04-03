from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # 菜单名称
    path = Column(String, nullable=False)  # 路由路径
    component = Column(String, nullable=False)  # 组件路径
    icon = Column(String)  # 图标
    type = Column(String, nullable=False)  # 类型：目录、菜单、按钮
    permission = Column(String)  # 权限标识
    parent_id = Column(Integer, ForeignKey("menus.id"), nullable=True)  # 父菜单ID
    level = Column(Integer, default=1)  # 菜单层级
    sort = Column(Integer, default=0)  # 排序
    status = Column(Boolean, default=True)  # 状态：启用/禁用
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    children = relationship("Menu", backref="parent", remote_side=[id]) 