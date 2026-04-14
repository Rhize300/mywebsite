# Struktur Dataset Phishing — Untuk Capturan / Dokumentasi

Dokumen ini merangkum **kolom dan nilai** yang perlu ditampilkan untuk capturan dataset `phishing_dataset.csv`.

---

## Kolom yang Ditampilkan (32 kolom)

| No | Nama Kolom | Nilai | Keterangan |
|----|------------|-------|------------|
| 1 | **index** | 0, 1, 2, ... | Nomor urut baris |
| 2 | having_IP_Address | -1 / 1 | -1 = bukan IP, 1 = domain berupa IP |
| 3 | URL_Length | 0 / 1 | 1 = panjang URL > 75 |
| 4 | Shortining_Service | -1 / 1 | 1 = pakai shortener (bit.ly, goo.gl, tinyurl) |
| 5 | having_At_Symbol | -1 / 1 | 1 = ada @ di URL |
| 6 | double_slash_redirecting | -1 / 1 | 1 = ada // setelah scheme |
| 7 | Prefix_Suffix | -1 / 1 | 1 = ada tanda - di hostname |
| 8 | having_Sub_Domain | -1 / 0 / 1 | subdomain (0/1) |
| 9 | SSLfinal_State | -1 / 1 | 1 = HTTPS |
| 10 | Domain_registeration_length | -1 / 1 | 1 = panjang hostname > 10 |
| 11 | Favicon | -1 / 1 | 1 = ada (default) |
| 12 | port | -1 / 1 | 1 = ada port di URL |
| 13 | HTTPS_token | -1 / 1 | 1 = kata "https" di hostname |
| 14 | Request_URL | -1 / 1 | 1 = ada path |
| 15 | URL_of_Anchor | -1 / 0 / 1 | default 0 |
| 16 | Links_in_tags | -1 / 0 / 1 | default 0 |
| 17 | SFH | -1 / 0 / 1 | default 0 |
| 18 | Submitting_to_email | -1 / 1 | -1 = tidak submit ke email |
| 19 | Abnormal_URL | -1 / 1 | 1 = ada kata login/secure/verify di URL |
| 20 | Redirect | -1 / 0 / 1 | default 0 |
| 21 | on_mouseover | -1 / 1 | default 1 |
| 22 | RightClick | -1 / 1 | default 1 |
| 23 | popUpWidnow | -1 / 1 | default 1 |
| 24 | Iframe | -1 / 1 | default 1 |
| 25 | age_of_domain | -1 / 1 | default 1 |
| 26 | DNSRecord | -1 / 1 | default 1 |
| 27 | web_traffic | -1 / 1 | default -1 |
| 28 | Page_Rank | -1 / 1 | default -1 |
| 29 | Google_Index | -1 / 1 | default -1 |
| 30 | Links_pointing_to_page | -1 / 1 | default 1 |
| 31 | Statistical_report | -1 / 1 | default 1 |
| 32 | **Result** | **-1 / 1** | **-1 = Legitimate, 1 = Phishing** |

*Catatan: Saat training, fitur **is_typo_domain** (domain mirip brand populer) ditambahkan oleh script, jadi model memakai **31 fitur** (tanpa index) + Result.*

---

## Contoh Baris (untuk capturan)

```text
index,having_IP_Address,URL_Length,Shortining_Service,having_At_Symbol,double_slash_redirecting,Prefix_Suffix,having_Sub_Domain,SSLfinal_State,Domain_registeration_length,Favicon,port,HTTPS_token,Request_URL,URL_of_Anchor,Links_in_tags,SFH,Submitting_to_email,Abnormal_URL,Redirect,on_mouseover,RightClick,popUpWidnow,Iframe,age_of_domain,DNSRecord,web_traffic,Page_Rank,Google_Index,Links_pointing_to_page,Statistical_report,Result
0,-1,1,1,1,-1,-1,-1,-1,-1,1,1,-1,1,-1,1,-1,-1,-1,0,1,1,1,1,-1,-1,-1,-1,1,1,-1,-1
1,1,1,1,1,1,-1,0,1,-1,1,1,-1,1,0,-1,-1,1,1,0,1,1,1,1,-1,-1,0,-1,1,1,1,-1
```

---

## Ringkasan untuk Capturan

- **Total kolom:** 32 (index + 30 fitur + Result).
- **Label:** `Result` → **-1** = Legitimate, **1** = Phishing.
- **Nilai fitur:** umumnya **-1**, **0**, atau **1** (tergantung definisi tiap fitur).
- **Jumlah baris:** sesuai banyaknya sampel (mis. 22.116 di `phishing_dataset.csv`).

Gunakan tabel dan contoh di atas untuk screenshot atau lampiran dokumentasi dataset.
