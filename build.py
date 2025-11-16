#!/usr/bin/env python3
import json
from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("icons", exist_ok=True)

# Manifest
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
        {"src": "./icons/icon-" + str(s) + "x" + str(s) + ".png", "sizes": str(s) + "x" + str(s), "type": "image/png", "purpose": "any maskable"}
        for s in [72, 96, 128, 144, 152, 192, 384, 512]
    ],
    "categories": ["health", "lifestyle", "medical"],
    "lang": "en",
    "dir": "ltr"
}

with open("manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)
print("✓ manifest.json created")

# Icons
for size in [72, 96, 128, 144, 152, 192, 384, 512]:
    img = Image.new('RGB', (size, size), color='#2DCE89')
    draw = ImageDraw.Draw(img)
    margin = size // 10
    draw.ellipse([margin, margin, size-margin, size-margin], fill='#1a9f6e')
    font_size = size // 2
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), "S", font=font)
    x = (size - (bbox[2] - bbox[0])) // 2
    y = (size - (bbox[3] - bbox[1])) // 2 - (size // 20)
    draw.text((x, y), "S", fill='white', font=font)
    img.save(f'icons/icon-{size}x{size}.png', 'PNG')
print("✓ Icons created")

# Service Worker
sw = '''const CACHE_NAME='soon-pwa-v1.5';const urlsToCache=['./','./index.html','./manifest.json'];self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE_NAME).then(cache=>cache.addAll(urlsToCache)));self.skipWaiting()});self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(cacheNames=>Promise.all(cacheNames.map(n=>n!==CACHE_NAME?caches.delete(n):null))));self.clients.claim()});self.addEventListener('fetch',e=>{e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)))});'''

with open("sw.js", "w") as f:
    f.write(sw)
print("✓ sw.js created")

print("\n✅ All PWA files generated!")
