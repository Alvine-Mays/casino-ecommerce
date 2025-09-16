import React, { useEffect } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import './styles.css'
import App from './pages/App'
import Dashboard from './pages/Dashboard'
import Users from './pages/Users'
import Products from './pages/Products'
import Inventory from './pages/Inventory'
import Categories from './pages/Categories'
import Analytics from './pages/Analytics'

const router = createBrowserRouter([
  { path: '/', element: <App />, children: [
    { index: true, element: <Navigate to="/orders" replace /> },
    { path: 'orders', element: <Dashboard /> },
    { path: 'products', element: <Products /> },
    { path: 'inventory', element: <Inventory /> },
    { path: 'categories', element: <Categories /> },
    { path: 'users', element: <Users /> },
    { path: 'analytics', element: <Analytics /> },
  ] },
])

const qc = new QueryClient()

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(() => {})
  })
}

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <QueryClientProvider client={qc}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>
)
