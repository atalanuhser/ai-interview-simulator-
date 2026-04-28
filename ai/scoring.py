import json
from ai.prompts import build_scoring_prompt
from ai.gemini_client import get_client


def parse_final_scores(final_data: dict) -> dict:
    """
    interview_engine'den gelen final JSON'u
    radar grafiği için hazır formata çevirir.
    """
    puanlar = final_data.get("puanlar", {})
    geri_bildirim = final_data.get("geri_bildirim", {})

    return {
        "radar": {
            "Teknik Yetkinlik": puanlar.get("teknik_yetkinlik", 0),
            "İletişim": puanlar.get("iletisim_becerileri", 0),
            "Problem Çözme": puanlar.get("problem_cozme", 0),
            "Deneyim Uyumu": puanlar.get("deneyim_uyumu", 0),
            "Motivasyon": puanlar.get("motivasyon", 0),
        },
        "genel_yorum": geri_bildirim.get("genel_yorum", ""),
        "guclu_yonler": geri_bildirim.get("guclu_yonler", []),
        "gelisim_alanlari": geri_bildirim.get("gelisim_alanlari", []),
        "tavsiye": geri_bildirim.get("tavsiye", ""),
        "toplam_soru": final_data.get("toplam_soru", 0),
    }


def generate_scores_from_history(qa_history: list, position: str, candidate_name: str) -> dict:
    """
    Yedek yol: Mülakat JSON'u gelmezse geçmişten puanlama yapar.
    """
    prompt = build_scoring_prompt(qa_history, position, candidate_name)

    client = get_client()
    response = client.models.generate_content(
        model="gemini-1.5-flash-8b",
        contents=prompt,
    )
    clean = (response.text or "").strip().replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(clean)
        return parse_final_scores(data)
    except json.JSONDecodeError:
        return {"error": "Puanlama yapılamadı", "raw": clean}
