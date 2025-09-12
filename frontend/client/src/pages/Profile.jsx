import useMe from '../hooks/useMe'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

const STATUSES = ['CREATED','PAID','IN_PREPARATION','READY_FOR_PICKUP','PICKED_UP','CANCELLED_NOT_COLLECTED','CLOSED']

export default function Profile() {
  const { data: me } = useMe(true)
  const { data: orders } = useQuery({ queryKey: ['myorders'], queryFn: async () => (await axios.get('/api/orders/mine')).data })
  const list = orders?.results || []
  const counts = STATUSES.reduce((acc, s) => ({ ...acc, [s]: list.filter(o=>o.status===s).length }), {})

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-bold mb-2">Mon profil</h1>
        <div className="grid md:grid-cols-2 gap-4">
          <Field label="Nom d'utilisateur" value={me?.username} />
          <Field label="Prénom" value={me?.first_name || '—'} />
          <Field label="Nom" value={me?.last_name || '—'} />
          <Field label="Email" value={me?.email || '—'} />
          <Field label="Téléphone" value={me?.phone || '—'} />
          <Field label="Rôle" value={me?.role} />
        </div>
      </section>

      <section>
        <h2 className="text-xl font-semibold mb-2">Résumé des commandes</h2>
        <div className="grid md:grid-cols-3 gap-3">
          <Stat title="Total" value={list.length} />
          {STATUSES.map(s => <Stat key={s} title={s} value={counts[s] || 0} />)}
        </div>
        <h3 className="text-lg font-semibold mt-4 mb-2">Dernières commandes</h3>
        <ul className="divide-y">
          {list.slice(0,5).map(o => (
            <li key={o.id} className="py-3 flex justify-between items-center">
              <div>
                <div className="font-medium">Commande #{o.id}</div>
                <div className="text-sm text-gray-500">{o.total_amount} {o.currency} · {o.status}</div>
              </div>
              <a href={`/confirmation/${o.id}`} className="px-3 py-1 bg-gray-200 rounded">Détails</a>
            </li>
          ))}
          {list.length===0 && <li className="py-3 text-gray-500">Aucune commande pour le moment.</li>}
        </ul>
      </section>
    </div>
  )
}

function Field({ label, value }) {
  return (
    <div className="p-3 border rounded">
      <div className="text-sm text-gray-500">{label}</div>
      <div className="font-medium">{value}</div>
    </div>
  )
}

function Stat({ title, value }) {
  return (
    <div className="p-3 border rounded bg-gray-50">
      <div className="text-sm text-gray-500">{title}</div>
      <div className="text-xl font-bold">{value}</div>
    </div>
  )
}
