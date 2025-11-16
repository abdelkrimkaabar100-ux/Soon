#!/usr/bin/env python3
"""
Build Soon PWA - Complete Setup Script
Generates all necessary PWA files with fixes
"""

import json
import os
from pathlib import Path

# Create directories
Path("icons").mkdir(exist_ok=True)

print("✓ Building Soon PWA v1.5...")
print("✓ Created directories")

# Generate manifest.json
manifest = {
    "name": "Soon - Mental Wellness Platform",
    "short_name": "Soon",
    "description": "A comprehensive mental wellness platform for humans and animals",
    "start_url": "./index.html",
    "display": "standalone",
    "background_color": "#2DCE89",
    "theme_color": "#2DCE89",
    "orientation": "portrait-primary",
    "icons": [
        {"src": "./icons/icon-72x72.png", "sizes": "72x72", "type": "image/png", "purpose": "any maskable"},
        {"src": "./icons/icon-96x96.png", "sizes": "96x96", "type": "image/png", "purpose": "any maskable"},
        {"src": "./icons/icon-128x128.png", "sizes": "128x128", "type": "image/png", "purpose": "any maskable"},
        {"src": "./icons/icon-144x144.png", "sizes": "144x144", "type": "image/png", "purpose": "any maskable"},
        {"src": "./icons/icon-152x152.png", "sizes": "152x152", "type": "image/png", "purpose": "any maskable"},
        {"src": "./icons/icon-192x192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
        {"src": "./icons/icon-384x384.png", "sizes": "384x384", "type": "image/png", "purpose": "any maskable"},
        {"src": "./icons/icon-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}
    ],
    "categories": ["health", "lifestyle", "medical"],
    "lang": "en",
    "dir": "ltr"
}

with open("manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print("✓ Created manifest.json")

# Generate service worker
sw_content = '''const CACHE_NAME = 'soon-pwa-v1.5';
const urlsToCache = [
  './',
  './index.html',
  './manifest.json',
  './icons/icon-192x192.png',
  './icons/icon-512x512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
      .catch(err => console.log('Cache error:', err))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request)
        .then(response => {
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }
          const responseToCache = response.clone();
          caches.open(CACHE_NAME)
            .then(cache => cache.put(event.request, responseToCache));
          return response;
        })
      )
      .catch(() => caches.match('./index.html'))
  );
});

self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'New update from Soon!',
    icon: './icons/icon-192x192.png',
    badge: './icons/icon-72x72.png',
    vibrate: [100, 50, 100]
  };
  event.waitUntil(
    self.registration.showNotification('Soon - Mental Wellness', options)
  );
});

self.addEventListener('notificationclick', event => {
  event.notification.close();
  event.waitUntil(clients.openWindow('./'));
});
'''

with open("sw.js", "w") as f:
    f.write(sw_content)

print("✓ Created sw.js")

# Generate icons
try:
    from PIL import Image, ImageDraw, ImageFont
    
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    for size in sizes:
        img = Image.new('RGB', (size, size), color='#2DCE89')
        draw = ImageDraw.Draw(img)
        margin = size // 10
        draw.ellipse([margin, margin, size-margin, size-margin], fill='#1a9f6e')
        font_size = size // 2
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        text = "S"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2
        y = (size - text_height) // 2 - (size // 20)
        draw.text((x, y), text, fill='white', font=font)
        img.save(f'icons/icon-{size}x{size}.png', 'PNG')
    print(f"✓ Created {len(sizes)} PWA icons")
except ImportError:
    print("⚠ PIL not available, skipping icon generation")

print("\n✅ PWA files generated successfully!")
print("📝 Next: Create index.html with all fixes")
