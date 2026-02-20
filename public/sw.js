// Service Worker for TechFela Script Generator
// Enables offline support and PWA functionality

const CACHE_NAME = 'techfela-scripts-v1';
const urlsToCache = [
    './',
    './index.html',
    './js/main.js',
    './js/utils.js',
    './manifest.json',
    'https://cdn.tailwindcss.com',
    'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js'
];

// Install event - caching resources
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Service Worker: Caching app shell');
                return cache.addAll(urlsToCache).catch(err => {
                    console.log('Service Worker: Some resources could not be cached:', err);
                });
            })
            .then(() => self.skipWaiting())
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Service Worker: Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', event => {
    const { request } = event;
    
    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }

    // Skip API calls to Gemini (these must always hit the network)
    if (request.url.includes('generativelanguage.googleapis.com')) {
        event.respondWith(
            fetch(request).catch(() => {
                return new Response(JSON.stringify({
                    error: 'Network error. Please check your internet connection and API key.'
                }), {
                    status: 503,
                    headers: { 'Content-Type': 'application/json' }
                });
            })
        );
        return;
    }

    // Cache-first strategy for CSS, JS, images
    if (request.url.match(/\.(js|css|png|gif|ico|svg|woff|woff2|ttf)$/)) {
        event.respondWith(
            caches.match(request)
                .then(response => response || fetch(request))
                .catch(() => new Response('Resource not found', { status: 404 }))
        );
        return;
    }

    // Network-first strategy for HTML and API calls
    event.respondWith(
        fetch(request)
            .then(response => {
                // Cache successful responses
                if (response.ok) {
                    const responseToCache = response.clone();
                    caches.open(CACHE_NAME).then(cache => {
                        cache.put(request, responseToCache);
                    });
                }
                return response;
            })
            .catch(() => {
                // Return cached version if network fails
                return caches.match(request)
                    .then(response => response || new Response('Content not available offline', { status: 503 }));
            })
    );
});

// Message event - for cache management from app
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    
    if (event.data && event.data.type === 'CLEAR_CACHE') {
        caches.delete(CACHE_NAME).then(() => {
            console.log('Service Worker: Cache cleared');
        });
    }
});

// Background sync for future features
self.addEventListener('sync', event => {
    if (event.tag === 'sync-scripts') {
        event.waitUntil(
            // TODO: Implement cloud sync functionality
            Promise.resolve()
        );
    }
});

console.log('Service Worker: Registered and ready');
