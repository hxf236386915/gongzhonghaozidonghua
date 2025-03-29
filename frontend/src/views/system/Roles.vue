<template>
    <div class="roles-container">
      <a-card title="角色管理" :bordered="false">
        <!-- 操作按钮区域 -->
        <div class="table-operations">
          <a-button type="primary" @click="showCreateModal">
            <plus-outlined /> 新建角色
          </a-button>
        </div>
  
        <!-- 角色列表 -->
        <a-table
          :columns="columns"
          :data-source="roleList"
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
              <a @click="showPermissionModal(record)">权限设置</a>
              <a-divider type="vertical" />
              <a-popconfirm
                title="确定要删除这个角色吗？"
                @confirm="handleDelete(record.id)"
              >
                <a class="danger-link">删除</a>
              </a-popconfirm>
            </a-space>
          </template>
        </a-table>
  
        <!-- 创建/编辑角色弹窗 -->
        <a-modal
          :title="modalTitle"
          :visible="modalVisible"
          @ok="handleModalOk"
          @cancel="handleModalCancel"
        >
          <a-form :model="formData" :rules="rules" ref="formRef">
            <a-form-item label="角色名称" name="name">
              <a-input v-model:value="formData.name" placeholder="请输入角色名称" />
            </a-form-item>
            <a-form-item label="角色编码" name="code">
              <a-input v-model:value="formData.code" placeholder="请输入角色编码" />
            </a-form-item>
            <a-form-item label="描述" name="description">
              <a-textarea v-model:value="formData.description" placeholder="请输入角色描述" />
            </a-form-item>
            <a-form-item label="状态" name="status">
              <a-switch
                :checked="formData.status === 'active'"
                @change="(checked) => formData.status = checked ? 'active' : 'inactive'"
              />
            </a-form-item>
          </a-form>
        </a-modal>
  
        <!-- 权限设置弹窗 -->
        <a-modal
          v-model:visible="permissionModalVisible"
          title="权限设置"
          width="600px"
          @ok="handlePermissionOk"
          @cancel="handlePermissionCancel"
        >
          <a-spin :spinning="permissionLoading">
            <a-tree
              v-model:checkedKeys="checkedPermissions"
              v-model:expandedKeys="expandedKeys"
              :tree-data="permissionTree"
              checkable
              :defaultExpandAll="true"
              :field-names="{
                title: 'name',
                key: 'id',
                children: 'children'
              }"
            >
              <template #title="{ name, type, code }">
                <span>
                  {{ name }}
                  <a-tag v-if="type === 'button'" size="small" color="blue">按钮</a-tag>
                  <a-tag v-if="type === 'menu'" size="small" color="green">菜单</a-tag>
                  <a-tag v-if="type === 'directory'" size="small" color="orange">目录</a-tag>
                </span>
                <span class="permission-code">{{ code }}</span>
              </template>
            </a-tree>
          </a-spin>
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
    name: 'Roles',
    components: {
      PlusOutlined
    },
    setup() {
      // 表格列定义
      const columns = [
        {
          title: '角色名称',
          dataIndex: 'name',
          key: 'name'
        },
        {
          title: '角色编码',
          dataIndex: 'code',
          key: 'code'
        },
        {
          title: '描述',
          dataIndex: 'description',
          key: 'description'
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
      const roleList = ref([])
      const modalVisible = ref(false)
      const modalTitle = ref('新建角色')
      const formRef = ref(null)
      const permissionModalVisible = ref(false)
      const permissionLoading = ref(false)
      const checkedPermissions = ref([])
      const expandedKeys = ref([])
      const permissionTree = ref([])
      const currentRole = ref(null)
  
      const pagination = reactive({
        current: 1,
        pageSize: 10,
        total: 0
      })
  
      const formData = reactive({
        id: null,
        name: '',
        code: '',
        description: '',
        status: 'active'
      })
  
      const rules = {
        name: [{ required: true, message: '请输入角色名称' }],
        code: [{ required: true, message: '请输入角色编码' }]
      }
  
      // 方法定义
      const fetchRoleList = async () => {
        loading.value = true
        try {
          const response = await axios.get('/api/system/roles', {
            params: {
              page: pagination.current,
              page_size: pagination.pageSize
            }
          })
          roleList.value = response.data.items
          pagination.total = response.data.total
        } catch (error) {
          message.error('获取角色列表失败')
        }
        loading.value = false
      }
  
      const fetchPermissionTree = async () => {
        try {
          const response = await axios.get('/api/system/permissions/tree')
          permissionTree.value = response.data
          expandedKeys.value = permissionTree.value.map(node => node.id)
        } catch (error) {
          message.error('获取权限树失败')
        }
      }
  
      const fetchRolePermissions = async (roleId) => {
        permissionLoading.value = true
        try {
          const response = await axios.get(`/api/system/roles/${roleId}/permissions`)
          checkedPermissions.value = response.data
          await fetchPermissionTree()
        } catch (error) {
          message.error('获取角色权限失败')
        } finally {
          permissionLoading.value = false
        }
      }
  
      const handleTableChange = (pag) => {
        pagination.current = pag.current
        pagination.pageSize = pag.pageSize
        fetchRoleList()
      }
  
      const showCreateModal = () => {
        modalTitle.value = '新建角色'
        Object.assign(formData, {
          id: null,
          name: '',
          code: '',
          description: '',
          status: 'active'
        })
        modalVisible.value = true
      }
  
      const showEditModal = (record) => {
        modalTitle.value = '编辑角色'
        Object.assign(formData, {
          id: record.id,
          name: record.name,
          code: record.code,
          description: record.description,
          status: record.status
        })
        modalVisible.value = true
      }
  
      const showPermissionModal = async (record) => {
        currentRole.value = record
        permissionModalVisible.value = true
        await fetchRolePermissions(record.id)
      }
  
      const handleModalOk = async () => {
        if (formRef.value) {
          try {
            await formRef.value.validate()
            loading.value = true
            
            if (formData.id) {
              await axios.put(`/api/system/roles/${formData.id}`, formData)
              message.success('更新角色成功')
            } else {
              await axios.post('/api/system/roles', formData)
              message.success('创建角色成功')
            }
            
            modalVisible.value = false
            fetchRoleList()
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
  
      const handlePermissionOk = async () => {
        if (!currentRole.value) return
        
        try {
          await axios.put(`/api/system/roles/${currentRole.value.id}/permissions`, {
            permission_ids: checkedPermissions.value
          })
          message.success('更新权限成功')
          permissionModalVisible.value = false
          fetchRoleList()
        } catch (error) {
          message.error('更新权限失败')
        }
      }
  
      const handlePermissionCancel = () => {
        permissionModalVisible.value = false
        checkedPermissions.value = []
        currentRole.value = null
      }
  
      const handleDelete = async (id) => {
        try {
          await axios.delete(`/api/system/roles/${id}`)
          message.success('删除角色成功')
          fetchRoleList()
        } catch (error) {
          message.error('删除角色失败')
        }
      }
  
      onMounted(() => {
        fetchRoleList()
      })
  
      return {
        columns,
        loading,
        roleList,
        modalVisible,
        modalTitle,
        formRef,
        formData,
        rules,
        pagination,
        permissionModalVisible,
        permissionLoading,
        checkedPermissions,
        expandedKeys,
        permissionTree,
        handleTableChange,
        showCreateModal,
        showEditModal,
        showPermissionModal,
        handleModalOk,
        handleModalCancel,
        handlePermissionOk,
        handlePermissionCancel,
        handleDelete
      }
    }
  })
  </script>
  
  <style scoped>
  .roles-container {
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
  
  .permission-code {
    margin-left: 8px;
    color: #999;
    font-size: 12px;
  }
  
  .ant-tag {
    margin-left: 4px;
  }
  </style>