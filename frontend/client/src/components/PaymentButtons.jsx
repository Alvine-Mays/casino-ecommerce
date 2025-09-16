import { api } from '../lib/api'
import { useNavigate } from 'react-router-dom'

export default function PaymentButtons({ orderId }) {
  const nav = useNavigate()
  const pay = async () => {
    const res = await api.post('/api/payments/intent', { order_id: orderId })
    const ref = res.data.reference
    await api.post('/api/payments/webhook', { reference: ref, status: 'SUCCEEDED' })
    nav(`/confirmation/${orderId}`)
  }
  return (
    <button onClick={pay} className="btn-primary">Payer avec CinetPay (sandbox)</button>
  )
}
