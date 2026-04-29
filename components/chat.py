import streamlit as st
import speech_recognition as sr
from services.ai_bridge import start_interview, send_answer

def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Dinleniyor...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio, language="tr-TR")
    except:
        return ""

def show():

    st.markdown("## 💬 Mülakat")

    if "messages" not in st.session_state:
        st.session_state.messages = []
        q = start_interview(st.session_state.user_name, st.session_state.job_title)
        st.session_state.messages.append(("AI", q))

    # 💎 BUBBLE UI
    for role, msg in st.session_state.messages:

        if role == "USER":
            st.markdown(f"""
            <div style="
                background:#6366f1;
                padding:10px;
                border-radius:12px;
                margin:6px;
                text-align:right;
                color:white;
            ">
            {msg}
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
            <div style="
                background:rgba(255,255,255,0.08);
                padding:10px;
                border-radius:12px;
                margin:6px;
                text-align:left;
                color:white;
            ">
            {msg}
            </div>
            """, unsafe_allow_html=True)

    mode = st.session_state.get("mode")

    if mode == "text":
        user_input = st.chat_input("Cevap yaz...")
    else:
        user_input = None
        if st.button("🎤 Konuş"):
            user_input = speech_to_text()

    if user_input:
        st.session_state.messages.append(("USER", user_input))
        reply = send_answer(user_input)
        st.session_state.messages.append(("AI", reply))
        st.rerun()

    if st.button("📊 Bitir"):
        st.session_state.page = "result"
        st.rerun()