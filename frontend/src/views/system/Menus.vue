<template>
    <div class="menus-container">
      <a-card title="菜单管理" :bordered="false">
        <!-- 操作按钮区域 -->
        <div class="table-operations">
          <a-button type="primary" @click="showCreateModal">
            <plus-outlined /> 新建菜单
          </a-button>
        </div>
  
        <!-- 菜单树形表格 -->
        <a-table
          :columns="columns"
          :data-source="menuList"
          :loading="loading"
          :pagination="false"
        >
          <template #icon="{ text }">
            <component :is="text" v-if="text" />
            <span v-else>-</span>
          </template>
          <template #type="{ text }">
            <a-tag>{{ text === 'menu' ? '菜单' : '按钮' }}</a-tag>
          </template>
          <template #status="{ text }">
            <a-tag :color="text === 'active' ? 'green' : 'red'">
              {{ text === 'active' ? '启用' : '禁用' }}
            </a-tag>
          </template>
          <template #action="{ record }">
            <a-space>
              <a @click="showCreateModal(record)">添加子菜单</a>
              <a-divider type="vertical" />
              <a @click="showEditModal(record)">编辑</a>
              <a-divider type="vertical" />
              <a-popconfirm
                title="确定要删除这个菜单吗？"
                @confirm="handleDelete(record.id)"
              >
                <a class="danger-link">删除</a>
              </a-popconfirm>
            </a-space>
          </template>
        </a-table>
  
        <!-- 创建/编辑菜单弹窗 -->
        <a-modal
          :title="modalTitle"
          :visible="modalVisible"
          @ok="handleModalOk"
          @cancel="handleModalCancel"
        >
          <a-form :model="formData" :rules="rules" ref="formRef">
            <a-form-item label="上级菜单" name="parent_id" v-if="!formData.id">
              <a-tree-select
                v-model:value="formData.parent_id"
                :tree-data="menuTreeData"
                placeholder="请选择上级菜单"
                allow-clear
                tree-default-expand-all
                style="width: 100%"
              />
            </a-form-item>
            <a-form-item label="菜单名称" name="name">
              <a-input v-model:value="formData.name" placeholder="请输入菜单名称" />
            </a-form-item>
            <a-form-item label="菜单类型" name="type">
              <a-radio-group v-model:value="formData.type">
                <a-radio value="menu">菜单</a-radio>
                <a-radio value="button">按钮</a-radio>
              </a-radio-group>
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
            <a-form-item label="权限标识" name="permission">
              <a-input v-model:value="formData.permission" placeholder="请输入权限标识" />
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
    name: 'Menus',
    components: {
      PlusOutlined
    },
    setup() {
      // 表格列定义
      const columns = [
        {
          title: '菜单名称',
          dataIndex: 'name',
          key: 'name'
        },
        {
          title: '图标',
          dataIndex: 'icon',
          key: 'icon',
          slots: { customRender: 'icon' }
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
          title: '权限标识',
          dataIndex: 'permission',
          key: 'permission'
        },
        {
          title: '排序',
          dataIndex: 'sort',
          key: 'sort'
        },
        {
          title: '状态',
          dataIndex: 'status',
          key: 'status',
          slots: { customRender: 'status' }
        },
        {
          title: '操作',
          key: 'action',
          slots: { customRender: 'action' }
        }
      ]
  
      // 状态定义
      const loading = ref(false)
      const menuList = ref([])
      const menuTreeData = ref([])
      const modalVisible = ref(false)
      const modalTitle = ref('新建菜单')
      const formRef = ref(null)
  
      const formData = reactive({
        id: null,
        parent_id: null,
        name: '',
        type: 'menu',
        icon: '',
        path: '',
        component: '',
        permission: '',
        sort: 0,
        status: 'active'
      })
  
      const rules = {
        name: [{ required: true, message: '请输入菜单名称' }],
        type: [{ required: true, message: '请选择菜单类型' }],
        path: [{ required: true, message: '请输入路由路径', when: () => formData.type === 'menu' }],
        component: [{ required: true, message: '请输入组件路径', when: () => formData.type === 'menu' }]
      }
  
      // 方法定义
      const fetchMenuList = async () => {
        loading.value = true
        try {
          const response = await axios.get('/api/system/menus')
          menuList.value = response.data
        } catch (error) {
          message.error('获取菜单列表失败')
        }
        loading.value = false
      }
  
      const fetchMenuTree = async () => {
        try {
          const response = await axios.get('/api/system/menus/tree')
          menuTreeData.value = response.data
        } catch (error) {
          message.error('获取菜单树失败')
        }
      }
  
      const showCreateModal = (record = null) => {
        modalTitle.value = '新建菜单'
        Object.assign(formData, {
          id: null,
          parent_id: record ? record.id : null,
          name: '',
          type: 'menu',
          icon: '',
          path: '',
          component: '',
          permission: '',
          sort: 0,
          status: 'active'
        })
        modalVisible.value = true
      }
  
      const showEditModal = (record) => {
        modalTitle.value = '编辑菜单'
        Object.assign(formData, {
          id: record.id,
          parent_id: record.parent_id,
          name: record.name,
          type: record.type,
          icon: record.icon,
          path: record.path,
          component: record.component,
          permission: record.permission,
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
              await axios.put(`/api/system/menus/${formData.id}`, formData)
              message.success('更新菜单成功')
            } else {
              await axios.post('/api/system/menus', formData)
              message.success('创建菜单成功')
            }
            
            modalVisible.value = false
            fetchMenuList()
            fetchMenuTree()
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
          await axios.delete(`/api/system/menus/${id}`)
          message.success('删除菜单成功')
          fetchMenuList()
          fetchMenuTree()
        } catch (error) {
          message.error('删除菜单失败')
        }
      }
  
      onMounted(() => {
        fetchMenuList()
        fetchMenuTree()
      })
  
      return {
        columns,
        loading,
        menuList,
        menuTreeData,
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
  .menus-container {
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