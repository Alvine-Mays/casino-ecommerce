import axios from 'axios'

// Client HTTP centralisé pour le frontend "staff"
// - API_BASE: base URL lue depuis VITE_API_URL (fichier .env.development)
// - withCredentials: active l'envoi des cookies/headers d'auth avec les requêtes cross-origin
export const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export const api = axios.create({
  baseURL: API_BASE,
  withCredentials: true,
})
