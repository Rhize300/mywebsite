# Notebook Directory

Direktori ini berisi notebook Jupyter/Colab untuk training model machine learning.

## File Notebook

- `train_phishing_url.ipynb` - Training model deteksi phishing URL
- `train_email.ipynb` - Training model deteksi email spam
- `train_apk.ipynb` - Training model deteksi APK berbahaya
- `train_hp_model.ipynb` - Training model deteksi nomor HP (opsional)

## Cara Penggunaan

1. Upload notebook ke Google Colab
2. Mount Google Drive untuk akses dataset
3. Install dependencies yang diperlukan
4. Jalankan semua cell secara berurutan
5. Download model hasil training
6. Simpan model di folder `model/`

## Dependencies

```python
!pip install pandas numpy scikit-learn matplotlib seaborn
!pip install requests beautifulsoup4 whois dnspython
!pip install tldextract email-validator
```

## Workflow Training

1. **Data Loading** - Load dataset dari folder `data/`
2. **Data Preprocessing** - Clean dan prepare data
3. **Feature Engineering** - Ekstraksi fitur sesuai kebutuhan
4. **Model Training** - Train model dengan algoritma yang dipilih
5. **Model Evaluation** - Evaluasi performa model
6. **Model Export** - Save model ke format pickle

## Model Performance

Target performa untuk setiap model:
- Phishing URL: Accuracy > 95%, F1-score > 0.94
- Email Spam: Accuracy > 94%, F1-score > 0.93
- APK Malware: Accuracy > 96%, F1-score > 0.95
- Phone Number: Accuracy > 90%, F1-score > 0.89

## Tips Training

- Gunakan cross-validation untuk evaluasi yang lebih robust
- Tune hyperparameters dengan GridSearchCV
- Handle class imbalance dengan SMOTE atau class_weight
- Save model dengan timestamp untuk versioning
- Dokumentasikan hasil training dan parameter yang digunakan 