import PyPDF2

# 1. CV Okuma Fonksiyonu (Arkadaşının beklediği isim)
def parse_cv(file):
    """
    PDF formatındaki CV'yi okur ve metne çevirir[cite: 1].
    """
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text.strip()
    except Exception as e:
        return f"CV okuma hatası: {e}"

# 2. İş İlanı Okuma Fonksiyonu (Arkadaşının beklediği isim)
def parse_job_description(input_data):
    """
    İş ilanı metnini hazırlar. 
    Not: Sprint 2'de buraya BeautifulSoup4 temizliği eklenecektir.
    """
    if isinstance(input_data, str):
        return input_data.strip()
    
    # Eğer iş ilanı da PDF olarak gelirse yukarıdaki mantığı kullanabiliriz
    return parse_cv(input_data)

# Test Bölümü
if __name__ == "__main__":
    print("Data Modülü: parse_cv ve parse_job_description hazır!")