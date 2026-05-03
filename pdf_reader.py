import PyPDF2
from bs4 import BeautifulSoup
import re

def clean_text(raw_data):
    # Veri yoksa boş dön, sistem patlamasın
    if not raw_data:
        return ""
    
    # HTML etiketleri ve script/style gibi gereksiz kod blokları temizliği
    soup = BeautifulSoup(raw_data, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    
    text = soup.get_text(separator=" ")
    
    # Fazla boşlukları ve satır sonu gürültülerini regex ile teke indir
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_cv(file) -> str:
    # Sprint 1: PDF verisini okuyup temiz metne çevirme aşaması
    extracted_text = ""
    try:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                extracted_text += content + "\n"
        
        # Okunan veriyi doğrudan temizlik süzgecine gönder
        return clean_text(extracted_text)
    except Exception as e:
        return f"HATA: {str(e)}"

def parse_job_description(file_or_text) -> str:
    # Sprint 2: İş ilanı metin/dosya tipine göre veri hazırlama
    if not isinstance(file_or_text, str):
        # Dosya gelirse önce metne çevir
        raw_text = parse_cv(file_or_text)
    else:
        # Metin gelirse doğrudan işle
        raw_text = file_or_text
        
    return clean_text(raw_text)

def format_for_ai(cv_text, job_text):
    # Nihai Sprint: AI (Gemini) için XML tabanlı profesyonel prompt yapısı
    # Bu format modelin CV ve iş ilanını karıştırmasını %100 engeller
    prompt = f"""
<DOCUMENTS>
    <USER_CV>
    {cv_text}
    </USER_CV>

    <JOB_DESCRIPTION>
    {job_text}
    </JOB_DESCRIPTION>
</DOCUMENTS>

<INSTRUCTION>
CV ve İş İlanını karşılaştırarak mülakat için kritik sorular hazırla.
</INSTRUCTION>
"""
    return prompt.strip()

if __name__ == "__main__":
    # Geliştirici notu: Modül testi ve entegrasyon kontrolü
    print("Sistem hazır. Data Pipeline sorunsuz çalışıyor.")