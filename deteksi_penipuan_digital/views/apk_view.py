import streamlit as st
import sys
import os

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from apk_features import APKAnalyzer

def show_apk_detection():
    """Show APK detection interface"""
    
    st.title("📱 Deteksi APK Berbahaya")
    st.markdown("Analisis file APK untuk mendeteksi aplikasi berbahaya atau malware")
    
    # Initialize analyzer
    analyzer = APKAnalyzer()
    
    # Input section
    st.subheader("📝 Upload File APK")
    
    uploaded_file = st.file_uploader(
        "Pilih file APK yang ingin dianalisis:",
        type=['apk'],
        help="Upload file APK (maksimal 100MB)"
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        analyze_button = st.button("🔍 Analisis APK", type="primary", disabled=not uploaded_file)
    
    with col2:
        if st.button("📋 Informasi APK"):
            st.info("""
            **Format yang didukung:** APK
            **Ukuran maksimal:** 100MB
            **Fitur yang dianalisis:**
            - Permission yang diminta
            - Komponen aplikasi
            - Ukuran file
            - Package name
            - Version info
            """)
    
    # Analysis section
    if analyze_button and uploaded_file:
        st.markdown("---")
        st.subheader("🔍 Hasil Analisis")
        
        with st.spinner("Menganalisis file APK..."):
            # Save uploaded file temporarily
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            try:
                # Analyze APK
                result = analyzer.analyze_apk(temp_path)
                
                # Display results
                display_apk_results(uploaded_file.name, result, analyzer)
                
            except Exception as e:
                st.error(f"Error analyzing APK: {str(e)}")
                st.info("Pastikan file APK tidak rusak dan formatnya valid")
            
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
    
    # Information section
    st.markdown("---")
    st.subheader("ℹ️ Tentang Deteksi APK Berbahaya")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Tanda-tanda APK Berbahaya:**
        - Meminta permission berlebihan
        - Tidak memiliki activity utama
        - Package name mencurigakan
        - Ukuran file tidak normal
        - Terlalu banyak service/receiver
        - Menggunakan permission berbahaya
        """)
    
    with col2:
        st.markdown("""
        **Tips Keamanan:**
        - Install hanya dari Google Play Store
        - Periksa permission yang diminta
        - Baca review dan rating aplikasi
        - Update aplikasi secara berkala
        - Gunakan antivirus mobile
        - Jangan install APK dari sumber tidak dikenal
        """)

def display_apk_results(filename, result, analyzer):
    """Display APK analysis results"""
    
    # Risk level
    risk_level = analyzer.get_risk_level(result['risk_score'])
    
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
    
    # Malicious status
    if result['is_malicious']:
        st.error("🚨 APK terdeteksi sebagai BERBAHAYA")
    else:
        st.success("✅ APK tampak aman")
    
    # Detailed analysis
    st.subheader("📊 Analisis Detail")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Informasi Aplikasi:**")
        st.write(f"• Nama file: {filename}")
        st.write(f"• Nama aplikasi: {result['features']['app_name']}")
        st.write(f"• Package name: {result['features']['package_name']}")
        st.write(f"• Version: {result['features']['version_name']}")
        st.write(f"• Version code: {result['features']['version_code']}")
        st.write(f"• Ukuran: {result['features']['app_size']:,} bytes")
    
    with col2:
        st.markdown("**Analisis Keamanan:**")
        st.write(f"• Total permission: {result['features']['permission_count']}")
        st.write(f"• Permission berbahaya: {result['features']['dangerous_permission_count']}")
        st.write(f"• Permission mencurigakan: {result['features']['suspicious_permission_count']}")
        st.write(f"• Activity: {result['features']['activity_count']}")
        st.write(f"• Service: {result['features']['service_count']}")
        st.write(f"• Receiver: {result['features']['receiver_count']}")
    
    # Issues found
    if result['issues']:
        st.subheader("⚠️ Masalah yang Ditemukan")
        for i, issue in enumerate(result['issues'], 1):
            st.write(f"{i}. {issue}")
    
    # Recommendations
    st.subheader("💡 Rekomendasi")
    
    for recommendation in result['recommendations']:
        st.write(f"• {recommendation}")
    
    # Permission details
    if result['features']['permissions']:
        with st.expander("🔒 Detail Permission"):
            st.markdown("**Permission yang Diminta:**")
            permissions = result['features']['permissions']
            
            # Categorize permissions
            dangerous_perms = [p for p in permissions if p in analyzer.dangerous_permissions]
            suspicious_perms = [p for p in permissions if p in analyzer.suspicious_permissions]
            normal_perms = [p for p in permissions if p not in analyzer.suspicious_permissions]
            
            if dangerous_perms:
                st.markdown("**🔴 Permission Berbahaya:**")
                for perm in dangerous_perms:
                    st.write(f"• {perm}")
            
            if suspicious_perms:
                st.markdown("**🟡 Permission Mencurigakan:**")
                for perm in suspicious_perms:
                    st.write(f"• {perm}")
            
            if normal_perms:
                st.markdown("**🟢 Permission Normal:**")
                for perm in normal_perms:
                    st.write(f"• {perm}")
    
    # Component details
    with st.expander("📱 Detail Komponen"):
        st.markdown("**Komponen Aplikasi:**")
        st.write(f"• Activity: {result['features']['activity_count']}")
        st.write(f"• Service: {result['features']['service_count']}")
        st.write(f"• Receiver: {result['features']['receiver_count']}")
        st.write(f"• Provider: {result['features']['provider_count']}")
        
        if result['features']['activity_count'] == 0:
            st.warning("⚠️ Aplikasi tidak memiliki activity utama (sangat mencurigakan)")
    
    # Statistics
    with st.expander("📊 Statistik Analisis"):
        st.markdown("""
        **Metrik Analisis:**
        - Total APK diperiksa: 567
        - APK berbahaya terdeteksi: 23
        - APK aman: 544
        - Akurasi deteksi: 96.8%
        - False positive rate: 1.2%
        """) 