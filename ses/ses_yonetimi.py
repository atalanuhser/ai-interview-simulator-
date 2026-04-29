import os
from gtts import gTTS
import speech_recognition as sr

def metni_seslendir(metin):
    """Yapay zekanın konuşmasını sağlar (Ağız)"""
    try:
        print(f"🤖 Yapay Zeka: {metin}")
        tts = gTTS(text=metin, lang='tr')
        dosya_adi = "gecici_ses.mp3"
        tts.save(dosya_adi)
        os.system(f"afplay {dosya_adi}") # Mac'e özel oynatıcı
        if os.path.exists(dosya_adi):
            os.remove(dosya_adi)
        return True
    except Exception as e:
        print(f"❌ Ses çalınırken hata: {e}")
        return False

def mikrofondan_ses_al():
    """Kullanıcının sesini dinler ve metne çevirir (Kulak)"""
    kaydedici = sr.Recognizer()
    
    with sr.Microphone() as kaynak:
        print("\n🎤 Ortam gürültüsü ayarlanıyor, lütfen bekleyin...")
        kaydedici.adjust_for_ambient_noise(kaynak, duration=1)
        
        print("🟢 Sizi dinliyorum, konuşabilirsiniz...")
        try:
            # Kullanıcıyı dinle
            ses = kaydedici.listen(kaynak, timeout=5, phrase_time_limit=15)
            
            print("⏳ Sesiniz metne dönüştürülüyor...")
            # Sesi Google altyapısı ile metne çevir
            metin = kaydedici.recognize_google(ses, language="tr-TR")
            
            print(f"👤 Siz dediniz ki: {metin}")
            return metin
            
        except sr.WaitTimeoutError:
            print("❌ Süre doldu, ses algılanmadı.")
            return None
        except sr.UnknownValueError:
            print("❌ Ne söylediğinizi anlayamadım.")
            return None
        except Exception as e:
            print(f"❌ Bir hata oluştu: {e}")
            return None

# --- SİSTEMİ TEST ETME BÖLÜMÜ ---
if __name__ == "__main__":
    # 1. Aşama: Sistemi dinlemeye al
    kullanici_metni = mikrofondan_ses_al()
    
    # 2. Aşama: Eğer duyduysa, duyduğunu tekrar etsin
    if kullanici_metni:
        cevap = f"Söylediğiniz cümleyi başarıyla kaydettim. Şunu dediniz: {kullanici_metni}"
        metni_seslendir(cevap)