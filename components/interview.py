import streamlit as st
import time
import hashlib
from app.audio.audio import text_to_speech, process_audio_data
from app.ai.gemini_client import get_client
from app.ai.prompts import build_system_prompt


def mock_question():
    return "Tell me about yourself"


def render_interview_section():

    # ---------- GUARD: sadece interview page'indeyken render et ----------
    if st.session_state.get("page") != "interview":
        return

    # ---------- STATE ----------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "last_audio_hash" not in st.session_state:
        st.session_state.last_audio_hash = None
    if "audio_key" not in st.session_state:
        st.session_state.audio_key = 0
    if "confirm_finish" not in st.session_state:
        st.session_state.confirm_finish = False

    mode = st.session_state.get("interview_mode", "text")

    # ---------- STYLE ----------
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

    .stApp {
        background:
            radial-gradient(ellipse 80% 50% at 20% 10%, rgba(79,70,229,0.18) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 80%, rgba(16,185,129,0.10) 0%, transparent 55%),
            linear-gradient(160deg, #070b14 0%, #0c1022 40%, #080d1a 100%);
        min-height: 100vh;
    }

    #MainMenu, footer, header { visibility: hidden !important; }
    .stDeployButton, [data-testid="stToolbar"],
    [data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }

    .block-container {
        max-width: 860px !important;
        margin: auto;
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
    }

    /* ── HEADER ── */
    .iv-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 20px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 28px;
    }
    .iv-title {
        font-family: 'Syne', sans-serif;
        font-size: 30px;
        font-weight: 800;
        color: white;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .iv-title .accent { color: #4ade80; }
    .mode-pill {
        background: rgba(74,222,128,0.08);
        border: 1px solid rgba(74,222,128,0.22);
        color: #4ade80;
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        padding: 5px 13px;
        border-radius: 20px;
    }

    /* ── BACK BUTTON ── */
    .back-btn > div > button {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        color: rgba(255,255,255,0.55) !important;
        border-radius: 10px !important;
        font-size: 13px !important;
        padding: 4px 14px !important;
        height: 34px !important;
        min-height: unset !important;
        width: auto !important;
        transition: all 0.2s ease !important;
    }
    .back-btn > div > button:hover {
        background: rgba(255,255,255,0.09) !important;
        color: white !important;
    }

    /* ── CHAT ── */
    .chat-row-ai {
        display: flex; align-items: flex-start; gap: 14px;
        margin-bottom: 16px;
        animation: fadeSlideUp 0.4s ease both;
    }
    .chat-row-user {
        display: flex; align-items: flex-start;
        flex-direction: row-reverse; gap: 14px;
        margin-bottom: 16px;
        animation: fadeSlideUp 0.4s ease both;
    }
    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .avatar {
        width: 42px; height: 42px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 20px; flex-shrink: 0; margin-top: 2px;
    }
    .avatar-ai {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        box-shadow: 0 0 22px rgba(124,58,237,0.5), 0 4px 12px rgba(0,0,0,0.4);
    }
    .avatar-user {
        background: rgba(74,222,128,0.10);
        border: 1px solid rgba(74,222,128,0.28);
        box-shadow: 0 0 14px rgba(74,222,128,0.15);
    }
    .bubble-wrap { display: flex; flex-direction: column; max-width: 70%; }
    .bubble-wrap-user { align-items: flex-end; }
    .sender-label {
        font-size: 10px; font-weight: 700; letter-spacing: 0.10em;
        text-transform: uppercase; color: rgba(255,255,255,0.3);
        margin-bottom: 6px; padding: 0 4px;
    }
    .chat-bubble {
        padding: 18px 22px; border-radius: 20px;
        font-size: 15.5px; line-height: 1.65; color: white; word-wrap: break-word;
    }
    .bubble-ai {
        background: linear-gradient(135deg, #1e1b4b 0%, #2d2a6e 100%);
        border: 1px solid rgba(139,92,246,0.22);
        border-bottom-left-radius: 5px;
        box-shadow: 0 8px 32px rgba(79,70,229,0.22), 0 2px 8px rgba(0,0,0,0.4),
                    inset 0 1px 0 rgba(255,255,255,0.06);
    }
    .bubble-user {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.10);
        border-bottom-right-radius: 5px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.3);
    }
    .q-divider {
        display: flex; align-items: center; gap: 12px; margin: 24px 0;
    }
    .q-divider-line {
        flex: 1; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent);
    }
    .q-divider-label {
        font-size: 10.5px; font-weight: 600; letter-spacing: 0.10em;
        text-transform: uppercase; color: rgba(255,255,255,0.18); white-space: nowrap;
    }

    /* ── VOICE RECORDER ── */
    .voice-panel {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(74,222,128,0.12);
        border-radius: 20px;
        padding: 28px 28px 22px;
        margin-top: 20px;
    }
    .voice-panel-title {
        font-size: 10px; font-weight: 700; letter-spacing: 0.14em;
        text-transform: uppercase; color: rgba(74,222,128,0.6);
        margin-bottom: 18px;
    }
    .mic-status {
        display: flex; align-items: center; gap: 12px;
        margin-bottom: 16px;
        color: rgba(255,255,255,0.38); font-size: 13px;
    }
    .pulse-ring {
        position: relative; width: 14px; height: 14px; flex-shrink: 0;
    }
    .pulse-ring::before {
        content: ''; position: absolute; inset: 0;
        border-radius: 50%; background: #4ade80;
        animation: pulseDot 1.8s ease infinite;
        box-shadow: 0 0 10px rgba(74,222,128,0.7);
    }
    @keyframes pulseDot {
        0%, 100% { transform: scale(1); opacity: 1; }
        50%       { transform: scale(0.55); opacity: 0.3; }
    }

    /* audio_input widget güzelleştirme */
    [data-testid="stAudioInput"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 14px !important;
        padding: 6px !important;
    }
    [data-testid="stAudioInput"] > label {
        color: rgba(255,255,255,0.3) !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
    }

    /* ── CHAT INPUT ── */
    .stChatInput > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 14px !important;
        margin-top: 20px !important;
    }
    .stChatInput textarea {
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14.5px !important;
    }

    /* ── AUDIO PLAYER ── */
    .stAudio { margin-top: 10px; opacity: 0.72; }

    /* ── FINISH BUTTON ── */
    .finish-zone {
        margin-top: 36px;
        padding-top: 20px;
        border-top: 1px solid rgba(255,255,255,0.05);
        display: flex;
        justify-content: flex-end;
    }
    .finish-btn > div > button {
        background: transparent !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        color: rgba(255,255,255,0.35) !important;
        border-radius: 10px !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        letter-spacing: 0.05em !important;
        padding: 6px 18px !important;
        height: 34px !important;
        min-height: unset !important;
        transition: all 0.25s ease !important;
    }
    .finish-btn > div > button:hover {
        border-color: rgba(239,68,68,0.45) !important;
        color: rgba(239,68,68,0.75) !important;
        background: rgba(239,68,68,0.06) !important;
    }

    /* ── CONFIRM MODAL ── */
    .confirm-overlay {
        margin-top: 12px;
        background: rgba(10,12,28,0.95);
        border: 1px solid rgba(239,68,68,0.2);
        border-radius: 18px;
        padding: 28px 28px 22px;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.6);
        animation: fadeSlideUp 0.25s ease both;
    }
    .confirm-title {
        font-family: 'Syne', sans-serif;
        font-size: 17px; font-weight: 700; color: white;
        margin-bottom: 8px;
    }
    .confirm-desc {
        font-size: 13px; color: rgba(255,255,255,0.38);
        line-height: 1.6; margin-bottom: 22px;
    }
    .confirm-actions { display: flex; gap: 10px; justify-content: flex-end; }

    /* Yes/Confirm button */
    .confirm-yes > div > button {
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        border: none !important;
        color: white !important;
        border-radius: 10px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        padding: 6px 22px !important;
        height: 36px !important;
        min-height: unset !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 16px rgba(239,68,68,0.35) !important;
    }
    .confirm-yes > div > button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 6px 24px rgba(239,68,68,0.5) !important;
    }

    /* Cancel button */
    .confirm-no > div > button {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        color: rgba(255,255,255,0.55) !important;
        border-radius: 10px !important;
        font-size: 13px !important;
        padding: 6px 22px !important;
        height: 36px !important;
        min-height: unset !important;
        transition: all 0.2s ease !important;
    }
    .confirm-no > div > button:hover {
        background: rgba(255,255,255,0.10) !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------- HEADER ----------
    col_back, col_head = st.columns([1, 9])
    with col_back:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← Back", key="iv_back"):
            st.session_state.page = "mode"
            st.session_state.chat_history = []
            st.session_state.confirm_finish = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_head:
        mode_icon  = "🎤" if mode == "voice" else "✍️"
        mode_label = "VOICE MODE" if mode == "voice" else "TEXT MODE"
        st.markdown(f"""
        <div class="iv-header">
            <div class="iv-title">💬 Interview <span class="accent">Session</span></div>
            <div class="mode-pill">{mode_icon}&nbsp;{mode_label}</div>
        </div>
        """, unsafe_allow_html=True)

    # ---------- FIRST QUESTION ----------
    if len(st.session_state.chat_history) == 0:
        first_q = mock_question()
        audio_data = None
        if mode == "voice":
            audio_data = text_to_speech(first_q)
        st.session_state.chat_history.append(("AI", first_q, audio_data))

    # ---------- RENDER CHAT ----------
    ai_count = 0
    for item in st.session_state.chat_history:
        sender = item[0]
        msg    = item[1]
        audio  = item[2] if len(item) == 3 else None

        if sender == "AI":
            if ai_count > 0:
                st.markdown(f"""
                <div class="q-divider">
                    <div class="q-divider-line"></div>
                    <div class="q-divider-label">Question {ai_count + 1}</div>
                    <div class="q-divider-line"></div>
                </div>
                """, unsafe_allow_html=True)
            ai_count += 1

            st.markdown(f"""
            <div class="chat-row-ai">
                <div class="avatar avatar-ai">🤖</div>
                <div class="bubble-wrap">
                    <div class="sender-label">Interviewer</div>
                    <div class="chat-bubble bubble-ai">{msg}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if audio:
                st.audio(audio, format="audio/mp3")

        else:
            st.markdown(f"""
            <div class="chat-row-user">
                <div class="avatar avatar-user">🧑</div>
                <div class="bubble-wrap bubble-wrap-user">
                    <div class="sender-label">You</div>
                    <div class="chat-bubble bubble-user">{msg}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # auto-scroll
    st.markdown("""
    <div id="iv-bottom"></div>
    <script>
        (function(){
            var el = document.getElementById('iv-bottom');
            if(el) el.scrollIntoView({behavior:'smooth',block:'end'});
        })();
    </script>
    """, unsafe_allow_html=True)

    # ---------- INPUT ----------
    user_input = None

    if mode == "text":
        user_input = st.chat_input("Type your answer here…")

    else:
        st.markdown("""
        <div class="voice-panel">
            <div class="voice-panel-title">🎙 Your Answer</div>
            <div class="mic-status">
                <div class="pulse-ring"></div>
                Speak clearly — recording starts when you click the mic
            </div>
        </div>
        """, unsafe_allow_html=True)

        audio = st.audio_input(
            "Record your answer",
            key=f"audio_{st.session_state.audio_key}"
        )

        if audio is not None:
            audio_bytes = audio.getvalue()
            audio_hash  = hashlib.md5(audio_bytes).hexdigest()

            if audio_hash != st.session_state.last_audio_hash:
                st.session_state.last_audio_hash = audio_hash
                user_input = process_audio_data(audio_bytes)

                if user_input is None:
                    st.warning("⚠️ Could not understand audio. Please try again.")

    # ---------- PROCESS RESPONSE ----------
    if user_input:
        st.session_state.chat_history.append(("You", user_input))
        time.sleep(1)

        client = get_client()

        system_prompt = build_system_prompt(
            st.session_state.get("candidate_name", "Candidate"),
            st.session_state.get("position", "Software Engineer"),
            st.session_state.get("job_text", ""),
            st.session_state.get("cv_text", "")
        )

        messages = [{"role": "system", "content": system_prompt}]

        for item in st.session_state.chat_history:
            role = "assistant" if item[0] == "AI" else "user"
            messages.append({"role": role, "content": item[1]})

        messages.append({
            "role": "user",
            "content": "Ask the next interview question based on previous answers."
        })

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.2,
            max_tokens=500
        )

        ai_response = response.choices[0].message.content
        audio_data  = text_to_speech(ai_response) if mode == "voice" else None

        st.session_state.chat_history.append(("AI", ai_response, audio_data))
        st.session_state.audio_key += 1
        st.rerun()

    # ---------- FINISH ZONE ----------
    st.markdown('<div class="finish-zone">', unsafe_allow_html=True)
    st.markdown('<div class="finish-btn">', unsafe_allow_html=True)
    if st.button("End Interview", key="finish_btn"):
        st.session_state.confirm_finish = True
    st.markdown('</div></div>', unsafe_allow_html=True)

    # ---------- CONFIRM MODAL ----------
    if st.session_state.confirm_finish:
        st.markdown("""
        <div class="confirm-overlay">
            <div class="confirm-title">End this interview?</div>
            <div class="confirm-desc">
                Your answers will be scored and a full report will be generated.<br>
                You won't be able to add more answers after this.
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_gap, col_no, col_yes = st.columns([4, 1.2, 1.2])

        with col_no:
            st.markdown('<div class="confirm-no">', unsafe_allow_html=True)
            if st.button("Cancel", key="confirm_cancel"):
                st.session_state.confirm_finish = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col_yes:
            st.markdown('<div class="confirm-yes">', unsafe_allow_html=True)
            if st.button("Finish ✓", key="confirm_yes"):
                from app.ui.components.score_ui import render_score_ui
                from app.ai.scoring import generate_scores_from_history

                formatted_history = []
                current_q = None
                for item in st.session_state.chat_history:
                    if item[0] == "AI":
                        current_q = item[1]
                    elif item[0] == "You" and current_q:
                        formatted_history.append({
                            "question": current_q,
                            "answer": item[1]
                        })

                result = generate_scores_from_history(
                    formatted_history,
                    st.session_state.get("position", "Software Engineer"),
                    st.session_state.get("candidate_name", "Candidate")
                )

                st.session_state.score_result = result
                st.session_state.page = "score"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)