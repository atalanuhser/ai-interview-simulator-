import os
from gtts import gTTS
import speech_recognition as sr

def text_to_speech(text: str):
    """AI yanıtını İngilizce sese çevirir."""
    try:
        if not text: return
        tts = gTTS(text=text, lang='en')
        tts.save("temp_voice.mp3")
        os.system("afplay temp_voice.mp3") 
        os.remove("temp_voice.mp3")
    except Exception as e:
        print(f"TTS Error: {e}")

def speech_to_text() -> str:
    """Kullanıcının İngilizce konuşmasını metne çevirir."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=5)
            return r.recognize_google(audio, language="en-US")
        except:
            return ""