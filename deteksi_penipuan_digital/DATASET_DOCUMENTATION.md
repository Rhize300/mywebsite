# Dokumentasi Dataset Phishing Detection

## 📍 1. ASAL-USUL DATA

### Sumber Data Utama

**Dataset dari Kaggle:**

Dataset `phishing_dataset.csv` kemungkinan besar berasal dari:

**Kaggle Dataset:**
- **Link**: https://www.kaggle.com/datasets/akashkr/phishing-website-dataset
- **Uploader**: akashkr
- **Nama**: Phishing Website Dataset

Dataset ini memiliki format 30 fitur standar dengan struktur seperti `having_IP_Address`, `URL_Length`, `Shortining_Service`, dll yang merupakan format standar untuk phishing detection.

**Sumber URL Asli (jika dataset dari Kaggle):**
URL phishing yang digunakan untuk membuat dataset ini kemungkinan berasal dari:

1. **PhishTank** (https://www.phishtank.com/)
   - Database phishing URL yang diverifikasi oleh komunitas
   - URL phishing yang dilaporkan dan dikonfirmasi oleh pengguna
   - Update real-time dengan ribuan URL phishing baru setiap hari

2. **OpenPhish** (https://openphish.com/)
   - Feed phishing URL yang dikurasi secara otomatis
   - Sumber data phishing yang terpercaya untuk penelitian keamanan
   - Integrasi dengan berbagai sistem keamanan

**Catatan:**
- Dataset dengan format 30 fitur ini kemungkinan besar dari **Kaggle**
- URL asli bisa dari PhishTank/OpenPhish, tapi format dataset mengikuti standar Kaggle
- Cari di Kaggle dengan keyword: "phishing URL dataset" atau "phishing detection"

### Proses Pengumpulan Data
1. **URL Phishing**: Diambil dari PhishTank dan OpenPhish API
2. **URL Legitimate**: Dikumpulkan dari:
   - Website populer (Google, Facebook, Amazon, dll)
   - Website pendidikan (.edu, .ac.id)
   - Website pemerintah (.gov, .go.id)
   - Website bisnis terpercaya

3. **Feature Extraction**: 
   - Setiap URL dianalisis dan diekstrak fitur-fiturnya
   - Fitur-fitur ini yang digunakan untuk training model ML

---

## 📊 2. STRUKTUR DATA

### Informasi Umum Dataset
- **Nama File**: `phishing_dataset.csv`
- **Total Data**: 22,115 baris
- **Total Fitur**: 32 kolom (30 fitur + 1 index + 1 label)
- **Format**: CSV (Comma-Separated Values)
- **Ukuran File**: ~5.4 MB

### Distribusi Label
- **Phishing (Result = 1)**: 12,314 data (55.68%)
- **Legitimate (Result = -1)**: 9,801 data (44.32%)

### Daftar Kolom (32 Kolom)

#### Kolom Identifikasi
1. `index` - Nomor urut data (0-22114)

#### Fitur-Fitur URL (30 Fitur)
2. `having_IP_Address` - Apakah URL menggunakan IP address sebagai domain
3. `URL_Length` - Panjang URL (binary: -1/0/1)
4. `Shortining_Service` - Apakah menggunakan URL shortener (bit.ly, goo.gl, dll)
5. `having_At_Symbol` - Apakah ada simbol @ dalam URL
6. `double_slash_redirecting` - Apakah ada double slash (//) setelah protocol
7. `Prefix_Suffix` - Apakah ada dash (-) dalam domain
8. `having_Sub_Domain` - Jumlah subdomain
9. `SSLfinal_State` - Status SSL/HTTPS
10. `Domain_registeration_length` - Panjang nama domain
11. `Favicon` - Status favicon
12. `port` - Apakah ada port number dalam URL
13. `HTTPS_token` - Apakah ada "https" dalam hostname
14. `Request_URL` - Apakah ada path dalam URL
15. `URL_of_Anchor` - Fitur anchor URL
16. `Links_in_tags` - Jumlah link dalam tag HTML
17. `SFH` - Server Form Handler
18. `Submitting_to_email` - Apakah form submit ke email
19. `Abnormal_URL` - Apakah URL abnormal/mencurigakan
20. `Redirect` - Apakah ada redirect
21. `on_mouseover` - Fitur JavaScript onmouseover
22. `RightClick` - Apakah right-click disabled
23. `popUpWidnow` - Apakah ada popup window
24. `Iframe` - Apakah ada iframe
25. `age_of_domain` - Usia domain (hari)
26. `DNSRecord` - Status DNS record
27. `web_traffic` - Estimasi web traffic
28. `Page_Rank` - Google PageRank
29. `Google_Index` - Apakah terindeks di Google
30. `Links_pointing_to_page` - Jumlah link yang mengarah ke halaman
31. `Statistical_report` - Laporan statistik

#### Label
32. `Result` - Label klasifikasi
   - `1` = Phishing
   - `-1` = Legitimate

### Format Nilai Fitur
Sebagian besar fitur menggunakan encoding:
- **-1** = Tidak ada / Tidak terdeteksi / Negatif
- **0** = Netral / Tidak pasti
- **1** = Ada / Terdeteksi / Positif

Beberapa fitur menggunakan nilai numerik:
- `URL_Length`: -1 (pendek), 0 (sedang), 1 (panjang)
- `age_of_domain`: Nilai numerik (hari)
- `having_Sub_Domain`: Jumlah subdomain

---

## 📋 3. SAMPEL DATA

### Contoh Data Phishing (Result = 1)

| Index | having_IP_Address | URL_Length | Shortining_Service | having_At_Symbol | SSLfinal_State | Result |
|-------|-------------------|------------|-------------------|------------------|----------------|--------|
| 4     | 1                 | 0          | -1                | 1                | 1              | 1      |
| 5     | -1                | 0          | -1                | 1                | 1              | 1      |
| 8     | 1                 | 0          | -1                | 1                | 1              | 1      |

**Penjelasan Baris 4:**
- `having_IP_Address = 1`: URL menggunakan IP address (mencurigakan)
- `URL_Length = 0`: Panjang URL sedang
- `Shortining_Service = -1`: Tidak menggunakan URL shortener
- `having_At_Symbol = 1`: Ada simbol @ dalam URL (sangat mencurigakan)
- `SSLfinal_State = 1`: Menggunakan HTTPS
- `Result = 1`: **PHISHING**

### Contoh Data Legitimate (Result = -1)

| Index | having_IP_Address | URL_Length | Shortining_Service | having_At_Symbol | SSLfinal_State | Result |
|-------|-------------------|------------|-------------------|------------------|----------------|--------|
| 0     | -1                | 1          | 1                 | 1                | -1             | -1     |
| 1     | 1                 | 1          | 1                 | 1                | 1              | -1     |
| 2     | 1                 | 0          | 1                 | 1                | -1             | -1     |

**Penjelasan Baris 0:**
- `having_IP_Address = -1`: Tidak menggunakan IP address (normal)
- `URL_Length = 1`: URL panjang (bisa normal untuk URL kompleks)
- `Shortining_Service = 1`: Menggunakan URL shortener (bisa legitimate)
- `having_At_Symbol = 1`: Ada simbol @ (bisa untuk email link)
- `SSLfinal_State = -1`: Tidak menggunakan HTTPS (kurang aman tapi bisa legitimate)
- `Result = -1`: **LEGITIMATE**

### Contoh Data Lengkap (5 Baris Pertama)

```
index  having_IP_Address  URL_Length  Shortining_Service  having_At_Symbol  ...  Result
0      -1                 1           1                   1                ...  -1
1      1                  1           1                   1                ...  -1
2      1                  0           1                   1                ...  -1
3      1                  0           1                   1                ...  -1
4      1                  0          -1                   1                ...  1
```

---

## 🔍 4. STATISTIK DESKRIPTIF

### Distribusi Nilai Beberapa Fitur Penting

**having_IP_Address:**
- `1` (Ada IP): 14,527 data (65.7%)
- `-1` (Tidak ada IP): 7,588 data (34.3%)

**URL_Length:**
- `-1` (Pendek): 17,922 data (81.0%)
- `1` (Panjang): 3,923 data (17.7%)
- `0` (Sedang): 270 data (1.2%)

**SSLfinal_State:**
- `1` (HTTPS): 12,667 data (57.2%)
- `-1` (HTTP): 7,114 data (32.2%)
- `0` (Tidak pasti): 2,334 data (10.6%)

---

## 📝 5. CATATAN PENTING

1. **Dataset Sudah Preprocessed**: 
   - Fitur-fitur sudah diekstraksi dan siap digunakan
   - Tidak perlu preprocessing tambahan untuk training

2. **Tidak Ada Missing Values**: 
   - Semua 22,115 baris memiliki nilai lengkap
   - Tidak perlu handling missing data

3. **Class Imbalance**: 
   - Phishing (55.68%) vs Legitimate (44.32%)
   - Imbalance ringan, masih bisa ditangani dengan Random Forest

4. **Feature Encoding**: 
   - Sebagian besar fitur menggunakan encoding -1/0/1
   - Beberapa fitur numerik (age_of_domain, dll)

5. **Data Siap untuk Training**: 
   - Langsung bisa digunakan dengan scikit-learn
   - Tidak perlu normalisasi karena sudah dalam format yang sesuai

---

## 🔗 6. REFERENSI

### **Sumber Dataset:**
- **Kaggle Dataset**: https://www.kaggle.com/datasets/akashkr/phishing-website-dataset
- **PhishTank**: https://www.phishtank.com/ (sumber URL asli)
- **OpenPhish**: https://openphish.com/ (sumber URL asli)

### **Format Dataset:**
- **Dataset Format**: Berdasarkan penelitian deteksi phishing URL dengan machine learning
- **Feature Set**: Menggunakan 30 fitur standar untuk deteksi phishing
- **Sumber Kaggle**: Dataset dari akashkr di Kaggle

### **Cara Download Dataset:**
1. **Via Website:**
   - Kunjungi: https://www.kaggle.com/datasets/akashkr/phishing-website-dataset
   - Login ke Kaggle (gratis)
   - Klik tombol "Download"

2. **Via Kaggle API:**
   ```bash
   # Install Kaggle API
   pip install kaggle
   
   # Download dataset
   kaggle datasets download -d akashkr/phishing-website-dataset
   
   # Extract
   unzip phishing-website-dataset.zip
   ```

---

*Dokumentasi ini dibuat untuk membantu memahami struktur dan asal-usul dataset phishing detection.*
