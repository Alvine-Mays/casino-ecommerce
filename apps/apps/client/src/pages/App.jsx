import { Outlet, Link, useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { getAccess, logout } from '../auth'
import useMe from '../hooks/useMe'

export default function App() {
  const nav = useNavigate()
  const [authed, setAuthed] = useState(!!getAccess())
  const { data: me, refetch } = useMe(authed)
  useEffect(() => {
    const update = () => { setAuthed(!!getAccess()); refetch() }
    window.addEventListener('auth-changed', update)
    window.addEventListener('storage', update)
    return () => {
      window.removeEventListener('auth-changed', update)
      window.removeEventListener('storage', update)
    }
  }, [refetch])
  const onLogout = () => { logout(); nav('/') }
  return (
    <div>
      <header className="border-b">
        <div className="max-w-5xl mx-auto flex items-center justify-between p-4">
          <Link to="/" className="text-2xl font-bold" style={{color:'#E30613'}}>Géant Casino</Link>
          <nav className="flex items-center gap-4">
            <Link to="/cart">Panier</Link>
            <Link to="/orders">Mes commandes</Link>
            {authed ? (
              <>
                <Link to="/profile" className="text-gray-700">Bonjour, {me?.first_name || me?.username || 'client'}</Link>
                <button onClick={onLogout} className="px-3 py-1 rounded bg-gray-200">Déconnexion</button>
              </>
            ) : (
              <>
                <Link to="/signin">Connexion</Link>
                <Link to="/signup">Inscription</Link>
              </>
            )}
          </nav>
        </div>
      </header>
      <main className="max-w-5xl mx-auto p-4">
        <Outlet />
      </main>
      <footer className="border-t text-center text-sm p-4 text-gray-500">© {new Date().getFullYear()} Géant Casino</footer>
    </div>
  )
}
