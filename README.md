#  AI-Powered Interview Simulation

> **YMH220 / YMH210 — Python Project**


## What is this project?

This app helps people who are new to jobs or looking for internships. You give the app your CV as a PDF file and a job text. The app reads both and uses AI to make interview questions just for you. The questions are said out loud. You answer with your voice. At the end, you see a graph that shows how well you did.

---

## What can the app do?

-  Read your CV from a PDF file
-  Clean up the job text so the AI understands it better
-  Make interview questions using Groq AI — questions are made just for your CV and the job
-  Listen to your voice answers from the microphone
-  Say the questions out loud so you can hear them
-  Show a score graph at the end of the interview
-  Handle errors in every part so the app does not break

---

## Tools we used

| Tool | What it does |
|------|--------------|
| `streamlit` | Makes the screen and buttons |
| `PyPDF2` | Reads the text from your PDF CV |
| `BeautifulSoup4` | Cleans up the job text |
| `SpeechRecognition` | Turns your voice into text (STT) |
| `gTTS` | Turns text into voice — the app speaks to you (TTS) |
| `groq` | Connects to Groq AI (free to use) |
| `Plotly` | Draws the score graph |
| `Pandas` | Keeps the score numbers |
| `pytest` | Checks that the important parts of the app work |

---

## Who did what

###  Person 1 — Cemre YURTSEVER | Screen and Design

This person made the app look good and easy to use.

- Made the main screen with Streamlit
- Added the PDF upload button
- Made the chat screen where the interview happens
- **Key job:** Made the score graph (radar chart) with Plotly that you see at the end

---

###  Person 2 — İlayda MEMİŞ | Data and Text

This person got the right information ready for the AI.

- Read the text from the PDF CV file using PyPDF2
- Cleaned up the job text using BeautifulSoup4
- **Key job:** Made the text clean and simple so the AI can read and understand it well

---

###  Person 3 — Fırat Yunus YAŞAROĞLU | Voice

This person made the app listen and speak.

- Made the app listen to your voice and turn it into text (STT)
- Made the app say the questions out loud (TTS)
- **Key job:** Fixed microphone errors and made sure the voice plays fast with no big wait

---

###  Person 4 — Yarengül KOCAOĞLU | AI and Questions

This person is the brain of the app.

- Connected the app to Groq AI
- Wrote the instructions (prompts) that tell the AI what kind of questions to ask
- **Key job:** Decided how the AI gives you a score and feedback at the end of the interview

---

###  Person 5 — Nuhser ATALA | Putting it all together + Scrum Master

This person joined all the parts and made sure nothing broke.

- Put all the code from the other 4 people into one file (`main.py`)
- Managed GitHub so people did not break each other's work
- Wrote the tests with pytest
- Wrote the project report and this README
- **Key job:** Fixed the screen freeze problem — when the app speaks, the screen must not stop. This needed special code to keep everything moving at the same time.

---

## How to set up the app

### Step 1 — Copy the project to your computer

```bash
git clone https://github.com/[your-username]/ai-interview-simulation.git
cd ai-interview-simulation
```

### Step 2 — Make a clean Python space

```bash
python -m venv venv
```

### Step 3 — Turn on the clean Python space

**Windows:**
```bash
venv\Scripts\activate
```

**Mac / Linux:**
```bash
source venv/bin/activate
```

### Step 4 — Get all the tools

```bash
pip install -r requirements.txt
```

### Step 5 — Add your API key

Make a new file in the project folder. Call it `.env`. Write this inside:

```
GROQ_API_KEY=your_key_here
```

> You can get a free key here: [https://console.groq.com](https://console.groq.com)

### Step 6 — Start the app

```bash
streamlit run main.py
```

The app will open in your browser by itself.

---

## How to use the app

1. Open the app — it opens in your browser.
2. Upload your CV as a PDF file.
3. Paste the job text into the box.
4. Click "Start Interview".
5. The app asks you questions out loud — answer each one into your microphone.
6. When the interview is done, you will see a graph with your scores.

---

## Project files

```
ai-interview-simulation/
│
├── main.py                  # The main app file
├── requirements.txt         # List of all tools needed
├── .env                     # Your API key (do not share this!)
├── .gitignore
├── README.md
│
├── modules/
│   ├── pdf_reader.py        # Reads the CV file          → İlayda
│   ├── text_cleaner.py      # Cleans the job text        → İlayda
│   ├── ai_engine.py         # Talks to Groq AI           → Yarengül
│   ├── stt.py               # Voice to text              → Fırat Yunus
│   ├── tts.py               # Text to voice              → Fırat Yunus
│   ├── scorer.py            # Score and graph            → Yarengül & Cemre
│   └── ui.py                # Screen and buttons         → Cemre
│
└── tests/
    └── test_modules.py      # Test file                  → Nuhser
```

---

## How to run the tests

```bash
pytest tests/
```

---
# 🔑 API Key Documentation
## AI-Powered Interview Simulation — Groq API

---

## 1. Overview

| | |
|---|---|
| **API Provider** | Groq |
| **Model** | `llama-3.3-70b-versatile` |
| **Base URL** | `https://api.groq.com/openai/v1` |
| **Authentication** | API Key (Bearer Token) |
| **Environment Variable** | `GROQ_API_KEY` |
| **Loaded In** | `app/ai/gemini_client.py` |
| **Used In** | `app/ai/interview_engine.py` |
| **Cost** | Free (rate limits apply) |

---

## 2. How to Get the API Key

1. Go to [https://console.groq.com](https://console.groq.com)
2. Create a free account and confirm your email
3. Click **API Keys** in the left menu
4. Click **Create API Key** → give it any name (e.g. `interview-app`)
5. **Copy the key immediately** — it will not be shown again

---

## 3. Setting Up the Key

Create a `.env` file in the root folder of the project (same level as `main.py`):

```
GROQ_API_KEY=your_api_key_here
```

**Example:**
```
GROQ_API_KEY=gsk_abc123xyz456...
```

> ⚠️ Make sure `.env` is in your `.gitignore` — never upload it to GitHub.

---

## 4. How the Key is Used in the Code

### `app/ai/gemini_client.py` — Connection file

This file loads the key from `.env` and creates the Groq client object.
All other files in the project use this client.

```python
from groq import Groq
from dotenv import import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_client():
    return client
```

**What each line does:**

| Line | What it does |
|------|-------------|
| `load_dotenv()` | Reads the `.env` file and loads `GROQ_API_KEY` into memory |
| `os.getenv("GROQ_API_KEY")` | Gets the key value from the environment |
| `Groq(api_key=...)` | Creates the connection to Groq with that key |
| `get_client()` | Returns the client so other files can use it |

---

### `app/ai/interview_engine.py` — Where the API is called

This file has two functions that call the Groq API.

#### `start_interview()` — Starts the interview, asks the first question

```python
def start_interview(candidate_name: str, position: str, ...):
    system_prompt = build_system_prompt(candidate_name, ...)
    client = get_client()
    history = [{"role": "system", "content": system_prompt}]
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=history + [{"role": "user", "content": ...}],
        temperature=0.2,
        max_tokens=500,
    )
    
    first_question = response.choices[0].message.content
    history.append({"role": "assistant", "content": ...})
    return history, first_question
```

#### `send_answer()` — Sends user's answer, gets next question

```python
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
    clean = text.replace("```json", "").replace("```", "")
    history.append({"role": "assistant", "content": ...})
    
    if '"interview_finished": true' in clean:
        final_data = json.loads(clean)
        return None, True, final_data, history
```

---

## 5. API Parameters Explained

| Parameter | Value | Why |
|-----------|-------|-----|
| `model` | `llama-3.3-70b-versatile` | Large, capable model — gives smart interview questions |
| `temperature` | `0.2` | Low value = consistent, focused answers. Not too creative. Good for interviews. |
| `max_tokens` | `500` | Limits response length. Enough for one question or one score. |

---

## 6. Request & Response Flow

### What we send (Request)

```json
{
  "model": "llama-3.3-70b-versatile",
  "messages": [
    { "role": "system",    "content": "You are an HR interviewer. Use only the CV and job text..." },
    { "role": "user",      "content": "CV: ...\nJob: ...\nStart the interview." },
    { "role": "assistant", "content": "Tell me about your experience with Python." },
    { "role": "user",      "content": "I worked on a web scraping project using Python..." }
  ],
  "temperature": 0.2,
  "max_tokens": 500
}
```

> The full conversation `history` is sent every time — this is how the AI remembers what was already said.

### What we get back (Response)

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "That's interesting. Can you explain how you handled errors in that project?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 412,
    "completion_tokens": 28,
    "total_tokens": 440
  }
}
```

The part we use: `response.choices[0].message.content`

### When the interview ends

When all questions are done, the AI returns a JSON string inside the response:

```json
{
  "interview_finished": true,
  "scores": {
    "technical_competency": 8,
    "communication": 7,
    "problem_solving": 6,
    "experience_fit": 8,
    "motivation": 9
  },
  "feedback": "Strong technical background. Work on clearer communication.",
  "recommendation": "suitable"
}
```

The code detects `"interview_finished": true` and stops the interview.

---

## 7. Conversation History

The project keeps a `history` list that grows with every message:

```python
history = [
    {"role": "system",    "content": "You are an HR interviewer..."},
    {"role": "user",      "content": "CV: ...\nJob: ..."},
    {"role": "assistant", "content": "Question 1..."},
    {"role": "user",      "content": "User answer 1..."},
    {"role": "assistant", "content": "Question 2..."},
    ...
]
```

This full history is sent with every API call so the AI has context for the whole conversation.

---

## 8. Rate Limits (Free Tier)

| Limit | Value |
|-------|-------|
| Requests per minute | 30 |
| Tokens per minute | 6,000 |
| Tokens per day | 500,000 |

Each interview uses approximately **400–600 tokens per question**.
A 5-question interview uses roughly **2,000–3,000 tokens** total.

---

## 9. Error Codes

| Code | Error | Cause | Fix |
|------|-------|-------|-----|
| `401` | Unauthorized | Wrong or missing API key | Check `GROQ_API_KEY` in `.env` |
| `429` | Rate limit exceeded | Too many requests | Wait 1 minute and try again |
| `400` | Bad request | Empty or too-long message | Check what is being sent to the API |
| `500` | Server error | Groq side issue | Wait a few minutes and retry |

---

## 10. Security

- ✅ Key is stored in `.env` — not in any Python file
- ✅ Key is loaded with `load_dotenv()` + `os.getenv()`
- ✅ `.env` must be listed in `.gitignore`
- ❌ Never hardcode the key directly in `gemini_client.py` or any other file
- ❌ Never print the key in the terminal

**If the key is exposed:**
1. Go to [console.groq.com](https://console.groq.com) → API Keys
2. Delete the exposed key immediately
3. Create a new key
4. Update your `.env` file

---

## 11. File Map

```
app/
└── ai/
    ├── gemini_client.py    ← loads key, creates Groq client
    ├── interview_engine.py ← calls the API (start_interview, send_answer)
    ├── prompts.py          ← builds the system prompt sent to the API
    ├── scoring.py          ← handles the final score JSON from the API
    ├── pipeline.py         ← manages the full interview flow
    └── test_connection.py  ← tests if the API key works
```

---

## 12. Testing the Connection

Run this to check if your API key works:

```bash
python app/ai/test_connection.py
```

If the key is correct, you will see a response from the model in the terminal.
If you see a `401` error, the key in your `.env` file is wrong.


## Who made this?

This app was made by 5 students for the YMH220/YMH210 Python class.

| Name | Student ID | Role |
|------|-----------|------|
| Cemre YURTSEVER | 250541127 | Screen & Design |
| İlayda MEMİŞ | 240541109 | Data & Text |
| Fırat Yunus YAŞAROĞLU | 240541017 | Voice |
| Yarengül KOCAOĞLU | 240541013 | AI & Questions |
| Nuhser ATALA | 240541033 | Putting it together + Scrum Master |
