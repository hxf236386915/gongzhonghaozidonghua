<template>
  <div class="article-list">
    <div class="header">
      <h2>文章管理</h2>
      <div class="actions">
        <a-button type="primary" @click="handleCreate">
          <template #icon><plus-outlined /></template>
          新增文章
        </a-button>
      </div>
    </div>

    <div class="filters">
      <a-space>
        <a-select
          v-model:value="filters.status"
          style="width: 120px"
          placeholder="文章状态"
          @change="handleFilter"
        >
          <a-select-option value="">全部</a-select-option>
          <a-select-option value="draft">草稿</a-select-option>
          <a-select-option value="published">已发布</a-select-option>
        </a-select>

        <a-select
          v-model:value="filters.categoryId"
          style="width: 120px"
          placeholder="文章分类"
          @change="handleFilter"
        >
          <a-select-option value="">全部分类</a-select-option>
          <a-select-option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </a-select-option>
        </a-select>

        <a-input-search
          v-model:value="filters.keyword"
          placeholder="搜索文章标题"
          style="width: 200px"
          @search="handleFilter"
        />
      </a-space>
    </div>

    <a-table
      :columns="columns"
      :data-source="articles"
      :loading="loading"
      :pagination="pagination"
      @change="handleTableChange"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'status'">
          <a-tag :color="record.status === 'published' ? 'green' : 'orange'">
            {{ record.status === 'published' ? '已发布' : '草稿' }}
          </a-tag>
        </template>

        <template v-if="column.key === 'action'">
          <a-space>
            <a @click="handleEdit(record)">编辑</a>
            <a-divider type="vertical" />
            <a-popconfirm
              title="确定要删除这篇文章吗？"
              @confirm="handleDelete(record)"
            >
              <a class="danger">删除</a>
            </a-popconfirm>
          </a-space>
        </template>
      </template>
    </a-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { PlusOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import axios from 'axios'

const router = useRouter()
const loading = ref(false)
const articles = ref([])
const categories = ref([])
const filters = ref({
  status: '',
  categoryId: '',
  keyword: ''
})
const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0
})

const columns = [
  {
    title: '标题',
    dataIndex: 'title',
    key: 'title',
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    width: 100,
  },
  {
    title: '创建时间',
    dataIndex: 'created_at',
    key: 'created_at',
    width: 180,
  },
  {
    title: '更新时间',
    dataIndex: 'updated_at',
    key: 'updated_at',
    width: 180,
  },
  {
    title: '操作',
    key: 'action',
    width: 150,
  }
]

const fetchArticles = async () => {
  loading.value = true
  try {
    const { data } = await axios.get('/api/articles', {
      params: {
        skip: (pagination.value.current - 1) * pagination.value.pageSize,
        limit: pagination.value.pageSize,
        status: filters.value.status,
        category_id: filters.value.categoryId
      }
    })
    articles.value = data.items
    pagination.value.total = data.total
  } catch (error) {
    console.error('Error fetching articles:', error)
    message.error('获取文章列表失败')
  }
  loading.value = false
}

const fetchCategories = async () => {
  try {
    const { data } = await axios.get('/api/categories')
    categories.value = data
  } catch (error) {
    console.error('Error fetching categories:', error)
    message.error('获取分类列表失败')
  }
}

const handleCreate = () => {
  router.push('/articles/edit')
}

const handleEdit = (record) => {
  router.push(`/articles/edit/${record.id}`)
}

const handleDelete = async (record) => {
  try {
    await axios.delete(`/api/articles/${record.id}`)
    message.success('删除成功')
    fetchArticles()
  } catch (error) {
    console.error('Error deleting article:', error)
    message.error('删除失败')
  }
}

const handleFilter = () => {
  pagination.value.current = 1
  fetchArticles()
}

const handleTableChange = (pag) => {
  pagination.value.current = pag.current
  pagination.value.pageSize = pag.pageSize
  fetchArticles()
}

onMounted(() => {
  fetchArticles()
  fetchCategories()
})
</script>

<style scoped>
.article-list {
  padding: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.filters {
  margin-bottom: 24px;
}

.danger {
  color: #ff4d4f;
}
</style> 