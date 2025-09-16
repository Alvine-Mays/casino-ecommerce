import { useMutation } from '@tanstack/react-query'
import { api } from '../lib/api'
import { useState } from 'react'
import PaymentButtons from '../components/PaymentButtons'
import PolicyNotice from '../components/PolicyNotice'
import SlotsSelector from '../components/SlotsSelector'

export default function Checkout() {
  const [order, setOrder] = useState(null)
  const [form, setForm] = useState({
    contact_name: '', contact_phone: '', contact_email: '',
    pickup_date: new Date().toISOString().slice(0,10),
    pickup_start: '10:00', pickup_end: '12:00'
  })
  const create = useMutation({
    mutationFn: async () => (await api.post('/api/orders', form)).data,
    onSuccess: setOrder
  })
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Checkout</h1>
      <PolicyNotice />
      <div className="grid md:grid-cols-2 gap-4">
        <div className="space-y-3">
          <input className="border p-2 w-full" placeholder="Nom complet" value={form.contact_name} onChange={e=>setForm({...form, contact_name:e.target.value})} />
          <input className="border p-2 w-full" placeholder="Téléphone" value={form.contact_phone} onChange={e=>setForm({...form, contact_phone:e.target.value})} />
          <input className="border p-2 w-full" placeholder="Email (optionnel)" value={form.contact_email} onChange={e=>setForm({...form, contact_email:e.target.value})} />
          <div className="flex gap-2 items-center">
            <input type="date" className="border p-2" value={form.pickup_date} onChange={e=>setForm({...form, pickup_date:e.target.value})} />
          </div>
          <SlotsSelector date={form.pickup_date} value={{start:form.pickup_start,end:form.pickup_end}} onChange={(s)=>setForm({...form, pickup_start:s.start, pickup_end:s.end})} />
          {!order && <button className="btn-primary" onClick={()=>create.mutate()}>Valider la commande</button>}
        </div>
        <div>
          {order ? <PaymentButtons orderId={order.id} /> : <div className="text-gray-500">Validez d’abord la commande.</div>}
        </div>
      </div>
    </div>
  )
}
