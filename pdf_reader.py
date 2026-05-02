from bs4 import BeautifulSoup 
import PyPDF2

def clean_text(raw_html):
    """
    Web'den gelen metindeki HTML etiketlerini ve gürültülü veriyi temizler.
    """
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    cleansed_text = soup.get_text(separator=" ")
    
    # Boşlukları ve satırları düzenle
    lines = (line.strip() for line in cleansed_text.splitlines())
    return "\n".join(line for line in lines if line)

def parse_cv(file) -> str:
    """
    Sprint 1: PDF CV'yi okur.
    """
    try:
        reader = PyPDF2.PdfReader(file)
        text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text.strip()
    except:
        return "CV Okuma Hatası"

def parse_job_description(file_or_text) -> str:
    """
    Sprint 2: İş ilanı metnini temizleyerek AI modülüne hazırlar.
    """
    if isinstance(file_or_text, str):
        return clean_text(file_or_text)
    
    raw_text = parse_cv(file_or_text)
    return clean_text(raw_text)

def format_for_ai(cv_text, job_text):
    """
    Temizlenmiş verileri AI analiz şablonuna sokar.
    """
    return f"ADAY ÖZGEÇMİŞİ:\n{cv_text}\n\n---\n\nİŞ İLANI GEREKSİNİMLERİ:\n{job_text}"

if __name__ == "__main__":
    print("Sprint 2 Modülü Hazır: Veri temizleme ve formatlama aktif.")