# 🔗 Link Dataset yang Digunakan

## 📋 Ringkasan

Dokumen ini berisi **semua link dataset** yang digunakan untuk training dan testing model deteksi penipuan digital.

---

## 🔗 1. DATASET PHISHING URL (Utama)

### **A. PhishTank**
**Website:** https://www.phishtank.com/

**Deskripsi:**
- Database phishing URL yang diverifikasi oleh komunitas
- URL phishing yang dilaporkan dan dikonfirmasi oleh pengguna
- Update real-time dengan ribuan URL phishing baru setiap hari
- Gratis untuk penggunaan non-komersial

**Link Penting:**
- **Homepage**: https://www.phishtank.com/
- **API Documentation**: https://www.phishtank.com/api_info.php
- **Download Data**: https://www.phishtank.com/developer_info.php
- **Register API Key**: https://www.phishtank.com/register.php

**Cara Menggunakan:**
1. Daftar akun gratis di PhishTank
2. Dapatkan API key
3. Gunakan API untuk download data phishing URL
4. Format: CSV atau JSON

**Contoh API Endpoint:**
```
http://data.phishtank.com/data/online-valid.json
```

---

### **B. OpenPhish**
**Website:** https://openphish.com/

**Deskripsi:**
- Feed phishing URL yang dikurasi secara otomatis
- Sumber data phishing yang terpercaya untuk penelitian keamanan
- Integrasi dengan berbagai sistem keamanan
- Update setiap 5 menit

**Link Penting:**
- **Homepage**: https://openphish.com/
- **Download Feed**: https://openphish.com/feed.txt
- **API Access**: https://openphish.com/api.html
- **Documentation**: https://openphish.com/faq.html

**Cara Menggunakan:**
1. Download feed langsung dari URL
2. Format: Text file dengan satu URL per baris
3. Update otomatis setiap 5 menit

**Contoh Download:**
```bash
wget https://openphish.com/feed.txt
```

---

## 📧 2. DATASET EMAIL SPAM (Opsional)

### **A. SpamAssassin Public Corpus**
**Website:** https://spamassassin.apache.org/old/publiccorpus/

**Deskripsi:**
- Dataset email spam dan ham (non-spam) yang dikurasi oleh Apache SpamAssassin
- Dataset standar untuk penelitian email spam detection
- Gratis dan open source

**Link Penting:**
- **Homepage**: https://spamassassin.apache.org/
- **Public Corpus**: https://spamassassin.apache.org/old/publiccorpus/
- **Download**: 
  - https://spamassassin.apache.org/old/publiccorpus/20030228_easy_ham.tar.bz2
  - https://spamassassin.apache.org/old/publiccorpus/20030228_spam.tar.bz2
  - https://spamassassin.apache.org/old/publiccorpus/20030228_hard_ham.tar.bz2

**Format:**
- Email dalam format raw (text)
- Terorganisir dalam folder spam dan ham

---

### **B. Enron Email Dataset**
**Website:** https://www.cs.cmu.edu/~enron/

**Deskripsi:**
- Dataset email dari Enron Corporation (sebelum skandal)
- Dataset besar dengan ratusan ribu email
- Digunakan untuk penelitian email classification

**Link Penting:**
- **Homepage**: https://www.cs.cmu.edu/~enron/
- **Download**: https://www.cs.cmu.edu/~enron/enron_mail_20150507.tgz
- **Documentation**: https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz

**Format:**
- Email dalam format raw
- Terorganisir berdasarkan folder pengguna

---

## 📱 3. DATASET APK MALWARE (Opsional)

### **A. VirusTotal**
**Website:** https://www.virustotal.com/

**Deskripsi:**
- Platform untuk analisis file malware
- Database besar APK malware dan benign
- API untuk akses data

**Link Penting:**
- **Homepage**: https://www.virustotal.com/
- **API Documentation**: https://developers.virustotal.com/reference
- **Register API Key**: https://www.virustotal.com/gui/join-us

**Cara Menggunakan:**
1. Daftar akun gratis
2. Dapatkan API key
3. Gunakan API untuk download metadata APK
4. Download file APK (jika diizinkan)

**Note:** 
- API gratis memiliki rate limit
- Beberapa fitur memerlukan API key berbayar

---

### **B. AndroZoo**
**Website:** https://androzoo.uni.lu/

**Deskripsi:**
- Database besar APK Android (malware dan benign)
- Dataset untuk penelitian Android malware detection
- Gratis untuk penelitian akademik

**Link Penting:**
- **Homepage**: https://androzoo.uni.lu/
- **API Documentation**: https://androzoo.uni.lu/api_doc
- **Request Access**: https://androzoo.uni.lu/access

**Cara Menggunakan:**
1. Request akses untuk penelitian akademik
2. Dapatkan API key
3. Gunakan API untuk download metadata dan APK

**Note:**
- Perlu registrasi dan approval
- Terutama untuk penelitian akademik

---

## 📞 4. DATASET NOMOR HP PENIPUAN (Opsional)

### **Sumber Data:**
- **User Reports**: Data dari laporan pengguna aplikasi
- **Operator Data**: Data dari operator telekomunikasi (jika tersedia)
- **Public Blacklist**: Daftar nomor yang dilaporkan sebagai penipuan

**Link Referensi:**
- **Truecaller**: https://www.truecaller.com/ (untuk referensi, bukan download)
- **Nomor Penipuan Indonesia**: Berbagai forum dan komunitas online

**Note:**
- Dataset nomor HP biasanya dikumpulkan dari laporan pengguna
- Tidak ada dataset publik yang besar untuk nomor HP penipuan

---

## 📊 5. DATASET YANG SUDAH DIPREPROCESS

### **Dataset yang Digunakan di Proyek Ini:**

**File:** `data/phishing_dataset.csv`

**Informasi:**
- **Total Data**: 22,115 baris
- **Format**: CSV dengan 32 kolom (30 fitur + index + label)
- **Sumber**: Kemungkinan dari Kaggle (format standar phishing detection)
- **URL Asli**: PhishTank + OpenPhish (URL mentah)
- **Status**: Sudah siap untuk training

### **Sumber Dataset dari Kaggle:**

**Link Dataset:**
- **Kaggle Dataset**: https://www.kaggle.com/datasets/akashkr/phishing-website-dataset
- **Uploader**: akashkr
- **Nama Dataset**: Phishing Website Dataset

**Deskripsi:**
- Dataset dengan format 30 fitur standar untuk phishing detection
- Format encoding: -1, 0, 1 untuk sebagian besar fitur
- Total data: ~11,000 - 22,000+ baris (tergantung versi)
- Fitur: `having_IP_Address`, `URL_Length`, `Shortining_Service`, dll

**Cara Download:**
1. Kunjungi: https://www.kaggle.com/datasets/akashkr/phishing-website-dataset
2. Klik "Download" (perlu login Kaggle)
3. Atau gunakan Kaggle API:
   ```bash
   kaggle datasets download -d akashkr/phishing-website-dataset
   ```

**Catatan:**
- Dataset ini kemungkinan besar adalah sumber dataset yang digunakan di proyek ini
- URL asli bisa dari PhishTank/OpenPhish, tapi format dataset mengikuti dataset Kaggle ini

**Struktur:**
- Kolom 1-30: Fitur-fitur URL
- Kolom 31: Index
- Kolom 32: Label (1 = Phishing, -1 = Legitimate)

**Note:**
- Dataset ini sudah dipreprocess dan fitur-fitur sudah diekstraksi
- Tidak perlu preprocessing tambahan
- Langsung bisa digunakan untuk training model

---

## 🔄 6. CARA MENDAPATKAN DATASET BARU

### **A. Download dari PhishTank:**

**Metode 1: API (Recommended)**
```python
import requests

# Daftar dulu di PhishTank untuk dapat API key
api_key = "YOUR_API_KEY"
url = f"http://data.phishtank.com/data/{api_key}/online-valid.json"

response = requests.get(url)
data = response.json()

# Simpan ke file
import json
with open('phishing_urls.json', 'w') as f:
    json.dump(data, f)
```

**Metode 2: Download Manual**
1. Kunjungi: https://www.phishtank.com/developer_info.php
2. Download file CSV atau JSON
3. Extract URL phishing dari file tersebut

---

### **B. Download dari OpenPhish:**

**Metode 1: Download Feed**
```bash
# Download feed langsung
wget https://openphish.com/feed.txt

# Atau dengan curl
curl -o phishing_urls.txt https://openphish.com/feed.txt
```

**Metode 2: Python Script**
```python
import requests

url = "https://openphish.com/feed.txt"
response = requests.get(url)

# Simpan ke file
with open('phishing_urls.txt', 'w') as f:
    f.write(response.text)

# Parse URL
urls = response.text.strip().split('\n')
print(f"Total URLs: {len(urls)}")
```

---

### **C. Ekstraksi Fitur dari URL:**

Setelah mendapatkan URL, ekstrak fitur-fitur menggunakan script:

```python
from utils.url_features import extract_url_features
import pandas as pd

# Baca URL dari file
with open('phishing_urls.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

# Ekstrak fitur untuk setiap URL
features_list = []
for url in urls:
    features = extract_url_features(url)
    features['url'] = url
    features['label'] = 1  # Phishing
    features_list.append(features)

# Convert ke DataFrame
df = pd.DataFrame(features_list)
df.to_csv('phishing_dataset_new.csv', index=False)
```

---

## 📚 7. REFERENSI DATASET LAINNYA

### **Dataset Phishing URL Lainnya:**

1. **URLhaus** (https://urlhaus.abuse.ch/)
   - Database malware URL
   - API tersedia
   - Update real-time

2. **Malware Domain List** (https://www.malwaredomainlist.com/)
   - Daftar domain malware
   - Update berkala

3. **Google Safe Browsing** (https://developers.google.com/safe-browsing)
   - API untuk cek URL berbahaya
   - Tidak untuk download dataset besar

### **Dataset Email Spam Lainnya:**

1. **TREC Spam Corpus** (https://plg.uwaterloo.ca/~gvcormac/treccorpus/)
   - Dataset email spam dari TREC
   - Digunakan untuk penelitian

2. **Lingspam Dataset** (http://nlp.cs.aueb.gr/software_and_datasets/lingspam_public.tar.gz)
   - Dataset email spam linguistik
   - Gratis untuk penelitian

### **Dataset APK Malware Lainnya:**

1. **Drebin Dataset** (https://www.sec.cs.tu-bs.de/~danarp/drebin/)
   - Dataset Android malware
   - Untuk penelitian akademik

2. **AMD (Android Malware Dataset)** (https://www.unb.ca/cic/datasets/android-adware.html)
   - Dataset Android malware dan adware
   - Gratis untuk penelitian

---

## ⚠️ 8. CATATAN PENTING

### **Legal & Ethical:**
1. **Gunakan untuk Tujuan Baik**: Dataset ini hanya untuk penelitian dan keamanan
2. **Respect Terms of Service**: Baca dan ikuti terms of service dari setiap sumber
3. **Rate Limiting**: Hormati rate limit API untuk menghindari ban
4. **Academic Use**: Beberapa dataset hanya untuk penggunaan akademik

### **Best Practices:**
1. **Backup Dataset**: Simpan backup dataset yang sudah didownload
2. **Version Control**: Gunakan versioning untuk dataset
3. **Documentation**: Dokumentasikan sumber dan tanggal download
4. **Update Berkala**: Update dataset secara berkala untuk akurasi lebih baik

### **Security:**
1. **Jangan Akses URL Phishing**: Jangan akses URL phishing secara langsung
2. **Gunakan Sandbox**: Gunakan environment terisolasi untuk testing
3. **VPN/Proxy**: Gunakan VPN jika perlu untuk keamanan

---

## 📝 9. SUMMARY LINK PENTING

### **Dataset Phishing (Format Siap Pakai):**
- ✅ **Kaggle Dataset**: https://www.kaggle.com/datasets/akashkr/phishing-website-dataset ⭐ **UTAMA**
- ✅ PhishTank: https://www.phishtank.com/ (sumber URL asli)
- ✅ OpenPhish: https://openphish.com/ (sumber URL asli)
- ✅ URLhaus: https://urlhaus.abuse.ch/

### **Email Spam:**
- ✅ SpamAssassin: https://spamassassin.apache.org/old/publiccorpus/
- ✅ Enron Dataset: https://www.cs.cmu.edu/~enron/

### **APK Malware:**
- ✅ VirusTotal: https://www.virustotal.com/
- ✅ AndroZoo: https://androzoo.uni.lu/

### **Dataset yang Sudah Dipreprocess:**
- ✅ `data/phishing_dataset.csv` (22,115 data, sudah siap digunakan)

---

## 🔗 10. QUICK ACCESS LINKS

**Copy-paste links ini untuk akses cepat:**

```
⭐ KAGGLE DATASET (UTAMA): https://www.kaggle.com/datasets/akashkr/phishing-website-dataset
PhishTank Homepage: https://www.phishtank.com/
PhishTank API: https://www.phishtank.com/api_info.php
OpenPhish Feed: https://openphish.com/feed.txt
SpamAssassin: https://spamassassin.apache.org/old/publiccorpus/
Enron Dataset: https://www.cs.cmu.edu/~enron/
VirusTotal: https://www.virustotal.com/
AndroZoo: https://androzoo.uni.lu/
```

---

*Dokumentasi ini berisi semua link dataset yang digunakan untuk program deteksi penipuan digital. Update link secara berkala jika ada perubahan.*
