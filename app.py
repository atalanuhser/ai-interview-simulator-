import streamlit as st
import time

st.set_page_config(page_title="AI Mülakat", layout="wide")

st.markdown("""
<style>

.stApp {
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.block-container {
    padding-top: 0 !important;
}

.main > div {
    padding-top: 0rem !important;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.6rem;
}

div[data-testid="stVerticalBlock"] > div:first-child {
    margin-top: -20px;
}

.block-container {
    max-width: 820px;
}

.title {
    font-size:30px;
    font-weight:600;
    text-align:center;
    color:white;
    margin-bottom:4px;
}

.subtitle {
    text-align:center;
    color:#94a3b8;
    font-size:14px;
    margin-bottom:18px;
}

.card {
    background: rgba(20,20,30,0.55);
    padding: 22px;
    border-radius: 14px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.06);
}

input, textarea {
    border-radius: 10px !important;
    background: rgba(255,255,255,0.05) !important;
    color: white !important;
    height: 42px !important;
}

.stButton>button {
    height: 42px;
    border-radius: 10px;
    font-size: 15px;
    background: linear-gradient(90deg,#6366f1,#8b5cf6);
    color:white;
    border:none;
}

.section-title {
    font-size:15px;
    font-weight:500;
    color:#cbd5e1;
    margin-top:8px;
    margin-bottom:4px;
}

.fade {
    animation: fadeIn 0.4s ease-in;
}

@keyframes fadeIn {
    from {opacity:0; transform:translateY(10px);}
    to {opacity:1; transform:translateY(0);}
}

header {visibility:hidden;}
footer {visibility:hidden;}

</style>
""", unsafe_allow_html=True)


def set_bg(url):
    st.markdown(f"""
    <style>
    .stApp {{
        background:
        linear-gradient(rgba(5,10,20,0.85), rgba(5,10,20,0.95)),
        url("{url}");
    }}
    </style>
    """, unsafe_allow_html=True)


if "page" not in st.session_state:
    st.session_state.page = "home"


if st.session_state.page == "home":

    set_bg("https://images.unsplash.com/photo-1492724441997-5dc865305da7")

    st.markdown('<div class="fade">', unsafe_allow_html=True)

    st.markdown('<div class="title">AI Mülakat</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Kendini test et. Gerçek mülakata hazırlan.</div>', unsafe_allow_html=True)

    import components.upload as upload
    upload.show()

    st.markdown('</div>', unsafe_allow_html=True)


elif st.session_state.page == "mode":

    set_bg("https://images.unsplash.com/photo-1557804506-669a67965ba0")

    st.markdown('<div class="title">Mülakat Türü</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✍️ Yazılı", use_container_width=True):
            st.session_state.mode = "text"
            st.session_state.page = "loading"
            st.rerun()

    with col2:
        if st.button("🎤 Sesli", use_container_width=True):
            st.session_state.mode = "voice"
            st.session_state.page = "loading"
            st.rerun()


elif st.session_state.page == "loading":

    set_bg("https://images.unsplash.com/photo-1517245386807-bb43f82c33c4")

    st.markdown('<div class="title">Hazırlanıyor...</div>', unsafe_allow_html=True)
    st.progress(80)
    time.sleep(1.2)

    st.session_state.page = "chat"
    st.rerun()


elif st.session_state.page == "chat":

    set_bg("https://images.unsplash.com/photo-1552664730-d307ca884978")

    import components.chat as chat
    chat.show()


elif st.session_state.page == "result":

    set_bg("https://images.unsplash.com/photo-1551288049-bebda4e38f71")

    import components.result as result
    result.show()