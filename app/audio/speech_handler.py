import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import io

def text_to_speech(text: str):
    """
    AI yanıtını sese çevirir ve Streamlit arayüzünde (tarayıcıda) oynatır.
    OS bağımsızdır (Windows ve Mac'te çalışır).
    """
    if not text:
        return
        
    try:
        # Sesi diske yazmadan doğrudan belleğe (RAM) kaydet
        tts = gTTS(text=text, lang='en')
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        
        # Sesi kullanıcının tarayıcısında oynat
        st.audio(audio_fp, format="audio/mp3")
        
    except Exception as e:
        st.error(f"TTS Error: {str(e)}")

def process_audio_data(audio_bytes) -> str:
    """
    Tarayıcıdaki mikrofondan gelen ham ses verisini alır ve metne çevirir.
    """
    r = sr.Recognizer()
    
    try:
        # Gelen bayt verisini ses dosyası gibi işle
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
            
        # Google üzerinden İngilizce olarak metne çevir
        text = r.recognize_google(audio, language="en-US")
        return text
        
    except sr.UnknownValueError:
        return "Error: Could not understand audio"
    except sr.RequestError:
        return "Error: Speech service is down"
    except Exception as e:
        return f"System Error: {str(e)}"