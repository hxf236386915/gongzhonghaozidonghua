from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.menu import Menu
from datetime import datetime

def init_menu_data():
    db = SessionLocal()
    try:
        # 检查是否已有菜单数据
        if db.query(Menu).first():
            print("Menu data already exists")
            return

        # 创建顶级菜单
        dashboard = Menu(
            name="仪表盘",
            path="/dashboard",
            component="Dashboard",
            icon="DashboardOutlined",
            type="menu",
            permission="dashboard",
            level=1,
            sort=1
        )
        db.add(dashboard)

        system = Menu(
            name="系统管理",
            path="/system",
            component="RouteView",
            icon="SettingOutlined",
            type="menu",
            permission="system",
            level=1,
            sort=2
        )
        db.add(system)
        db.flush()  # 获取system的id

        # 系统管理子菜单
        menus = [
            Menu(
                name="用户管理",
                path="/system/users",
                component="system/user/index",
                icon="UserOutlined",
                type="menu",
                permission="system:user",
                parent_id=system.id,
                level=2,
                sort=1
            ),
            Menu(
                name="角色管理",
                path="/system/roles",
                component="system/role/index",
                icon="TeamOutlined",
                type="menu",
                permission="system:role",
                parent_id=system.id,
                level=2,
                sort=2
            ),
            Menu(
                name="菜单管理",
                path="/system/menus",
                component="system/menu/index",
                icon="MenuOutlined",
                type="menu",
                permission="system:menu",
                parent_id=system.id,
                level=2,
                sort=3
            ),
            Menu(
                name="操作日志",
                path="/system/logs",
                component="system/log/index",
                icon="ProfileOutlined",
                type="menu",
                permission="system:log",
                parent_id=system.id,
                level=2,
                sort=4
            )
        ]
        
        db.add_all(menus)
        db.commit()
        print("Menu data initialized successfully")
        
    except Exception as e:
        print(f"Error initializing menu data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_menu_data() 