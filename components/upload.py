import streamlit as st
from services.parser import pdf_to_text

def show():

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("### 👤 Kişisel Bilgiler")

    name = st.text_input("Ad Soyad", placeholder="Örn: Cemre Yılmaz")

    st.markdown("### 🎯 Mülakat Türü")

    mode = st.radio("", ["Pozisyon gir", "İş ilanı yükle"], horizontal=True)

    job_text = ""

    if mode == "Pozisyon gir":
        job_text = st.text_input("Pozisyon", placeholder="Örn: Backend Developer")

    else:
        pdf = st.file_uploader("İş ilanı (PDF)", type=["pdf"])
        if pdf:
            job_text = pdf_to_text(pdf)
            st.success("İş ilanı başarıyla okundu")

    st.markdown("### 📎 CV")

    cv = st.file_uploader("CV yükle (opsiyonel)", type=["pdf"])

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Devam Et", use_container_width=True):
        if not name:
            st.warning("İsim gir")
        elif not job_text:
            st.warning("Pozisyon veya ilan gir")
        else:
            st.session_state.user_name = name
            st.session_state.job_title = job_text
            st.session_state.cv = cv
            st.session_state.page = "mode"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)