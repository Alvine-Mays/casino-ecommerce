import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'

// Page staff: catégories (création + mise à jour image URL/fichier)
export default function Categories() {
  const [name, setName] = useState('')
  const [image, setImage] = useState('')
  const { data, refetch } = useQuery({
    queryKey: ['staff-categories'],
    queryFn: async () => (await api.get('/api/catalog/categories')).data,
  })
  const list = data || []

  const create = async () => {
    await api.post('/api/catalog/staff/categories', { name, image_url: image || undefined })
    setName(''); setImage(''); refetch()
  }

  const upload = async (id, file) => {
    const form = new FormData()
    form.append('image', file)
    await api.post(`/api/catalog/staff/upload-category/${id}`, form)
    refetch()
  }

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Catégories</h1>
      <section className="p-3 border rounded">
        <h2 className="font-semibold mb-2">Créer une catégorie</h2>
        <div className="grid md:grid-cols-4 gap-2">
          <input className="border p-2" placeholder="Nom" value={name} onChange={e=>setName(e.target.value)} />
          <input className="border p-2" placeholder="Image URL (optionnel)" value={image} onChange={e=>setImage(e.target.value)} />
          <button className="px-3 py-2 bg-gray-200 rounded" onClick={create}>Créer</button>
        </div>
      </section>

      <div className="grid md:grid-cols-3 gap-3">
        {list.map(c => (
          <div key={c.id} className="border rounded p-3 flex items-center gap-3">
            <div className="w-16 h-16 bg-gray-100 rounded overflow-hidden">
              {c.image_url ? <img src={c.image_url} alt="" className="w-full h-full object-cover"/> : <div className="w-full h-full flex items-center justify-center text-xs text-gray-400">(auto)</div>}
            </div>
            <div className="flex-1">
              <div className="font-medium">{c.name}</div>
              <div className="text-xs text-gray-500">#{c.id}</div>
            </div>
            <label className="text-xs cursor-pointer px-2 py-1 bg-gray-200 rounded">
              Importer image
              <input type="file" className="hidden" onChange={e=> e.target.files?.[0] && upload(c.id, e.target.files[0])} />
            </label>
          </div>
        ))}
        {list.length===0 && <div className="text-gray-500">Aucune catégorie</div>}
      </div>
    </div>
  )
}
