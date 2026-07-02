import streamlit as st
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.sidebar import create_sidebar
from views.phishing_view import show_phishing_detection
from views.hp_view import show_hp_detection
from views.email_view import show_email_detection
from views.apk_view import show_apk_detection

def main():
    st.set_page_config(
        page_title="Deteksi Penipuan Digital",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS (gunakan path absolut agar aman di lokal & Streamlit Cloud)
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style", "custom.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("File CSS kustom `style/custom.css` tidak ditemukan. Pastikan file ini ikut di-push ke repository jika ingin tampilan kustom.")
    
    # Sidebar
    create_sidebar()
    
    # Main content: hanya tampilkan phishing detection
    show_phishing_detection()

if __name__ == "__main__":
    main() 