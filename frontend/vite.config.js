import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  experimental: {
    renderBuiltUrl(filename) {
      // 使用本地图标
      if (filename.includes('favicon')) {
        return '/favicon.ico'
      }
      return filename
    }
  }
})
