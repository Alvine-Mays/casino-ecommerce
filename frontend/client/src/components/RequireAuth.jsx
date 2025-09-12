import { useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

function getAccess() { try { return localStorage.getItem('access') } catch { return null } }

export default function RequireAuth({ children }) {
  const nav = useNavigate()
  const loc = useLocation()
  useEffect(() => {
    const token = getAccess()
    if (!token) {
      const returnUrl = encodeURIComponent(loc.pathname + loc.search)
      nav(`/signin?returnUrl=${returnUrl}`)
    }
  }, [nav, loc.pathname, loc.search])
  const token = getAccess()
  if (!token) return null
  return children
}
