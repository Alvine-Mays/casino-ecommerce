import { api } from '../lib/api'
import { useState } from 'react'
import { setTokens } from '../auth'
import { useNavigate, useLocation, Link } from 'react-router-dom'

export default function SignIn() {
  const [form, setForm] = useState({ username: '', password: '' })
  const nav = useNavigate()
  const loc = useLocation()
  const search = new URLSearchParams(loc.search)
  const returnUrl = search.get('returnUrl') || '/'
  const submit = async () => {
    const res = await api.post('/api/auth/login', form)
    setTokens(res.data)
    nav(returnUrl)
  }
  return (
    <div className="max-w-sm mx-auto space-y-3">
      <h1 className="text-2xl font-bold">Connexion</h1>
      <input className="border p-2 w-full" placeholder="Nom d'utilisateur" value={form.username} onChange={e=>setForm({...form, username:e.target.value})} />
      <input className="border p-2 w-full" type="password" placeholder="Mot de passe" value={form.password} onChange={e=>setForm({...form, password:e.target.value})} />
      <button className="btn-primary w-full" onClick={submit}>Se connecter</button>
      <div className="text-sm text-gray-600">Nouveau client ? <Link to={`/signup?returnUrl=${encodeURIComponent(returnUrl)}`} className="text-[#E30613]">Créer un compte</Link></div>
    </div>
  )
}
