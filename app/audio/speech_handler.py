import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import io


def text_to_speech(text: str):
    """
    Text'i sese çevirir ve audio buffer döndürür
    (Artık direkt çalmaz → interview içinde kullanılır)
    """
    if not text:
        return None

    try:
        tts = gTTS(text=text, lang='en')

        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)

        return audio_fp  # 🔥 ÖNEMLİ

    except Exception as e:
        st.error(f"TTS Error: {str(e)}")
        return None


def process_audio_data(audio_bytes) -> str | None:
    """
    Mikrofon sesini text'e çevirir
    Hata olursa None döner (loop engeller)
    """
    r = sr.Recognizer()

    try:
        audio_file = io.BytesIO(audio_bytes)

        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)

        text = r.recognize_google(audio, language="en-US")
        return text

    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None
    except Exception:
        return None