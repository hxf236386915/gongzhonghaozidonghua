from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.auth import Role, Permission, RolePermission
from datetime import datetime

def init_auth_data():
    try:
        db = SessionLocal()
        
        # 清除现有数据
        db.query(RolePermission).delete()
        db.query(Permission).delete()
        db.query(Role).delete()
        db.commit()
        
        # 创建角色
        roles = [
            Role(
                id=1,
                name="超级管理员",
                code="super_admin",
                description="系统超级管理员",
                status="active",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Role(
                id=2,
                name="普通用户",
                code="regular_user",
                description="系统普通用户",
                status="active",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        db.bulk_save_objects(roles)
        db.commit()

        # 创建权限
        permissions = [
            Permission(id=1, name="仪表盘", code="dashboard", type="menu", path="/dashboard", component="Dashboard", sort=1, status="active"),
            Permission(id=2, name="系统管理", code="system", type="menu", path="/system", component="System", sort=2, status="active"),
            Permission(id=3, name="用户管理", code="user", type="menu", path="/system/user", component="User", parent_id=2, sort=1, status="active"),
            Permission(id=4, name="角色管理", code="role", type="menu", path="/system/role", component="Role", parent_id=2, sort=2, status="active"),
            Permission(id=5, name="权限管理", code="permission", type="menu", path="/system/permission", component="Permission", parent_id=2, sort=3, status="active"),
            Permission(id=6, name="菜单管理", code="menu", type="menu", path="/system/menu", component="Menu", parent_id=2, sort=4, status="active"),
            Permission(id=7, name="日志管理", code="log", type="menu", path="/system/log", component="Log", parent_id=2, sort=5, status="active"),
            Permission(id=8, name="系统设置", code="setting", type="menu", path="/system/setting", component="Setting", parent_id=2, sort=6, status="active"),
            Permission(id=9, name="文章管理", code="article", type="menu", path="/article", component="Article", sort=3, status="active"),
            Permission(id=10, name="文章列表", code="article_list", type="menu", path="/article/list", component="ArticleList", parent_id=9, sort=1, status="active"),
            Permission(id=11, name="写文章", code="article_write", type="menu", path="/article/write", component="ArticleWrite", parent_id=9, sort=2, status="active"),
            Permission(id=12, name="分类管理", code="category", type="menu", path="/article/category", component="Category", parent_id=9, sort=3, status="active"),
            Permission(id=13, name="标签管理", code="tag", type="menu", path="/article/tag", component="Tag", parent_id=9, sort=4, status="active"),
            Permission(id=14, name="评论管理", code="comment", type="menu", path="/article/comment", component="Comment", parent_id=9, sort=5, status="active"),
            Permission(id=15, name="素材管理", code="material", type="menu", path="/material", component="Material", sort=4, status="active"),
            Permission(id=16, name="图片管理", code="image", type="menu", path="/material/image", component="Image", parent_id=15, sort=1, status="active"),
            Permission(id=17, name="视频管理", code="video", type="menu", path="/material/video", component="Video", parent_id=15, sort=2, status="active"),
            Permission(id=18, name="音频管理", code="audio", type="menu", path="/material/audio", component="Audio", parent_id=15, sort=3, status="active"),
            Permission(id=19, name="文件管理", code="file", type="menu", path="/material/file", component="File", parent_id=15, sort=4, status="active"),
            Permission(id=20, name="发布管理", code="publish", type="menu", path="/publish", component="Publish", sort=5, status="active"),
            Permission(id=21, name="定时发布", code="schedule", type="menu", path="/publish/schedule", component="Schedule", parent_id=20, sort=1, status="active")
        ]
        db.bulk_save_objects(permissions)
        db.commit()

        # 创建角色-权限关系
        role_permissions = []
        # 超级管理员拥有所有权限
        for permission in permissions:
            role_permissions.append(
                RolePermission(
                    role_id=1,
                    permission_id=permission.id,
                    created_at=datetime.now()
                )
            )
        
        # 普通用户只有基本权限
        basic_permission_ids = [1, 9, 10, 11, 15, 16, 20, 21]
        for permission_id in basic_permission_ids:
            role_permissions.append(
                RolePermission(
                    role_id=2,
                    permission_id=permission_id,
                    created_at=datetime.now()
                )
            )
        
        db.bulk_save_objects(role_permissions)
        db.commit()
        
        print("认证数据初始化成功")
    except Exception as e:
        db.rollback()
        print(f"认证数据初始化失败：{str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    init_auth_data() 