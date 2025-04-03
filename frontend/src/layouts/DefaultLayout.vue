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
        <!-- 动态渲染菜单 -->
        <template v-for="menu in menuTree" :key="menu.path">
          <!-- 目录类型菜单 -->
          <a-sub-menu v-if="menu.type === 'directory'" :key="`dir:${menu.path}`">
            <template #icon>
              <component :is="menu.icon" />
            </template>
            <template #title>{{ menu.name }}</template>
            
            <!-- 子菜单 -->
            <template v-if="menu.children && menu.children.length">
              <a-menu-item 
                v-for="child in menu.children" 
                :key="`menu:${child.path}`"
                @click="() => router.push(child.path)"
              >
                <template #icon v-if="child.icon">
                  <component :is="child.icon" />
                </template>
                <span>{{ child.name }}</span>
              </a-menu-item>
            </template>
          </a-sub-menu>

          <!-- 菜单类型 -->
          <a-menu-item v-else :key="`menu:${menu.path}`" @click="() => router.push(menu.path)">
            <template #icon>
              <component :is="menu.icon" />
            </template>
            <span>{{ menu.name }}</span>
          </a-menu-item>
        </template>
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

<script setup lang="ts">
import { ref, onMounted, resolveComponent, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'
import axios from 'axios'
import type { Ref, Component } from 'vue'
import {
  DashboardOutlined,
  SettingOutlined,
  FileOutlined,
  UserOutlined,
  LogoutOutlined,
  DownOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  WechatOutlined,
  FileTextOutlined,
  TeamOutlined,
  SafetyCertificateOutlined,
  MenuOutlined,
  ProfileOutlined,
  TagsOutlined,
  UnorderedListOutlined
} from '@ant-design/icons-vue'
import type { MenuItem, ProcessedMenuItem, BaseMenuItem } from '../types/menu'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const collapsed = ref(false)
const selectedKeys = ref<string[]>([route.path])
const openKeys = ref<string[]>([])
const menuTree = ref<ProcessedMenuItem[]>([])

// 获取菜单树数据
const fetchMenuTree = async () => {
  try {
    const { data } = await axios.get('/api/system/menus/tree')
    // 处理图标
    const processMenuIcons = (menus: MenuItem[]): ProcessedMenuItem[] => {
      return menus.map(menu => {
        // 创建基础菜单项
        const baseMenu: BaseMenuItem = {
          id: menu.id,
          name: menu.name,
          path: menu.path,
          component: menu.component,
          type: menu.type,
          permission: menu.permission,
          parent_id: menu.parent_id,
          level: menu.level,
          sort: menu.sort,
          status: menu.status
        }

        // 处理图标
        const iconName = menu.icon?.replace(/Outlined$/, '')
        const processedIcon = iconName ? resolveComponent(`${iconName}Outlined`) as Component : null

        // 处理子菜单
        const processedChildren = menu.children?.length 
          ? processMenuIcons(menu.children)
          : undefined

        // 创建处理后的菜单项
        const processedMenu: ProcessedMenuItem = {
          ...baseMenu,
          icon: processedIcon,
          children: processedChildren
        }

        return processedMenu
      })
    }

    menuTree.value = processMenuIcons(data)
    
    // 初始化展开的菜单
    const currentPath = route.path
    const findParentMenu = (menus: ProcessedMenuItem[], path: string): boolean => {
      for (const menu of menus) {
        if (menu.path === path) return true
        if (menu.children && menu.children.length) {
          const found = findParentMenu(menu.children, path)
          if (found) {
            openKeys.value.push(menu.path)
            return true
          }
        }
      }
      return false
    }
    findParentMenu(menuTree.value, currentPath)
    selectedKeys.value = [currentPath]
  } catch (error) {
    console.error('获取菜单数据失败:', error)
    // 添加一些默认菜单用于测试
    const defaultMenus: ProcessedMenuItem[] = [
      {
        id: 1,
        name: '仪表盘',
        path: '/dashboard',
        component: 'Dashboard',
        icon: DashboardOutlined as Component,
        type: 'menu',
        permission: 'dashboard',
        level: 1,
        sort: 1,
        status: true
      },
      {
        id: 2,
        name: '系统管理',
        path: '/system',
        component: 'RouteView',
        icon: SettingOutlined as Component,
        type: 'directory',
        permission: 'system',
        level: 1,
        sort: 2,
        status: true,
        children: [
          {
            id: 3,
            name: '用户管理',
            path: '/system/users',
            component: 'system/user/index',
            icon: UserOutlined as Component,
            type: 'menu',
            permission: 'system:user',
            parent_id: 2,
            level: 2,
            sort: 1,
            status: true
          },
          {
            id: 4,
            name: '角色管理',
            path: '/system/roles',
            component: 'system/role/index',
            icon: TeamOutlined as Component,
            type: 'menu',
            permission: 'system:role',
            parent_id: 2,
            level: 2,
            sort: 2,
            status: true
          },
          {
            id: 5,
            name: '菜单管理',
            path: '/system/menus',
            component: 'system/menu/index',
            icon: MenuOutlined as Component,
            type: 'menu',
            permission: 'system:menu',
            parent_id: 2,
            level: 2,
            sort: 3,
            status: true
          }
        ]
      }
    ]
    menuTree.value = defaultMenus
  }
}

// 监听路由变化
watch(() => route.path, (newPath) => {
  selectedKeys.value = [newPath]
  // 更新展开的菜单
  const findParentMenu = (menus: ProcessedMenuItem[], path: string): boolean => {
    for (const menu of menus) {
      if (menu.path === path) return true
      if (menu.children && menu.children.length) {
        const found = findParentMenu(menu.children, path)
        if (found) {
          if (!openKeys.value.includes(menu.path)) {
            openKeys.value.push(menu.path)
          }
          return true
        }
      }
    }
    return false
  }
  findParentMenu(menuTree.value, newPath)
})

// 组件挂载时获取菜单数据
onMounted(() => {
  fetchMenuTree()
})

const handleLogout = async () => {
  await userStore.logout()
  router.push('/login')
}
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