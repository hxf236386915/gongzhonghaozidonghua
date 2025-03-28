<template>
  <!-- 路由视图组件,用于根据当前路由渲染对应的页面组件 -->
  <router-view />
</template>

<style>
:root {
  /* 颜色相关CSS变量定义 */
  --primary-color: #1890ff;  /* 主题色,蓝色调 */
  --primary-bg: #ffffff;     /* 主要背景色,白色 */
  --menu-bg: #f5f5f5;       /* 菜单背景色,浅灰色 */
  --text-color: rgba(0, 0, 0, 0.85);  /* 主要文本颜色,深灰近黑 */
  --text-color-secondary: rgba(0, 0, 0, 0.45);  /* 次要文本颜色,浅灰色 */
  --border-color: #e8e8e8;   /* 边框颜色,浅灰色 */
  --bg-gray: #f0f2f5;        /* 灰色背景,用于页面底色 */
  
  /* 间距相关CSS变量定义 */
  --spacing-xs: 4px;         /* 超小间距,用于紧凑元素 */
  --spacing-sm: 8px;         /* 小间距,用于常规元素间隔 */
  --spacing-md: 16px;      /* 中等间距,用于组件内部间隔 */
  --spacing-lg: 24px;        /* 大间距,用于主要区块间隔 */
  --spacing-xl: 32px;       /* 特大间距,用于大区块间隔 */
  
  /* 阴影相关CSS变量定义 */
  --shadow-1: 0 1px 2px rgba(0, 0, 0, 0.03);  /* 浅阴影,用于卡片等轻量级元素 */
  --shadow-2: 0 3px 6px -4px rgba(0, 0, 0, 0.12), 0 6px 16px 0 rgba(0, 0, 0, 0.08);  /* 中等阴影,用于浮动元素 */
  --shadow-3: 0 6px 16px -8px rgba(0, 0, 0, 0.08), 0 9px 28px 0 rgba(0, 0, 0, 0.05);  /* 深阴影,用于模态框等 */
  
  /* 圆角相关CSS变量定义 */
  --border-radius-base: 2px;  /* 基础圆角,用于按钮等基础组件 */
  --border-radius-sm: 4px;    /* 小圆角,用于卡片等较大组件 */
}

/* 全局重置样式 */
* {
  margin: 0;      /* 清除所有元素的外边距 */
  padding: 0;     /* 清除所有元素的内边距 */
  box-sizing: border-box;  /* 使用border-box盒模型,便于布局计算 */
}

/* HTML和BODY标签的基础样式 */
html, body {
  height: 100%;   /* 设置高度100%,确保可以撑满视口 */
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
    'Noto Sans', sans-serif;  /* 设置系统默认字体,优先使用系统字体提升性能 */
  font-size: 14px;  /* 设置基础字号大小 */
  line-height: 1.5;  /* 设置行高,提高文本可读性 */
  color: var(--text-color);  /* 使用预定义的文本颜色 */
  background: var(--bg-gray);  /* 使用预定义的背景色 */
}

/* Vue应用根节点样式 */
#app {
  height: 100%;  /* 设置应用容器高度100%,确保可以撑满父元素 */
}
</style>
