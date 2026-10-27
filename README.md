# TonShortGenerator 🎬⚡
> Automated AI YouTube Shorts Studio & Video Clipper (Engineered on OpenShorts Architecture)

Subdomain Live: [https://tonshortgenerator.tonhermes.web.id](https://tonshortgenerator.tonhermes.web.id)  
Full OpenShorts Studio: [https://tonshortgenerator.tonhermes.web.id/dashboard/](https://tonshortgenerator.tonhermes.web.id/dashboard/)

---

## 📌 Deskripsi & Masking Proyek
**TonShortGenerator** adalah aplikasi mandiri pengubah naskah/video menjadi format **YouTube Shorts (vertikal 9:16 - 1080x1920)**. Proyek ini memadukan:
1. **Frontend Masking Responsif**: Tema khas YouTube Red & Dark Mode / Light Mode toggle.
2. **OpenShorts Upstream Core**: Seluruh fitur dashboard, clipping logic, timeline layouting, dan subtitle burning dari `mutonby/openshorts` diintegrasikan langsung pada direktori upstream.
3. **Lightweight Edge-TTS & FFmpeg native engine**: Render video shorts cepat tanpa kuota token harian yang mahal.

---

## ⚖️ Hak Cipta & Atribusi Lisensi (License Notice)
Proyek ini menghormati dan mematuhi hak cipta kode sumber hulu:
* **Upstream Software**: [OpenShorts](https://github.com/mutonby/openshorts)
* **OpenShorts License**: MIT License &copy; 2024 OpenShorts (lihat berkas `NOTICE` dan direktori `upstream_openshorts/`).
* **Masking & Custom Deployment**: &copy; 2026 Muhamad Sulton (TonShortGenerator). Dilindungi di bawah Lisensi MIT.

---

## 🚀 Fitur Utama
* **YouTube Signature Dark & Red Design**: Tampilan khas YouTube Studio dengan aksen merah (#FF0000) dan mode malam.
* **OpenShorts Dashboard Terintegrasi**: Akses dashboard lengkap OpenShorts via `/dashboard/`.
* **Zero Token TTS**: Voiceover suara jernih Bahasa Indonesia & Inggris tanpa biaya API key.
* **Auto Dynamic Subtitles**: Pembuatan subtitle berirama per 3 kata otomatis dibakar (hardcoded) ke video.
* **Auto Aspect Ratio 9:16**: Standar YouTube Shorts 1080x1920 siap tayang.
