import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

const createProxyConfig = (target, onlyPost = true) => ({
  target,
  changeOrigin: true,
  configure: (proxy) => {
    proxy.on('proxyReq', (proxyReq, req) => {
      if (req.method === 'GET' && onlyPost) {
        console.log('Aborting GET request to', req.url);
        proxyReq.abort();
      }
    });
  }
});

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
      '/backend': createProxyConfig('http://127.0.0.1:5000/', false),
      '/admin': createProxyConfig('http://127.0.0.1:5000/'),
      // '/login': createProxyConfig('http://127.0.0.1:5000/'),
      '/logout': createProxyConfig('http://127.0.0.1:5000/'),
      '/verify': createProxyConfig('http://127.0.0.1:5000/'),
      '/update_password': createProxyConfig('http://127.0.0.1:5000/'),
    }
  }
})
