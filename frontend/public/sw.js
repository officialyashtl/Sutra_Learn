/**
 * SUTRA LEARN — Production Service Worker (Shell v2)
 * Hardened offline app-shell caching with zero response-conversion failures.
 * Never caches private learner API data or authenticated results.
 */

const CACHE_NAME = 'sutra-learn-shell-v2';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/favicon.svg',
  '/icons.svg',
  '/robots.txt',
  '/sitemap.xml'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // 1. Only process GET requests; allow all mutations/POSTs directly to network
  if (event.request.method !== 'GET') {
    return;
  }

  let url;
  try {
    url = new URL(event.request.url);
  } catch {
    return;
  }

  // 2. Bypass Service Worker cache for all API routes, result endpoints, and cross-origin backends
  if (
    url.pathname.startsWith('/api') ||
    url.pathname.includes('/results') ||
    url.pathname.includes('/assessments') ||
    url.pathname.includes('/auth') ||
    url.origin !== self.location.origin
  ) {
    return;
  }

  // 3. App shell caching with strict Response validity guarantees
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }

      return fetch(event.request)
        .then((networkResponse) => {
          // Cache successful immutable static assets
          if (
            networkResponse &&
            networkResponse.status === 200 &&
            (url.pathname.startsWith('/assets/') ||
              url.pathname.endsWith('.svg') ||
              url.pathname.endsWith('.png') ||
              url.pathname.endsWith('.woff2'))
          ) {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseClone);
            }).catch(() => {});
          }
          return networkResponse;
        })
        .catch(() => {
          // Guaranteed valid Response resolution on network failure
          if (event.request.mode === 'navigate') {
            return caches.match('/index.html').then((indexMatch) => {
              return (
                indexMatch ||
                new Response(
                  '<!DOCTYPE html><html><head><title>SUTRA LEARN</title></head><body><h2>Offline</h2><p>Application shell offline. Please check network connection.</p></body></html>',
                  {
                    status: 200,
                    headers: { 'Content-Type': 'text/html; charset=utf-8' }
                  }
                )
              );
            });
          }

          // Return valid 503 response for non-navigate asset requests - NEVER undefined!
          return new Response('', {
            status: 503,
            statusText: 'Service Unavailable (Offline Shell Fallback)'
          });
        });
    })
  );
});
