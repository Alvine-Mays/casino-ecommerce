import { useEffect, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import Scanner from '../components/Scanner'

export default function Dashboard() {
  const [status, setStatus] = useState('PAID')
  const { data, refetch } = useQuery({
    queryKey: ['staff-orders', status],
    queryFn: async () => (await axios.get(`/api/orders/staff/orders?status=${status}`)).data,
  })

  useEffect(() => {
    const ws = new WebSocket((location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + '/ws/staff/orders/')
    ws.onmessage = () => refetch()
    return () => ws.close()
  }, [refetch])

  return (
    <div>
      <div className="flex gap-2 mb-3">
        {['PAID','IN_PREPARATION','READY_FOR_PICKUP'].map(s => (
          <button key={s} onClick={() => setStatus(s)} className={`px-3 py-1 rounded ${status===s?'bg-[#E30613] text-white':'bg-gray-200'}`}>{s}</button>
        ))}
      </div>
      <ul className="space-y-2">
        {data?.results?.map(o => (
          <li key={o.id} className="border p-3 rounded">
            <div className="flex justify-between items-center">
              <span>#{o.id}</span>
              <span className="text-sm">{o.status}</span>
              <div className="flex gap-2">
                <button onClick={()=>axios.patch(`/api/orders/staff/orders/${o.id}/prepare`).then(()=>location.reload())} className="px-2 py-1 bg-gray-200 rounded">Préparer</button>
                <button onClick={()=>axios.patch(`/api/orders/staff/orders/${o.id}/ready`).then(()=>location.reload())} className="px-2 py-1 bg-gray-200 rounded">Prête</button>
              </div>
            </div>
          </li>
        ))}
      </ul>
      <div className="mt-6 p-3 border rounded">
        <h2 className="font-semibold mb-2">Flux retrait</h2>
        <TempFinalFlow />
      </div>
    </div>
  )
}

function TempFinalFlow() {
  const [temp, setTemp] = useState('')
  const [finalCode, setFinalCode] = useState('')
  const [valid, setValid] = useState(null)
  const validateTemp = async () => {
    const res = await axios.post('/api/pickup/staff/pickup/validate-temp', { code: temp })
    setValid(res.data.valid)
  }
  const sendFinal = async () => {
    await axios.post('/api/pickup/staff/pickup/send-final', { code: temp })
    alert('Code final envoyé')
  }
  const validateFinal = async () => {
    const res = await axios.post('/api/pickup/staff/pickup/validate-final', { code: finalCode })
    alert(res.data.valid ? 'Remise effectuée' : 'Code invalide')
  }
  return (
    <div className="space-y-3">
      <Scanner onCode={(c)=> setTemp(c)} />
      <div className="flex gap-2">
        <input value={temp} onChange={e=>setTemp(e.target.value)} placeholder="Code TEMP" className="border p-2" />
        <button onClick={validateTemp} className="px-3 py-2 bg-gray-200 rounded">Valider TEMP</button>
        <button onClick={sendFinal} className="px-3 py-2 bg-gray-200 rounded">Envoyer code final</button>
      </div>
      <div className="flex gap-2">
        <input value={finalCode} onChange={e=>setFinalCode(e.target.value)} placeholder="Code FINAL" className="border p-2" />
        <button onClick={validateFinal} className="px-3 py-2 bg-gray-200 rounded">Valider FINAL</button>
      </div>
    </div>
  )
}
