from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.menu import Menu
from datetime import datetime

# 初始菜单数据
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
        "created_at": datetime.now()
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
        "created_at": datetime.now()
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
        "created_at": datetime.now(),
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
        "created_at": datetime.now(),
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
        "created_at": datetime.now(),
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
        "created_at": datetime.now(),
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
        "created_at": datetime.now(),
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
        "created_at": datetime.now(),
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
        "created_at": datetime.now(),
        "permission": "settings:wechat"
    },
    {
        "id": 10,
        "name": "文章管理",
        "path": "/article",
        "component": "Layout",
        "icon": "FileTextOutlined",
        "type": "directory",
        "sort": 2,
        "status": "active",
        "created_at": datetime.now(),
        "permission": "article"
    },
    {
        "id": 11,
        "name": "文章列表",
        "path": "/article/list",
        "component": "@/views/article/List",
        "icon": "UnorderedListOutlined",
        "type": "menu",
        "parent_id": 10,
        "sort": 1,
        "status": "active",
        "created_at": datetime.now(),
        "permission": "article:list"
    },
    {
        "id": 12,
        "name": "文章分类",
        "path": "/article/categories",
        "component": "@/views/article/Categories",
        "icon": "TagsOutlined",
        "type": "menu",
        "parent_id": 10,
        "sort": 2,
        "status": "active",
        "created_at": datetime.now(),
        "permission": "article:category"
    }
]

def init_menus():
    db = SessionLocal()
    try:
        # 清空现有菜单数据
        db.query(Menu).delete()
        
        # 插入新的菜单数据
        for menu_data in menus_data:
            menu = Menu(**menu_data)
            db.add(menu)
        
        db.commit()
        print("菜单数据初始化成功！")
    except Exception as e:
        print(f"菜单数据初始化失败：{str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_menus() 