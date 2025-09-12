import axios from 'axios'
import { useState } from 'react'
import { setTokens } from '../auth'
import { useNavigate, useLocation, Link } from 'react-router-dom'

export default function SignUp() {
  const [form, setForm] = useState({ username: '', email: '', phone: '', password: '' })
  const [error, setError] = useState('')
  const nav = useNavigate()
  const loc = useLocation()
  const search = new URLSearchParams(loc.search)
  const returnUrl = search.get('returnUrl') || '/'
  const submit = async () => {
    setError('')
    try {
      const res = await axios.post('/api/auth/register', form)
      const { access, refresh } = res.data
      if (access && refresh) setTokens({ access, refresh })
      nav(returnUrl)
    } catch (e) {
      setError(e?.response?.data?.detail || 'Erreur lors de la création du compte')
    }
  }
  return (
    <div className="max-w-sm mx-auto space-y-3">
      <h1 className="text-2xl font-bold">Créer un compte</h1>
      <input className="border p-2 w-full" placeholder="Nom d'utilisateur" value={form.username} onChange={e=>setForm({...form, username:e.target.value})} />
      <input className="border p-2 w-full" type="email" placeholder="Email" value={form.email} onChange={e=>setForm({...form, email:e.target.value})} />
      <input className="border p-2 w-full" placeholder="Téléphone" value={form.phone} onChange={e=>setForm({...form, phone:e.target.value})} />
      <input className="border p-2 w-full" type="password" placeholder="Mot de passe" value={form.password} onChange={e=>setForm({...form, password:e.target.value})} />
      {error && <div className="text-red-600 text-sm">{error}</div>}
      <button className="btn-primary w-full" onClick={submit}>Créer mon compte</button>
      <div className="text-sm text-gray-600">Déjà un compte ? <Link to={`/signin?returnUrl=${encodeURIComponent(returnUrl)}`} className="text-[#E30613]">Se connecter</Link></div>
    </div>
  )
}
