import streamlit as st
import pandas as pd
import sys
import os
import json
import pickle
import numpy as np

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from url_features import extract_url_features

REPORT_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'reported_phishing_urls.json')
MODEL_FILE = os.path.join(os.path.dirname(__file__), '..', 'phishing_model.pkl')

# Load model
@st.cache_resource
def load_phishing_model():
    """Load the trained phishing detection model"""
    try:
        with open(MODEL_FILE, 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Fungsi bantu untuk baca/tulis report

def load_reported_urls():
    try:
        if not os.path.exists(REPORT_FILE) or os.path.getsize(REPORT_FILE) == 0:
            # Jika file tidak ada atau kosong, inisialisasi dengan list kosong
            with open(REPORT_FILE, 'w') as f:
                json.dump([], f)
            return set()
        with open(REPORT_FILE, 'r') as f:
            data = json.load(f)
            return set([u.lower() for u in data if isinstance(u, str)])
    except Exception:
        return set()

def save_reported_url(url):
    urls = load_reported_urls()
    urls.add(url.lower())
    with open(REPORT_FILE, 'w') as f:
        json.dump(list(urls), f)

def extract_model_features(url):
    """Extract features compatible with the trained model"""
    try:
        from urllib.parse import urlparse
        import tldextract
        
        parsed = urlparse(url)
        extracted = tldextract.extract(url)
        
        # Fungsi untuk cek typo domain
        def is_typo_domain(domain, threshold=0.8):
            """Cek apakah domain mirip dengan domain populer (typo-squatting)"""
            from difflib import SequenceMatcher
            popular_domains = [
                'microsoft.com', 'google.com', 'facebook.com', 'apple.com', 'amazon.com',
                'paypal.com', 'ebay.com', 'yahoo.com', 'instagram.com', 'twitter.com',
                'linkedin.com', 'netflix.com', 'whatsapp.com', 'telegram.org', 'bankofamerica.com',
                'wellsfargo.com', 'chase.com', 'gmail.com', 'outlook.com', 'icloud.com'
            ]
            domain = domain.lower()
            for popular in popular_domains:
                base = popular.split('.')[0]
                ratio = SequenceMatcher(None, domain, base).ratio()
                if ratio >= threshold and domain != base:
                    return 1
            return 0
        
        features = {
            'having_IP_Address': -1 if parsed.hostname.replace('.', '').isdigit() else 1,
            'URL_Length': 1 if len(url) > 75 else 0,
            'Shortining_Service': 1 if any(service in url for service in ['bit.ly', 'goo.gl', 'tinyurl']) else -1,
            'having_At_Symbol': 1 if '@' in url else -1,
            'double_slash_redirecting': 1 if '//' in url[8:] else -1,
            'Prefix_Suffix': 1 if '-' in parsed.hostname else -1,
            'having_Sub_Domain': 1 if len(parsed.hostname.split('.')) > 2 and not parsed.hostname.startswith('www.') else 0,
            'SSLfinal_State': 1 if parsed.scheme == 'https' else -1,
            'Domain_registeration_length': 1 if len(parsed.hostname) > 10 else -1,
            'Favicon': 1,  # Default value
            'port': 1 if parsed.port else -1,
            'HTTPS_token': 1 if 'https' in parsed.hostname else -1,
            'Request_URL': 1 if len(parsed.path) > 0 else -1,
            'URL_of_Anchor': 0,  # Default value
            'Links_in_tags': 0,  # Default value
            'SFH': 0,  # Default value
            'Submitting_to_email': -1,  # Default value
            'Abnormal_URL': 1 if any(suspicious in url for suspicious in ['login', 'secure', 'verify']) else -1,
            'Redirect': 0,  # Default value
            'on_mouseover': 1,  # Default value
            'RightClick': 1,  # Default value
            'popUpWidnow': 1,  # Default value
            'Iframe': 1,  # Default value
            'age_of_domain': 1,  # Default value
            'DNSRecord': 1,  # Default value
            'web_traffic': -1,  # Default value
            'Page_Rank': -1,  # Default value
            'Google_Index': -1,  # Default value
            'Links_pointing_to_page': 1,  # Default value
            'Statistical_report': 1,  # Default value
            'is_typo_domain': is_typo_domain(extracted.domain)  # Tambahkan fitur yang hilang
        }
        
        return features
    except Exception as e:
        st.error(f"Error extracting features: {e}")
        return None

def predict_phishing_with_model(url):
    """Predict phishing using the trained model"""
    # Whitelist untuk domain legitimate terkenal
    legitimate_domains = [
        'youtube.com', 'www.youtube.com',
        'google.com', 'www.google.com',
        'facebook.com', 'www.facebook.com',
        'github.com', 'www.github.com',
        'stackoverflow.com', 'www.stackoverflow.com',
        'reddit.com', 'www.reddit.com',
        'twitter.com', 'www.twitter.com',
        'instagram.com', 'www.instagram.com',
        'linkedin.com', 'www.linkedin.com',
        'netflix.com', 'www.netflix.com',
        'amazon.com', 'www.amazon.com',
        'microsoft.com', 'www.microsoft.com',
        'apple.com', 'www.apple.com',
        'wikipedia.org', 'www.wikipedia.org',
        'mozilla.org', 'www.mozilla.org',
        'ubuntu.com', 'www.ubuntu.com',
        'python.org', 'www.python.org',
        'nodejs.org', 'www.nodejs.org',
        'docker.com', 'www.docker.com',
        'kubernetes.io', 'www.kubernetes.io',
        'jenkins.io', 'www.jenkins.io',
        'gitlab.com', 'www.gitlab.com',
        'bitbucket.org', 'www.bitbucket.org',
        'slack.com', 'www.slack.com',
        'discord.com', 'www.discord.com',
        'zoom.us', 'www.zoom.us',
        'teams.microsoft.com', 'www.teams.microsoft.com',
        'dropbox.com', 'www.dropbox.com',
        'drive.google.com', 'www.drive.google.com',
        'gmail.com', 'www.gmail.com',
        'outlook.com', 'www.outlook.com',
        'yahoo.com', 'www.yahoo.com',
        'bing.com', 'www.bing.com',
        'duckduckgo.com', 'www.duckduckgo.com',
        'brave.com', 'www.brave.com',
        'opera.com', 'www.opera.com',
        'firefox.com', 'www.firefox.com',
        'chrome.com', 'www.chrome.com',
        'edge.com', 'www.edge.com',
        'safari.com', 'www.safari.com'
    ]
    
    # Whitelist untuk domain pendidikan Indonesia
    education_domains = [
        # Universitas Indonesia
        'ui.ac.id', 'www.ui.ac.id',
        'gunadarma.ac.id', 'www.gunadarma.ac.id', 'library.gunadarma.ac.id',
        'itb.ac.id', 'www.itb.ac.id',
        'ugm.ac.id', 'www.ugm.ac.id',
        'unair.ac.id', 'www.unair.ac.id',
        'undip.ac.id', 'www.undip.ac.id',
        'unpad.ac.id', 'www.unpad.ac.id',
        'ipb.ac.id', 'www.ipb.ac.id',
        'unbraw.ac.id', 'www.unbraw.ac.id',
        'unhas.ac.id', 'www.unhas.ac.id',
        'uns.ac.id', 'www.uns.ac.id',
        'unsoed.ac.id', 'www.unsoed.ac.id',
        'unnes.ac.id', 'www.unnes.ac.id',
        'unm.ac.id', 'www.unm.ac.id',
        'unand.ac.id', 'www.unand.ac.id',
        'unsri.ac.id', 'www.unsri.ac.id',
        'unila.ac.id', 'www.unla.ac.id',
        'unmul.ac.id', 'www.unmul.ac.id',
        'untan.ac.id', 'www.untan.ac.id',
        'unud.ac.id', 'www.unud.ac.id',
        'unram.ac.id', 'www.unram.ac.id',
        'unhalu.ac.id', 'www.unhalu.ac.id',
        'untad.ac.id', 'www.untad.ac.id',
        'unima.ac.id', 'www.unima.ac.id',
        'unpatti.ac.id', 'www.unpatti.ac.id',
        'unipa.ac.id', 'www.unipa.ac.id',
        'unmus.ac.id', 'www.unmus.ac.id',
        'unp.ac.id', 'www.unp.ac.id',
        'unand.ac.id', 'www.unand.ac.id',
        'unsri.ac.id', 'www.unsri.ac.id',
        'unila.ac.id', 'www.unila.ac.id',
        'unmul.ac.id', 'www.unmul.ac.id',
        'untan.ac.id', 'www.untan.ac.id',
        'unud.ac.id', 'www.unud.ac.id',
        'unram.ac.id', 'www.unram.ac.id',
        'unhalu.ac.id', 'www.unhalu.ac.id',
        'untad.ac.id', 'www.untad.ac.id',
        'unima.ac.id', 'www.unima.ac.id',
        'unpatti.ac.id', 'www.unpatti.ac.id',
        'unipa.ac.id', 'www.unipa.ac.id',
        'unmus.ac.id', 'www.unmus.ac.id',
        'unp.ac.id', 'www.unp.ac.id',
        # Institut
        'its.ac.id', 'www.its.ac.id',
        'ipb.ac.id', 'www.ipb.ac.id',
        'isi.ac.id', 'www.isi.ac.id',
        'ipdn.ac.id', 'www.ipdn.ac.id',
        # Politeknik
        'polban.ac.id', 'www.polban.ac.id',
        'poltek.ac.id', 'www.poltek.ac.id',
        'polinema.ac.id', 'www.polinema.ac.id',
        'polman.ac.id', 'www.polman.ac.id',
        'polines.ac.id', 'www.polines.ac.id',
        'poltekkes.ac.id', 'www.poltekkes.ac.id',
        # Sekolah Tinggi
        'stis.ac.id', 'www.stis.ac.id',
        'stmik.ac.id', 'www.stmik.ac.id',
        'stikom.ac.id', 'www.stikom.ac.id',
        'stie.ac.id', 'www.stie.ac.id',
        'stkip.ac.id', 'www.stkip.ac.id',
        # Domain pendidikan umum
        'ac.id', 'www.ac.id',
        'sch.id', 'www.sch.id',
        'go.id', 'www.go.id'
    ]
    
    # Gabungkan semua whitelist
    all_legitimate_domains = legitimate_domains + education_domains
    
    # Cek apakah domain ada di whitelist
    from urllib.parse import urlparse
    parsed = urlparse(url)
    domain = parsed.hostname.lower()
    
    if domain in all_legitimate_domains:
        return 0, 0.95  # Legitimate dengan confidence tinggi
    
    model = load_phishing_model()
    if model is None:
        return None, 0.0
    
    features = extract_model_features(url)
    if features is None:
        return None, 0.0
    
    try:
        # Convert to DataFrame
        feature_df = pd.DataFrame([features])
        
        # Predict
        prediction = model.predict(feature_df)[0]
        probability = model.predict_proba(feature_df)[0]
        
        return prediction, max(probability)
    except Exception as e:
        st.error(f"Error predicting: {e}")
        return None, 0.0

def show_phishing_detection():
    """Show phishing URL detection interface"""
    
    st.title("🔗 Deteksi Phishing URL")
    st.markdown("Analisis URL untuk mendeteksi website phishing yang mencurigakan")
    
    # Input section
    st.subheader("📝 Masukkan URL")
    
    url_input = st.text_input(
        "URL yang ingin diperiksa:",
        placeholder="https://example.com",
        help="Masukkan URL lengkap termasuk http:// atau https://"
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        analyze_button = st.button("🔍 Analisis URL", type="primary")
    
    with col2:
        if st.button("📋 Contoh URL"):
            st.session_state.example_url = "https://www.kkinstagram.com/reel/DKfBEo8xnhg/"
    
    # Show example if requested
    if 'example_url' in st.session_state:
        st.info(f"Contoh URL: {st.session_state.example_url}")
        url_input = st.session_state.example_url
    
    # Analysis section
    if analyze_button and url_input:
        st.markdown("---")
        st.subheader("🔍 Hasil Analisis")
        
        with st.spinner("Menganalisis URL dengan AI..."):
            # Use ML model for prediction
            prediction, confidence = predict_phishing_with_model(url_input)
            
            # Extract features for display
            features = extract_url_features(url_input)
            
            # Override: jika ada di report, langsung berbahaya
            reported_urls = load_reported_urls()
            is_reported = url_input.lower() in reported_urls
            
            if is_reported:
                prediction = 1
                confidence = 0.95
            
            # Calculate risk score based on ML prediction
            if prediction == 1:  # Phishing
                risk_score = int(confidence * 100)
            else:  # Legitimate
                risk_score = int((1 - confidence) * 20)  # Low risk for legitimate
            
            # Display results
            display_phishing_results(url_input, features, risk_score, is_reported, prediction, confidence)
            
            # Tombol report
            if not is_reported and prediction == 0:
                if st.button('Laporkan Salah Deteksi (URL ini Phishing!)'):
                    save_reported_url(url_input)
                    st.success('URL berhasil dilaporkan sebagai phishing. Jika dicek lagi, akan selalu dianggap berbahaya.')
                    st.experimental_rerun()
    
    # Information section
    st.markdown("---")
    st.subheader("ℹ️ Tentang Phishing URL")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Tanda-tanda URL Phishing:**
        - Domain yang mirip dengan website asli
        - Menggunakan IP address sebagai domain
        - Terlalu banyak subdomain
        - Mengandung kata-kata mencurigakan
        - Tidak menggunakan HTTPS
        - Domain baru (usia < 30 hari)
        """)
    
    with col2:
        st.markdown("""
        **Tips Keamanan:**
        - Selalu periksa domain dengan teliti
        - Jangan klik link dari email mencurigakan
        - Gunakan bookmark untuk website penting
        - Aktifkan two-factor authentication
        - Update browser secara berkala
        """)

def display_phishing_results(url, features, risk_score, is_reported=False, prediction=None, confidence=None):
    """Display phishing analysis results"""
    
    # Risk level based on ML prediction
    if prediction == 1:  # Phishing detected
        if confidence >= 0.9:
            risk_level = "🔴 Sangat Tinggi (PHISHING)"
            risk_color = "red"
        elif confidence >= 0.7:
            risk_level = "🟠 Tinggi (PHISHING)"
            risk_color = "orange"
        else:
            risk_level = "🟡 Sedang (PHISHING)"
            risk_color = "yellow"
    else:  # Legitimate
        if confidence >= 0.9:
            risk_level = "🟢 Aman (LEGITIMATE)"
            risk_color = "green"
        else:
            risk_level = "🟡 Sedang (LEGITIMATE)"
            risk_color = "yellow"
    
    # Main result
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; border: 2px solid {risk_color}; border-radius: 10px;'>
            <h2>Skor Risiko: {risk_score}/100</h2>
            <h3>{risk_level}</h3>
            <p>Confidence: {confidence*100:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed analysis
    st.subheader("📊 Analisis Detail")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Fitur URL:**")
        st.write(f"• Panjang URL: {features['url_length']} karakter")
        st.write(f"• Panjang domain: {features['domain_length']} karakter")
        st.write(f"• Jumlah subdomain: {features['subdomain_count']}")
        st.write(f"• Kedalaman URL: {features['url_depth']}")
        st.write(f"• Usia domain: {features['domain_age']} hari")
    
    with col2:
        st.markdown("**Indikator Keamanan:**")
        st.write(f"• HTTPS: {'✅ Ya' if features['https_used'] else '❌ Tidak'}")
        st.write(f"• IP dalam domain: {'❌ Ya' if features['ip_in_domain'] else '✅ Tidak'}")
        st.write(f"• Kata mencurigakan: {features['suspicious_words']}")
        st.write(f"• Karakter khusus: {features['special_chars']}")
        st.write(f"• Redirect: {features['redirect_count']}")
    
    # ML Model Info
    st.subheader("🤖 Hasil AI Model")
    if prediction == 1:
        st.error(f"**PHISHING DETECTED** - Model AI mendeteksi URL ini sebagai phishing dengan confidence {confidence*100:.1f}%")
    else:
        st.success(f"**LEGITIMATE** - Model AI mengklasifikasikan URL ini sebagai aman dengan confidence {confidence*100:.1f}%")
    
    # Recommendations
    st.subheader("💡 Rekomendasi")
    
    if prediction == 1:  # Phishing
        st.error("⚠️ **PERINGATAN TINGGI - PHISHING DETECTED**")
        st.markdown("""
        - **JANGAN** akses website ini
        - **JANGAN** masukkan informasi pribadi
        - **JANGAN** download file dari website ini
        - Laporkan URL ini ke pihak berwenang
        - Hapus bookmark jika ada
        """)
    elif risk_score >= 40:
        st.warning("⚠️ **WASPADA**")
        st.markdown("""
        - Periksa domain dengan teliti
        - Jangan masukkan data sensitif
        - Gunakan mode incognito jika harus akses
        - Verifikasi dengan sumber terpercaya
        """)
    else:
        st.success("✅ **AMAN**")
        st.markdown("""
        - Website ini tampak aman
        - Tetap waspada saat memasukkan data
        - Pastikan menggunakan HTTPS
        - Verifikasi domain sebelum login
        """)
    
    # Feature breakdown
    with st.expander("🔍 Detail Fitur"):
        st.dataframe(pd.DataFrame([features]).T, use_container_width=True)
    
    if is_reported:
        st.warning('URL ini sudah pernah dilaporkan sebagai phishing oleh pengguna.')
    
    # Statistik chart (bar chart)
    st.subheader('📈 Statistik Deteksi')
    stats_keys = ['Aman', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi']
    # Simpan statistik ke session
    if 'phishing_stats' not in st.session_state:
        st.session_state['phishing_stats'] = {k: 0 for k in stats_keys}
    # Update statistik
    if prediction == 1 and confidence >= 0.9:
        st.session_state['phishing_stats']['Sangat Tinggi'] += 1
    elif prediction == 1 and confidence >= 0.7:
        st.session_state['phishing_stats']['Tinggi'] += 1
    elif prediction == 1:
        st.session_state['phishing_stats']['Sedang'] += 1
    elif prediction == 0 and confidence < 0.8:
        st.session_state['phishing_stats']['Rendah'] += 1
    else:
        st.session_state['phishing_stats']['Aman'] += 1
    # Pastikan semua kategori ada dan bertipe int
    stats_df = pd.DataFrame({
        'Kategori': stats_keys,
        'Jumlah': [int(st.session_state['phishing_stats'].get(k, 0)) for k in stats_keys]
    })
    stats_df.set_index('Kategori', inplace=True)
    st.bar_chart(stats_df) 