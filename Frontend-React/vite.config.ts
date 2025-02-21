import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({plugins: [react()],
    base: '/groups/',
    server: {
      proxy: {
        '/groups/api': {
          target: 'http://localhost:5000', // Your backend server
          changeOrigin: true,
        //   rewrite: (path) => path.replace(/^\/api/, ''), // Adjust this if needed
        },
        '/groups/auth': {
          target: 'http://localhost:5000',
          changeOrigin: true
        }
      },
    },
  });