// Minimaler Service Worker fuer PWA-Installierbarkeit
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', () => self.clients.claim());
