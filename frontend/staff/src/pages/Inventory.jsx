import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../lib/api'

// Page staff: stocks (liste + ajustements +/-)
export default function Inventory() {
  const [q, setQ] = useState('')
  const qc = useQueryClient()
  const { data, isFetching } = useQuery({
    queryKey: ['staff-inventory'],
    queryFn: async () => (await api.get(`/api/inventory/staff/inventory`)).data,
  })
  const listRaw = data?.results || data || []
  const list = q ? listRaw.filter(i => (i.product_name||'').toLowerCase().includes(q.toLowerCase())) : listRaw

  const adjust = useMutation({
    mutationFn: async ({ product_id, delta }) => (await api.patch(`/api/inventory/staff/inventory/${product_id}`, { delta })).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['staff-inventory'] })
  })

  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-bold">Stocks</h1>
      <div className="flex gap-2">
        <input className="border p-2 flex-1" placeholder="Filtrer par nom de produit" value={q} onChange={e=>setQ(e.target.value)} />
      </div>
      <div className="overflow-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="text-left border-b"><th className="p-2">Produit</th><th className="p-2">Qté dispo</th><th className="p-2">Seuil bas</th><th className="p-2">Actions</th></tr>
          </thead>
          <tbody>
            {list.map(it => (
              <tr key={it.product} className="border-b">
                <td className="p-2">{it.product_name || it.product}</td>
                <td className="p-2">{it.qty_available}</td>
                <td className="p-2">{it.low_stock_threshold}</td>
                <td className="p-2 flex gap-2">
                  <button className="px-2 py-1 bg-gray-200 rounded" disabled={adjust.isPending} onClick={()=>adjust.mutate({ product_id: it.product, delta: -1 })}>-1</button>
                  <button className="px-2 py-1 bg-gray-200 rounded" disabled={adjust.isPending} onClick={()=>adjust.mutate({ product_id: it.product, delta: +1 })}>+1</button>
                </td>
              </tr>
            ))}
            {list.length===0 && (
              <tr><td className="p-3 text-gray-500" colSpan={4}>{isFetching? 'Chargement...' : 'Aucun stock'}</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
