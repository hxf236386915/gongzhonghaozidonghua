<!-- Dashboard.vue - 仪表盘页面组件 -->
<!-- 该组件用于展示系统的主要统计数据、操作日志和系统信息 -->
<template>
  <!-- 仪表盘容器 -->
  <div class="dashboard">
    <!-- 数据概览卡片区域 - 使用网格布局展示四个统计卡片 -->
    <div class="stat-cards">
      <!-- 用户总数统计卡片 -->
      <a-card class="stat-card">
        <!-- 卡片标题插槽 -->
        <template #title>
          <div class="card-title">
            <user-outlined /> <!-- 用户图标组件 -->
            <span>用户总数</span>
          </div>
        </template>
        <!-- 卡片内容区域 -->
        <div class="card-content">
          <!-- 数字展示区域 - 使用可选链运算符防止空值 -->
          <div class="number">{{ stats.userCount || 0 }}</div>
          <!-- 趋势指标区域 -->
          <div class="trend">
            <span class="label">较上月</span>
            <span class="value up">
              <arrow-up-outlined /> <!-- 上升箭头图标 -->
              12%
            </span>
          </div>
        </div>
      </a-card>

      <!-- 角色总数统计卡片 -->
      <a-card class="stat-card">
        <template #title>
          <div class="card-title">
            <team-outlined /> <!-- 团队图标组件 -->
            <span>角色总数</span>
          </div>
        </template>
        <div class="card-content">
          <div class="number">{{ stats.roleCount || 0 }}</div>
          <div class="trend">
            <span class="label">较上月</span>
            <span class="value up">
              <arrow-up-outlined />
              8%
            </span>
          </div>
        </div>
      </a-card>

      <!-- 菜单总数统计卡片 -->
      <a-card class="stat-card">
        <template #title>
          <div class="card-title">
            <appstore-outlined /> <!-- 应用图标组件 -->
            <span>菜单总数</span>
          </div>
        </template>
        <div class="card-content">
          <div class="number">{{ stats.menuCount || 0 }}</div>
          <div class="trend">
            <span class="label">较上月</span>
            <span class="value same">
              <minus-outlined /> <!-- 持平图标 -->
              0%
            </span>
          </div>
        </div>
      </a-card>

      <!-- 今日操作日志统计卡片 -->
      <a-card class="stat-card">
        <template #title>
          <div class="card-title">
            <file-text-outlined /> <!-- 文件图标组件 -->
            <span>今日操作日志</span>
          </div>
        </template>
        <div class="card-content">
          <div class="number">{{ stats.todayLogs || 0 }}</div>
          <div class="trend">
            <span class="label">较昨日</span>
            <span class="value down">
              <arrow-down-outlined /> <!-- 下降箭头图标 -->
              5%
            </span>
          </div>
        </div>
      </a-card>
    </div>

    <!-- 系统信息和操作日志区域 -->
    <div class="info-section">
      <!-- 使用 Ant Design 栅格系统，设置列间距为24 -->
      <a-row :gutter="24">
        <!-- 左侧操作日志面板 - 占据12列（一半宽度）-->
        <a-col :span="12">
          <a-card title="最近操作日志" class="log-card">
            <!-- 卡片右上角额外操作区域 -->
            <template #extra>
              <a-button type="link">查看更多</a-button>
            </template>
            <!-- 无数据时显示空状态 -->
            <a-empty v-if="!recentLogs.length" />
            <!-- 有数据时显示日志列表 -->
            <a-list v-else class="log-list">
              <!-- 遍历日志数据 -->
              <a-list-item v-for="log in recentLogs" :key="log.id">
                <a-list-item-meta>
                  <!-- 用户头像区域 -->
                  <template #avatar>
                    <a-avatar :style="{ backgroundColor: log.type === 'success' ? '#52c41a' : '#1890ff' }">
                      {{ log.username[0]?.toUpperCase() }}
                    </a-avatar>
                  </template>
                  <!-- 日志标题 -->
                  <template #title>
                    {{ log.action }}
                  </template>
                  <!-- 日志描述信息 -->
                  <template #description>
                    <span>{{ log.username }}</span>
                    <span class="log-time">{{ log.time }}</span>
                  </template>
                </a-list-item-meta>
              </a-list-item>
            </a-list>
          </a-card>
        </a-col>
        
        <!-- 右侧系统信息面板 - 占据12列（一半宽度）-->
        <a-col :span="12">
          <a-card title="系统信息" class="system-card">
            <!-- 使用描述列表组件展示系统信息 -->
            <a-descriptions :column="1">
              <a-descriptions-item label="系统名称">
                公众号文章自动化运营平台
              </a-descriptions-item>
              <a-descriptions-item label="当前版本">
                1.0.0
              </a-descriptions-item>
              <a-descriptions-item label="服务器时间">
                {{ systemInfo.serverTime }}
              </a-descriptions-item>
              <a-descriptions-item label="运行时长">
                {{ systemInfo.uptime }}
              </a-descriptions-item>
            </a-descriptions>
          </a-card>
        </a-col>
      </a-row>
    </div>
  </div>
</template>

<script>
// 导入Vue组合式API相关函数
import { defineComponent, ref, onMounted } from 'vue'
// 导入Ant Design Vue的图标组件
import {
  UserOutlined,      // 用户图标
  TeamOutlined,      // 团队图标
  AppstoreOutlined,  // 应用图标
  FileTextOutlined,  // 文件图标
  ArrowUpOutlined,   // 上升箭头图标
  ArrowDownOutlined, // 下降箭头图标
  MinusOutlined      // 横线图标
} from '@ant-design/icons-vue'

// 定义组件
export default defineComponent({
  // 组件名称
  name: 'Dashboard',
  
  // 注册使用到的图标组件
  components: {
    UserOutlined,
    TeamOutlined,
    AppstoreOutlined,
    FileTextOutlined,
    ArrowUpOutlined,
    ArrowDownOutlined,
    MinusOutlined
  },

  // 组件逻辑设置
  setup() {
    // 定义统计数据响应式对象
    const stats = ref({
      userCount: 0,    // 用户总数
      roleCount: 0,    // 角色总数
      menuCount: 0,    // 菜单总数
      todayLogs: 0     // 今日日志数
    })

    // 定义最近操作日志数据
    const recentLogs = ref([
      {
        id: 1,
        username: 'admin',
        action: '更新了系统配置',
        time: '2024-03-28 13:45',
        type: 'success'
      },
      {
        id: 2,
        username: 'editor',
        action: '发布了新文章',
        time: '2024-03-28 11:30',
        type: 'info'
      }
    ])

    // 定义系统信息数据
    const systemInfo = ref({
      serverTime: new Date().toLocaleString(),  // 服务器当前时间
      uptime: '2天 3小时 45分钟'                // 系统运行时长
    })

    // 获取数据的异步函数
    const fetchData = async () => {
      // TODO: 替换为实际的API调用
      stats.value = {
        userCount: 128,
        roleCount: 15,
        menuCount: 56,
        todayLogs: 234
      }
    }

    // 组件挂载时获取数据
    onMounted(() => {
      fetchData()
    })

    // 返回模板中需要使用的数据
    return {
      stats,
      recentLogs,
      systemInfo
    }
  }
})
</script>

<style>
/* 仪表盘容器样式 */
.dashboard {
  width: 100%;  /* 容器宽度占满父元素 */
}

/* 统计卡片区域样式 */
.stat-cards {
  display: grid;  /* 使用网格布局 */
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));  /* 响应式网格列 */
  gap: var(--spacing-lg);  /* 卡片间距使用预定义变量 */
  margin-bottom: var(--spacing-lg);  /* 底部外边距 */
}

/* 单个统计卡片样式 */
.stat-card {
  background: #fff;  /* 白色背景 */
  padding: var(--spacing-lg);  /* 内边距 */
  border-radius: var(--border-radius-base);  /* 圆角 */
  box-shadow: var(--shadow-1);  /* 阴影效果 */
  transition: all 0.3s;  /* 过渡动画 */
}

/* 统计卡片悬停效果 */
.stat-card:hover {
  box-shadow: var(--shadow-2);  /* 更深的阴影 */
  transform: translateY(-2px);  /* 向上浮动效果 */
}

/* 卡片标题样式 */
.card-title {
  color: var(--text-color-secondary);  /* 次要文本颜色 */
  font-size: 14px;  /* 字体大小 */
  display: flex;  /* 弹性布局 */
  align-items: center;  /* 垂直居中 */
  gap: var(--spacing-xs);  /* 图标和文字间距 */
}

/* 数字展示样式 */
.number {
  font-size: 36px;  /* 大号字体 */
  font-weight: 600;  /* 加粗 */
  color: var(--primary-color);  /* 主题色 */
  margin: var(--spacing-md) 0;  /* 上下外边距 */
  line-height: 1.2;  /* 行高 */
}

/* 趋势指标容器样式 */
.trend {
  display: flex;  /* 弹性布局 */
  align-items: center;  /* 垂直居中 */
  justify-content: space-between;  /* 两端对齐 */
  margin-top: var(--spacing-sm);  /* 上外边距 */
}

/* 趋势标签样式 */
.trend .label {
  color: var(--text-color-secondary);  /* 次要文本颜色 */
  font-size: 14px;  /* 字体大小 */
}

/* 趋势值样式 */
.trend .value {
  display: flex;  /* 弹性布局 */
  align-items: center;  /* 垂直居中 */
  gap: var(--spacing-xs);  /* 图标和文字间距 */
  font-size: 14px;  /* 字体大小 */
}

/* 上升趋势样式 */
.trend .value.up {
  color: #52c41a;  /* 绿色 */
}

/* 下降趋势样式 */
.trend .value.down {
  color: #ff4d4f;  /* 红色 */
}

/* 持平趋势样式 */
.trend .value.same {
  color: #faad14;  /* 黄色 */
}

/* 信息区域样式 */
.info-section {
  display: grid;  /* 网格布局 */
  grid-template-columns: repeat(2, 1fr);  /* 两列等宽 */
  gap: var(--spacing-lg);  /* 列间距 */
  margin-top: var(--spacing-lg);  /* 上外边距 */
}

/* 信息卡片样式 */
.info-card {
  background: #fff;  /* 白色背景 */
  padding: var(--spacing-lg);  /* 内边距 */
  border-radius: var(--border-radius-base);  /* 圆角 */
  box-shadow: var(--shadow-1);  /* 阴影 */
}

/* 信息卡片标题样式 */
.info-card .title {
  font-size: 16px;  /* 字体大小 */
  font-weight: 500;  /* 字重 */
  color: var(--text-color);  /* 文本颜色 */
  margin-bottom: var(--spacing-md);  /* 下外边距 */
}

/* 日志列表样式 */
.log-list {
  max-height: 400px;  /* 最大高度 */
  overflow-y: auto;  /* 垂直滚动 */
}

/* 日志项样式 */
.log-item {
  padding: var(--spacing-sm) 0;  /* 上下内边距 */
  border-bottom: 1px solid var(--border-color);  /* 底部边框 */
}

/* 最后一个日志项样式 */
.log-item:last-child {
  border-bottom: none;  /* 移除底部边框 */
}

/* 日志时间样式 */
.log-time {
  color: var(--text-color-secondary);  /* 次要文本颜色 */
  margin-left: var(--spacing-md);  /* 左外边距 */
}

/* 响应式布局样式 */
@media screen and (max-width: 768px) {
  /* 小屏幕下统计卡片改为单列 */
  .stat-cards {
    grid-template-columns: 1fr;  /* 单列布局 */
    gap: var(--spacing-md);  /* 减小间距 */
  }
  
  /* 小屏幕下信息区域改为单列 */
  .info-section {
    grid-template-columns: 1fr;  /* 单列布局 */
    gap: var(--spacing-md);  /* 减小间距 */
  }
  
  /* 小屏幕下减小卡片内边距 */
  .stat-card,
  .info-card {
    padding: var(--spacing-md);  /* 使用中等内边距 */
  }
}
</style> 