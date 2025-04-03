<template>
  <div class="article-edit">
    <div class="header">
      <h2>{{ isEdit ? '编辑文章' : '新建文章' }}</h2>
      <div class="actions">
        <a-space>
          <a-button @click="handleCancel">取消</a-button>
          <a-button type="primary" :loading="saving" @click="handleSave">保存</a-button>
        </a-space>
      </div>
    </div>

    <div class="main">
      <div class="editor-container">
        <div class="title-input">
          <a-input
            v-model:value="article.title"
            placeholder="请输入文章标题"
            size="large"
          />
        </div>

        <div class="toolbar">
          <a-space>
            <a-upload
              name="file"
              :show-upload-list="false"
              :before-upload="handleImageUpload"
            >
              <a-button>
                <template #icon><upload-outlined /></template>
                上传图片
              </a-button>
            </a-upload>

            <a-upload
              name="file"
              :show-upload-list="false"
              :before-upload="handleWordImport"
              accept=".docx,.doc"
            >
              <a-button>
                <template #icon><file-word-outlined /></template>
                导入Word
              </a-button>
            </a-upload>

            <a-button @click="showImportUrlModal = true">
              <template #icon><link-outlined /></template>
              导入链接
            </a-button>
          </a-space>
        </div>

        <div class="editor">
          <MdEditor
            v-model="article.content"
            style="height: calc(100vh - 300px)"
            :preview="true"
            :toolbars="[
              'bold',
              'underline',
              'italic',
              'strikethrough',
              'title',
              'sub',
              'sup',
              'quote',
              'unorderedList',
              'orderedList',
              'task',
              'codeRow',
              'code',
              'link',
              'image',
              'table',
              'mermaid',
              'katex',
              'revoke',
              'next',
              'save',
              'prettier',
              'pageFullscreen',
              'fullscreen',
              'preview',
              'htmlPreview',
              'catalog'
            ]"
          />
        </div>
      </div>

      <div class="sidebar">
        <a-card title="文章设置" :bordered="false">
          <a-form layout="vertical">
            <a-form-item label="文章分类">
              <a-select
                v-model:value="article.category_id"
                placeholder="请选择分类"
              >
                <a-select-option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </a-select-option>
              </a-select>
            </a-form-item>

            <a-form-item label="文章状态">
              <a-select
                v-model:value="article.status"
                placeholder="请选择状态"
              >
                <a-select-option value="draft">草稿</a-select-option>
                <a-select-option value="published">发布</a-select-option>
              </a-select>
            </a-form-item>

            <a-form-item label="封面图">
              <a-upload
                v-model:file-list="coverList"
                list-type="picture-card"
                :show-upload-list="false"
                :before-upload="handleCoverUpload"
              >
                <img v-if="article.cover_image" :src="article.cover_image" alt="cover" style="width: 100%" />
                <div v-else>
                  <plus-outlined />
                  <div style="margin-top: 8px">上传</div>
                </div>
              </a-upload>
            </a-form-item>
          </a-form>
        </a-card>
      </div>
    </div>

    <!-- 导入链接弹窗 -->
    <a-modal
      v-model:visible="showImportUrlModal"
      title="导入链接"
      @ok="handleImportUrl"
      :confirmLoading="importing"
    >
      <a-input v-model:value="importUrl" placeholder="请输入文章链接" />
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { PlusOutlined, UploadOutlined, FileWordOutlined, LinkOutlined } from '@ant-design/icons-vue'
import axios from 'axios'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'

const route = useRoute()
const router = useRouter()
const isEdit = !!route.params.id

const article = ref({
  title: '',
  content: '',
  category_id: undefined,
  status: 'draft',
  cover_image: ''
})
const categories = ref([])
const saving = ref(false)
const importing = ref(false)
const showImportUrlModal = ref(false)
const importUrl = ref('')
const coverList = ref([])

// 获取文章详情
const fetchArticle = async () => {
  if (!isEdit) return
  
  try {
    const { data } = await axios.get(`/api/articles/articles/${route.params.id}`)
    article.value = data
  } catch (error) {
    message.error('获取文章失败')
  }
}

// 获取分类列表
const fetchCategories = async () => {
  try {
    const { data } = await axios.get('/api/articles/categories')
    categories.value = data
  } catch (error) {
    message.error('获取分类列表失败')
  }
}

// 保存文章
const handleSave = async () => {
  if (!article.value.title) {
    message.error('请输入文章标题')
    return
  }

  saving.value = true
  try {
    if (isEdit) {
      await axios.put(`/api/articles/articles/${route.params.id}`, article.value)
    } else {
      await axios.post('/api/articles/articles', article.value)
    }
    message.success('保存成功')
    router.push('/articles')
  } catch (error) {
    message.error('保存失败')
  }
  saving.value = false
}

// 取消编辑
const handleCancel = () => {
  router.push('/articles')
}

// 上传图片
const handleImageUpload = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  try {
    const { data } = await axios.post('/api/articles/articles/upload/image', formData)
    // 在编辑器中插入图片
    const imageUrl = data.url
    const imageMarkdown = `![${file.name}](${imageUrl})`
    const textarea = document.querySelector('.v-md-editor textarea')
    const start = textarea.selectionStart
    const end = textarea.selectionEnd
    const content = article.value.content
    article.value.content = content.substring(0, start) + imageMarkdown + content.substring(end)
    return false
  } catch (error) {
    message.error('上传图片失败')
    return false
  }
}

// 导入Word文档
const handleWordImport = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  try {
    const { data } = await axios.post('/api/articles/articles/import/word', formData)
    article.value = data
    message.success('导入成功')
    return false
  } catch (error) {
    message.error('导入失败')
    return false
  }
}

// 导入链接
const handleImportUrl = async () => {
  if (!importUrl.value) {
    message.error('请输入文章链接')
    return
  }

  importing.value = true
  try {
    const { data } = await axios.post('/api/articles/articles/import/url', {
      url: importUrl.value
    })
    article.value = data
    showImportUrlModal.value = false
    message.success('导入成功')
  } catch (error) {
    message.error('导入失败')
  }
  importing.value = false
}

// 上传封面图
const handleCoverUpload = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  try {
    const { data } = await axios.post('/api/articles/articles/upload/image', formData)
    article.value.cover_image = data.url
    return false
  } catch (error) {
    message.error('上传封面图失败')
    return false
  }
}

onMounted(() => {
  fetchArticle()
  fetchCategories()
})
</script>

<style scoped>
.article-edit {
  height: 100%;
  padding: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.main {
  display: flex;
  gap: 24px;
  height: calc(100% - 72px);
}

.editor-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
  padding: 24px;
  border-radius: 2px;
}

.title-input {
  margin-bottom: 24px;
}

.toolbar {
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.editor {
  flex: 1;
}

.sidebar {
  width: 300px;
}
</style> 