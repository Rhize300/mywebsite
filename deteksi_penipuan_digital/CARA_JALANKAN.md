# 🚀 Cara Menjalankan Aplikasi Streamlit

## 📋 Prasyarat

1. **Python 3.8 atau lebih baru** terinstall di komputer Anda
2. **Pip** (Python package manager) sudah terinstall
3. **Internet connection** untuk download dependencies

---

## 🔧 Langkah-langkah Instalasi & Menjalankan

### **Langkah 1: Buka Terminal/Command Prompt**

**Windows:**
- Tekan `Win + R`, ketik `cmd` atau `powershell`, lalu Enter
- Atau buka PowerShell dari Start Menu

**Mac/Linux:**
- Buka Terminal

### **Langkah 2: Navigasi ke Folder Proyek**

```bash
cd D:\detector\deteksi_penipuan_digital
```

**Atau jika menggunakan path lain:**
```bash
cd path/ke/folder/deteksi_penipuan_digital
```

### **Langkah 3: Install Dependencies**

Install semua library yang diperlukan:

```bash
pip install -r requirements.txt
```

**Jika menggunakan Python 3 khusus:**
```bash
python3 -m pip install -r requirements.txt
```

**Jika ada masalah permission (Windows):**
```bash
pip install --user -r requirements.txt
```

**Waktu instalasi:** ~2-5 menit (tergantung kecepatan internet)

### **Langkah 4: Jalankan Aplikasi Streamlit**

```bash
streamlit run app.py
```

**Atau jika streamlit tidak dikenali:**
```bash
python -m streamlit run app.py
```

**Atau:**
```bash
python3 -m streamlit run app.py
```

---

## 🌐 Mengakses Aplikasi

Setelah menjalankan perintah di atas, Anda akan melihat output seperti ini:

```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

**Aplikasi akan otomatis terbuka di browser default Anda.**

Jika tidak terbuka otomatis:
1. Buka browser (Chrome, Firefox, Edge, dll)
2. Ketik di address bar: `http://localhost:8501`
3. Tekan Enter

---

## 📱 Cara Menggunakan Aplikasi

### **1. Halaman Utama**
- Aplikasi akan menampilkan halaman **Deteksi Phishing URL**
- Ada input field untuk memasukkan URL

### **2. Masukkan URL**
- Ketik atau paste URL yang ingin dianalisis
- Contoh: `https://www.kkinstagram.com/reel/DKfBEo8xnhg/`
- Atau klik tombol "📋 Contoh URL" untuk menggunakan contoh

### **3. Klik "🔍 Analisis URL"**
- Sistem akan menganalisis URL
- Tunggu beberapa detik (proses analisa)

### **4. Lihat Hasil**
- **Risk Score** (0-100)
- **Risk Level** (Aman/Tinggi/Sangat Tinggi)
- **Confidence** (%)
- **Analisis Detail** (fitur-fitur URL)
- **Rekomendasi** (tindakan yang harus dilakukan)

---

## 🛠️ Troubleshooting (Mengatasi Masalah)

### **Masalah 1: "streamlit: command not found"**

**Solusi:**
```bash
pip install streamlit
```

Atau install ulang:
```bash
pip install --upgrade streamlit
```

### **Masalah 2: "ModuleNotFoundError: No module named 'xxx'"**

**Solusi:**
Install ulang dependencies:
```bash
pip install -r requirements.txt --upgrade
```

### **Masalah 3: "Port 8501 already in use"**

**Solusi A:** Tutup aplikasi Streamlit yang sedang berjalan

**Solusi B:** Gunakan port lain:
```bash
streamlit run app.py --server.port 8502
```

### **Masalah 4: File tidak ditemukan (model, CSS, dll)**

**Pastikan:**
- Anda berada di folder yang benar (`deteksi_penipuan_digital`)
- File `phishing_model.pkl` ada di root folder
- Folder `style/`, `views/`, `utils/` ada

**Cek struktur folder:**
```bash
# Windows
dir

# Mac/Linux
ls
```

### **Masalah 5: Error saat load model**

**Pastikan:**
- File `phishing_model.pkl` ada (13 MB)
- Tidak ada file yang corrupt

**Jika model tidak ada, download atau train ulang model.**

### **Masalah 6: WHOIS timeout**

Ini normal jika domain tidak bisa di-query WHOIS. Aplikasi akan menggunakan nilai default.

### **Masalah 7: Browser tidak terbuka otomatis**

**Solusi:**
- Buka browser manual
- Ketik: `http://localhost:8501`

---

## 🔄 Menghentikan Aplikasi

**Untuk menghentikan aplikasi:**
1. Kembali ke terminal/command prompt
2. Tekan `Ctrl + C` (Windows/Mac/Linux)
3. Konfirmasi dengan menekan `Y` atau `Enter`

---

## 📝 Perintah Lengkap (Quick Reference)

```bash
# 1. Masuk ke folder proyek
cd D:\detector\deteksi_penipuan_digital

# 2. Install dependencies (hanya pertama kali)
pip install -r requirements.txt

# 3. Jalankan aplikasi
streamlit run app.py

# 4. Atau dengan port custom
streamlit run app.py --server.port 8502

# 5. Atau dengan host custom (untuk akses dari device lain)
streamlit run app.py --server.address 0.0.0.0
```

---

## 🌍 Mengakses dari Device Lain (Network)

Jika ingin mengakses aplikasi dari device lain di jaringan yang sama:

1. **Jalankan dengan network address:**
```bash
streamlit run app.py --server.address 0.0.0.0
```

2. **Cari IP address komputer Anda:**
   - Windows: `ipconfig` (lihat IPv4 Address)
   - Mac/Linux: `ifconfig` atau `ip addr`

3. **Akses dari device lain:**
   - Buka browser di device lain
   - Ketik: `http://[IP_ADDRESS]:8501`
   - Contoh: `http://192.168.1.100:8501`

---

## ⚙️ Konfigurasi Tambahan

### **Mengubah Port Default**

Buat file `.streamlit/config.toml`:
```toml
[server]
port = 8502
```

### **Mengubah Tema**

Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

---

## 📦 Dependencies yang Diinstall

Saat menjalankan `pip install -r requirements.txt`, library berikut akan diinstall:

- `streamlit` - Framework web app
- `pandas` - Data processing
- `numpy` - Numerical computing
- `scikit-learn` - Machine learning
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `whois` - Domain WHOIS query
- `tldextract` - Domain extraction
- `joblib` - Model loading
- Dan lainnya...

---

## ✅ Checklist Sebelum Menjalankan

- [ ] Python 3.8+ terinstall
- [ ] Sudah masuk ke folder proyek yang benar
- [ ] File `app.py` ada
- [ ] File `phishing_model.pkl` ada (13 MB)
- [ ] File `requirements.txt` ada
- [ ] Folder `views/`, `utils/`, `style/` ada
- [ ] Internet connection aktif (untuk install dependencies)

---

## 🎯 Contoh Output Terminal

```
(venv) D:\detector\deteksi_penipuan_digital> streamlit run app.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501

  For better performance, install the Watchdog module:
  $ xcode-select --install
```

---

## 💡 Tips

1. **Gunakan Virtual Environment** (opsional tapi disarankan):
```bash
# Buat virtual environment
python -m venv venv

# Aktifkan (Windows)
venv\Scripts\activate

# Aktifkan (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
streamlit run app.py
```

2. **Update Streamlit:**
```bash
pip install --upgrade streamlit
```

3. **Clear Cache Streamlit:**
```bash
streamlit cache clear
```

---

## 🆘 Butuh Bantuan?

Jika masih ada masalah:
1. Cek error message di terminal
2. Pastikan semua file ada di tempatnya
3. Coba install ulang dependencies
4. Restart terminal dan coba lagi

---

**Selamat menggunakan aplikasi Deteksi Penipuan Digital! 🛡️**
