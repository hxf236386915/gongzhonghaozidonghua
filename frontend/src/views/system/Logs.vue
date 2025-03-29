<template>
    <div class="logs-container">
      <a-card title="操作日志" :bordered="false">
        <!-- 搜索区域 -->
        <a-form layout="inline" class="search-form">
          <a-form-item label="用户名">
            <a-input v-model:value="searchForm.username" placeholder="请输入用户名" />
          </a-form-item>
          <a-form-item label="操作类型">
            <a-select v-model:value="searchForm.operation_type" placeholder="请选择操作类型" style="width: 120px">
              <a-select-option value="create">新增</a-select-option>
              <a-select-option value="update">修改</a-select-option>
              <a-select-option value="delete">删除</a-select-option>
              <a-select-option value="query">查询</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="状态">
            <a-select v-model:value="searchForm.status" placeholder="请选择状态" style="width: 120px">
              <a-select-option value="success">成功</a-select-option>
              <a-select-option value="error">失败</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="操作时间">
            <a-range-picker v-model:value="searchForm.time_range" />
          </a-form-item>
          <a-form-item>
            <a-button type="primary" @click="handleSearch">查询</a-button>
            <a-button style="margin-left: 8px" @click="handleReset">重置</a-button>
          </a-form-item>
        </a-form>
  
        <!-- 日志列表 -->
        <a-table
          :columns="columns"
          :data-source="logList"
          :loading="loading"
          :pagination="pagination"
          @change="handleTableChange"
        >
          <template #status="{ text }">
            <a-tag :color="text === 'success' ? 'green' : 'red'">
              {{ text === 'success' ? '成功' : '失败' }}
            </a-tag>
          </template>
          <template #action="{ record }">
            <a-space>
              <a @click="showDetailModal(record)">详情</a>
            </a-space>
          </template>
        </a-table>
  
        <!-- 日志详情弹窗 -->
        <a-modal
          title="日志详情"
          :visible="detailModalVisible"
          @ok="handleDetailModalOk"
          @cancel="handleDetailModalCancel"
          width="800px"
        >
          <a-descriptions :column="2">
            <a-descriptions-item label="用户名">{{ currentLog.username }}</a-descriptions-item>
            <a-descriptions-item label="操作类型">{{ currentLog.operation_type }}</a-descriptions-item>
            <a-descriptions-item label="操作模块">{{ currentLog.module }}</a-descriptions-item>
            <a-descriptions-item label="请求方法">{{ currentLog.method }}</a-descriptions-item>
            <a-descriptions-item label="请求URL">{{ currentLog.url }}</a-descriptions-item>
            <a-descriptions-item label="IP地址">{{ currentLog.ip_address }}</a-descriptions-item>
            <a-descriptions-item label="操作状态">
              <a-tag :color="currentLog.status === 'success' ? 'green' : 'red'">
                {{ currentLog.status === 'success' ? '成功' : '失败' }}
              </a-tag>
            </a-descriptions-item>
            <a-descriptions-item label="操作时间">{{ currentLog.created_at }}</a-descriptions-item>
          </a-descriptions>
          <a-divider />
          <div>
            <h4>请求参数：</h4>
            <pre>{{ currentLog.request_data }}</pre>
          </div>
          <div v-if="currentLog.response_data">
            <h4>响应数据：</h4>
            <pre>{{ currentLog.response_data }}</pre>
          </div>
          <div v-if="currentLog.error_message">
            <h4>错误信息：</h4>
            <pre class="error-message">{{ currentLog.error_message }}</pre>
          </div>
        </a-modal>
      </a-card>
    </div>
  </template>
  
  <script>
  import { defineComponent, ref, reactive, onMounted } from 'vue'
  import { message } from 'ant-design-vue'
  import axios from 'axios'
  
  export default defineComponent({
    name: 'Logs',
    setup() {
      // 表格列定义
      const columns = [
        {
          title: '用户名',
          dataIndex: 'username',
          key: 'username'
        },
        {
          title: '操作类型',
          dataIndex: 'operation_type',
          key: 'operation_type'
        },
        {
          title: '操作模块',
          dataIndex: 'module',
          key: 'module'
        },
        {
          title: 'IP地址',
          dataIndex: 'ip_address',
          key: 'ip_address'
        },
        {
          title: '状态',
          dataIndex: 'status',
          key: 'status',
          slots: { customRender: 'status' }
        },
        {
          title: '操作时间',
          dataIndex: 'created_at',
          key: 'created_at'
        },
        {
          title: '操作',
          key: 'action',
          slots: { customRender: 'action' }
        }
      ]
  
      // 状态定义
      const loading = ref(false)
      const logList = ref([])
      const detailModalVisible = ref(false)
      const currentLog = ref({})
  
      const searchForm = reactive({
        username: '',
        operation_type: undefined,
        status: undefined,
        time_range: []
      })
  
      const pagination = reactive({
        current: 1,
        pageSize: 10,
        total: 0
      })
  
      // 方法定义
      const fetchLogList = async () => {
        loading.value = true
        try {
          const response = await axios.get('/api/system/logs', {
            params: {
              page: pagination.current,
              page_size: pagination.pageSize,
              ...searchForm
            }
          })
          logList.value = response.data.items
          pagination.total = response.data.total
        } catch (error) {
          message.error('获取日志列表失败')
        }
        loading.value = false
      }
  
      const handleSearch = () => {
        pagination.current = 1
        fetchLogList()
      }
  
      const handleReset = () => {
        searchForm.username = ''
        searchForm.operation_type = undefined
        searchForm.status = undefined
        searchForm.time_range = []
        handleSearch()
      }
  
      const handleTableChange = (pag) => {
        pagination.current = pag.current
        pagination.pageSize = pag.pageSize
        fetchLogList()
      }
  
      const showDetailModal = (record) => {
        currentLog.value = record
        detailModalVisible.value = true
      }
  
      const handleDetailModalOk = () => {
        detailModalVisible.value = false
      }
  
      const handleDetailModalCancel = () => {
        detailModalVisible.value = false
      }
  
      onMounted(() => {
        fetchLogList()
      })
  
      return {
        columns,
        loading,
        logList,
        detailModalVisible,
        currentLog,
        searchForm,
        pagination,
        handleSearch,
        handleReset,
        handleTableChange,
        showDetailModal,
        handleDetailModalOk,
        handleDetailModalCancel
      }
    }
  })
  </script>
  
  <style scoped>
  .logs-container {
    padding: 24px;
  }
  
  .search-form {
    margin-bottom: 24px;
  }
  
  pre {
    background-color: #f5f5f5;
    padding: 12px;
    border-radius: 4px;
    max-height: 300px;
    overflow: auto;
  }
  
  .error-message {
    color: #ff4d4f;
  }
  </style>