from google import genai
from google.genai import types
from dotenv import load_dotenv
from app.ai.prompts import build_system_prompt
from app.ai.gemini_client import get_client
import os
import json

load_dotenv()


def start_interview(candidate_name: str, position: str, job_text: str, cv_text: str):
    system_prompt = build_system_prompt(candidate_name, position, job_text, cv_text)
    client = get_client()
    chat = client.chats.create(
        model="gemini-2.0-flash-lite",
        config=types.GenerateContentConfig(system_instruction=system_prompt)
    )
    response = chat.send_message("Start the interview. Ask the first question.")
    return chat, response.text.strip()


def send_answer(chat, user_answer: str):
    response = chat.send_message(user_answer)
    text = response.text.strip()
    clean = text.replace("```json", "").replace("```", "").strip()

    if '"interview_finished": true' in clean:
        try:
            final_data = json.loads(clean)
            return None, True, final_data
        except json.JSONDecodeError:
            return None, True, {"raw": clean}

    return text, False, None


def get_chat_history(chat) -> list:
    history = []
    messages = chat.get_history()

    for i in range(0, len(messages) - 1, 2):
        if i + 1 < len(messages):
            question = messages[i].parts[0].text if messages[i].parts else ""
            answer = messages[i + 1].parts[0].text if messages[i + 1].parts else ""
            if question and answer:
                history.append({"question": question, "answer": answer})

    return history
