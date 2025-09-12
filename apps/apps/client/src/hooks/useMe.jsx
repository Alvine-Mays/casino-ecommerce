import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

const fetchMe = async () => (await axios.get('/api/auth/me')).data

export default function useMe(enabled = true) {
  return useQuery({ queryKey: ['me'], queryFn: fetchMe, enabled })
}
