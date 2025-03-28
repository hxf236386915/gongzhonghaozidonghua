from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# 角色-权限关联表
role_permission = Table(
    'role_permission',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)

# 用户-角色关联表
user_role = Table(
    'user_role',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    full_name = Column(String(100))
    hashed_password = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    roles = relationship("Role", secondary=user_role, back_populates="users")

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    users = relationship("User", secondary=user_role, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permission, back_populates="roles")

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    code = Column(String(50), unique=True)  # 权限编码，如 'user:create'
    description = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    roles = relationship("Role", secondary=role_permission, back_populates="permissions")

class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey('menus.id'), nullable=True)
    name = Column(String(50))
    path = Column(String(200))
    component = Column(String(200))
    icon = Column(String(50))
    sort_order = Column(Integer, default=0)
    is_hidden = Column(Boolean, default=False)
    permission_code = Column(String(50))  # 关联的权限编码
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    children = relationship("Menu", backref="parent", remote_side=[id])

class OperationLog(Base):
    __tablename__ = "operation_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(50))  # 操作类型：CREATE, UPDATE, DELETE, etc.
    resource = Column(String(50))  # 资源类型：USER, ROLE, MENU, etc.
    resource_id = Column(Integer)  # 资源ID
    details = Column(JSON)  # 详细信息，JSON格式
    ip_address = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 