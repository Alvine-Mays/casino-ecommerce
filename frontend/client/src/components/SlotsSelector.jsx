import { useEffect, useState } from 'react'
import { api } from '../lib/api'

export default function SlotsSelector({ date, value, onChange }) {
  const [slots, setSlots] = useState([])
  useEffect(() => {
    if (!date) return
    api.get(`/api/orders/slots?date=${date}`).then(res => setSlots(res.data.slots))
  }, [date])

  return (
    <div className="space-y-2">
      <div className="text-sm text-gray-600">Créneaux pour {date}</div>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
        {slots.map(s => {
          const k = `${s.start}-${s.end}`
          const disabled = s.remaining <= 0
          const selected = value && value.start === s.start && value.end === s.end
          return (
            <button key={k} disabled={disabled}
              onClick={() => onChange(s)}
              className={`border rounded p-2 text-sm ${selected? 'border-[#E30613] bg-red-50' : ''} ${disabled?'opacity-50':''}`}>
              {s.start}–{s.end} ({s.remaining})
            </button>
          )
        })}
      </div>
    </div>
  )
}
