import platform

# Python 3.13'te bazı Windows makinelerde WMI sorgusu takılabiliyor.
# google-genai -> aiohttp import zincirinde platform bilgisi okunurken bu tetikleniyor.
if hasattr(platform, "_wmi_query"):
    platform._wmi_query = lambda *args, **kwargs: ("0", "1", "0", "0", "0")

from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

def test_api_connection():
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemma-3-4b-it",
        contents="Merhaba! Sadece 'Bağlantı başarılı.' yaz."
    )
    print("API Baglantisi Basarili!")
    print(response.text)

if __name__ == "__main__":
    test_api_connection()