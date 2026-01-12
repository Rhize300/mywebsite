# Proses URL dari Input Mentah sampai Labeling

## 📋 Ringkasan

Dokumen ini menjelaskan **langkah demi langkah** bagaimana URL mentah (raw input) diproses sampai menjadi **label final** (Phishing atau Legitimate).

---

## 🔄 Alur Lengkap Proses

```
[1] URL MENTAH (Input)
    ↓
[2] PREPROCESSING & VALIDASI
    ↓
[3] PARSING URL
    ↓
[4] EKSTRAKSI FITUR (30 fitur)
    ↓
[5] KONVERSI KE FORMAT MODEL
    ↓
[6] PREDIKSI MODEL ML
    ↓
[7] POST-PROCESSING & VALIDASI
    ↓
[8] LABELING FINAL
    ↓
[9] OUTPUT: Label + Confidence + Risk Score
```

---

## 📝 TAHAP 1: URL MENTAH (Input)

### 1.1 Input dari User
User memasukkan URL melalui interface Streamlit:

**Contoh Input:**
```
https://www.kkinstagram.com/reel/DKfBEo8xnhg/
```

**Atau:**
```
http://192.168.1.1/login.php?user=admin
```

**Atau:**
```
bit.ly/3xYz9K
```

### 1.2 Format Input
- Bisa dengan atau tanpa `http://` atau `https://`
- Bisa URL lengkap atau URL shortener
- Bisa dengan query parameters, path, dll

**Kode:**
```python
url_input = st.text_input("URL yang ingin diperiksa:")
# url_input = "https://www.kkinstagram.com/reel/DKfBEo8xnhg/"
```

---

## 🔧 TAHAP 2: PREPROCESSING & VALIDASI

### 2.1 Normalisasi URL
Jika URL tidak memiliki protocol, tambahkan `http://`:

```python
if not url.startswith(('http://', 'https://')):
    url = 'http://' + url
```

### 2.2 Validasi Format URL
Cek apakah URL memiliki format yang valid:

```python
from urllib.parse import urlparse
parsed = urlparse(url)

# Validasi minimal
if not parsed.netloc:  # Tidak ada hostname
    return None  # URL tidak valid
```

### 2.3 Lowercase Conversion
Konversi domain ke lowercase untuk konsistensi:

```python
domain = parsed.hostname.lower()
# "WWW.KKINSTAGRAM.COM" → "www.kkinstagram.com"
```

**Hasil Tahap 2:**
- URL sudah dinormalisasi
- Format valid
- Domain sudah lowercase

---

## 🔍 TAHAP 3: PARSING URL

### 3.1 Parse dengan urllib.parse
Memecah URL menjadi komponen-komponennya:

```python
from urllib.parse import urlparse

parsed = urlparse(url)
# Input: "https://www.kkinstagram.com/reel/DKfBEo8xnhg/"

# Hasil parsing:
parsed.scheme      # "https"
parsed.netloc      # "www.kkinstagram.com"
parsed.hostname    # "www.kkinstagram.com"
parsed.path        # "/reel/DKfBEo8xnhg/"
parsed.query       # "" (kosong)
parsed.fragment    # "" (kosong)
parsed.port        # None
```

### 3.2 Extract Domain dengan tldextract
Memisahkan domain, subdomain, dan TLD:

```python
import tldextract

extracted = tldextract.extract(url)
# Input: "https://www.kkinstagram.com/reel/DKfBEo8xnhg/"

# Hasil extraction:
extracted.subdomain  # "www"
extracted.domain     # "kkinstagram"
extracted.suffix     # "com"
```

**Hasil Tahap 3:**
- URL sudah di-parse menjadi komponen
- Domain, subdomain, TLD sudah terpisah
- Siap untuk ekstraksi fitur

---

## 🎯 TAHAP 4: EKSTRAKSI FITUR (30 Fitur)

Sistem mengekstrak **30 fitur** dari URL yang sudah di-parse. Fitur-fitur ini yang akan digunakan model ML untuk prediksi.

### 4.1 Fitur Struktur URL (8 fitur)

#### **Fitur 1: `having_IP_Address`**
**Cara ekstraksi:**
```python
# Cek apakah hostname adalah IP address
if parsed.hostname.replace('.', '').isdigit():
    having_IP_Address = -1  # Tidak ada IP (normal)
else:
    having_IP_Address = 1   # Ada IP (mencurigakan)
```

**Contoh:**
- `https://192.168.1.1/login` → `1` (mencurigakan)
- `https://www.google.com` → `-1` (normal)

#### **Fitur 2: `URL_Length`**
**Cara ekstraksi:**
```python
url_length = len(url)
if url_length > 75:
    URL_Length = 1   # Panjang (mencurigakan)
elif url_length < 54:
    URL_Length = -1  # Pendek (normal)
else:
    URL_Length = 0   # Sedang
```

**Contoh:**
- `https://www.kkinstagram.com/reel/DKfBEo8xnhg/` (52 chars) → `-1`
- URL panjang dengan banyak parameter → `1`

#### **Fitur 3: `Shortining_Service`**
**Cara ekstraksi:**
```python
shorteners = ['bit.ly', 'goo.gl', 'tinyurl', 't.co', 'ow.ly']
if any(service in url for service in shorteners):
    Shortining_Service = 1   # Pakai shortener (mencurigakan)
else:
    Shortining_Service = -1  # Tidak pakai (normal)
```

**Contoh:**
- `bit.ly/3xYz9K` → `1` (mencurigakan)
- `https://www.google.com` → `-1` (normal)

#### **Fitur 4: `having_At_Symbol`**
**Cara ekstraksi:**
```python
if '@' in url:
    having_At_Symbol = 1   # Ada @ (SANGAT mencurigakan)
else:
    having_At_Symbol = -1  # Tidak ada (normal)
```

**Contoh:**
- `https://www.google.com@evil.com` → `1` (sangat mencurigakan)
- `https://www.google.com` → `-1` (normal)

#### **Fitur 5: `double_slash_redirecting`**
**Cara ekstraksi:**
```python
# Cek double slash setelah protocol (http:// atau https://)
if '//' in url[8:]:  # Setelah "https://"
    double_slash_redirecting = 1   # Ada (mencurigakan)
else:
    double_slash_redirecting = -1  # Tidak ada (normal)
```

**Contoh:**
- `https://www.google.com//evil.com` → `1` (mencurigakan)
- `https://www.google.com` → `-1` (normal)

#### **Fitur 6: `Prefix_Suffix`**
**Cara ekstraksi:**
```python
if '-' in parsed.hostname:
    Prefix_Suffix = 1   # Ada dash (mencurigakan)
else:
    Prefix_Suffix = -1  # Tidak ada (normal)
```

**Contoh:**
- `www-fake-google.com` → `1` (mencurigakan)
- `www.google.com` → `-1` (normal)

#### **Fitur 7: `having_Sub_Domain`**
**Cara ekstraksi:**
```python
parts = parsed.hostname.split('.')
if len(parts) > 2 and not parsed.hostname.startswith('www.'):
    having_Sub_Domain = 1   # Banyak subdomain (mencurigakan)
else:
    having_Sub_Domain = 0   # Normal
```

**Contoh:**
- `sub1.sub2.sub3.example.com` → `1` (mencurigakan)
- `www.google.com` → `0` (normal)

#### **Fitur 8: `Request_URL`**
**Cara ekstraksi:**
```python
if len(parsed.path) > 0:
    Request_URL = 1   # Ada path (normal)
else:
    Request_URL = -1   # Tidak ada path
```

**Contoh:**
- `https://www.google.com/search` → `1`
- `https://www.google.com` → `-1`

### 4.2 Fitur Keamanan (3 fitur)

#### **Fitur 9: `SSLfinal_State`**
**Cara ekstraksi:**
```python
if parsed.scheme == 'https':
    SSLfinal_State = 1   # HTTPS (aman)
else:
    SSLfinal_State = -1  # HTTP (kurang aman)
```

**Contoh:**
- `https://www.google.com` → `1` (aman)
- `http://www.google.com` → `-1` (kurang aman)

#### **Fitur 10: `port`**
**Cara ekstraksi:**
```python
if parsed.port:
    port = 1   # Ada port (bisa mencurigakan)
else:
    port = -1  # Tidak ada port (normal)
```

**Contoh:**
- `https://www.google.com:8080` → `1`
- `https://www.google.com` → `-1`

#### **Fitur 11: `HTTPS_token`**
**Cara ekstraksi:**
```python
if 'https' in parsed.hostname:
    HTTPS_token = 1   # Ada "https" di hostname (SANGAT mencurigakan)
else:
    HTTPS_token = -1  # Tidak ada (normal)
```

**Contoh:**
- `https://https-google.com` → `1` (sangat mencurigakan)
- `https://www.google.com` → `-1` (normal)

### 4.3 Fitur Domain (4 fitur)

#### **Fitur 12: `Domain_registeration_length`**
**Cara ekstraksi:**
```python
if len(parsed.hostname) > 10:
    Domain_registeration_length = 1   # Panjang (bisa mencurigakan)
else:
    Domain_registeration_length = -1  # Pendek (normal)
```

#### **Fitur 13: `age_of_domain`**
**Cara ekstraksi:**
```python
import whois
from datetime import datetime

try:
    w = whois.whois(domain)
    if w.creation_date:
        creation_date = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
        age = (datetime.now() - creation_date).days
        age_of_domain = age
    else:
        age_of_domain = 0
except:
    age_of_domain = 0  # Default jika gagal query
```

**Contoh:**
- Domain baru (<30 hari) → `age_of_domain = 5` (sangat mencurigakan)
- Domain lama (>1 tahun) → `age_of_domain = 500` (normal)

#### **Fitur 14: `DNSRecord`**
**Cara ekstraksi:**
```python
# Cek apakah DNS record valid
try:
    import socket
    socket.gethostbyname(domain)
    DNSRecord = 1   # Valid
except:
    DNSRecord = -1  # Tidak valid (mencurigakan)
```

#### **Fitur 15: `is_typo_domain`** ⭐ **PENTING**
**Cara ekstraksi:**
```python
from difflib import SequenceMatcher

popular_domains = ['google.com', 'facebook.com', 'instagram.com', ...]
domain = extracted.domain.lower()

for popular in popular_domains:
    base = popular.split('.')[0]  # "google" dari "google.com"
    ratio = SequenceMatcher(None, domain, base).ratio()
    
    if ratio >= 0.8 and domain != base:
        is_typo_domain = 1  # MIRIP! (SANGAT mencurigakan)
        break
else:
    is_typo_domain = 0  # Tidak mirip (normal)
```

**Contoh:**
- `kkinstagram.com` vs `instagram.com` → `ratio = 0.88` → `is_typo_domain = 1` ⚠️
- `google.com` → `is_typo_domain = 0` (normal)

### 4.4 Fitur Konten (5 fitur)

#### **Fitur 16: `Abnormal_URL`**
**Cara ekstraksi:**
```python
suspicious_words = ['login', 'secure', 'verify', 'account', 'update']
if any(word in url.lower() for word in suspicious_words):
    Abnormal_URL = 1   # Ada kata mencurigakan
else:
    Abnormal_URL = -1  # Tidak ada
```

**Contoh:**
- `https://www.fake.com/login` → `1` (mencurigakan)
- `https://www.google.com` → `-1` (normal)

#### **Fitur 17-20: Default Values**
```python
Favicon = 1              # Default
URL_of_Anchor = 0         # Default
Links_in_tags = 0        # Default
SFH = 0                  # Default
Submitting_to_email = -1 # Default
```

### 4.5 Fitur JavaScript/HTML (4 fitur)

```python
on_mouseover = 1    # Default
RightClick = 1      # Default
popUpWidnow = 1     # Default
Iframe = 1          # Default
```

### 4.6 Fitur Reputasi (6 fitur)

```python
web_traffic = -1           # Default
Page_Rank = -1             # Default
Google_Index = -1          # Default
Links_pointing_to_page = 1 # Default
Statistical_report = 1     # Default
Redirect = 0               # Default
```

**Hasil Tahap 4:**
- Dictionary dengan 30 fitur
- Setiap fitur memiliki nilai: `-1`, `0`, atau `1` (atau numerik untuk `age_of_domain`)

**Contoh Output:**
```python
{
    'having_IP_Address': -1,
    'URL_Length': -1,
    'Shortining_Service': -1,
    'having_At_Symbol': -1,
    'double_slash_redirecting': -1,
    'Prefix_Suffix': -1,
    'having_Sub_Domain': 1,
    'SSLfinal_State': 1,
    'is_typo_domain': 1,  # ⚠️ MIRIP INSTAGRAM!
    'Abnormal_URL': -1,
    # ... 20 fitur lainnya
}
```

---

## 🔄 TAHAP 5: KONVERSI KE FORMAT MODEL

### 5.1 Convert Dictionary ke DataFrame
Fitur yang sudah diekstrak dikonversi ke format yang sesuai dengan model ML:

```python
import pandas as pd

# Convert dictionary ke DataFrame
feature_df = pd.DataFrame([features])
# Shape: (1, 30) - 1 baris, 30 kolom
```

### 5.2 Pastikan Urutan Kolom
Urutan kolom harus sama dengan saat training:

```python
# Pastikan urutan kolom sesuai training
columns_order = [
    'having_IP_Address',
    'URL_Length',
    'Shortining_Service',
    # ... 27 kolom lainnya
]

feature_df = feature_df[columns_order]
```

**Hasil Tahap 5:**
- DataFrame dengan shape (1, 30)
- Siap untuk input ke model ML

---

## 🤖 TAHAP 6: PREDIKSI MODEL ML

### 6.1 Load Model
```python
import pickle

@st.cache_resource
def load_phishing_model():
    with open('phishing_model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

model = load_phishing_model()
```

**Model:**
- **Algoritma**: Random Forest Classifier
- **n_estimators**: 100 pohon
- **Ukuran**: ~13 MB

### 6.2 Prediksi Class
```python
# Prediksi class (1 = phishing, -1 = legitimate)
prediction = model.predict(feature_df)[0]
```

**Output:**
- `prediction = 1` → **PHISHING**
- `prediction = -1` → **LEGITIMATE**

### 6.3 Prediksi Probability (Confidence)
```python
# Prediksi probability untuk setiap class
probability = model.predict_proba(feature_df)[0]
# probability = [prob_legitimate, prob_phishing]
# Contoh: [0.14, 0.86]

confidence = max(probability)
# confidence = 0.86 (86%)
```

**Output:**
- `confidence = 0.86` → 86% yakin dengan prediksi

**Hasil Tahap 6:**
- `prediction = 1` (PHISHING)
- `confidence = 0.86` (86%)

---

## ✅ TAHAP 7: POST-PROCESSING & VALIDASI

### 7.1 Cek Whitelist (Jika belum dicek)
```python
legitimate_domains = ['google.com', 'facebook.com', ...]
if domain in legitimate_domains:
    prediction = -1  # Override ke LEGITIMATE
    confidence = 0.95
```

### 7.2 Cek User Report
```python
reported_urls = load_reported_urls()
if url.lower() in reported_urls:
    prediction = 1   # Override ke PHISHING
    confidence = 0.95
```

**Hasil Tahap 7:**
- Prediksi sudah divalidasi
- Override jika perlu (whitelist/report)

---

## 🏷️ TAHAP 8: LABELING FINAL

### 8.1 Mapping Prediction ke Label
```python
if prediction == 1:
    label = "PHISHING"
    label_code = 1
elif prediction == -1:
    label = "LEGITIMATE"
    label_code = -1
else:
    label = "UNKNOWN"
    label_code = 0
```

### 8.2 Hitung Risk Score
```python
if prediction == 1:  # Phishing
    risk_score = int(confidence * 100)
    # Contoh: 0.86 → 86
else:  # Legitimate
    risk_score = int((1 - confidence) * 20)
    # Contoh: 0.95 → 1
```

### 8.3 Kategori Risk Level
```python
if prediction == 1:  # Phishing
    if confidence >= 0.9:
        risk_level = "🔴 Sangat Tinggi (PHISHING)"
    elif confidence >= 0.7:
        risk_level = "🟠 Tinggi (PHISHING)"
    else:
        risk_level = "🟡 Sedang (PHISHING)"
else:  # Legitimate
    if confidence >= 0.9:
        risk_level = "🟢 Aman (LEGITIMATE)"
    else:
        risk_level = "🟡 Sedang (LEGITIMATE)"
```

**Hasil Tahap 8:**
- `label = "PHISHING"`
- `label_code = 1`
- `risk_score = 86`
- `risk_level = "🟠 Tinggi (PHISHING)"`

---

## 📤 TAHAP 9: OUTPUT FINAL

### 9.1 Struktur Output
```python
output = {
    'url': 'https://www.kkinstagram.com/reel/DKfBEo8xnhg/',
    'prediction': 1,
    'label': 'PHISHING',
    'confidence': 0.86,
    'risk_score': 86,
    'risk_level': '🟠 Tinggi (PHISHING)',
    'features': {
        'having_IP_Address': -1,
        'URL_Length': -1,
        'is_typo_domain': 1,  # ⚠️ MIRIP INSTAGRAM!
        # ... 27 fitur lainnya
    }
}
```

### 9.2 Display ke User
```python
# Tampilkan hasil
st.markdown(f"**Label:** {label}")
st.markdown(f"**Risk Score:** {risk_score}/100")
st.markdown(f"**Confidence:** {confidence*100:.1f}%")
st.markdown(f"**Risk Level:** {risk_level}")
```

---

## 🔄 Contoh Lengkap: URL sampai Labeling

### **Input:**
```
https://www.kkinstagram.com/reel/DKfBEo8xnhg/
```

### **Proses:**

**1. Preprocessing:**
- URL sudah valid
- Domain: `www.kkinstagram.com`

**2. Parsing:**
- `scheme = "https"`
- `hostname = "www.kkinstagram.com"`
- `domain = "kkinstagram"`
- `suffix = "com"`

**3. Ekstraksi Fitur:**
- `having_IP_Address = -1` (tidak ada IP)
- `URL_Length = -1` (pendek)
- `SSLfinal_State = 1` (HTTPS)
- `is_typo_domain = 1` ⚠️ **MIRIP INSTAGRAM!**
- `Abnormal_URL = -1` (tidak ada kata mencurigakan)
- ... (30 fitur)

**4. Konversi:**
- DataFrame shape: (1, 30)

**5. Prediksi Model:**
- `prediction = 1` (PHISHING)
- `confidence = 0.86` (86%)

**6. Post-processing:**
- Tidak ada di whitelist
- Tidak ada di report

**7. Labeling:**
- `label = "PHISHING"`
- `risk_score = 86`
- `risk_level = "🟠 Tinggi (PHISHING)"`

### **Output Final:**
```
URL: https://www.kkinstagram.com/reel/DKfBEo8xnhg/
Label: PHISHING
Risk Score: 86/100
Confidence: 86.0%
Risk Level: 🟠 Tinggi (PHISHING)

⚠️ PERINGATAN TINGGI - PHISHING DETECTED
- JANGAN akses website ini
- JANGAN masukkan informasi pribadi
```

---

## 📊 Ringkasan Proses

| Tahap | Input | Output | Waktu |
|-------|-------|--------|-------|
| 1. Input | URL string | URL string | <1ms |
| 2. Preprocessing | URL string | URL normalized | <1ms |
| 3. Parsing | URL string | Parsed components | <1ms |
| 4. Ekstraksi Fitur | Parsed URL | 30 fitur | ~2-5 detik |
| 5. Konversi | 30 fitur | DataFrame | <1ms |
| 6. Prediksi ML | DataFrame | Prediction + Confidence | ~100ms |
| 7. Post-processing | Prediction | Validated prediction | <1ms |
| 8. Labeling | Prediction | Label + Risk Score | <1ms |
| 9. Output | Label | Display hasil | <1ms |

**Total waktu:** ~2-6 detik (tergantung WHOIS query)

---

## 🎯 Fitur Paling Penting untuk Labeling

Berdasarkan analisa, fitur-fitur berikut **paling berpengaruh** dalam menentukan label:

1. **`is_typo_domain`** - Typo-squatting detection
2. **`having_IP_Address`** - IP sebagai domain
3. **`having_At_Symbol`** - Simbol @ dalam URL
4. **`SSLfinal_State`** - Status HTTPS
5. **`age_of_domain`** - Usia domain
6. **`Abnormal_URL`** - Kata mencurigakan
7. **`Shortining_Service`** - URL shortener

---

*Dokumentasi ini menjelaskan proses lengkap dari URL mentah sampai labeling final.*
