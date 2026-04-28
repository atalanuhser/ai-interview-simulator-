import pytest
from unittest.mock import patch, MagicMock
from ai.prompts import build_system_prompt, build_scoring_prompt
from ai.scoring import parse_final_scores


def test_build_system_prompt():
    prompt = build_system_prompt("Ahmet Yılmaz", "Python Developer", "Django gerekli", "2 yıl deneyim")
    assert "Ahmet Yılmaz" in prompt
    assert "Python Developer" in prompt
    assert "Django gerekli" in prompt


def test_build_scoring_prompt():
    history = [{"question": "Django nedir?", "answer": "Web framework"}]
    prompt = build_scoring_prompt(history, "Python Developer", "Ahmet Yılmaz")
    assert "Django nedir?" in prompt
    assert "Web framework" in prompt


def test_parse_final_scores():
    mock_data = {
        "puanlar": {
            "teknik_yetkinlik": 85,
            "iletisim_becerileri": 70,
            "problem_cozme": 75,
            "deneyim_uyumu": 80,
            "motivasyon": 90
        },
        "geri_bildirim": {
            "genel_yorum": "İyi bir aday.",
            "guclu_yonler": ["Teknik bilgi", "İletişim"],
            "gelisim_alanlari": ["Takım çalışması"],
            "tavsiye": "Uygun."
        },
        "toplam_soru": 8
    }
    result = parse_final_scores(mock_data)
    assert result["radar"]["Teknik Yetkinlik"] == 85
    assert result["toplam_soru"] == 8
    assert "genel_yorum" in result
