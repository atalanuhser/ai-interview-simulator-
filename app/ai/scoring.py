import json
from app.ai.gemini_client import get_client
from app.ai.prompts import build_scoring_prompt


def parse_final_scores(final_data: dict) -> dict:
    scores = final_data.get("scores", {})
    feedback = final_data.get("feedback", {})

    return {
        "radar": {
            "Technical Competency": scores.get("technical_competency", 0),
            "Communication": scores.get("communication_skills", 0),
            "Problem Solving": scores.get("problem_solving", 0),
            "Experience Fit": scores.get("experience_fit", 0),
            "Motivation": scores.get("motivation", 0),
        },
        "overall_comment": feedback.get("overall_comment", ""),
        "strengths": feedback.get("strengths", []),
        "areas_for_improvement": feedback.get("areas_for_improvement", []),
        "recommendation": feedback.get("recommendation", ""),
        "total_questions": final_data.get("total_questions", 0),
    }


def generate_scores_from_history(qa_history: list, position: str, candidate_name: str) -> dict:
    from google import genai
    from dotenv import load_dotenv
    import os
    load_dotenv()

    prompt = build_scoring_prompt(qa_history, position, candidate_name)
    client = get_client()

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    clean = response.text.strip().replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(clean)
        return parse_final_scores(data)
    except json.JSONDecodeError:
        return {"error": "Scoring failed", "raw": clean}
