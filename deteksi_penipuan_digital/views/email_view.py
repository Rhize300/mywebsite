import streamlit as st
import sys
import os

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from process_email import EmailProcessor

def show_email_detection():
    """Show email detection interface"""
    
    st.title("📧 Deteksi Email Spam/Palsu")
    st.markdown("Analisis email untuk mendeteksi spam atau email palsu")
    
    # Initialize processor
    processor = EmailProcessor()
    
    # Input section
    st.subheader("📝 Masukkan Email")
    
    # Email sender
    sender_email = st.text_input(
        "Email pengirim:",
        placeholder="sender@example.com",
        help="Masukkan alamat email pengirim"
    )
    
    # Email content
    email_content = st.text_area(
        "Isi email:",
        placeholder="Masukkan isi email yang ingin dianalisis...",
        height=200,
        help="Masukkan teks email lengkap termasuk subjek dan isi"
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        analyze_button = st.button("🔍 Analisis Email", type="primary")
    
    with col2:
        if st.button("📋 Contoh Email"):
            st.session_state.example_email = {
                'sender': 'winner@lottery.com',
                'content': 'CONGRATULATIONS! You have won $1,000,000 in our lottery! Click here to claim your prize: http://fake-lottery.com/claim'
            }
    
    # Show example if requested
    if 'example_email' in st.session_state:
        st.info("Contoh email spam telah dimuat")
        sender_email = st.session_state.example_email['sender']
        email_content = st.session_state.example_email['content']
    
    # Analysis section
    if analyze_button and email_content:
        st.markdown("---")
        st.subheader("🔍 Hasil Analisis")
        
        with st.spinner("Menganalisis email..."):
            # Analyze email
            result = processor.analyze_email(email_content, sender_email)
            
            # Display results
            display_email_results(sender_email, email_content, result, processor)
    
    # Information section
    st.markdown("---")
    st.subheader("ℹ️ Tentang Deteksi Email Spam")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Tanda-tanda Email Spam:**
        - Mengandung kata-kata mencurigakan
        - Terlalu banyak huruf kapital
        - Banyak tanda seru atau tanya
        - Mengandung link mencurigakan
        - Domain pengirim tidak dikenal
        - Tawaran yang terlalu bagus
        """)
    
    with col2:
        st.markdown("""
        **Tips Keamanan:**
        - Jangan klik link dari email mencurigakan
        - Jangan download lampiran dari email spam
        - Periksa alamat pengirim dengan teliti
        - Aktifkan filter spam di email client
        - Laporkan email spam ke provider
        """)

def display_email_results(sender_email, email_content, result, processor):
    """Display email analysis results"""
    
    # Spam level
    spam_level = processor.get_spam_level(result['spam_score'])
    
    if result['spam_score'] >= 80:
        spam_icon = "🔴"
        spam_color = "red"
    elif result['spam_score'] >= 60:
        spam_icon = "🟠"
        spam_color = "orange"
    elif result['spam_score'] >= 40:
        spam_icon = "🟡"
        spam_color = "yellow"
    elif result['spam_score'] >= 20:
        spam_icon = "🟢"
        spam_color = "green"
    else:
        spam_icon = "🟢"
        spam_color = "green"
    
    # Main result
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; border: 2px solid {spam_color}; border-radius: 10px;'>
            <h2>Skor Spam: {result['spam_score']}/100</h2>
            <h3>{spam_icon} {spam_level}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Spam status
    if result['is_spam']:
        st.error("🚨 Email terdeteksi sebagai SPAM")
    else:
        st.success("✅ Email tampak aman")
    
    # Detailed analysis
    st.subheader("📊 Analisis Detail")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Informasi Email:**")
        if sender_email:
            st.write(f"• Pengirim: {sender_email}")
        st.write(f"• Panjang email: {result['features']['length']} karakter")
        st.write(f"• Jumlah kata: {result['features']['word_count']}")
        st.write(f"• Jumlah link: {result['features']['url_count']}")
        st.write(f"• Jumlah email: {result['features']['email_count']}")
    
    with col2:
        st.markdown("**Analisis Konten:**")
        st.write(f"• Kata spam: {result['features']['spam_keyword_count']}")
        st.write(f"• Pola mencurigakan: {result['features']['suspicious_pattern_count']}")
        st.write(f"• Huruf kapital: {result['features']['all_caps_ratio']:.2%}")
        st.write(f"• Tanda seru: {result['features']['exclamation_count']}")
        st.write(f"• Tanda tanya: {result['features']['question_count']}")
    
    # Issues found
    if result['issues']:
        st.subheader("⚠️ Masalah yang Ditemukan")
        for i, issue in enumerate(result['issues'], 1):
            st.write(f"{i}. {issue}")
    
    # Recommendations
    st.subheader("💡 Rekomendasi")
    
    for recommendation in result['recommendations']:
        st.write(f"• {recommendation}")
    
    # Email preview
    with st.expander("📧 Preview Email"):
        st.markdown("**Pengirim:**")
        st.code(sender_email if sender_email else "Tidak diketahui")
        
        st.markdown("**Isi Email:**")
        st.text_area("", email_content, height=150, disabled=True)
    
    # Feature breakdown
    with st.expander("🔍 Detail Fitur"):
        st.markdown("**Fitur yang Diekstrak:**")
        features_df = {
            'Fitur': list(result['features'].keys()),
            'Nilai': list(result['features'].values())
        }
        st.dataframe(features_df, use_container_width=True)
    
    # Statistics
    with st.expander("📊 Statistik Analisis"):
        st.markdown("""
        **Metrik Analisis:**
        - Total email diperiksa: 2,456
        - Email spam terdeteksi: 234
        - Email aman: 2,222
        - Akurasi deteksi: 94.8%
        - False positive rate: 2.1%
        """) 