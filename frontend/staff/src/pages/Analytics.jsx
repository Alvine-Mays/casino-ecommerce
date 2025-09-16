import { useEffect, useState } from 'react'
import { api } from '../lib/api'

// Page staff: rapports et statistiques
export default function Analytics() {
  const [overview, setOverview] = useState(null)
  const [daily, setDaily] = useState({ orders: [], revenue: [] })
  const [low, setLow] = useState({ low_stock: [] })
  const [top, setTop] = useState({ top: [] })

  useEffect(() => {
    api.get('/api/orders/staff/stats/overview').then(r => setOverview(r.data))
    api.get('/api/orders/staff/stats/daily?days=14').then(r => setDaily(r.data))
    api.get('/api/orders/staff/stats/low-stock').then(r => setLow(r.data))
    api.get('/api/orders/staff/stats/top-products?days=30').then(r => setTop(r.data))
  }, [])

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Rapports & Statistiques</h1>

      <section>
        <h2 className="font-semibold mb-2">Aperçu</h2>
        <div className="grid md:grid-cols-4 gap-3">
          <Card title="Total revenu" value={`${overview?.total_revenue ?? 0} XAF`} />
          <Card title="Cmd du jour" value={overview?.today_orders ?? 0} />
          {overview && Object.entries(overview.counts || {}).slice(0,6).map(([k,v]) => (
            <Card key={k} title={k} value={v} />
          ))}
        </div>
      </section>

      <section>
        <h2 className="font-semibold mb-2">Séries quotidiennes (14 jours)</h2>
        <div className="grid md:grid-cols-2 gap-4">
          <SeriesTable title="Commandes" rows={(daily.orders||[]).map(r=>({date:r.d, value:r.count}))} />
          <SeriesTable title="Revenu" rows={(daily.revenue||[]).map(r=>({date:r.d, value:r.total}))} />
        </div>
      </section>

      <section className="grid md:grid-cols-2 gap-4">
        <div>
          <h2 className="font-semibold mb-2">Ruptures / Bas de stock</h2>
          <table className="min-w-full text-sm">
            <thead><tr className="text-left border-b"><th className="p-2">Produit</th><th className="p-2">Qté</th><th className="p-2">Seuil</th></tr></thead>
            <tbody>
              {(low.low_stock||[]).map(it => (
                <tr key={it.product_id} className="border-b"><td className="p-2">{it.product_name||it.product_id}</td><td className="p-2">{it.qty_available}</td><td className="p-2">{it.low_stock_threshold}</td></tr>
              ))}
              {(low.low_stock||[]).length===0 && <tr><td className="p-3 text-gray-500" colSpan={3}>Aucun bas de stock</td></tr>}
            </tbody>
          </table>
        </div>
        <div>
          <h2 className="font-semibold mb-2">Top produits (30 jours)</h2>
          <table className="min-w-full text-sm">
            <thead><tr className="text-left border-b"><th className="p-2">Produit</th><th className="p-2">Qté</th><th className="p-2">Montant</th></tr></thead>
            <tbody>
              {(top.top||[]).map(it => (
                <tr key={`${it.product_id}-${it.name}`} className="border-b"><td className="p-2">{it.name||it.product_id}</td><td className="p-2">{it.qty}</td><td className="p-2">{it.amount}</td></tr>
              ))}
              {(top.top||[]).length===0 && <tr><td className="p-3 text-gray-500" colSpan={3}>Aucune vente</td></tr>}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}

function Card({ title, value }) {
  return (
    <div className="p-4 border rounded bg-gray-50">
      <div className="text-xs uppercase text-gray-500">{title}</div>
      <div className="text-2xl font-bold">{value}</div>
    </div>
  )
}

function SeriesTable({ title, rows }) {
  return (
    <div className="p-3 border rounded">
      <div className="font-semibold mb-2">{title}</div>
      <table className="min-w-full text-sm">
        <thead><tr className="text-left border-b"><th className="p-2">Date</th><th className="p-2">Valeur</th></tr></thead>
        <tbody>
          {rows.map((r, i) => <tr key={i} className="border-b"><td className="p-2">{String(r.date).slice(0,10)}</td><td className="p-2">{r.value}</td></tr>)}
          {rows.length===0 && <tr><td className="p-3 text-gray-500" colSpan={2}>Aucune donnée</td></tr>}
        </tbody>
      </table>
    </div>
  )
}
