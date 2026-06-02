# HealthCare AI - Dokter Digital 🩺

HealthCare AI adalah asisten medis digital berbasis kecerdasan buatan (AI) yang didukung oleh **Google Gemini Pro Intelligence**. Aplikasi ini dirancang untuk memberikan konsultasi kesehatan yang empati, profesional, dan akurat secara instan.

## ✨ Fitur Utama
- **Konsultasi AI 24/7**: Berbasis Gemini Flash untuk respon yang cepat dan cerdas.
- **Deteksi Gejala Dinamis**: AI akan menanyakan detail gejala sebelum memberikan analisis.
- **UI Premium**: Desain modern dan minimalis menggunakan Streamlit.
- **Persistensi API**: Kunci API disimpan dengan aman secara lokal untuk kemudahan penggunaan.

## 🚀 Cara Menjalankan
1. Instal dependensi:
   ```bash
   pip install -r requirements.txt
   ```
2. Jalankan aplikasi:
   ```bash
   streamlit run app.py
   ```
3. Masukkan Google Gemini API Key Anda saat pertama kali dijalankan.

## 📁 Struktur Proyek
- `app.py`: Logika utama aplikasi dan antarmuka chat.
- `api_key.txt`: Penyimpanan lokal untuk kunci API (diabaikan oleh git).
- `assets/`: Aset gambar dan ikon.
- `requirements.txt`: Daftar pustaka Python yang dibutuhkan.