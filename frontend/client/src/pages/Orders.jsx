import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'

export default function Orders() {
  const { data } = useQuery({ queryKey: ['myorders'], queryFn: async () => (await api.get('/api/orders/mine')).data })
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Mes commandes</h1>
      <ul className="space-y-2">
        {data?.results?.map(o => (
          <li key={o.id} className="border rounded p-3">
            <div className="flex justify-between"><span>#{o.id}</span><span>{o.status}</span></div>
            <div className="text-sm text-gray-500">{o.total_amount} XAF</div>
          </li>
        ))}
      </ul>
    </div>
  )
}
