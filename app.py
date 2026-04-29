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