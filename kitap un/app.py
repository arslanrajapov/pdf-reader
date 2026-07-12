import streamlit as st
import fitz
import requests
import io

st.set_page_config(layout="wide")

st.title("📖 clean reader")

# --- KONTROL PANELİ ---
c_top1, c_top2 = st.columns([2, 1])
with c_top1:
    font_size = st.slider("Punto Boyutu", 12, 30, 20)

# --- PDF İŞLEME ---
if 'page_num' not in st.session_state:
    st.session_state.page_num = 0

url = st.text_input("Kitap Linki:")

if url:
    try:
        # Tarayıcı gibi davranması için headers ekliyoruz
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        pdf_document = fitz.open(stream=io.BytesIO(response.content), filetype="pdf")
        total_pages = len(pdf_document)
        
        # --- SAYFA GEÇİŞ SİSTEMİ ---
        st.write("---")
        col_ctrl, col_counter = st.columns([2, 1])
        
        with col_ctrl:
            page_input = st.number_input("Sayfaya Git:", min_value=1, max_value=total_pages, value=st.session_state.page_num + 1)
            if st.session_state.page_num != page_input - 1:
                st.session_state.page_num = page_input - 1
                st.rerun() 
        
        with col_counter:
            st.markdown(f"<h2 style='text-align: right;'>{st.session_state.page_num + 1} | {total_pages}</h2>", unsafe_allow_html=True)

        # Metin Çıkarma
        page = pdf_document.load_page(st.session_state.page_num)
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: b[1])
        text = "\n\n".join([b[4] for b in blocks])
        
        st.markdown(f"""
            <div style="font-size: {font_size}px; padding: 20px; line-height: 1.6; font-family: serif; background-color: #1a1a1a; color: #e0e0e0; border-radius: 10px;">
                {text}
            </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Kitap yüklenemedi: {e}")