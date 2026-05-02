import PyPDF2

def extract_content(input_data):
    """
    Sprint 1: CV ve metin verilerini mülakat simülasyonu için hazırlar[cite: 1, 2].
    """
    # 1. Metin girişi kontrolü (Örn: Yapıştırılan iş ilanı)
    if isinstance(input_data, str):
        return input_data.strip()

    # 2. PDF dosyası kontrolü (Örn: Yüklenen CV)
    try:
        reader = PyPDF2.PdfReader(input_data)
        extracted_text = ""
        
        # Tüm sayfaları tek tek oku[cite: 1]
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        
        return extracted_text.strip()

    except Exception as e:
        # Hata durumunda sistemi durdurmaz, mesaj döner
        return f"Veri okuma hatası: {str(e)}"

# Geliştirici Testi
if __name__ == "__main__":
    print("Sprint 1 Modülü Hazır.")