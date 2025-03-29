<!-- Dashboard.vue - 仪表盘页面组件 -->
<!-- 该组件用于展示系统的主要统计数据、操作日志和系统信息 -->
<template>
  <div class="dashboard-container">
    <a-card title="仪表盘" :bordered="false">
      <a-row :gutter="24">
        <a-col :span="6">
          <a-card>
            <template #title>
              <span>
                <user-outlined />
                用户总数
              </span>
            </template>
            <div class="card-content">
              <h2>{{ stats.userCount }}</h2>
              <p>活跃用户: {{ stats.activeUserCount }}</p>
            </div>
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card>
            <template #title>
              <span>
                <team-outlined />
                角色总数
              </span>
            </template>
            <div class="card-content">
              <h2>{{ stats.roleCount }}</h2>
              <p>活跃角色: {{ stats.activeRoleCount }}</p>
            </div>
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card>
            <template #title>
              <span>
                <safety-certificate-outlined />
                权限总数
              </span>
            </template>
            <div class="card-content">
              <h2>{{ stats.permissionCount }}</h2>
              <p>菜单权限: {{ stats.menuPermissionCount }}</p>
            </div>
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card>
            <template #title>
              <span>
                <profile-outlined />
                今日操作日志
              </span>
            </template>
            <div class="card-content">
              <h2>{{ stats.todayLogCount }}</h2>
              <p>异常日志: {{ stats.errorLogCount }}</p>
            </div>
          </a-card>
        </a-col>
      </a-row>
    </a-card>
  </div>
</template>

<script>
// 导入Vue组合式API相关函数
import { defineComponent, reactive, onMounted } from 'vue'
// 导入Ant Design Vue的图标组件
import {
  UserOutlined,      // 用户图标
  TeamOutlined,      // 团队图标
  SafetyCertificateOutlined,  // 安全证书图标
  ProfileOutlined      // 个人资料图标
} from '@ant-design/icons-vue'

// 定义组件
export default defineComponent({
  // 组件名称
  name: 'Dashboard',
  
  // 注册使用到的图标组件
  components: {
    UserOutlined,
    TeamOutlined,
    SafetyCertificateOutlined,
    ProfileOutlined
  },

  // 组件逻辑设置
  setup() {
    // 定义统计数据响应式对象
    const stats = reactive({
      userCount: 100,    // 用户总数
      activeUserCount: 80,    // 活跃用户数
      roleCount: 5,    // 角色总数
      activeRoleCount: 4,    // 活跃角色数
      permissionCount: 20,    // 权限总数
      menuPermissionCount: 15,    // 菜单权限数
      todayLogCount: 50,    // 今日操作日志数
      errorLogCount: 2    // 异常日志数
    })

    // 获取数据的异步函数
    const fetchData = async () => {
      // TODO: 替换为实际的API调用
      stats.userCount = 128
      stats.roleCount = 15
      stats.permissionCount = 56
      stats.todayLogCount = 234
    }

    // 组件挂载时获取数据
    onMounted(() => {
      fetchData()
    })

    // 返回模板中需要使用的数据
    return {
      stats
    }
  }
})
</script>

<style>
/* 仪表盘容器样式 */
.dashboard-container {
  padding: 24px;
}

.card-content {
  text-align: center;
}

.card-content h2 {
  font-size: 24px;
  margin-bottom: 8px;
}

.card-content p {
  margin: 0;
  color: rgba(0, 0, 0, 0.45);
}
</style> 