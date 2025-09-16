import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'

const fetchMe = async () => (await api.get('/api/auth/me')).data

export default function useMe(enabled = true) {
  return useQuery({ queryKey: ['me'], queryFn: fetchMe, enabled })
}
