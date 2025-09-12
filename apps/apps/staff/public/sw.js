self.addEventListener('install', (e) => {
  self.skipWaiting()
})
self.addEventListener('activate', (e) => {
  self.clients.claim()
})
self.addEventListener('fetch', (e) => {
  // network-first
  e.respondWith(fetch(e.request).catch(() => caches.match(e.request)))
})
