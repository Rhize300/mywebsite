import streamlit as st

def create_sidebar():
    """Create sidebar navigation"""
    
    st.sidebar.title("🛡️ Deteksi Penipuan Digital")
    st.sidebar.markdown("---")
    
    # Navigation menu
    st.sidebar.markdown("APLIKASI")
    st.sidebar.markdown("> Phishing URL")
    
    st.sidebar.markdown("---")
    
    # Information section
    st.sidebar.subheader("ℹ️ Informasi")
    st.sidebar.markdown("""
    Aplikasi ini membantu mendeteksi berbagai jenis penipuan digital:
    
    🔗 **Phishing URL**: Deteksi website palsu

    """)
   
    st.sidebar.markdown("---")
    
    # Statistics
    st.sidebar.subheader("📊 Statistik")
    st.sidebar.metric(
        label="URL Diperiksa",
        value="1,234",
        help="Total URL yang telah dianalisis"
    )
    
    st.sidebar.markdown("---")
    
    # Footer
    st.sidebar.markdown("""
    <div style='text-align: center; color: #666; font-size: 12px;'>
        Made with ❤️ for Digital Security
    </div>
    """, unsafe_allow_html=True)
    
    # Tidak perlu return apa-apa 