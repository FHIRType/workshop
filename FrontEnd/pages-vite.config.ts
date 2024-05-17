import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'


// https://vitejs.dev/config/
export default ({
  plugins: [react()],
  /* preview: {
     port: 8080,
     strictPort: true
   },
   server: {
     port: 8080,
     strictPort: true,
     host: true,
     origin: "http://0.0.0.0:8080"
   }, */
  lib: {
    // Could also be a dictionary or array of multiple entry points
    entry: resolve(__dirname, 'assets/index-BzP8WVmH.js'),
    name: 'module',
    // the proper extensions will be added
    fileName: 'index-BzP8WVmH',
  },
  base: "/landing-page/",
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: ['./tsconfig.json', './tsconfig.node.json'],
    tsconfigRootDir: __dirname,
  },
})
