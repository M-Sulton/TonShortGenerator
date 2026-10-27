# TonShortGenerator 🎬⚡

[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Ubuntu%20VPS%20%7C%20FastAPI-black.svg)]()
[![Status](https://img.shields.io/badge/Status-Active%20Production-success.svg)]()

> **TonShortGenerator** adalah platform open-source generator video YouTube Shorts otomatis berdurasi vertikal (9:16 - 1080x1920) yang terinspirasi dari arsitektur [OpenShorts](https://github.com/mutonby/openshorts). Dilengkapi dengan sintesis suara kecerdasan buatan (AI Edge-TTS), auto dynamic burn-in subtitles, palet visual bertema khas YouTube Crimson Red, dan mode gelap/terang responsif.

---

## 🚀 Fitur Utama

- **Vertical 9:16 Layout Engine**: Render resolusi standar YouTube Shorts 1080x1920.
- **AI Neural Voiceover**: Integrasi Edge-TTS multi-bahasa tanpa batas kuota API token.
- **Auto Burned-in Subtitles**: Generator subtitle dinamis sinkron per ketukan suara pembicara.
- **YouTube Red Signature UI**: Antarmuka modern bernuansa merah YouTube dengan dark/light theme switch responsif untuk mobile dan desktop.
- **Autonomous VPS Integration**: Berjalan mandiri dengan Caddy reverse-proxy dan PM2 process manager.

---

## 🛠️ Arsitektur & Teknologi

- **Backend**: FastAPI & Python 3.12 (Asynchronous Job Processing)
- **Voiceover**: Microsoft Edge Neural TTS
- **Video Processing**: FFmpeg v6.1+ filter-complex burn-in rendering
- **Frontend**: Tailwind CSS, FontAwesome 6, Vanilla JS
- **Server**: Caddy v2 Reverse Proxy dengan Auto-SSL & PM2

---

## 🌐 Akses & Deployment

- **Subdomain Aktif**: [https://TonShortGenerator.tonhermes.web.id](https://TonShortGenerator.tonhermes.web.id)
- **Local Port**: `http://localhost:3015`

### Menjalankan di Lokal / Server:
```bash
git clone https://github.com/M-Sulton/TonShortGenerator.git
cd TonShortGenerator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 3015
```

---

## 📄 Hak Cipta & Lisensi

Hak Cipta © 2025 - 2026 **Muhamad Sulton** / TonHermes. Seluruh Hak Dilindungi Undang-Undang.  
Didistribusikan di bawah lisensi [MIT License](LICENSE).
