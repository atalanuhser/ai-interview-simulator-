<<<<<<< HEAD
import PyPDF2
from bs4 import BeautifulSoup
import re
import os
from docx import Document  # Word dosyaları için

class InterviewDataProcessor:
    """

    Özellikler: PDF/Word okuma, KVKK Maskeleme, Yetenek Avcısı, Fedai Kontrolü.
    """
    def __init__(self):
        self.phone_pattern = r'(\d{3,4}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2})'
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        #  yetenekler listesi
        self.skill_keywords = ["Python", "Java", "C#", "SQL", "JavaScript", "React", "Angular", "Machine Learning", "Deep Learning", "HTML", "CSS", "Django", "Flask"]

    def validate_file(self, file_path):
        """FEDAİ: Dosya tipini ve boyutunu kontrol eder."""
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in ['.pdf', '.docx']:
            return False, "Sadece PDF veya DOCX dosyaları kabul edilir!"
        
        # 5 MB'dan büyük dosyaları alma (Sunucuyu korur)
        if os.path.getsize(file_path) > 5 * 1024 * 1024:
            return False, "Dosya çok büyük! Lütfen 5MB'dan küçük bir dosya yükleyin."
        
        return True, "Dosya uygun."

    def _extract_from_pdf(self, file):
        try:
            reader = PyPDF2.PdfReader(file)
            text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
            return text.strip() if text else "ERROR:EMPTY"
        except: return "ERROR:FAILED"

    def _extract_from_docx(self, file_path):
        """Word dosyasından metni söker."""
        try:
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs]).strip()
        except: return "ERROR:FAILED"

    def _get_skills(self, text):
        """Metindeki yetenekleri bulur ve AI'ya liste yapar."""
        found_skills = [skill for skill in self.skill_keywords if skill.lower() in text.lower()]
        return ", ".join(found_skills) if found_skills else "Belirtilmemiş"

    def _clean_and_mask(self, raw_text):
        """Temizlik ve KVKK maskelemesi."""
        soup = BeautifulSoup(raw_text, "html.parser")
        text = soup.get_text(separator=" ")
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,!?\-]', '', text)
        text = re.sub(self.phone_pattern, '[TELEFON GİZLENDİ]', text)
        text = re.sub(self.email_pattern, '[E-POSTA GİZLENDİ]', text)
        return text.strip()

    def final_process(self, file_path, job_description):
        
        # 1. Fedai Kontrolü
        is_valid, msg = self.validate_file(file_path)
        if not is_valid: return {"status": "error", "message": msg}

        # 2. Dosya Tipine Göre Oku
        ext = os.path.splitext(file_path)[1].lower()
        cv_raw = self._extract_from_pdf(file_path) if ext == ".pdf" else self._extract_from_docx(file_path)

        if "ERROR" in cv_raw:
            return {"status": "error", "message": "Dosya okunamadı veya içeriği boş!"}

        # 3. Temizle ve Yetenekleri Ayıkla
        clean_cv = self._clean_and_mask(cv_raw)
        clean_job = self._clean_and_mask(job_description)
        skills = self._get_skills(clean_cv)

        # 4. Kusursuz Prompt
        prompt = f"""
        ROL: Senior Teknik İK Direktörü
        ADAY YETENEK ÖZETİ: {skills}
        
        GÖREV: Aşağıdaki CV ve İş Tanımını analiz et. Adayın bildiği "{skills}" teknolojileri ile 
        iş tanımındaki beklentileri kıyaslayarak EN ZORLU teknik soruları üret.
        
        --- CV İÇERİĞİ ---
        {clean_cv}
        
        --- İŞ TANIMI ---
        {clean_job}
        """
        return {"status": "success", "data": prompt}

if __name__ == "__main__":
    print("Veri Hattı:HAZIR!")
=======
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
>>>>>>> dd65b8b0ff520f33678bff0ce96fb968e9ed8166
