# Data Directory

Direktori ini berisi dataset untuk training dan testing model deteksi penipuan digital.

## File Dataset

- `phishing_dataset.csv` - Dataset URL phishing dan legitimate
- `email_spam.csv` - Dataset email spam dan ham
- `apk_berbahaya.csv` - Dataset APK malware dan benign
- `nomor_hp_penipuan.csv` - Dataset nomor HP penipuan (opsional)

## Format Dataset

### Phishing Dataset
```csv
url,label,features...
https://example.com,0,feature1,feature2,...
https://fake-bank.com,1,feature1,feature2,...
```

### Email Dataset
```csv
content,label,sender
"Email content here",0,sender@example.com
"Spam content here",1,spam@fake.com
```

### APK Dataset
```csv
package_name,label,permissions,features...
com.example.app,0,perm1;perm2,feature1,feature2,...
com.malware.app,1,perm1;perm2,feature1,feature2,...
```

## Sumber Dataset

- Phishing URLs: PhishTank, OpenPhish
- Email Spam: SpamAssassin, Enron Dataset
- APK Malware: VirusTotal, AndroZoo
- Phone Numbers: User reports, Operator data

## Preprocessing

Dataset telah dipreprocessing dan siap untuk training model. Fitur-fitur telah diekstraksi sesuai dengan kebutuhan masing-masing model.

## Update Dataset

Dataset dapat diperbarui secara berkala untuk meningkatkan akurasi model. Pastikan untuk:

1. Backup dataset lama
2. Validasi data baru
3. Retrain model dengan dataset yang diperbarui
4. Test performa model baru 