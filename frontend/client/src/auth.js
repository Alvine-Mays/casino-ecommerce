import { api } from './lib/api'

// Gestion simple des tokens côté client + intercepteurs axios
// - Stockage local (localStorage) de access/refresh
// - Intercepteur request: ajoute Authorization: Bearer <token>
// - Intercepteur response: redirige vers /signin en cas de 401
export function setTokens({ access, refresh }) {
  localStorage.setItem('access', access)
  localStorage.setItem('refresh', refresh)
  try { window.dispatchEvent(new Event('auth-changed')) } catch {}
}

export function getAccess() { try { return localStorage.getItem('access') } catch { return null } }

export function logout() {
  try {
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    window.dispatchEvent(new Event('auth-changed'))
  } catch {}
}

api.interceptors.request.use((config) => {
  const token = getAccess()
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (r) => r,
  (error) => {
    const status = error?.response?.status
    if (status === 401) {
      const path = window.location.pathname + window.location.search
      if (!window.location.pathname.startsWith('/signin')) {
        window.location.href = `/signin?returnUrl=${encodeURIComponent(path)}`
      }
    }
    return Promise.reject(error)
  }
)
