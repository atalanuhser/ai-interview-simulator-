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
#  API Key Documentation

## AI-Powered Interview Simulation

### Groq API — Technical Reference

-----

## 1. Overview

|                  |                                |
|------------------|--------------------------------|
|**API Provider**  |Groq                            |
|**API Type**      |REST                            |
|**Base URL**      |`https://api.groq.com/openai/v1`|
|**Model Used**    |`llama3-8b-8192`                |
|**Authentication**|Bearer Token (API Key)          |
|**Cost**          |Free (with rate limits)         |
|**Official Docs** |<https://console.groq.com/docs> |

-----

## 2. How to Get Your API Key

1. Go to <https://console.groq.com>
1. Click **Sign Up** → create a free account
1. Confirm your email address
1. After login, click **API Keys** in the left menu
1. Click **Create API Key** → give it a name (e.g. `interview-app`)
1. **Copy the key immediately** — it will not be shown again

-----

## 3. Where the Key Lives in the Project

The key is stored in a `.env` file in the root folder of the project:

```
ai-interview-simulation/
├── .env              ← key goes here
├── main.py
├── .gitignore        ← .env must be listed here
```

**`.env` file content:**

```env
GROQ_API_KEY=your_api_key_here
```

** Never commit `.env` to GitHub.**
Make sure your `.gitignore` contains:

```
.env
```

-----

## 4. How the Key is Loaded in the Code

The project uses the `python-dotenv` library to read the key from the `.env` file.

**In `ai_engine.py`:**

```python
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)
```

-----

## 5. How the API is Used

### 5.1 Generating Interview Questions

The CV text and job description are sent to the API. The model returns interview questions.

```python
def generate_questions(cv_text: str, job_text: str) -> str:
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are a professional HR interviewer. Ask questions based only on the CV and job description provided."
            },
            {
                "role": "user",
                "content": f"CV:\n{cv_text}\n\nJob Description:\n{job_text}\n\nGenerate 5 interview questions."
            }
        ],
        max_tokens=1024,
        temperature=0.7
    )
    return response.choices[0].message.content
```

### 5.2 Evaluating User Answers

After the interview, answers are sent back to the API for scoring.

```python
def evaluate_answer(question: str, answer: str) -> dict:
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are an HR evaluator. Score the answer from 0 to 10 and give short feedback."
            },
            {
                "role": "user",
                "content": f"Question: {question}\nAnswer: {answer}\n\nReturn a JSON with: score (0-10), feedback (1 sentence)."
            }
        ],
        max_tokens=256,
        temperature=0.3
    )
    return response.choices[0].message.content
```

-----

## 6. API Request & Response Structure

### Request (what we send)

```json
{
  "model": "llama3-8b-8192",
  "messages": [
    { "role": "system", "content": "You are a professional HR interviewer..." },
    { "role": "user",   "content": "CV: ...\nJob: ...\nGenerate 5 questions." }
  ],
  "max_tokens": 1024,
  "temperature": 0.7
}
```

### Response (what we get back)

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "model": "llama3-8b-8192",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "1. Can you walk me through your experience with Python?\n2. ..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 312,
    "completion_tokens": 180,
    "total_tokens": 492
  }
}
```

The content we use: `response.choices[0].message.content`

-----

## 7. Rate Limits (Free Tier)

|Limit              |Value |
|-------------------|------|
|Requests per minute|30    |
|Tokens per minute  |14,400|
|Tokens per day     |14,400|
|Requests per day   |14,400|


> These limits apply to the free tier as of 2025. Check [console.groq.com](https://console.groq.com) for current limits.

-----

## 8. Error Codes

|HTTP Code|Error                |Cause                          |Fix                                  |
|---------|---------------------|-------------------------------|-------------------------------------|
|`401`    |`Unauthorized`       |API key is wrong or missing    |Check the key in your `.env` file    |
|`429`    |`Rate limit exceeded`|Too many requests              |Wait and try again, or use a new key |
|`400`    |`Bad request`        |The prompt is empty or too long|Check what you are sending to the API|
|`500`    |`Server error`       |Groq side problem              |Wait a few minutes and try again     |

**Error handling in code:**

```python
try:
    response = client.chat.completions.create(...)
except Exception as e:
    print(f"API Error: {e}")
```

-----

## 9. Model Parameters

|Parameter    |Value Used                          |What it does                                   |
|-------------|------------------------------------|-----------------------------------------------|
|`model`      |`llama3-8b-8192`                    |The AI model — fast and free                   |
|`max_tokens` |`1024` (questions) / `256` (scoring)|Max length of the response                     |
|`temperature`|`0.7` (questions) / `0.3` (scoring) |Higher = more creative. Lower = more consistent|

-----

## 10. Security Rules

- ✅ Store the key in `.env` only
- ✅ Add `.env` to `.gitignore`
- ❌ Never hardcode the key in Python files
- ❌ Never share the key in chat, email, or GitHub
- ❌ Never print the key in the terminal or logs

**If your key is exposed:**

1. Go to [console.groq.com](https://console.groq.com)
1. Click **API Keys**
1. **Delete** the exposed key
1. Create a new one
1. Update your `.env` file

-----

## 11. Useful Links

|Resource        |Link                                                                          |
|----------------|------------------------------------------------------------------------------|
|Groq Console    |[console.groq.com](https://console.groq.com)                                  |
|Groq API Docs   |[console.groq.com/docs](https://console.groq.com/docs)                        |
|Groq Models List|[console.groq.com/docs/models](https://console.groq.com/docs/models)          |
|Groq Rate Limits|[console.groq.com/docs/rate-limits](https://console.groq.com/docs/rate-limits)|
|Python Groq SDK |[pypi.org/project/groq](https://pypi.org/project/groq/)                       |

## What we did each week

| Sprint | Weeks | What we finished |
|--------|-------|------------------|
| Sprint 1 | 1–2 | App opens. PDF upload works. API is connected. |
| Sprint 2 | 3–4–5 | Voice tools, data tools, and AI all work on their own. |
| Sprint 3 | 6–7 | All parts work together. A full interview works from start to end. |
| Sprint 4 | 8 | Tests done. Errors fixed. App is clean and ready to hand in. |

---

## Who made this?

This app was made by 5 students for the YMH220/YMH210 Python class.

| Name | Student ID | Role |
|------|-----------|------|
| Cemre YURTSEVER | 250541127 | Screen & Design |
| İlayda MEMİŞ | 240541109 | Data & Text |
| Fırat Yunus YAŞAROĞLU | 240541017 | Voice |
| Yarengül KOCAOĞLU | 240541013 | AI & Questions |
| Nuhser ATALA | 240541033 | Putting it together + Scrum Master |
