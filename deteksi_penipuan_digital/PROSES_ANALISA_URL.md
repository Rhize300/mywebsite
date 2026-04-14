# Proses Analisa URL - Deteksi Phishing

## 📋 Ringkasan Proses

Proses analisa URL dimulai dari **input URL** oleh user hingga menghasilkan **prediksi phishing atau legitimate** dengan confidence score. Proses ini terdiri dari **5 tahap utama**.

---

## 🔄 Alur Proses Analisa URL

```
INPUT URL
    ↓
[1] Validasi & Whitelist Check
    ↓
[2] Ekstraksi Fitur URL
    ↓
[3] Konversi Fitur ke Format Model
    ↓
[4] Prediksi dengan Machine Learning Model
    ↓
[5] Perhitungan Risk Score & Display Hasil
    ↓
OUTPUT: Prediksi + Confidence + Risk Score
```

---

## 📝 TAHAP 1: Validasi & Whitelist Check

### 1.1 Input URL dari User
User memasukkan URL melalui interface Streamlit:
```python
url_input = st.text_input("URL yang ingin diperiksa:")
# Contoh: "https://www.kkinstagram.com/reel/DKfBEo8xnhg/"
```

### 1.2 Cek Whitelist Domain
Sistem mengecek apakah domain ada di **whitelist legitimate**:

**A. Domain Populer Terkenal:**
- `google.com`, `facebook.com`, `youtube.com`
- `github.com`, `stackoverflow.com`, `reddit.com`
- `amazon.com`, `microsoft.com`, `apple.com`
- `gmail.com`, `outlook.com`, `yahoo.com`
- Dan 40+ domain lainnya

**B. Domain Pendidikan Indonesia:**
- `ui.ac.id`, `itb.ac.id`, `ugm.ac.id`
- `gunadarma.ac.id`, `unair.ac.id`
- Dan 50+ domain pendidikan lainnya

**Hasil:**
- ✅ **Jika ada di whitelist** → Langsung return `LEGITIMATE` dengan confidence 95%
- ❌ **Jika tidak ada** → Lanjut ke Tahap 2 (Ekstraksi Fitur)

**Kode:**
```python
if domain in all_legitimate_domains:
    return 0, 0.95  # Legitimate dengan confidence tinggi
```

---

## 🔍 TAHAP 2: Ekstraksi Fitur URL

Jika URL tidak ada di whitelist, sistem mengekstrak **30 fitur** dari URL untuk dianalisis.

### 2.1 Parsing URL
```python
from urllib.parse import urlparse
import tldextract

parsed = urlparse(url)
# parsed.scheme = "https"
# parsed.hostname = "www.kkinstagram.com"
# parsed.path = "/reel/DKfBEo8xnhg/"

extracted = tldextract.extract(url)
# extracted.domain = "kkinstagram"
# extracted.suffix = "com"
# extracted.subdomain = "www"
```

### 2.2 Ekstraksi 30 Fitur

#### **A. Fitur Struktur URL (8 fitur)**

1. **`having_IP_Address`**
   - Cek apakah domain menggunakan IP address (misal: `192.168.1.1`)
   - Nilai: `-1` (tidak ada IP) atau `1` (ada IP)
   - **Indikator phishing**: IP address sebagai domain sangat mencurigakan

2. **`URL_Length`**
   - Panjang total URL
   - Nilai: `-1` (pendek <75), `0` (sedang), `1` (panjang >75)
   - **Indikator phishing**: URL panjang sering digunakan untuk menyembunyikan tujuan

3. **`Shortining_Service`**
   - Cek apakah menggunakan URL shortener
   - Service: `bit.ly`, `goo.gl`, `tinyurl`, dll
   - Nilai: `1` (ada) atau `-1` (tidak ada)
   - **Indikator phishing**: URL shortener menyembunyikan tujuan sebenarnya

4. **`having_At_Symbol`**
   - Cek apakah ada simbol `@` dalam URL
   - Nilai: `1` (ada) atau `-1` (tidak ada)
   - **Indikator phishing**: Simbol `@` sangat mencurigakan (biasanya untuk email)

5. **`double_slash_redirecting`**
   - Cek apakah ada double slash `//` setelah protocol
   - Nilai: `1` (ada) atau `-1` (tidak ada)
   - **Indikator phishing**: Bisa digunakan untuk redirect

6. **`Prefix_Suffix`**
   - Cek apakah ada dash `-` dalam hostname
   - Nilai: `1` (ada) atau `-1` (tidak ada)
   - **Indikator phishing**: Domain dengan dash sering mencurigakan

7. **`having_Sub_Domain`**
   - Hitung jumlah subdomain
   - Nilai: `1` (banyak subdomain) atau `0` (sedikit)
   - **Indikator phishing**: Banyak subdomain bisa mencurigakan

8. **`Request_URL`**
   - Cek apakah ada path dalam URL
   - Nilai: `1` (ada path) atau `-1` (tidak ada)
   - **Indikator phishing**: Path kompleks bisa mencurigakan

#### **B. Fitur Keamanan (3 fitur)**

9. **`SSLfinal_State`**
   - Cek apakah menggunakan HTTPS
   - Nilai: `1` (HTTPS) atau `-1` (HTTP)
   - **Indikator phishing**: HTTP tanpa SSL kurang aman

10. **`port`**
    - Cek apakah ada port number dalam URL
    - Nilai: `1` (ada port) atau `-1` (tidak ada)
    - **Indikator phishing**: Port non-standar bisa mencurigakan

11. **`HTTPS_token`**
    - Cek apakah ada kata "https" dalam hostname
    - Nilai: `1` (ada) atau `-1` (tidak ada)
    - **Indikator phishing**: Sangat mencurigakan jika ada "https" di hostname

#### **C. Fitur Domain (4 fitur)**

12. **`Domain_registeration_length`**
    - Panjang nama domain
    - Nilai: `1` (panjang >10) atau `-1` (pendek)
    - **Indikator phishing**: Domain panjang bisa mencurigakan

13. **`age_of_domain`**
    - Usia domain dalam hari (dari WHOIS)
    - Nilai: Numerik (hari)
    - **Indikator phishing**: Domain baru (<30 hari) sangat mencurigakan
    - **Cara cek**: Query WHOIS dengan timeout 5 detik

14. **`DNSRecord`**
    - Status DNS record
    - Nilai: `1` (valid) atau `-1` (tidak valid)
    - **Indikator phishing**: DNS tidak valid mencurigakan

15. **`is_typo_domain`**
    - Cek apakah domain mirip dengan domain populer (typo-squatting)
    - Membandingkan dengan: `google.com`, `facebook.com`, `apple.com`, dll
    - Menggunakan `SequenceMatcher` dengan threshold 0.8
    - Nilai: `1` (mirip) atau `0` (tidak mirip)
    - **Indikator phishing**: Typo domain sangat mencurigakan
    - **Contoh**: `kkinstagram.com` mirip dengan `instagram.com`

#### **D. Fitur Konten (5 fitur)**

16. **`Abnormal_URL`**
    - Cek apakah URL mengandung kata mencurigakan
    - Kata: `login`, `secure`, `verify`
    - Nilai: `1` (ada) atau `-1` (tidak ada)
    - **Indikator phishing**: Kata-kata ini sering digunakan phishing

17. **`Favicon`**
    - Status favicon (default: `1`)
    - Nilai: `1` (ada) atau `-1` (tidak ada)

18. **`URL_of_Anchor`**
    - Fitur anchor URL (default: `0`)
    - Nilai: `0` (default)

19. **`Links_in_tags`**
    - Jumlah link dalam tag HTML (default: `0`)
    - Nilai: `0` (default)

20. **`SFH`** (Server Form Handler)
    - Status form handler (default: `0`)
    - Nilai: `0` (default)

#### **E. Fitur JavaScript & HTML (4 fitur)**

21. **`on_mouseover`**
    - Fitur JavaScript onmouseover (default: `1`)
    - Nilai: `1` (default)

22. **`RightClick`**
    - Apakah right-click disabled (default: `1`)
    - Nilai: `1` (default)

23. **`popUpWidnow`**
    - Apakah ada popup window (default: `1`)
    - Nilai: `1` (default)

24. **`Iframe`**
    - Apakah ada iframe (default: `1`)
    - Nilai: `1` (default)

#### **F. Fitur Reputasi (6 fitur)**

25. **`web_traffic`**
    - Estimasi web traffic (default: `-1`)
    - Nilai: `-1` (default)

26. **`Page_Rank`**
    - Google PageRank (default: `-1`)
    - Nilai: `-1` (default)

27. **`Google_Index`**
    - Apakah terindeks di Google (default: `-1`)
    - Nilai: `-1` (default)

28. **`Links_pointing_to_page`**
    - Jumlah link yang mengarah ke halaman (default: `1`)
    - Nilai: `1` (default)

29. **`Statistical_report`**
    - Laporan statistik (default: `1`)
    - Nilai: `1` (default)

30. **`Redirect`**
    - Apakah ada redirect (default: `0`)
    - Nilai: `0` (default)

### 2.3 Contoh Ekstraksi Fitur

**Input URL:** `https://www.kkinstagram.com/reel/DKfBEo8xnhg/`

**Hasil Ekstraksi:**
```python
{
    'having_IP_Address': -1,        # Tidak ada IP
    'URL_Length': 1,                # URL panjang (>75 karakter)
    'Shortining_Service': -1,       # Tidak pakai shortener
    'having_At_Symbol': -1,         # Tidak ada @
    'double_slash_redirecting': -1,  # Tidak ada double slash
    'Prefix_Suffix': -1,            # Tidak ada dash
    'having_Sub_Domain': 1,         # Ada subdomain (www)
    'SSLfinal_State': 1,            # Menggunakan HTTPS
    'is_typo_domain': 1,            # MIRIP INSTAGRAM! (typo-squatting)
    'Abnormal_URL': -1,             # Tidak ada kata mencurigakan
    # ... dan 20 fitur lainnya
}
```

---

## 🔄 TAHAP 3: Konversi Fitur ke Format Model

Fitur yang sudah diekstrak dikonversi ke format yang sesuai dengan model ML:

```python
# Convert dictionary ke DataFrame
feature_df = pd.DataFrame([features])
# Shape: (1, 30) - 1 baris, 30 kolom
```

**Format yang dibutuhkan:**
- Semua fitur dalam bentuk numerik
- Urutan kolom sesuai dengan yang digunakan saat training
- Nilai: `-1`, `0`, atau `1` (kecuali fitur numerik seperti `age_of_domain`)

---

## 🤖 TAHAP 4: Prediksi dengan Machine Learning Model

### 4.1 Load Model
```python
@st.cache_resource
def load_phishing_model():
    with open('phishing_model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model
```

**Model yang digunakan:**
- **Algoritma**: Random Forest Classifier
- **n_estimators**: 100 pohon
- **Ukuran model**: ~13 MB

### 4.2 Prediksi
```python
# Predict class (1 = phishing, -1 = legitimate)
prediction = model.predict(feature_df)[0]

# Predict probability (confidence)
probability = model.predict_proba(feature_df)[0]
confidence = max(probability)
```

**Output:**
- `prediction`: `1` (phishing) atau `-1` (legitimate)
- `confidence`: Nilai 0.0 - 1.0 (tingkat kepercayaan)

**Contoh:**
- `prediction = 1`, `confidence = 0.86` → Phishing dengan confidence 86%
- `prediction = -1`, `confidence = 0.95` → Legitimate dengan confidence 95%

---

## 📊 TAHAP 5: Perhitungan Risk Score & Display Hasil

### 5.1 Cek User Report
Sistem mengecek apakah URL pernah dilaporkan user sebagai phishing:
```python
reported_urls = load_reported_urls()
is_reported = url_input.lower() in reported_urls

if is_reported:
    prediction = 1  # Langsung phishing
    confidence = 0.95
```

### 5.2 Hitung Risk Score
```python
if prediction == 1:  # Phishing
    risk_score = int(confidence * 100)
    # Contoh: confidence 0.86 → risk_score = 86
else:  # Legitimate
    risk_score = int((1 - confidence) * 20)
    # Contoh: confidence 0.95 → risk_score = 1
```

**Kategori Risk Score:**
- **0-20**: Aman (Legitimate)
- **21-40**: Rendah (Waspada)
- **41-60**: Sedang (Mencurigakan)
- **61-80**: Tinggi (PHISHING)
- **81-100**: Sangat Tinggi (PHISHING)

### 5.3 Display Hasil

**A. Hasil Utama:**
- Risk Score (0-100)
- Risk Level (Aman/Tinggi/Sangat Tinggi)
- Confidence (%)

**B. Analisis Detail:**
- Fitur URL (panjang, subdomain, dll)
- Indikator Keamanan (HTTPS, IP, dll)
- Hasil AI Model (PHISHING/LEGITIMATE)

**C. Rekomendasi:**
- Jika PHISHING: Jangan akses, jangan masukkan data
- Jika Waspada: Periksa domain dengan teliti
- Jika Aman: Tetap waspada saat memasukkan data

---

## 🔄 Contoh Lengkap Proses Analisa

### Input:
```
URL: https://www.kkinstagram.com/reel/DKfBEo8xnhg/
```

### Proses:

**1. Whitelist Check:**
- ❌ Tidak ada di whitelist → Lanjut

**2. Ekstraksi Fitur:**
- `having_IP_Address = -1` (tidak ada IP)
- `URL_Length = 1` (panjang)
- `SSLfinal_State = 1` (HTTPS)
- `is_typo_domain = 1` ⚠️ **MIRIP INSTAGRAM!**
- `Abnormal_URL = -1` (tidak ada kata mencurigakan)
- ... (30 fitur total)

**3. Konversi ke DataFrame:**
- Shape: (1, 30)

**4. Prediksi Model:**
- `prediction = 1` (PHISHING)
- `confidence = 0.86` (86%)

**5. Risk Score:**
- `risk_score = 86` (Sangat Tinggi)

### Output:
```
🔴 Skor Risiko: 86/100
🟠 Tinggi (PHISHING)
Confidence: 86.0%

⚠️ PERINGATAN TINGGI - PHISHING DETECTED
- JANGAN akses website ini
- JANGAN masukkan informasi pribadi
- Laporkan URL ini ke pihak berwenang
```

---

## 🛠️ Teknologi yang Digunakan

1. **URL Parsing**: `urllib.parse.urlparse()`
2. **Domain Extraction**: `tldextract`
3. **WHOIS Query**: `python-whois` (dengan timeout 5 detik)
4. **HTTP Request**: `requests` (untuk cek redirect, favicon)
5. **String Matching**: `difflib.SequenceMatcher` (typo detection)
6. **Machine Learning**: `scikit-learn RandomForestClassifier`
7. **Data Processing**: `pandas`

---

## ⚡ Optimasi & Error Handling

1. **Caching Model**: Model di-cache dengan `@st.cache_resource` untuk performa
2. **Timeout WHOIS**: 5 detik untuk menghindari hang
3. **Error Handling**: Jika ekstraksi gagal, return nilai default
4. **Whitelist First**: Cek whitelist dulu untuk performa lebih cepat
5. **User Report**: URL yang dilaporkan langsung dianggap phishing

---

## 📈 Akurasi Model

Berdasarkan testing:
- **Akurasi**: 96.7%
- **Precision**: 97% (phishing), 96% (legitimate)
- **Recall**: 95% (phishing), 98% (legitimate)
- **F1-Score**: 0.96-0.97

---

*Dokumentasi ini menjelaskan proses lengkap analisa URL dari input hingga output prediksi phishing.*
