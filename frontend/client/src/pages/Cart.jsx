import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../lib/api'
import { Link } from 'react-router-dom'

export default function Cart() {
  const qc = useQueryClient()
  const { data } = useQuery({ queryKey: ['cart'], queryFn: async () => (await api.get('/api/orders/cart')).data })
  const remove = useMutation({
    mutationFn: async (id) => (await api.delete(`/api/orders/cart/items/${id}`)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['cart'] })
  })
  const total = data?.items?.reduce((t, it) => t + (it.quantity || 0), 0)
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Panier</h1>
      <ul className="divide-y">
        {data?.items?.map((it) => (
          <li key={it.id} className="flex items-center justify-between py-3">
            <div>Produit #{it.product}</div>
            <div>x{it.quantity}</div>
            <button className="text-red-600" onClick={() => remove.mutate(it.id)}>Retirer</button>
          </li>
        ))}
      </ul>
      <div className="mt-4 flex justify-between items-center">
        <div>Total items: {total}</div>
        <Link to="/checkout" className="btn-primary">Aller au checkout</Link>
      </div>
    </div>
  )
}
