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
