from app.ai.gemini_client import get_client

def test_api_connection():
    client = get_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Say only: Connection successful."}]
    )
    print("API Connection Successful!")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    test_api_connection()