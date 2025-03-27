<template>
  <div class="login-container">
    <div class="login-box">
      <h2>公众号文章自动化运营平台</h2>
      <a-form
        :model="formState"
        name="login"
        @finish="handleSubmit"
        autocomplete="off"
      >
        <a-form-item
          name="username"
          :rules="[{ required: true, message: '请输入用户名' }]"
        >
          <a-input
            v-model:value="formState.username"
            placeholder="用户名"
            size="large"
          >
            <template #prefix>
              <user-outlined />
            </template>
          </a-input>
        </a-form-item>

        <a-form-item
          name="password"
          :rules="[{ required: true, message: '请输入密码' }]"
        >
          <a-input-password
            v-model:value="formState.password"
            placeholder="密码"
            size="large"
          >
            <template #prefix>
              <lock-outlined />
            </template>
          </a-input-password>
        </a-form-item>

        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            :loading="loading"
            block
            size="large"
          >
            登录
          </a-button>
        </a-form-item>
      </a-form>

      <div class="login-tips">
        默认账号：admin<br>
        默认密码：houxuefeng123
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, reactive, ref } from 'vue'
import { UserOutlined, LockOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

export default defineComponent({
  name: 'Login',
  components: {
    UserOutlined,
    LockOutlined
  },
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const loading = ref(false)

    const formState = reactive({
      username: '',
      password: ''
    })

    const handleSubmit = async (values) => {
      loading.value = true
      try {
        await userStore.login(values.username, values.password)
        message.success('登录成功')
        router.push('/dashboard')
      } catch (error) {
        message.error(error.message)
      } finally {
        loading.value = false
      }
    }

    return {
      formState,
      loading,
      handleSubmit
    }
  }
})
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f0f2f5;
}

.login-box {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.login-box h2 {
  text-align: center;
  margin-bottom: 40px;
  color: #1890ff;
}

.login-tips {
  margin-top: 24px;
  color: #999;
  text-align: center;
  font-size: 14px;
  line-height: 1.5;
}
</style>