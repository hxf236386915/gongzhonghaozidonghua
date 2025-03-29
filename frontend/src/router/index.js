import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import Login from '@/views/Login.vue'
import Dashboard from '@/views/Dashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/',
      component: DefaultLayout,
      children: [
        {
          path: '',
          redirect: '/dashboard'
        },
        {
          path: 'dashboard',
          name: 'dashboard',
          component: Dashboard
        },
        {
          path: 'system',
          name: 'system',
          children: [
            {
              path: 'users',
              name: 'users',
              component: () => import('@/views/system/Users.vue')
            },
            {
              path: 'roles',
              name: 'roles',
              component: () => import('@/views/system/Roles.vue')
            },
            {
              path: 'permissions',
              name: 'permissions',
              component: () => import('@/views/system/Permissions.vue')
            },
            {
              path: 'menus',
              name: 'menus',
              component: () => import('@/views/system/Menus.vue')
            },
            {
              path: 'logs',
              name: 'logs',
              component: () => import('@/views/system/Logs.vue')
            }
          ]
        },
        {
          path: '/settings',
          name: 'Settings',
          component: () => import('@/views/settings/index.vue'),
          meta: { title: '设置', icon: 'SettingOutlined' },
          children: [
            {
              path: 'wechat',
              name: 'WechatSettings',
              component: () => import('@/views/settings/WechatSettings.vue'),
              meta: { title: '公众号设置', icon: 'WechatOutlined', permission: 'settings:wechat' }
            }
          ]
        }
      ]
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const token = userStore.token

  if (to.path !== '/login' && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router