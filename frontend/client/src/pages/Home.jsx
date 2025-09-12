import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import axios from 'axios'

export default function Home() {
  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: async () => (await axios.get('/api/catalog/categories')).data,
  })
  const { data: products } = useQuery({
    queryKey: ['products'],
    queryFn: async () => (await axios.get('/api/catalog/products?is_active=true')).data,
  })

  return (
    <div>
      <div className="bg-[#E30613] text-white p-6 rounded mb-4">
        <h1 className="text-3xl font-bold">Click & Collect Brazzaville</h1>
        <p>Commandez en ligne, retirez en magasin.</p>
      </div>
      <h2 className="text-xl font-semibold mb-2">Catégories</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mb-6">
        {categories?.map((c) => (
          <div key={c.id} className="border p-3 rounded text-center">{c.name}</div>
        ))}
      </div>
      <h2 className="text-xl font-semibold mb-2">Produits</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {products?.results?.map((p) => (
          <Link to={`/product/${p.id}`} key={p.id} className="border rounded p-3 hover:shadow">
            <div className="font-medium">{p.name}</div>
            <div className="text-sm text-gray-500">{p.current_price?.amount} XAF</div>
          </Link>
        ))}
      </div>
    </div>
  )
}
