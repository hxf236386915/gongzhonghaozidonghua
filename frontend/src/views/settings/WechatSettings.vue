<template>
  <div class="wechat-settings">
    <a-card title="公众号授权管理">
      <template #extra>
        <a-button type="primary" @click="showAuthModal">
          <plus-outlined /> 添加授权
        </a-button>
      </template>

      <a-table
        :columns="columns"
        :data-source="accounts"
        :loading="loading"
        row-key="id"
      >
        <template #action="{ record }">
          <a-space>
            <a @click="handleRefreshToken(record)">刷新</a>
            <a-divider type="vertical" />
            <a-popconfirm
              title="确定要删除这个授权吗？"
              @confirm="handleDelete(record)"
            >
              <a class="danger-link">删除</a>
            </a-popconfirm>
          </a-space>
        </template>
      </a-table>
    </a-card>

    <!-- 授权弹窗 -->
    <a-modal
      v-model:visible="authModalVisible"
      title="添加公众号授权"
      @ok="handleAuthModalOk"
      :confirmLoading="confirmLoading"
    >
      <a-form
        ref="authForm"
        :model="authForm"
        :rules="rules"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 16 }"
      >
        <a-form-item label="公众号名称" name="name">
          <a-input v-model:value="authForm.name" placeholder="请输入公众号名称" />
        </a-form-item>
        <a-form-item label="AppID" name="appid">
          <a-input v-model:value="authForm.appid" placeholder="请输入AppID" />
        </a-form-item>
        <a-form-item label="AppSecret" name="appsecret">
          <a-input v-model:value="authForm.appsecret" placeholder="请输入AppSecret" />
        </a-form-item>
        <a-form-item :wrapper-col="{ offset: 6, span: 16 }">
          <a-button :loading="testing" @click="handleTest">测试</a-button>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import axios from 'axios'
import { PlusOutlined } from '@ant-design/icons-vue'

export default defineComponent({
  name: 'WechatSettings',
  components: {
    PlusOutlined
  },
  setup() {
    const loading = ref(false)
    const accounts = ref([])
    const authModalVisible = ref(false)
    const confirmLoading = ref(false)
    const testing = ref(false)

    const columns = [
      {
        title: '公众号名称',
        dataIndex: 'name',
        key: 'name'
      },
      {
        title: 'AppID',
        dataIndex: 'appid',
        key: 'appid'
      },
      {
        title: '创建时间',
        dataIndex: 'created_at',
        key: 'created_at'
      },
      {
        title: '更新时间',
        dataIndex: 'updated_at',
        key: 'updated_at'
      },
      {
        title: '操作',
        key: 'action',
        slots: { customRender: 'action' }
      }
    ]

    const authForm = ref({
      name: '',
      appid: '',
      appsecret: ''
    })

    const rules = {
      name: [{ required: true, message: '请输入公众号名称' }],
      appid: [{ required: true, message: '请输入AppID' }],
      appsecret: [{ required: true, message: '请输入AppSecret' }]
    }

    // 获取账号列表
    const fetchAccounts = async () => {
      loading.value = true
      try {
        const response = await axios.get('/api/system/wechat/accounts')
        accounts.value = response.data
      } catch (error) {
        message.error('获取公众号列表失败')
      } finally {
        loading.value = false
      }
    }

    // 显示授权弹窗
    const showAuthModal = () => {
      authModalVisible.value = true
      authForm.value = {
        name: '',
        appid: '',
        appsecret: ''
      }
    }

    // 测试配置
    const handleTest = async () => {
      testing.value = true
      try {
        const response = await axios.post('/api/system/wechat/accounts/test', authForm.value)
        if (response.data.success) {
          message.success('测试通过')
        } else {
          message.error(response.data.message)
        }
      } catch (error) {
        message.error('测试失败')
      } finally {
        testing.value = false
      }
    }

    // 保存授权
    const handleAuthModalOk = async () => {
      confirmLoading.value = true
      try {
        await axios.post('/api/system/wechat/accounts', authForm.value)
        message.success('添加成功')
        authModalVisible.value = false
        fetchAccounts()
      } catch (error) {
        message.error('添加失败')
      } finally {
        confirmLoading.value = false
      }
    }

    // 刷新token
    const handleRefreshToken = async (record) => {
      try {
        const response = await axios.post(`/api/system/wechat/accounts/${record.id}/refresh`)
        if (response.data.success) {
          message.success('刷新成功')
          fetchAccounts()
        } else {
          message.error(response.data.message)
        }
      } catch (error) {
        message.error('刷新失败')
      }
    }

    // 删除授权
    const handleDelete = async (record) => {
      try {
        await axios.delete(`/api/system/wechat/accounts/${record.id}`)
        message.success('删除成功')
        fetchAccounts()
      } catch (error) {
        message.error('删除失败')
      }
    }

    onMounted(() => {
      fetchAccounts()
    })

    return {
      loading,
      accounts,
      columns,
      authModalVisible,
      confirmLoading,
      testing,
      authForm,
      rules,
      showAuthModal,
      handleTest,
      handleAuthModalOk,
      handleRefreshToken,
      handleDelete
    }
  }
})
</script>

<style scoped>
.wechat-settings {
  padding: 24px;
}
.danger-link {
  color: #ff4d4f;
}
</style> 