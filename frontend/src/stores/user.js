import { defineStore } from 'pinia'
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api'
})

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: null
  }),

  actions: {
    async login(username, password) {
      try {
        // 创建 FormData 对象
        const formData = new FormData()
        formData.append('username', username)
        formData.append('password', password)

        const response = await api.post('/auth/login', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        const { access_token, user } = response.data
        
        this.token = access_token
        this.userInfo = user
        localStorage.setItem('token', access_token)
        
        // 设置全局请求头
        api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
        
        return true
      } catch (error) {
        console.error('登录失败:', error)
        if (error.response?.data?.detail) {
          throw new Error(error.response.data.detail)
        } else {
          throw new Error('登录失败，请检查网络连接')
        }
      }
    },

    async getUserInfo() {
      try {
        const response = await api.get('/users/me')
        this.userInfo = response.data
        return response.data
      } catch (error) {
        console.error('获取用户信息失败:', error)
        throw error
      }
    },

    logout() {
      this.token = ''
      this.userInfo = null
      localStorage.removeItem('token')
      delete api.defaults.headers.common['Authorization']
    }
  }
}) 