# Model Directory

Direktori ini berisi model machine learning yang telah dilatih untuk deteksi penipuan digital.

## File Model

- `phishing_model.pkl` - Model untuk deteksi phishing URL
- `email_model.pkl` - Model untuk deteksi email spam
- `apk_model.pkl` - Model untuk deteksi APK berbahaya
- `hp_model.pkl` - Model untuk deteksi nomor HP penipuan (opsional)

## Cara Training Model

1. Buka notebook di folder `notebook/`
2. Jalankan training sesuai dengan jenis model
3. Export model ke format `.pkl`
4. Simpan di folder ini

## Format Model

Semua model menggunakan format pickle (.pkl) dan dapat dimuat dengan:

```python
import pickle

with open('model/phishing_model.pkl', 'rb') as f:
    model = pickle.load(f)
```

## Versi Model

- Phishing Model: v1.0 (Random Forest)
- Email Model: v1.0 (Naive Bayes)
- APK Model: v1.0 (Random Forest)
- HP Model: v1.0 (Rule-based) 