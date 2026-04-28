# AI Interview Simulator

YMH220/YMH210 Python Course Project — AI-powered interview simulation that prepares recent graduates and internship seekers for job interviews based on their CVs.

## Team

- Cemre YURTSEVER — UI & Visualization (Streamlit, Plotly)
- İlayda MEMİŞ — Data & Backend (PyPDF2, BeautifulSoup4)
- Fırat Yunus YAŞAROĞLU — Audio & Speech (SpeechRecognition, gTTS)
- Yarengül KOCAOĞLU — AI & Prompt Engineering (Gemini API)
- Nuhser ATALA — Integration & QA (Scrum Master)

## Tech Stack

- Python 3.12+
- Streamlit (UI)
- PyPDF2, BeautifulSoup4 (data processing)
- SpeechRecognition, gTTS (audio)
- google-generativeai (AI)
- Plotly, Pandas (visualization)
- pytest (testing)

## Setup

1. Clone the repository:
   git clone https://github.com/atalanuhser/ai-interview-simulator-.git

2. Enter the folder:
   cd ai-interview-simulator-

3. Create a virtual environment:
   python -m venv venv

4. Activate the virtual environment:
   - Windows: venv\Scripts\activate
   - Mac/Linux: source venv/bin/activate

5. Install dependencies:
   pip install -r requirements.txt

6. Create a .env file in the root with your API key:
   GEMINI_API_KEY=your_key_here

7. Run the app:
   streamlit run app.py
