import fs from 'node:fs'
import path from 'node:path'
import url from 'node:url'

const __dirname = path.dirname(url.fileURLToPath(import.meta.url))
const projectRoot = path.resolve(__dirname, '..')

function loadEnvVar(name) {
  if (process.env[name]) return process.env[name]
  const envPath = path.join(projectRoot, '.env.development')
  try {
    const text = fs.readFileSync(envPath, 'utf8')
    for (const rawLine of text.split(/\r?\n/)) {
      const line = rawLine.trim()
      if (!line || line.startsWith('#') || !line.includes('=')) continue
      const [k, v] = line.split('=', 2)
      if (k === name) return v
    }
  } catch {}
  return null
}

const apiBase = loadEnvVar('VITE_API_URL') || 'http://127.0.0.1:8000'
const urlToCheck = `${apiBase.replace(/\/$/, '')}/api/health/`

console.log(`[integration:staff] Checking ${urlToCheck}`)

try {
  const res = await fetch(urlToCheck, { method: 'GET' })
  const text = await res.text()
  let json
  try { json = JSON.parse(text) } catch {}
  if (res.status !== 200) {
    console.error(`[integration:staff] Expected 200, got ${res.status}. Body:`, text)
    process.exit(1)
  }
  if (!json || json.status !== 'ok') {
    console.error(`[integration:staff] Expected {"status":"ok"}, got:`, text)
    process.exit(1)
  }
  console.log('[integration:staff] OK')
  process.exit(0)
} catch (err) {
  console.error('[integration:staff] Error:', err)
  process.exit(1)
}
