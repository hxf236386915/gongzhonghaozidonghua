from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import httpx

router = APIRouter()

# 模拟数据
users_data = [
    {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "password": "houxuefeng123",  # 默认密码
        "roles": [1],  # 超级管理员角色ID
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    }
]

# 权限数据
permissions_data = [
    # 仪表盘
    {
        "id": 1,
        "name": "仪表盘",
        "code": "dashboard",
        "type": "menu",
        "path": "/dashboard",
        "component": "@/views/Dashboard",
        "sort": 0,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    # 系统管理
    {
        "id": 2,
        "name": "系统管理",
        "code": "system",
        "type": "directory",
        "path": "/system",
        "component": "Layout",
        "sort": 1,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    # 用户管理及其按钮权限
    {
        "id": 3,
        "name": "用户管理",
        "code": "system:user",
        "type": "menu",
        "path": "/system/users",
        "component": "@/views/system/Users",
        "parent_id": 2,
        "sort": 1,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 4,
        "name": "用户查询",
        "code": "system:user:query",
        "type": "button",
        "parent_id": 3,
        "sort": 1,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 5,
        "name": "用户新增",
        "code": "system:user:create",
        "type": "button",
        "parent_id": 3,
        "sort": 2,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 6,
        "name": "用户修改",
        "code": "system:user:update",
        "type": "button",
        "parent_id": 3,
        "sort": 3,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 7,
        "name": "用户删除",
        "code": "system:user:delete",
        "type": "button",
        "parent_id": 3,
        "sort": 4,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    # 角色管理及其按钮权限
    {
        "id": 8,
        "name": "角色管理",
        "code": "system:role",
        "type": "menu",
        "path": "/system/roles",
        "component": "@/views/system/Roles",
        "parent_id": 2,
        "sort": 2,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 9,
        "name": "角色查询",
        "code": "system:role:query",
        "type": "button",
        "parent_id": 8,
        "sort": 1,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 10,
        "name": "角色新增",
        "code": "system:role:create",
        "type": "button",
        "parent_id": 8,
        "sort": 2,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 11,
        "name": "角色修改",
        "code": "system:role:update",
        "type": "button",
        "parent_id": 8,
        "sort": 3,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 12,
        "name": "角色删除",
        "code": "system:role:delete",
        "type": "button",
        "parent_id": 8,
        "sort": 4,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 13,
        "name": "角色权限设置",
        "code": "system:role:permission",
        "type": "button",
        "parent_id": 8,
        "sort": 5,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    # 权限管理及其按钮权限
    {
        "id": 14,
        "name": "权限管理",
        "code": "system:permission",
        "type": "menu",
        "path": "/system/permissions",
        "component": "@/views/system/Permissions",
        "parent_id": 2,
        "sort": 3,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 15,
        "name": "权限查询",
        "code": "system:permission:query",
        "type": "button",
        "parent_id": 14,
        "sort": 1,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 16,
        "name": "权限新增",
        "code": "system:permission:create",
        "type": "button",
        "parent_id": 14,
        "sort": 2,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 17,
        "name": "权限修改",
        "code": "system:permission:update",
        "type": "button",
        "parent_id": 14,
        "sort": 3,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 18,
        "name": "权限删除",
        "code": "system:permission:delete",
        "type": "button",
        "parent_id": 14,
        "sort": 4,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    # 菜单管理及其按钮权限
    {
        "id": 19,
        "name": "菜单管理",
        "code": "system:menu",
        "type": "menu",
        "path": "/system/menus",
        "component": "@/views/system/Menus",
        "parent_id": 2,
        "sort": 4,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 20,
        "name": "菜单查询",
        "code": "system:menu:query",
        "type": "button",
        "parent_id": 19,
        "sort": 1,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 21,
        "name": "菜单新增",
        "code": "system:menu:create",
        "type": "button",
        "parent_id": 19,
        "sort": 2,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 22,
        "name": "菜单修改",
        "code": "system:menu:update",
        "type": "button",
        "parent_id": 19,
        "sort": 3,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 23,
        "name": "菜单删除",
        "code": "system:menu:delete",
        "type": "button",
        "parent_id": 19,
        "sort": 4,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    # 操作日志
    {
        "id": 24,
        "name": "操作日志",
        "code": "system:log",
        "type": "menu",
        "path": "/system/logs",
        "component": "@/views/system/Logs",
        "sort": 5,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 25,
        "name": "日志查询",
        "code": "system:log:query",
        "type": "button",
        "parent_id": 24,
        "sort": 1,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    # 设置管理
    {
        "id": 26,
        "name": "设置管理",
        "code": "settings",
        "type": "directory",
        "path": "/settings",
        "component": "Layout",
        "sort": 6,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 27,
        "name": "公众号设置",
        "code": "settings:wechat",
        "type": "menu",
        "path": "/settings/wechat",
        "component": "@/views/settings/WechatSettings",
        "parent_id": 26,
        "sort": 1,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 28,
        "name": "公众号查询",
        "code": "settings:wechat:query",
        "type": "button",
        "parent_id": 27,
        "sort": 1,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 29,
        "name": "公众号新增",
        "code": "settings:wechat:create",
        "type": "button",
        "parent_id": 27,
        "sort": 2,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 30,
        "name": "公众号删除",
        "code": "settings:wechat:delete",
        "type": "button",
        "parent_id": 27,
        "sort": 3,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 31,
        "name": "Token刷新",
        "code": "settings:wechat:refresh",
        "type": "button",
        "parent_id": 27,
        "sort": 4,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    }
]

# 角色数据
roles_data = [
    {
        "id": 1,
        "name": "超级管理员",
        "code": "admin",
        "description": "系统超级管理员",
        "status": "active",
        "permissions": [p["id"] for p in permissions_data],
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 2,
        "name": "普通用户",
        "code": "user",
        "description": "普通用户",
        "status": "active",
        "permissions": [1, 24, 25],
        "created_at": "2024-03-29 10:00:00"
    }
]

menus_data = [
    {
        "id": 1,
        "name": "仪表盘",
        "path": "/dashboard",
        "component": "@/views/Dashboard",
        "icon": "DashboardOutlined",
        "type": "menu",
        "sort": 0,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 2,
        "name": "系统管理",
        "path": "/system",
        "component": "Layout",
        "icon": "SettingOutlined",
        "type": "directory",
        "sort": 1,
        "status": "active",
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 3,
        "name": "用户管理",
        "path": "/system/users",
        "component": "@/views/system/Users",
        "icon": "UserOutlined",
        "type": "menu",
        "parent_id": 2,
        "sort": 1,
        "status": "active",
        "created_at": "2024-03-29 10:00:00",
        "permission": "system:user:list"
    },
    {
        "id": 4,
        "name": "角色管理",
        "path": "/system/roles",
        "component": "@/views/system/Roles",
        "icon": "TeamOutlined",
        "type": "menu",
        "parent_id": 2,
        "sort": 2,
        "status": "active",
        "created_at": "2024-03-29 10:00:00",
        "permission": "system:role:list"
    },
    {
        "id": 5,
        "name": "权限管理",
        "path": "/system/permissions",
        "component": "@/views/system/Permissions",
        "icon": "SafetyCertificateOutlined",
        "type": "menu",
        "parent_id": 2,
        "sort": 3,
        "status": "active",
        "created_at": "2024-03-29 10:00:00",
        "permission": "system:permission:list"
    },
    {
        "id": 6,
        "name": "菜单管理",
        "path": "/system/menus",
        "component": "@/views/system/Menus",
        "icon": "MenuOutlined",
        "type": "menu",
        "parent_id": 2,
        "sort": 4,
        "status": "active",
        "created_at": "2024-03-29 10:00:00",
        "permission": "system:menu:list"
    },
    {
        "id": 7,
        "name": "操作日志",
        "path": "/system/logs",
        "component": "@/views/system/Logs",
        "icon": "ProfileOutlined",
        "type": "menu",
        "sort": 2,
        "status": "active",
        "created_at": "2024-03-29 10:00:00",
        "permission": "system:log:list"
    },
    {
        "id": 8,
        "name": "设置",
        "path": "/settings",
        "component": "LAYOUT",
        "icon": "SettingOutlined",
        "type": "directory",
        "sort": 6,
        "status": "active",
        "created_at": "2024-03-29 10:00:00",
        "permission": "settings"
    },
    {
        "id": 9,
        "name": "公众号设置",
        "path": "/settings/wechat",
        "component": "@/views/settings/WechatSettings",
        "icon": "WechatOutlined",
        "type": "menu",
        "parent_id": 8,
        "sort": 1,
        "status": "active",
        "created_at": "2024-03-29 10:00:00",
        "permission": "settings:wechat"
    }
]

# 日志相关模型
class LogResponse(BaseModel):
    id: int
    username: str
    operation_type: str
    module: str
    method: str
    url: str
    ip_address: str
    status: str
    request_data: Optional[str] = None
    response_data: Optional[str] = None
    error_message: Optional[str] = None
    created_at: str

# 模拟日志数据
logs_data = [
    {
        "id": 1,
        "username": "admin",
        "operation_type": "create",
        "module": "用户管理",
        "method": "POST",
        "url": "/api/system/users",
        "ip_address": "127.0.0.1",
        "status": "success",
        "request_data": '{"username": "test1", "email": "test1@example.com"}',
        "response_data": '{"id": 2, "username": "test1"}',
        "created_at": "2024-03-29 10:00:00"
    },
    {
        "id": 2,
        "username": "admin",
        "operation_type": "update",
        "module": "角色管理",
        "method": "PUT",
        "url": "/api/system/roles/1",
        "ip_address": "127.0.0.1",
        "status": "success",
        "request_data": '{"name": "普通用户", "status": "active"}',
        "response_data": '{"id": 1, "name": "普通用户"}',
        "created_at": "2024-03-29 11:00:00"
    },
    {
        "id": 3,
        "username": "test1",
        "operation_type": "delete",
        "module": "菜单管理",
        "method": "DELETE",
        "url": "/api/system/menus/1",
        "ip_address": "127.0.0.1",
        "status": "error",
        "request_data": '{"id": 1}',
        "error_message": "无权限执行此操作",
        "created_at": "2024-03-29 12:00:00"
    }
]

# 公众号授权数据
wechat_accounts = []

# 公众号相关API
@router.get("/wechat/accounts")
async def get_wechat_accounts():
    """获取已授权的公众号列表"""
    return wechat_accounts

@router.post("/wechat/accounts")
async def create_wechat_account(account: dict):
    """创建公众号授权"""
    # 生成ID
    account["id"] = len(wechat_accounts) + 1
    account["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    wechat_accounts.append(account)
    return account

@router.delete("/wechat/accounts/{account_id}")
async def delete_wechat_account(account_id: int):
    """删除公众号授权"""
    account = next((a for a in wechat_accounts if a["id"] == account_id), None)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    wechat_accounts.remove(account)
    return {"message": "Account deleted successfully"}

@router.post("/wechat/accounts/test")
async def test_wechat_account(account: dict):
    """测试公众号配置"""
    try:
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": account["appid"],
            "secret": account["appsecret"]
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            result = response.json()
            if "access_token" in result:
                return {"success": True, "message": "测试通过"}
            else:
                return {"success": False, "message": f"测试失败：{result.get('errmsg', '未知错误')}"}
    except Exception as e:
        return {"success": False, "message": f"测试失败：{str(e)}"}

@router.post("/wechat/accounts/{account_id}/refresh")
async def refresh_wechat_token(account_id: int):
    """刷新公众号token"""
    account = next((a for a in wechat_accounts if a["id"] == account_id), None)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    try:
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": account["appid"],
            "secret": account["appsecret"]
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            result = response.json()
            if "access_token" in result:
                account["access_token"] = result["access_token"]
                account["expires_in"] = result["expires_in"]
                account["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return {"success": True, "message": "Token刷新成功"}
            else:
                return {"success": False, "message": f"Token刷新失败：{result.get('errmsg', '未知错误')}"}
    except Exception as e:
        return {"success": False, "message": f"Token刷新失败：{str(e)}"}

# 权限管理API
@router.get("/permissions")
async def get_permissions():
    return permissions_data

@router.get("/permissions/tree")
async def get_permissions_tree():
    return build_tree(permissions_data)

@router.post("/permissions")
async def create_permission(permission: dict):
    permission["id"] = len(permissions_data) + 1
    permission["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    permissions_data.append(permission)
    return permission

@router.put("/permissions/{permission_id}")
async def update_permission(permission_id: int, permission: dict):
    for i, p in enumerate(permissions_data):
        if p["id"] == permission_id:
            permissions_data[i].update(permission)
            return permissions_data[i]
    raise HTTPException(status_code=404, detail="Permission not found")

@router.delete("/permissions/{permission_id}")
async def delete_permission(permission_id: int):
    for i, p in enumerate(permissions_data):
        if p["id"] == permission_id:
            del permissions_data[i]
            return {"message": "Permission deleted"}
    raise HTTPException(status_code=404, detail="Permission not found")

# 菜单管理API
@router.get("/menus")
async def get_menus():
    return menus_data

@router.get("/menus/tree")
async def get_menus_tree():
    return build_tree(menus_data)

@router.post("/menus")
async def create_menu(menu: dict):
    menu["id"] = len(menus_data) + 1
    menu["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    menus_data.append(menu)
    return menu

@router.put("/menus/{menu_id}")
async def update_menu(menu_id: int, menu: dict):
    for i, m in enumerate(menus_data):
        if m["id"] == menu_id:
            menus_data[i].update(menu)
            return menus_data[i]
    raise HTTPException(status_code=404, detail="Menu not found")

@router.delete("/menus/{menu_id}")
async def delete_menu(menu_id: int):
    for i, m in enumerate(menus_data):
        if m["id"] == menu_id:
            del menus_data[i]
            return {"message": "Menu deleted"}
    raise HTTPException(status_code=404, detail="Menu not found")

# 用户管理API
@router.get("/users")
async def get_users(page: int = 1, page_size: int = 10, username: str = None, status: str = None):
    filtered_users = users_data
    if username:
        filtered_users = [u for u in filtered_users if username.lower() in u["username"].lower()]
    if status:
        filtered_users = [u for u in filtered_users if u["status"] == status]
    
    # 处理用户角色信息
    users_with_roles = []
    for user in filtered_users:
        user_copy = user.copy()
        user_copy["roles"] = [
            {"id": role_id, "name": next(r["name"] for r in roles_data if r["id"] == role_id)}
            for role_id in user["roles"]
        ]
        users_with_roles.append(user_copy)
    
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "items": users_with_roles[start:end],
        "total": len(users_with_roles)
    }

@router.post("/users")
async def create_user(user: dict):
    user["id"] = len(users_data) + 1
    user["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 添加角色信息
    user["roles"] = [{"id": role_id, "name": next(r["name"] for r in roles_data if r["id"] == role_id)} for role_id in user["roles"]]
    users_data.append(user)
    return user

@router.put("/users/{user_id}")
async def update_user(user_id: int, user: dict):
    for i, u in enumerate(users_data):
        if u["id"] == user_id:
            # 添加角色信息
            user["roles"] = [{"id": role_id, "name": next(r["name"] for r in roles_data if r["id"] == role_id)} for role_id in user["roles"]]
            users_data[i].update(user)
            return users_data[i]
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    for i, u in enumerate(users_data):
        if u["id"] == user_id:
            del users_data[i]
            return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")

# 重置密码API
@router.put("/users/{user_id}/reset-password")
async def reset_user_password(user_id: int):
    """重置用户密码"""
    user = next((u for u in users_data if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 重置密码为默认密码
    user["password"] = "houxuefeng123"
    
    return {"message": "Password has been reset successfully"}

# 角色管理API
@router.get("/roles")
async def get_roles(page: int = 1, page_size: int = 10, name: str = None, status: str = None):
    filtered_roles = roles_data
    if name:
        filtered_roles = [r for r in filtered_roles if name.lower() in r["name"].lower()]
    if status:
        filtered_roles = [r for r in filtered_roles if r["status"] == status]
    
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "items": filtered_roles[start:end],
        "total": len(filtered_roles)
    }

@router.post("/roles")
async def create_role(role: dict):
    role["id"] = len(roles_data) + 1
    role["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    roles_data.append(role)
    return role

@router.put("/roles/{role_id}")
async def update_role(role_id: int, role: dict):
    for i, r in enumerate(roles_data):
        if r["id"] == role_id:
            roles_data[i].update(role)
            return roles_data[i]
    raise HTTPException(status_code=404, detail="Role not found")

@router.delete("/roles/{role_id}")
async def delete_role(role_id: int):
    for i, r in enumerate(roles_data):
        if r["id"] == role_id:
            del roles_data[i]
            return {"message": "Role deleted"}
    raise HTTPException(status_code=404, detail="Role not found")

@router.get("/roles/{role_id}/permissions")
async def get_role_permissions(role_id: int):
    """获取角色的权限设置"""
    role = next((r for r in roles_data if r["id"] == role_id), None)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # 返回角色已设置的权限ID列表
    return role["permissions"]

@router.put("/roles/{role_id}/permissions")
async def update_role_permissions(role_id: int, data: dict):
    """更新角色的权限设置"""
    role = next((r for r in roles_data if r["id"] == role_id), None)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # 验证权限ID是否有效
    invalid_permissions = [p_id for p_id in data["permission_ids"] 
                         if not any(p["id"] == p_id for p in permissions_data)]
    if invalid_permissions:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid permission IDs: {invalid_permissions}"
        )
    
    # 更新角色权限
    role["permissions"] = data["permission_ids"]
    
    # 返回更新后的权限列表
    return {"message": "Permissions updated", "permissions": role["permissions"]}

# 辅助函数：构建树形结构
def build_tree(items, parent_id=None):
    tree = []
    for item in items:
        if item.get("parent_id") == parent_id:
            children = build_tree(items, item["id"])
            if children:
                item["children"] = children
            tree.append(item)
    return tree

@router.get("/logs", response_model=dict)
async def get_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    username: Optional[str] = None,
    operation_type: Optional[str] = None,
    status: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None
):
    """获取操作日志列表"""
    filtered_logs = logs_data.copy()
    
    # 应用过滤条件
    if username:
        filtered_logs = [log for log in filtered_logs if username.lower() in log["username"].lower()]
    if operation_type:
        filtered_logs = [log for log in filtered_logs if log["operation_type"] == operation_type]
    if status:
        filtered_logs = [log for log in filtered_logs if log["status"] == status]
    if start_time:
        start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        filtered_logs = [log for log in filtered_logs if datetime.strptime(log["created_at"], "%Y-%m-%d %H:%M:%S") >= start_dt]
    if end_time:
        end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        filtered_logs = [log for log in filtered_logs if datetime.strptime(log["created_at"], "%Y-%m-%d %H:%M:%S") <= end_dt]
    
    # 计算分页
    total = len(filtered_logs)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_logs = filtered_logs[start_idx:end_idx]
    
    return {
        "items": paginated_logs,
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.get("/logs/{log_id}", response_model=LogResponse)
async def get_log_detail(log_id: int):
    """获取操作日志详情"""
    log = next((log for log in logs_data if log["id"] == log_id), None)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log 
    return log 