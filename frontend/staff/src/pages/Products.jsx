import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'

// Page staff: catalogue produits (liste + recherche + création + import)
export default function Products() {
  const [q, setQ] = useState('')
  const [name, setName] = useState('')
  const [categoryId, setCategoryId] = useState('')
  const [price, setPrice] = useState('')
  const [file, setFile] = useState(null)

  const { data, refetch, isFetching } = useQuery({
    queryKey: ['staff-products', q],
    queryFn: async () => (await api.get(`/api/catalog/products?search=${encodeURIComponent(q)}`)).data,
  })
  const list = data?.results || data || []

  const createProduct = async () => {
    await api.post('/api/catalog/staff/products', {
      name,
      category_id: categoryId || undefined,
      price: price || undefined,
    })
    setName(''); setCategoryId(''); setPrice('');
    refetch()
  }

  const importFile = async () => {
    if (!file) return
    const form = new FormData()
    form.append('file', file)
    await api.post('/api/catalog/staff/import', form)
    setFile(null)
    refetch()
  }

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Produits</h1>

      <section className="p-3 border rounded">
        <h2 className="font-semibold mb-2">Créer un produit</h2>
        <div className="grid md:grid-cols-4 gap-2">
          <input className="border p-2" placeholder="Nom" value={name} onChange={e=>setName(e.target.value)} />
          <input className="border p-2" placeholder="ID Catégorie (optionnel)" value={categoryId} onChange={e=>setCategoryId(e.target.value)} />
          <input className="border p-2" placeholder="Prix (optionnel)" value={price} onChange={e=>setPrice(e.target.value)} />
          <button className="px-3 py-2 bg-gray-200 rounded" onClick={createProduct}>Créer</button>
        </div>
      </section>

      <section className="p-3 border rounded">
        <h2 className="font-semibold mb-2">Importer (CSV / JSON / Excel)</h2>
        <div className="flex items-center gap-2">
          <input type="file" onChange={e=>setFile(e.target.files?.[0]||null)} />
          <button className="px-3 py-2 bg-gray-200 rounded" onClick={importFile}>Importer</button>
        </div>
        <div className="text-xs text-gray-500 mt-1">CSV attendu: colonnes name, category, price</div>
      </section>

      <div className="flex gap-2">
        <input className="border p-2 flex-1" placeholder="Rechercher des produits" value={q} onChange={e=>setQ(e.target.value)} />
        <button className="px-3 py-2 bg-gray-200 rounded" onClick={()=>refetch()} disabled={isFetching}>Rechercher</button>
      </div>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-3">
        {list.map(p => (
          <div key={p.id} className="border rounded p-3">
            <div className="font-medium">{p.name}</div>
            <div className="text-sm text-gray-500">#{p.id} · {p.current_price?.amount} {p.current_price?.currency}</div>
            <div className="text-xs text-gray-500">Actif: {String(p.is_active)}</div>
          </div>
        ))}
        {list.length===0 && <div className="text-gray-500">Aucun produit</div>}
      </div>
    </div>
  )
}
