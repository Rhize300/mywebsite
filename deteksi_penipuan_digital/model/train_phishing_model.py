import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os
import sys
# Tambahkan path absolut ke utils agar url_features bisa diimpor
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
from url_features import is_typo_domain

# Path dataset dan model
DATA_PATH = 'data/phishing_dataset.csv'
MODEL_PATH = 'phishing_model.pkl'

# Baca dataset
print('Membaca dataset...')
df = pd.read_csv(DATA_PATH)
print('Jumlah data:', len(df))

# Tambahkan fitur is_typo_domain
print('Menambahkan fitur is_typo_domain...')
if 'is_typo_domain' not in df.columns:
    # Asumsi domain ada di kolom 'index', 'Result', sisanya fitur
    # Kita ekstrak domain dari URL jika ada kolom URL, jika tidak, dari fitur domain
    if 'url' in df.columns:
        import tldextract
        df['is_typo_domain'] = df['url'].apply(lambda x: is_typo_domain(tldextract.extract(x).domain))
    elif 'having_IPhaving_IP_Address' in df.columns:
        # Asumsi domain ada di kolom index, tidak ada kolom url, skip (atau bisa diisi 0)
        df['is_typo_domain'] = 0
    else:
        df['is_typo_domain'] = 0

# Pisahkan fitur dan label
y = df['Result']
X = df.drop(['index', 'Result'], axis=1)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Training model
print('Training Random Forest...')
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluasi
y_pred = model.predict(X_test)
print('Akurasi:', accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Simpan model
with open(MODEL_PATH, 'wb') as f:
    pickle.dump(model, f)
print(f'Model disimpan ke {MODEL_PATH}') 