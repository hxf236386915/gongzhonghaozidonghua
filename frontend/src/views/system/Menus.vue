<template>
  <div class="menu-container">
    <div class="menu-header">
      <a-breadcrumb>
        <a-breadcrumb-item>单位管理</a-breadcrumb-item>
        <a-breadcrumb-item>菜单管理</a-breadcrumb-item>
      </a-breadcrumb>
    </div>

    <div class="menu-content">
      <div class="operation-bar">
        <a-button type="primary" @click="showAddMenuModal">
          <plus-outlined /> 新增菜单
        </a-button>
      </div>

      <a-table
        :columns="columns"
        :data-source="menuList"
        :row-key="record => record.id"
        :pagination="false"
        class="menu-table"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'menuType'">
            <a-tag :color="record.type === 'directory' ? 'blue' : 'green'">
              {{ record.type === 'directory' ? '目录' : '菜单' }}
            </a-tag>
          </template>
          
          <template v-if="column.key === 'menuIcon'">
            <span v-if="record.icon">
              <component :is="record.icon" />
              {{ record.icon }}
            </span>
          </template>

          <template v-if="column.key === 'status'">
            <a-tag :color="record.status === 'active' ? 'success' : 'error'">
              {{ record.status === 'active' ? '启用' : '禁用' }}
            </a-tag>
          </template>

          <template v-if="column.key === 'action'">
            <a-space>
              <a-button type="link" size="small" @click="handleEdit(record)">
                <template #icon><edit-outlined /></template>
                编辑
              </a-button>
              <a-button type="link" size="small" @click="handleDelete(record)" danger>
                <template #icon><delete-outlined /></template>
                删除
              </a-button>
            </a-space>
          </template>
        </template>
      </a-table>
    </div>

    <!-- 新增/编辑菜单弹窗 -->
    <a-modal
      :title="modalTitle"
      :visible="modalVisible"
      @ok="handleModalOk"
      @cancel="handleModalCancel"
      :confirm-loading="modalLoading"
    >
      <a-form
        ref="menuFormRef"
        :model="menuForm"
        :rules="rules"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 16 }"
      >
        <a-form-item label="上级菜单" name="parent_id">
          <a-tree-select
            v-model:value="menuForm.parent_id"
            :tree-data="menuTreeData"
            placeholder="请选择上级菜单"
            allow-clear
            :field-names="{ label: 'name', value: 'id', children: 'children' }"
          />
        </a-form-item>

        <a-form-item label="菜单类型" name="type">
          <a-radio-group v-model:value="menuForm.type">
            <a-radio value="directory">目录</a-radio>
            <a-radio value="menu">菜单</a-radio>
          </a-radio-group>
        </a-form-item>

        <a-form-item label="菜单名称" name="name">
          <a-input v-model:value="menuForm.name" placeholder="请输入菜单名称" />
        </a-form-item>

        <a-form-item label="菜单图标" name="icon">
          <a-input v-model:value="menuForm.icon" placeholder="请输入菜单图标" />
        </a-form-item>

        <a-form-item label="路由路径" name="path">
          <a-input v-model:value="menuForm.path" placeholder="请输入路由路径" />
        </a-form-item>

        <a-form-item label="组件路径" name="component" v-if="menuForm.type === 'menu'">
          <a-input v-model:value="menuForm.component" placeholder="请输入组件路径" />
        </a-form-item>

        <a-form-item label="显示排序" name="sort">
          <a-input-number v-model:value="menuForm.sort" :min="0" style="width: 100%" />
        </a-form-item>

        <a-form-item label="菜单状态" name="status">
          <a-switch
            v-model:checked="menuForm.status"
            :checked-value="'active'"
            :unchecked-value="'inactive'"
            checked-children="启用"
            un-checked-children="禁用"
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
} from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import axios from 'axios'

const columns = [
  {
    title: '菜单名称',
    dataIndex: 'name',
    key: 'name',
    width: '200px'
  },
  {
    title: '菜单类型',
    key: 'menuType',
    width: '100px'
  },
  {
    title: '图标',
    key: 'menuIcon',
    width: '150px'
  },
  {
    title: '路由路径',
    dataIndex: 'path',
    key: 'path',
    width: '200px'
  },
  {
    title: '组件路径',
    dataIndex: 'component',
    key: 'component',
    width: '200px'
  },
  {
    title: '排序',
    dataIndex: 'sort',
    key: 'sort',
    width: '80px'
  },
  {
    title: '状态',
    key: 'status',
    width: '100px'
  },
  {
    title: '操作',
    key: 'action',
    width: '150px',
    fixed: 'right'
  }
]

const menuList = ref([])
const menuTreeData = ref([])
const modalVisible = ref(false)
const modalLoading = ref(false)
const modalTitle = ref('新增菜单')
const menuFormRef = ref(null)
const menuForm = ref({
  parent_id: null,
  type: 'menu',
  name: '',
  icon: '',
  path: '',
  component: '',
  sort: 0,
  status: 'active'
})

const rules = {
  name: [{ required: true, message: '请输入菜单名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择菜单类型', trigger: 'change' }],
  path: [{ required: true, message: '请输入路由路径', trigger: 'blur' }],
  component: [{ required: true, message: '请输入组件路径', trigger: 'blur' }],
  sort: [{ required: true, message: '请输入显示排序', trigger: 'blur' }]
}

// 获取菜单列表
const fetchMenuList = async () => {
  try {
    const response = await axios.get('/api/system/menus')
    menuList.value = response.data
  } catch (error) {
    message.error('获取菜单列表失败')
  }
}

// 获取菜单树形数据
const fetchMenuTree = async () => {
  try {
    const response = await axios.get('/api/system/menus/tree')
    menuTreeData.value = response.data
  } catch (error) {
    message.error('获取菜单树形数据失败')
  }
}

// 显示新增菜单弹窗
const showAddMenuModal = () => {
  modalTitle.value = '新增菜单'
  menuForm.value = {
    parent_id: null,
    type: 'menu',
    name: '',
    icon: '',
    path: '',
    component: '',
    sort: 0,
    status: 'active'
  }
  modalVisible.value = true
}

// 显示编辑菜单弹窗
const handleEdit = (record) => {
  modalTitle.value = '编辑菜单'
  menuForm.value = { ...record }
  modalVisible.value = true
}

// 处理删除菜单
const handleDelete = async (record) => {
  try {
    await axios.delete(`/api/system/menus/${record.id}`)
    message.success('删除成功')
    fetchMenuList()
    fetchMenuTree()
  } catch (error) {
    message.error('删除失败')
  }
}

// 处理弹窗确认
const handleModalOk = async () => {
  try {
    await menuFormRef.value.validate()
    modalLoading.value = true
    
    if (menuForm.value.id) {
      await axios.put(`/api/system/menus/${menuForm.value.id}`, menuForm.value)
      message.success('更新成功')
    } else {
      await axios.post('/api/system/menus', menuForm.value)
      message.success('创建成功')
    }
    
    modalVisible.value = false
    fetchMenuList()
    fetchMenuTree()
  } catch (error) {
    console.error('表单验证失败:', error)
  } finally {
    modalLoading.value = false
  }
}

// 处理弹窗取消
const handleModalCancel = () => {
  modalVisible.value = false
  menuFormRef.value?.resetFields()
}

onMounted(() => {
  fetchMenuList()
  fetchMenuTree()
})
</script>

<style lang="less" scoped>
.menu-container {
  padding: 24px;
  background: #fff;
  min-height: 100%;

  .menu-header {
    margin-bottom: 24px;
  }

  .menu-content {
    .operation-bar {
      margin-bottom: 16px;
      display: flex;
      justify-content: flex-start;
    }

    .menu-table {
      :deep(.ant-table-thead > tr > th) {
        background: #fafafa;
        font-weight: 500;
      }

      :deep(.ant-table-tbody > tr > td) {
        padding: 12px 8px;
      }
    }
  }
}

:deep(.ant-form-item) {
  margin-bottom: 24px;
}

:deep(.ant-modal-body) {
  padding-top: 24px;
}
</style>