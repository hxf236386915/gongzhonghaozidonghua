<template>
  <a-layout class="app-layout">
    <a-layout-sider width="180" class="app-sider">
      <div class="logo">
        <h1>公众号平台</h1>
      </div>
      <a-menu
        v-model:selectedKeys="selectedKeys"
        v-model:openKeys="openKeys"
        theme="light"
        mode="inline"
      >
        <a-menu-item key="dashboard">
          <template #icon>
            <dashboard-outlined />
          </template>
          <router-link to="/dashboard">仪表盘</router-link>
        </a-menu-item>

        <a-sub-menu key="system">
          <template #icon>
            <setting-outlined />
          </template>
          <template #title>系统管理</template>
          
          <a-menu-item key="users">
            <router-link to="/system/users">用户管理</router-link>
          </a-menu-item>
          
          <a-menu-item key="roles">
            <router-link to="/system/roles">角色管理</router-link>
          </a-menu-item>
          
          <a-menu-item key="permissions">
            <router-link to="/system/permissions">权限管理</router-link>
          </a-menu-item>
          
          <a-menu-item key="menus">
            <router-link to="/system/menus">菜单管理</router-link>
          </a-menu-item>
        </a-sub-menu>

        <a-menu-item key="logs">
          <template #icon>
            <file-outlined />
          </template>
          <router-link to="/system/logs">操作日志</router-link>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    
    <a-layout class="main-layout">
      <a-layout-header class="layout-header">
        <div class="header-left">
          <menu-fold-outlined
            v-if="!collapsed"
            class="trigger"
            @click="() => (collapsed = true)"
          />
          <menu-unfold-outlined
            v-else
            class="trigger"
            @click="() => (collapsed = false)"
          />
        </div>
        <div class="header-right">
          <a-dropdown>
            <a class="ant-dropdown-link" @click.prevent>
              <a-avatar class="avatar" size="small">
                {{ userStore.userInfo?.username?.[0]?.toUpperCase() }}
              </a-avatar>
              <span class="username">{{ userStore.userInfo?.username }}</span>
              <down-outlined />
            </a>
            <template #overlay>
              <a-menu>
                <a-menu-item key="profile">
                  <user-outlined />
                  <span>个人信息</span>
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item key="logout" @click="handleLogout">
                  <logout-outlined />
                  <span>退出登录</span>
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </div>
      </a-layout-header>
      
      <a-layout-content class="layout-content">
        <div class="content-wrapper">
          <router-view></router-view>
        </div>
      </a-layout-content>
      
      <a-layout-footer class="layout-footer">
        公众号文章自动化运营平台 ©2024 Created by Your Company
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>

<script>
import { defineComponent, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  DashboardOutlined,
  SettingOutlined,
  FileOutlined,
  UserOutlined,
  LogoutOutlined,
  DownOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined
} from '@ant-design/icons-vue'

export default defineComponent({
  name: 'DefaultLayout',
  components: {
    DashboardOutlined,
    SettingOutlined,
    FileOutlined,
    UserOutlined,
    LogoutOutlined,
    DownOutlined,
    MenuFoldOutlined,
    MenuUnfoldOutlined
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const userStore = useUserStore()
    
    const collapsed = ref(false)
    const selectedKeys = ref([route.name])
    const openKeys = ref(['system'])

    // 监听路由变化，更新选中的菜单项
    watch(() => route.name, (newVal) => {
      selectedKeys.value = [newVal]
    })

    const handleLogout = async () => {
      await userStore.logout()
      router.push('/login')
    }

    return {
      collapsed,
      selectedKeys,
      openKeys,
      userStore,
      handleLogout
    }
  }
})
</script>

<style>
/* 重置基础样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 基础布局 */
.app-layout {
  min-height: 100vh;
  display: flex;
  position: relative;
  margin: 0;
  padding: 0;
  background: var(--bg-gray);
}

/* 侧边栏 */
/* 侧边栏容器样式 */
.app-sider {
  /* 固定定位,使侧边栏固定在视口左侧 */
  position: fixed;
  /* 设置左边距为0,紧贴视口左边 */
  left: 0;
  /* 设置顶部边距为0,紧贴视口顶部 */
  top: 0;
  /* 设置底部边距为0,延伸到视口底部 */
  bottom: 0;
  /* 设置较高的z-index确保侧边栏显示在其他内容之上 */
  z-index: 1000;
  /* 设置高度为视口高度 */
  height: 100vh;
  /* 固定宽度为180px,使用!important确保不被其他样式覆盖 */
  width: 180px !important;
  /* 使用CSS变量设置背景色 */
  background: var(--menu-bg) !important;
  /* 添加右侧边框线 */
  border-right: 1px solid var(--border-color);
  /* 清除外边距 */
  margin: 0;
  /* 清除内边距 */
  padding: 0;
  /* flex布局相关属性,固定宽度为180px */
  flex: 0 0 180px !important;
  /* 设置最大宽度为180px */
  max-width: 180px !important;
  /* 设置最小宽度为180px */
  min-width: 180px !important;
  /* 隐藏溢出内容 */
  overflow: hidden; 
}

/* Logo */
.logo {
  height: 64px;
  padding: 0 24px;
  background: var(--primary-bg);
  display: flex;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
  margin: 0;
}

.logo h1 {
  color: var(--text-color);
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  white-space: nowrap;
}

/* 主布局区域 */
.main-layout {
  position: fixed;  /* 设置相对定位,作为子元素的定位参考 */
  min-height: 100vh;  /* 设置最小高度为视口高度,确保内容区域至少占满整个屏幕 */
  margin-left: 0 !important;  /* 强制设置左边距为0,确保与侧边栏紧贴 */
  margin-right: 10px !important; /* 设置右边距为10px,与浏览器边缘保持距离 */
  padding: 0;  /* 清除内边距,最大化可用空间 */
  width: calc(100% - 200px)  !important;  /* 设置宽度为视口宽度减去侧边栏宽度180px */
  display: flex;  /* 启用flex布局,便于内容垂直排列 */
  flex-direction: column;  /* 设置flex主轴方向为垂直方向 */
  background: var(--bg-gray);  /* 使用CSS变量设置背景色为灰色 */
  flex: auto;  /* 允许flex项目根据内容自动伸缩 */
}

/* 头部 */
.layout-header {
  height: calc(100vh - 64px);  /* 设置头部高度为视口高度减去64px,即除去logo区域的高度 */
  padding: 0 24px;  /* 设置内边距,左右24px,上下0px,给内容留出适当空间 */
  background: var(--primary-bg) !important;  /* 使用CSS变量设置背景色,!important确保样式优先级 */
  position: fixed;  /* 固定定位,使头部始终固定在顶部 */
  top: 0;  /* 固定到顶部位置 */
  left: 180px;  /* 左侧距离为180px,与侧边栏宽度对应 */
  right: 0;  /* 右侧距离为0,确保头部延伸到右边界 */
  z-index: 100;  /* 设置层级为100,确保头部显示在其他元素之上 */
  display: flex;  /* 启用flex布局,便于子元素的排列 */
  align-items: center;  /* flex子项在交叉轴上居中对齐 */
  justify-content: space-between;  /* flex子项在主轴上两端对齐,中间留有空隙 */
  border-bottom: 1px solid var(--border-color);  /* 添加底部边框线,使用CSS变量定义颜色 */
  margin: 0;  /* 清除外边距,确保头部紧贴边界 */
}

.header-left .trigger {
  font-size: 18px;
  cursor: pointer;
  padding: 12px;
  color: var(--text-color-secondary);
  transition: color 0.3s;
}

.header-left .trigger:hover {
  color: var(--primary-color);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-right .username {
  color: var(--text-color);
  margin: 0 8px;
}

.header-right .avatar {
  background: var(--primary-color);
}

/* 主要内容区域 */
.layout-content {
  position: relative;
  flex: 1;
  margin: 64px 0 0 0;
  padding: 0;
  background: var(--bg-gray);
  min-height: calc(100vh - 64px);
  width: 100%;
  display: flex;
  flex-direction: column;
}

/* 内容包装器 */
.content-wrapper {
  position: relative;
  flex: 1;
  background: #fff;
  margin: 0;
  padding: 24px;
  width: 100%;
  border: none;
  border-radius: 0;
}

/* 页脚 */
.layout-footer {
  position: relative;
  text-align: center;
  padding: 24px;
  margin: 0;
  color: var(--text-color-secondary);
  background: transparent;
  width: 100%;
  border-top: 1px solid var(--border-color);
}

/* Ant Design Vue 样式覆盖 */
:deep(.ant-layout) {
  background: var(--bg-gray) !important;
}

:deep(.ant-layout-sider) {
  margin: 0 !important;
  padding: 0 !important;
  background: var(--menu-bg) !important;
  flex: 0 0 180px !important;
  max-width: 180px !important;
  min-width: 180px !important;
  width: 180px !important;
}

:deep(.ant-layout-sider-children) {
  width: 180px !important;
  margin: 0 !important;
  padding: 0 !important;
}

:deep(.ant-layout-header) {
  padding: 0 !important;
  margin: 0 !important;
  height: 64px !important;
  line-height: 64px !important;
}

:deep(.ant-layout-content) {
  margin: 0 !important;
  padding: 0 !important;
}

:deep(.ant-menu) {
  border-right: none !important;
  background: var(--menu-bg) !important;
}

:deep(.ant-menu-root) {
  width: 180px !important;
  margin: 0 !important;
  padding: 0 !important;
}

:deep(.ant-menu-item),
:deep(.ant-menu-submenu) {
  width: 180px !important;
  margin: 0 !important;
  padding-left: 24px !important;
  
  &:hover {
    background: #e6e6e6 !important;
  }
  
  &.ant-menu-item-selected {
    background: #e6e6e6 !important;
  }
}

/* 响应式布局 */
@media screen and (max-width: 768px) {
  .app-sider {
    transform: translateX(-180px);
  }
  
  .main-layout {
    margin: 0 !important;
    width: 100% !important;
  }
  
  .layout-header {
    left: 0;
  }
  
  .layout-content {
    padding: 0;
  }
  
  .content-wrapper {
    padding: 12px;
  }
  
  .layout-footer {
    padding: 12px;
  }
}
</style> 