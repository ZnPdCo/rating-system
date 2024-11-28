import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      '/backend': 'http://127.0.0.1:5000/',
      '/admin': 'http://127.0.0.1:5000/',
      '/login': 'http://127.0.0.1:5000/',
      '/logout': 'http://127.0.0.1:5000/',
      '/verify': 'http://127.0.0.1:5000/',
      '/update_password': 'http://127.0.0.1:5000/',
    }
  }
})
