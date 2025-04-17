import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    cors: true,
    fs: {
      strict: false,
      allow: ['..']
    },
    static: {
      directory: path.join(__dirname, 'public'),
      serveDirectory: true
    }
  },
  publicDir: 'public',
  assetsInclude: ['**/*.mp4']
});