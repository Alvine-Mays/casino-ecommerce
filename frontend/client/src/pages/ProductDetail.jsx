import { useParams } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../lib/api'

export default function ProductDetail() {
  const { id } = useParams()
  const qc = useQueryClient()
  const { data } = useQuery({
    queryKey: ['product', id],
    queryFn: async () => (await api.get(`/api/catalog/products/${id}`)).data,
  })
  const add = useMutation({
    mutationFn: async () => (await api.post('/api/orders/cart/items', { product_id: id, quantity: 1 })).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['cart'] })
  })
  if (!data) return null
  return (
    <div className="grid md:grid-cols-2 gap-6">
      <div>
        <div className="bg-gray-100 h-64 rounded" />
      </div>
      <div>
        <h1 className="text-2xl font-bold mb-2">{data.name}</h1>
        <div className="text-lg mb-4">{data.current_price?.amount} XAF</div>
        <button className="btn-primary" onClick={() => add.mutate()}>Ajouter au panier</button>
      </div>
    </div>
  )
}
