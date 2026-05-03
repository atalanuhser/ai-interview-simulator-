import os
import requests
from dotenv import load_dotenv

load_dotenv()


def test_api_connection():
    api_key = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemma-3-4b-it:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": "Say only: Connection successful."}]
            }
        ]
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        print("API Connection Successful!")
        print(text)
    else:
        print(f"Error {response.status_code}: {response.text}")


if __name__ == "__main__":
    test_api_connection()