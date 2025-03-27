import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import { createPinia } from 'pinia'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

const app = createApp(App)
const pinia = createPinia()

app.config.globalProperties.$axios = axios.create({
  baseURL: 'http://localhost:8000'
})

app.use(pinia)
app.use(router)
app.use(Antd)

app.mount('#app')
