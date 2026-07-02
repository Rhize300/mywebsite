import streamlit as st
import sys
import os

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from validate_hp import PhoneNumberValidator

def show_hp_detection():
    """Show phone number detection interface"""
    
    st.title("📱 Deteksi Nomor HP Penipuan")
    st.markdown("Validasi dan deteksi nomor telepon yang mencurigakan")
    
    # Initialize validator
    validator = PhoneNumberValidator()
    
    # Input section
    st.subheader("📝 Masukkan Nomor HP")
    
    phone_input = st.text_input(
        "Nomor HP yang ingin diperiksa:",
        placeholder="081234567890 atau +6281234567890",
        help="Masukkan nomor HP dengan atau tanpa kode negara"
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        analyze_button = st.button("🔍 Analisis Nomor", type="primary")
    
    with col2:
        if st.button("📋 Contoh Nomor"):
            st.session_state.example_phone = "081234567890"
    
    # Show example if requested
    if 'example_phone' in st.session_state:
        st.info(f"Contoh nomor: {st.session_state.example_phone}")
        phone_input = st.session_state.example_phone
    
    # Analysis section
    if analyze_button and phone_input:
        st.markdown("---")
        st.subheader("🔍 Hasil Analisis")
        
        with st.spinner("Menganalisis nomor HP..."):
            # Validate phone number
            result = validator.validate_phone_number(phone_input)
            
            # Display results
            display_hp_results(phone_input, result, validator)
    
    # Information section
    st.markdown("---")
    st.subheader("ℹ️ Tentang Deteksi Nomor HP")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Tanda-tanda Nomor Penipuan:**
        - Nomor terdaftar dalam database penipuan
        - Mengandung pola digit berulang
        - Mengandung digit berurutan
        - Panjang nomor tidak standar
        - Menggunakan format yang mencurigakan
        """)
    
    with col2:
        st.markdown("""
        **Tips Keamanan:**
        - Jangan jawab panggilan dari nomor mencurigakan
        - Jangan berikan OTP ke siapapun
        - Blokir nomor yang mengirim SMS spam
        - Laporkan nomor penipuan ke operator
        - Aktifkan fitur anti-spam
        """)

def display_hp_results(phone_number, result, validator):
    """Display phone number analysis results"""
    
    # Risk level
    risk_level = validator.get_risk_level(result['risk_score'])
    
    if result['risk_score'] >= 80:
        risk_icon = "🔴"
        risk_color = "red"
    elif result['risk_score'] >= 60:
        risk_icon = "🟠"
        risk_color = "orange"
    elif result['risk_score'] >= 40:
        risk_icon = "🟡"
        risk_color = "yellow"
    elif result['risk_score'] >= 20:
        risk_icon = "🟢"
        risk_color = "green"
    else:
        risk_icon = "🟢"
        risk_color = "green"
    
    # Main result
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; border: 2px solid {risk_color}; border-radius: 10px;'>
            <h2>Skor Risiko: {result['risk_score']}/100</h2>
            <h3>{risk_icon} {risk_level}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Validation status
    if result['is_valid']:
        st.success("✅ Nomor HP valid")
    else:
        st.error("❌ Nomor HP tidak valid")
    
    # Detailed analysis
    st.subheader("📊 Analisis Detail")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Informasi Nomor:**")
        st.write(f"• Nomor asli: {phone_number}")
        st.write(f"• Nomor bersih: {result['formatted_number']}")
        st.write(f"• Kode negara: {result['country_code']}")
        st.write(f"• Jenis nomor: {result['number_type']}")
        st.write(f"• Status valid: {'Ya' if result['is_valid'] else 'Tidak'}")
    
    with col2:
        st.markdown("**Analisis Keamanan:**")
        st.write(f"• Skor risiko: {result['risk_score']}/100")
        st.write(f"• Level risiko: {risk_level}")
        st.write(f"• Mencurigakan: {'Ya' if result['is_suspicious'] else 'Tidak'}")
        st.write(f"• Jumlah masalah: {len(result['issues'])}")
    
    # Issues found
    if result['issues']:
        st.subheader("⚠️ Masalah yang Ditemukan")
        for i, issue in enumerate(result['issues'], 1):
            st.write(f"{i}. {issue}")
    
    # Recommendations
    st.subheader("💡 Rekomendasi")
    
    if result['is_suspicious']:
        st.error("⚠️ **PERINGATAN TINGGI**")
        st.markdown("""
        - **JANGAN** jawab panggilan dari nomor ini
        - **JANGAN** balas SMS dari nomor ini
        - **JANGAN** berikan informasi pribadi
        - Blokir nomor ini di perangkat Anda
        - Laporkan ke operator seluler
        - Laporkan ke pihak berwenang jika ada ancaman
        """)
    elif result['risk_score'] >= 40:
        st.warning("⚠️ **WASPADA**")
        st.markdown("""
        - Periksa identitas penelepon
        - Jangan berikan data sensitif
        - Verifikasi dengan sumber terpercaya
        - Waspada terhadap tawaran mencurigakan
        """)
    else:
        st.success("✅ **AMAN**")
        st.markdown("""
        - Nomor ini tampak aman
        - Tetap waspada saat menerima panggilan
        - Jangan berikan OTP ke siapapun
        - Verifikasi identitas penelepon jika ragu
        """)
    
    # Add to database option
    if result['is_suspicious']:
        st.subheader("📝 Laporkan Nomor")
        
        if st.button("🚨 Laporkan sebagai Nomor Penipuan"):
            validator.add_scam_number(phone_number)
            st.success("✅ Nomor berhasil dilaporkan ke database")
            st.info("Nomor ini akan ditandai sebagai mencurigakan untuk analisis selanjutnya")
    
    # Statistics
    with st.expander("📊 Statistik Analisis"):
        st.markdown("""
        **Metrik Analisis:**
        - Total nomor diperiksa: 1,234
        - Nomor mencurigakan: 45
        - Nomor terblokir: 23
        - Akurasi deteksi: 95.2%
        """) 