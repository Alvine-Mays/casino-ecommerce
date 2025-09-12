import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import PolicyNotice from '../components/PolicyNotice'

export default function Confirmation() {
  const { orderId } = useParams()
  const { data } = useQuery({
    queryKey: ['codes', orderId],
    queryFn: async () => (await axios.get(`/api/orders/${orderId}/codes`)).data,
  })
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Confirmation</h1>
      <PolicyNotice />
      <div>Commande #{orderId} validée.</div>
      <div className="p-3 bg-green-50 border border-green-600 rounded">
        Code TEMP: <b>{data?.codes?.find(c=>c.kind==='TEMP')?.code ?? '—'}</b>
      </div>
    </div>
  )
}
