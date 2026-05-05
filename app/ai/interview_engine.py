from app.ai.gemini_client import get_client
from app.ai.prompts import build_system_prompt
import json


def start_interview(candidate_name: str, position: str, job_text: str, cv_text: str):
    system_prompt = build_system_prompt(candidate_name, position, job_text, cv_text)
    client = get_client()
    history = [{"role": "system", "content": system_prompt}]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=history + [{"role": "user", "content": "Start the interview. Ask the first question."}],
        temperature=0.2,
        max_tokens=500,
    )
    first_question = response.choices[0].message.content.strip()
    history.append({"role": "assistant", "content": first_question})
    return history, first_question


def send_answer(history: list, user_answer: str):
    client = get_client()
    history.append({"role": "user", "content": user_answer})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=history,
        temperature=0.2,
        max_tokens=500,
    )
    text = response.choices[0].message.content.strip()
    clean = text.replace("```json", "").replace("```", "").strip()
    history.append({"role": "assistant", "content": text})

    if '"interview_finished": true' in clean:
        try:
            final_data = json.loads(clean)
            return None, True, final_data, history
        except json.JSONDecodeError:
            return None, True, {"raw": clean}, history

    return text, False, None, history


def get_chat_history(history: list) -> list:
    qa_list = []
    messages = [m for m in history if m["role"] != "system"]
    for i in range(0, len(messages) - 1, 2):
        if i + 1 < len(messages):
            qa_list.append({
                "question": messages[i]["content"],
                "answer": messages[i + 1]["content"]
            })
    return qa_list