import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
    target: process.env.VITE_API_BASE || 'http://localhost:5001',
    changeOrigin: true,
    },
  },
})
