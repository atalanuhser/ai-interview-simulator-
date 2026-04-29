import httpx
from google import genai
from google.genai import errors
from google.genai.types import HttpOptions, HttpRetryOptions

# Google AI Studio / Gemini’den aldığın API anahtarını tırnak içine yapıştır
API_KEY = "AIzaSyClxO5_Zwb0mcL_L0nuluERMph0fxI1keM"

if not API_KEY:
    raise RuntimeError("API_KEY boş; anahtarı yukarıdaki satıra yaz.")

# ms cinsinden; None olunca bağlantı çok uzun sürebilir (senin gördüğün takılma)
_HTTP_TIMEOUT_MS = 120_000  # 120 saniye
# Varsayılan 5 deneme + bekleme uzun sürer; takılmayı azaltmak için düşük tutuldu
_RETRY = HttpRetryOptions(attempts=2, initial_delay=1.0, max_delay=8.0)

client = genai.Client(
    api_key=API_KEY,
    http_options=HttpOptions(timeout=_HTTP_TIMEOUT_MS, retry_options=_RETRY),
)

# gemini-1.5-flash bu API sürümünde yok (404); güncel stabil Flash modeli:
MODEL = "gemini-2.5-flash"
_PROMPT = (
    "Selam Gemini! Ben Yarengül. En yeni kütüphane ile sana bağlandım. "
    "İlk testimiz başarılı mı?"
)

_QUOTA_BUSY_MSG = "Şu an meşgulüm, 30 saniye sonra tekrar dene"
_NET_FAIL_MSG = (
    "İnternet / güvenlik duvarı nedeniyle Google API'ye bağlanılamıyor. "
    "Bağlantıyı, DNS'i ve VPN/proxy ayarlarını kontrol et."
)

try:
    response = client.models.generate_content(
        model=MODEL,
        contents=_PROMPT,
    )
except errors.APIError as e:
    if e.code == 429:
        print(_QUOTA_BUSY_MSG)
    else:
        print(f"API hatası ({e.code}): {e}")
except httpx.TimeoutException:
    print(
        "İstek zaman aşımına uğradı. Ağ yavaş veya engelli olabilir; biraz sonra tekrar dene."
    )
except httpx.RequestError:
    print(_NET_FAIL_MSG)
else:
    print("Gemini'nin Cevabı:")
    print("-" * 20)
    print(response.text)
