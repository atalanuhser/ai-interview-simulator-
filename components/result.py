import streamlit as st
import plotly.express as px

def show():

    st.markdown("# 📊 Performans")

    data = {
        "Kategori": ["Teknik", "İletişim", "Problem Çözme"],
        "Puan": [7,8,6]
    }

    fig = px.line_polar(data, r="Puan", theta="Kategori", line_close=True)
    st.plotly_chart(fig)

    st.markdown("### 🧠 AI Yorum")
    st.write("Genel olarak iyi performans, teknik derinlik geliştirilmeli.")

    if st.button("🔄 Yeniden Başla"):
        st.session_state.clear()
        st.session_state.page = "home"
        st.rerun()