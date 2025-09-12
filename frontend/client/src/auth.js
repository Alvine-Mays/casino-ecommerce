import axios from 'axios'

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

axios.interceptors.request.use((config) => {
  const token = getAccess()
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

axios.interceptors.response.use(
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
