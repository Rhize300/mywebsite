# Deteksi Penipuan Digital

Aplikasi Streamlit untuk mendeteksi berbagai jenis penipuan digital seperti phishing URL, nomor HP penipuan, email spam/palsu, dan APK berbahaya.

## Fitur

- 🔗 **Deteksi Phishing URL**: Analisis URL untuk mendeteksi website phishing
- 📱 **Deteksi Nomor HP Penipuan**: Validasi dan deteksi nomor HP yang mencurigakan
- 📧 **Deteksi Email Spam/Palsu**: Analisis email untuk mendeteksi spam atau email palsu
- 📱 **Deteksi APK Berbahaya**: Analisis file APK untuk mendeteksi malware

## Instalasi

1. Clone repository ini
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Jalankan aplikasi:
```bash
streamlit run app.py
```

## Struktur Proyek

```
deteksi_penipuan_digital/
├── app.py                           # Aplikasi Streamlit utama
├── requirements.txt                 # Daftar library Python
├── README.md                        # Dokumentasi proyek
│
├── model/                           # Model yang dilatih dari Colab
│   ├── phishing_model.pkl
│   ├── hp_model.pkl                # (opsional, jika pakai ML)
│   ├── email_model.pkl
│   └── apk_model.pkl
│
├── data/                            # Dataset lokal (opsional)
│   ├── phishing_dataset.csv
│   ├── nomor_hp_penipuan.csv
│   ├── email_spam.csv
│   └── apk_berbahaya.csv
│
├── notebook/                        # Training model di Google Colab
│   ├── train_phishing_url.ipynb
│   ├── train_email.ipynb
│   ├── train_apk.ipynb
│   └── train_hp_model.ipynb         # (opsional)
│
├── utils/                           # Fungsi pendukung (helper)
│   ├── url_features.py              # Ekstraksi fitur URL
│   ├── validate_hp.py               # Regex dan validasi nomor HP
│   ├── process_email.py             # Preprocessing email teks
│   └── apk_features.py              # Ekstraksi fitur file statis
│
├── views/                           # Tampilan fitur-fitur
│   ├── sidebar.py                   # Navigasi menu
│   ├── phishing_view.py             # Deteksi link phishing
│   ├── hp_view.py                   # Deteksi nomor penipuan
│   ├── email_view.py                # Deteksi email palsu
│   └── apk_view.py                  # Deteksi file/apk berbahaya
│
├── assets/                          # Aset visual
│   └── logo.png
│
└── style/
    └── custom.css                   # (opsional) Gaya CSS tambahan
```

## Penggunaan

1. Pilih jenis deteksi dari sidebar
2. Masukkan data yang ingin dianalisis
3. Klik tombol "Deteksi" untuk mendapatkan hasil
4. Lihat hasil analisis dan rekomendasi

## Model Machine Learning

Model-model yang digunakan:
- **Phishing URL**: Random Forest dengan fitur URL
- **Email Spam**: Naive Bayes dengan TF-IDF
- **APK Malware**: Random Forest dengan fitur statis APK
- **Nomor HP**: Rule-based dengan regex patterns

## Kontribusi

Silakan berkontribusi dengan:
1. Fork repository
2. Buat branch fitur baru
3. Commit perubahan
4. Push ke branch
5. Buat Pull Request

## Lisensi

MIT License 