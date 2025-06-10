// frontend/vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path' // Import path module for resolving aliases

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // Example: Alias '@' to '/src'
    },
  },
  build: {
    outDir: 'dist', // Ensure output directory is 'dist' as referenced in Dockerfile
  },
  server: { // Optional: For local dev proxy to backend
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // Your backend address
        changeOrigin: true,
        // rewrite: (path) => path.replace(/^\/api/, '') // if backend doesn't expect /api prefix
      },
      // Example for WebSocket proxying if your backend WebSocket is not under /api
      // '/ws': {
      //   target: 'ws://localhost:8000', // Your backend WebSocket address
      //   ws: true,
      //   changeOrigin: true,
      // }
    }
  }
})
