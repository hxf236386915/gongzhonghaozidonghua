import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import svgLoader from 'vite-svg-loader'
import type { UserConfig } from 'vite'

const config: UserConfig = {
  plugins: [vue(), svgLoader()],
  resolve: {
    alias: {
      '@': path.resolve(process.cwd(), 'src')
    }
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path
      }
    }
  }
}

export default defineConfig(config) 