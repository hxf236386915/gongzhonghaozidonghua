<template>
  <div class="users-container">
    <a-card title="用户管理" :bordered="false">
      <!-- 搜索区域 -->
      <a-form layout="inline" class="search-form">
        <a-form-item label="用户名">
          <a-input v-model:value="searchForm.username" placeholder="请输入用户名" />
        </a-form-item>
        <a-form-item label="状态">
          <a-select v-model:value="searchForm.status" placeholder="请选择状态" style="width: 120px">
            <a-select-option value="active">启用</a-select-option>
            <a-select-option value="inactive">禁用</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" @click="handleSearch">查询</a-button>
          <a-button style="margin-left: 8px" @click="handleReset">重置</a-button>
        </a-form-item>
      </a-form>

      <!-- 操作按钮区域 -->
      <div class="table-operations">
        <a-button type="primary" @click="showCreateModal">
          <plus-outlined /> 新建用户
        </a-button>
      </div>

      <!-- 用户列表 -->
      <a-table
        :columns="columns"
        :data-source="userList"
        :loading="loading"
        :pagination="pagination"
        @change="handleTableChange"
      >
        <template #status="{ text }">
          <a-tag :color="text === 'active' ? 'green' : 'red'">
            {{ text === 'active' ? '启用' : '禁用' }}
          </a-tag>
        </template>
        <template #action="{ record }">
          <a-space>
            <a @click="showEditModal(record)">编辑</a>
            <a-divider type="vertical" />
            <a @click="handleResetPassword(record)">重置密码</a>
            <a-divider type="vertical" />
            <a-popconfirm
              title="确定要删除这个用户吗？"
              @confirm="handleDelete(record.id)"
            >
              <a class="danger-link">删除</a>
            </a-popconfirm>
          </a-space>
        </template>
      </a-table>

      <!-- 创建/编辑用户弹窗 -->
      <a-modal
        :title="modalTitle"
        :visible="modalVisible"
        @ok="handleModalOk"
        @cancel="handleModalCancel"
      >
        <a-form :model="formData" :rules="rules" ref="formRef">
          <a-form-item label="用户名" name="username">
            <a-input v-model:value="formData.username" placeholder="请输入用户名" />
          </a-form-item>
          <a-form-item label="密码" name="password" v-if="!formData.id">
            <a-input-password v-model:value="formData.password" placeholder="请输入密码" />
          </a-form-item>
          <a-form-item label="邮箱" name="email">
            <a-input v-model:value="formData.email" placeholder="请输入邮箱" />
          </a-form-item>
          <a-form-item label="角色" name="roles">
            <a-select
              v-model:value="formData.roles"
              mode="multiple"
              placeholder="请选择角色"
              style="width: 100%"
            >
              <a-select-option v-for="role in roleList" :key="role.id" :value="role.id">
                {{ role.name }}
              </a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="状态" name="status">
            <a-switch
              :checked="formData.status === 'active'"
              @change="(checked) => formData.status = checked ? 'active' : 'inactive'"
            />
          </a-form-item>
        </a-form>
      </a-modal>
    </a-card>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { PlusOutlined } from '@ant-design/icons-vue'
import axios from 'axios'

export default defineComponent({
  name: 'Users',
  components: {
    PlusOutlined
  },
  setup() {
    // 表格列定义
    const columns = [
      {
        title: '用户名',
        dataIndex: 'username',
        key: 'username'
      },
      {
        title: '邮箱',
        dataIndex: 'email',
        key: 'email'
      },
      {
        title: '角色',
        dataIndex: 'roles',
        key: 'roles',
        customRender: ({ text }) => text.map(role => role.name).join(', ')
      },
      {
        title: '状态',
        dataIndex: 'status',
        key: 'status',
        slots: { customRender: 'status' }
      },
      {
        title: '创建时间',
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
    const userList = ref([])
    const roleList = ref([])
    const modalVisible = ref(false)
    const modalTitle = ref('新建用户')
    const formRef = ref(null)
    
    const searchForm = reactive({
      username: '',
      status: undefined
    })

    const pagination = reactive({
      current: 1,
      pageSize: 10,
      total: 0
    })

    const formData = reactive({
      id: null,
      username: '',
      password: '',
      email: '',
      roles: [],
      status: 'active'
    })

    const rules = {
      username: [{ required: true, message: '请输入用户名' }],
      password: [{ required: true, message: '请输入密码' }],
      email: [
        { required: true, message: '请输入邮箱' },
        { type: 'email', message: '请输入正确的邮箱格式' }
      ],
      roles: [{ required: true, message: '请选择角色' }]
    }

    // 方法定义
    const fetchUserList = async () => {
      loading.value = true
      try {
        const response = await axios.get('/api/system/users', {
          params: {
            page: pagination.current,
            page_size: pagination.pageSize,
            ...searchForm
          }
        })
        userList.value = response.data.items
        pagination.total = response.data.total
      } catch (error) {
        message.error('获取用户列表失败')
      }
      loading.value = false
    }

    const fetchRoleList = async () => {
      try {
        const response = await axios.get('/api/system/roles')
        roleList.value = response.data.items
      } catch (error) {
        message.error('获取角色列表失败')
      }
    }

    const handleSearch = () => {
      pagination.current = 1
      fetchUserList()
    }

    const handleReset = () => {
      searchForm.username = ''
      searchForm.status = undefined
      handleSearch()
    }

    const handleTableChange = (pag) => {
      pagination.current = pag.current
      pagination.pageSize = pag.pageSize
      fetchUserList()
    }

    const showCreateModal = () => {
      modalTitle.value = '新建用户'
      Object.assign(formData, {
        id: null,
        username: '',
        password: '',
        email: '',
        roles: [],
        status: 'active'
      })
      modalVisible.value = true
    }

    const showEditModal = (record) => {
      modalTitle.value = '编辑用户'
      Object.assign(formData, {
        id: record.id,
        username: record.username,
        email: record.email,
        roles: record.roles.map(role => role.id),
        status: record.status
      })
      modalVisible.value = true
    }

    const handleModalOk = async () => {
      if (formRef.value) {
        try {
          await formRef.value.validate()
          loading.value = true
          
          if (formData.id) {
            await axios.put(`/api/system/users/${formData.id}`, formData)
            message.success('更新用户成功')
          } else {
            await axios.post('/api/system/users', formData)
            message.success('创建用户成功')
          }
          
          modalVisible.value = false
          fetchUserList()
        } catch (error) {
          if (error.isAxiosError) {
            message.error(error.response?.data?.detail || '操作失败')
          }
        } finally {
          loading.value = false
        }
      }
    }

    const handleModalCancel = () => {
      modalVisible.value = false
    }

    const handleDelete = async (id) => {
      try {
        await axios.delete(`/api/system/users/${id}`)
        message.success('删除用户成功')
        fetchUserList()
      } catch (error) {
        message.error('删除用户失败')
      }
    }

    const handleResetPassword = async (record) => {
      try {
        await axios.put(`/api/system/users/${record.id}/reset-password`)
        message.success('密码已重置为：houxuefeng123')
      } catch (error) {
        message.error('重置密码失败')
      }
    }

    onMounted(() => {
      fetchUserList()
      fetchRoleList()
    })

    return {
      columns,
      loading,
      userList,
      roleList,
      modalVisible,
      modalTitle,
      formRef,
      formData,
      rules,
      searchForm,
      pagination,
      handleSearch,
      handleReset,
      handleTableChange,
      showCreateModal,
      showEditModal,
      handleModalOk,
      handleModalCancel,
      handleDelete,
      handleResetPassword
    }
  }
})
</script>

<style scoped>
.users-container {
  padding: 24px;
}

.search-form {
  margin-bottom: 24px;
}

.table-operations {
  margin-bottom: 16px;
}

.danger-link {
  color: #ff4d4f;
}

.danger-link:hover {
  color: #ff7875;
}
</style>