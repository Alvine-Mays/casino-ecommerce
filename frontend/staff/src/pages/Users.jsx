import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'

// Page staff: liste des utilisateurs (recherche + pagination simple côté API)
export default function Users() {
  const [q, setQ] = useState('')
  const { data, refetch, isFetching } = useQuery({
    queryKey: ['staff-users', q],
    queryFn: async () => (await api.get(`/api/auth/staff/users?q=${encodeURIComponent(q)}`)).data,
  })
  const list = data?.results || data || []
  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-bold">Utilisateurs</h1>
      <div className="flex gap-2">
        <input className="border p-2 flex-1" placeholder="Rechercher (nom, email, téléphone)" value={q} onChange={e=>setQ(e.target.value)} />
        <button className="px-3 py-2 bg-gray-200 rounded" onClick={()=>refetch()} disabled={isFetching}>Rechercher</button>
      </div>
      <div className="overflow-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="text-left border-b"><th className="p-2">#</th><th className="p-2">Username</th><th className="p-2">Nom</th><th className="p-2">Email</th><th className="p-2">Téléphone</th><th className="p-2">Rôle</th></tr>
          </thead>
          <tbody>
            {list.map(u => (
              <tr key={u.id} className="border-b">
                <td className="p-2">{u.id}</td>
                <td className="p-2">{u.username}</td>
                <td className="p-2">{u.first_name} {u.last_name}</td>
                <td className="p-2">{u.email}</td>
                <td className="p-2">{u.phone}</td>
                <td className="p-2">{u.role}</td>
              </tr>
            ))}
            {list.length===0 && (
              <tr><td className="p-3 text-gray-500" colSpan={6}>Aucun utilisateur</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
