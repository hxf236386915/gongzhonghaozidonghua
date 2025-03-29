<template>
    <div class="permissions-container">
      <a-card title="权限管理" :bordered="false">
        <!-- 操作按钮区域 -->
        <div class="table-operations">
          <a-button type="primary" @click="showCreateModal">
            <plus-outlined /> 新建权限
          </a-button>
        </div>
  
        <!-- 权限树形表格 -->
        <a-table
          :columns="columns"
          :data-source="permissionList"
          :loading="loading"
          :pagination="false"
        >
          <template #type="{ text }">
            <a-tag>{{ text }}</a-tag>
          </template>
          <template #action="{ record }">
            <a-space>
              <a @click="showCreateModal(record)">添加子权限</a>
              <a-divider type="vertical" />
              <a @click="showEditModal(record)">编辑</a>
              <a-divider type="vertical" />
              <a-popconfirm
                title="确定要删除这个权限吗？"
                @confirm="handleDelete(record.id)"
              >
                <a class="danger-link">删除</a>
              </a-popconfirm>
            </a-space>
          </template>
        </a-table>
  
        <!-- 创建/编辑权限弹窗 -->
        <a-modal
          :title="modalTitle"
          :visible="modalVisible"
          @ok="handleModalOk"
          @cancel="handleModalCancel"
        >
          <a-form :model="formData" :rules="rules" ref="formRef">
            <a-form-item label="上级权限" name="parent_id" v-if="!formData.id">
              <a-tree-select
                v-model:value="formData.parent_id"
                :tree-data="permissionTreeData"
                placeholder="请选择上级权限"
                allow-clear
                tree-default-expand-all
                style="width: 100%"
              />
            </a-form-item>
            <a-form-item label="权限名称" name="name">
              <a-input v-model:value="formData.name" placeholder="请输入权限名称" />
            </a-form-item>
            <a-form-item label="权限编码" name="code">
              <a-input v-model:value="formData.code" placeholder="请输入权限编码" />
            </a-form-item>
            <a-form-item label="权限类型" name="type">
              <a-select v-model:value="formData.type" placeholder="请选择权限类型">
                <a-select-option value="menu">菜单</a-select-option>
                <a-select-option value="button">按钮</a-select-option>
                <a-select-option value="api">接口</a-select-option>
              </a-select>
            </a-form-item>
            <a-form-item label="图标" name="icon" v-if="formData.type === 'menu'">
              <a-input v-model:value="formData.icon" placeholder="请输入图标名称" />
            </a-form-item>
            <a-form-item label="路由路径" name="path" v-if="formData.type === 'menu'">
              <a-input v-model:value="formData.path" placeholder="请输入路由路径" />
            </a-form-item>
            <a-form-item label="组件路径" name="component" v-if="formData.type === 'menu'">
              <a-input v-model:value="formData.component" placeholder="请输入组件路径" />
            </a-form-item>
            <a-form-item label="排序" name="sort">
              <a-input-number v-model:value="formData.sort" :min="0" style="width: 100%" />
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
    name: 'Permissions',
    components: {
      PlusOutlined
    },
    setup() {
      // 表格列定义
      const columns = [
        {
          title: '权限名称',
          dataIndex: 'name',
          key: 'name'
        },
        {
          title: '权限编码',
          dataIndex: 'code',
          key: 'code'
        },
        {
          title: '类型',
          dataIndex: 'type',
          key: 'type',
          slots: { customRender: 'type' }
        },
        {
          title: '路由路径',
          dataIndex: 'path',
          key: 'path'
        },
        {
          title: '组件路径',
          dataIndex: 'component',
          key: 'component'
        },
        {
          title: '排序',
          dataIndex: 'sort',
          key: 'sort'
        },
        {
          title: '操作',
          key: 'action',
          slots: { customRender: 'action' }
        }
      ]
  
      // 状态定义
      const loading = ref(false)
      const permissionList = ref([])
      const permissionTreeData = ref([])
      const modalVisible = ref(false)
      const modalTitle = ref('新建权限')
      const formRef = ref(null)
  
      const formData = reactive({
        id: null,
        parent_id: null,
        name: '',
        code: '',
        type: 'menu',
        icon: '',
        path: '',
        component: '',
        sort: 0,
        status: 'active'
      })
  
      const rules = {
        name: [{ required: true, message: '请输入权限名称' }],
        code: [{ required: true, message: '请输入权限编码' }],
        type: [{ required: true, message: '请选择权限类型' }]
      }
  
      // 方法定义
      const fetchPermissionList = async () => {
        loading.value = true
        try {
          const response = await axios.get('/api/system/permissions')
          permissionList.value = response.data
        } catch (error) {
          message.error('获取权限列表失败')
        }
        loading.value = false
      }
  
      const fetchPermissionTree = async () => {
        try {
          const response = await axios.get('/api/system/permissions/tree')
          permissionTreeData.value = response.data
        } catch (error) {
          message.error('获取权限树失败')
        }
      }
  
      const showCreateModal = (record = null) => {
        modalTitle.value = '新建权限'
        Object.assign(formData, {
          id: null,
          parent_id: record ? record.id : null,
          name: '',
          code: '',
          type: 'menu',
          icon: '',
          path: '',
          component: '',
          sort: 0,
          status: 'active'
        })
        modalVisible.value = true
      }
  
      const showEditModal = (record) => {
        modalTitle.value = '编辑权限'
        Object.assign(formData, {
          id: record.id,
          parent_id: record.parent_id,
          name: record.name,
          code: record.code,
          type: record.type,
          icon: record.icon,
          path: record.path,
          component: record.component,
          sort: record.sort,
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
              await axios.put(`/api/system/permissions/${formData.id}`, formData)
              message.success('更新权限成功')
            } else {
              await axios.post('/api/system/permissions', formData)
              message.success('创建权限成功')
            }
            
            modalVisible.value = false
            fetchPermissionList()
            fetchPermissionTree()
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
          await axios.delete(`/api/system/permissions/${id}`)
          message.success('删除权限成功')
          fetchPermissionList()
          fetchPermissionTree()
        } catch (error) {
          message.error('删除权限失败')
        }
      }
  
      onMounted(() => {
        fetchPermissionList()
        fetchPermissionTree()
      })
  
      return {
        columns,
        loading,
        permissionList,
        permissionTreeData,
        modalVisible,
        modalTitle,
        formRef,
        formData,
        rules,
        showCreateModal,
        showEditModal,
        handleModalOk,
        handleModalCancel,
        handleDelete
      }
    }
  })
  </script>
  
  <style scoped>
  .permissions-container {
    padding: 24px;
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