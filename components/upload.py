import streamlit as st
import streamlit.components.v1 as components
from app.ai.pdf_reader import parse_cv, parse_job_description
from app.ai.interview_engine import start_interview


RIGHT_CARD_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
  *{box-sizing:border-box;margin:0;padding:0;}
  body{background:transparent;font-family:'DM Sans',sans-serif;color:#fff;padding:4px 2px;}

  .card{background:rgba(8,11,35,.88);border:1px solid rgba(255,255,255,.08);border-radius:28px;padding:40px 36px;position:relative;overflow:hidden;transition:border-color .4s,box-shadow .4s;animation:fadeUp .7s ease both;}
  .card:hover{border-color:rgba(99,102,241,.3);box-shadow:0 0 60px rgba(99,102,241,.2);}
  .orb1{position:absolute;top:-70px;right:-70px;width:220px;height:220px;border-radius:50%;background:radial-gradient(circle,rgba(99,102,241,.22),transparent 70%);pointer-events:none;animation:orbP 4s ease-in-out infinite alternate;}
  .orb2{position:absolute;bottom:-60px;left:-60px;width:180px;height:180px;border-radius:50%;background:radial-gradient(circle,rgba(16,185,129,.18),transparent 70%);pointer-events:none;animation:orbP 5s 1s ease-in-out infinite alternate;}
  @keyframes orbP{to{transform:scale(1.35);opacity:.65;}}
  .inner{position:relative;z-index:1;animation:floatY 5s ease-in-out infinite;}
  @keyframes floatY{0%,100%{transform:translateY(0);}50%{transform:translateY(-8px);}}
  .title{font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:#fff;line-height:1.25;margin-bottom:10px;}
  .sub{font-size:14px;color:rgba(255,255,255,.36);font-weight:300;line-height:1.6;margin-bottom:28px;}
  .shimmer{height:2px;border-radius:2px;margin-bottom:24px;background:linear-gradient(90deg,transparent,rgba(99,102,241,.6),rgba(52,211,153,.4),transparent);background-size:200%;animation:shimmerMove 3s linear infinite;}
  @keyframes shimmerMove{to{background-position:200%;}}
  .feature{display:flex;align-items:flex-start;gap:14px;padding:16px 18px;border-radius:14px;background:rgba(99,102,241,.07);border:1px solid rgba(99,102,241,.12);margin-bottom:11px;transition:background .3s,border-color .3s,transform .3s;cursor:default;}
  .feature:hover{background:rgba(99,102,241,.15);border-color:rgba(99,102,241,.28);transform:translateX(5px);}
  .f-icon{font-size:22px;flex-shrink:0;margin-top:2px;}
  .f-title{font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:#c7d2fe;margin-bottom:4px;}
  .f-desc{font-size:12px;color:rgba(255,255,255,.35);font-weight:300;line-height:1.55;}
  .footer-banner{margin-top:20px;padding:18px 20px;border-radius:14px;background:linear-gradient(135deg,rgba(99,102,241,.12),rgba(16,185,129,.08));border:1px solid rgba(99,102,241,.2);}
  .footer-title{font-family:'Syne',sans-serif;font-size:15px;font-weight:700;background:linear-gradient(135deg,#818cf8,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:5px;}
  .footer-sub{font-size:12px;color:rgba(255,255,255,.3);font-weight:300;line-height:1.5;}
  @keyframes fadeUp{from{opacity:0;transform:translateY(20px);}to{opacity:1;transform:translateY(0);}}
</style>
</head>
<body>
<div class="card">
  <div class="orb1"></div><div class="orb2"></div>
  <div class="inner">
    <div class="title">&#129302; AI Interview<br>Simulator</div>
    <div class="sub">Practice smarter, not harder.<br>Your personal AI interviewer awaits.</div>
    <div class="shimmer"></div>
    <div class="feature"><div class="f-icon">&#10024;</div><div><div class="f-title">AI-Generated Questions</div><div class="f-desc">Questions crafted from your CV and the job description — no generic templates.</div></div></div>
    <div class="feature"><div class="f-icon">&#127908;</div><div><div class="f-title">Voice &amp; Text Interaction</div><div class="f-desc">Choose your preferred mode — speak naturally or type with full flexibility.</div></div></div>
    <div class="feature"><div class="f-icon">&#127919;</div><div><div class="f-title">Real Interview Simulation</div><div class="f-desc">Adaptive follow-ups, realistic pacing, and instant AI feedback.</div></div></div>
    <div class="footer-banner">
      <div class="footer-title">&#128640; Get ready for your dream job</div>
      <div class="footer-sub">Thousands of candidates improved with AI-powered practice sessions.</div>
    </div>
  </div>
</div>
</body>
</html>"""


def render_upload_section():

    st.set_page_config(layout="wide")

    st.markdown(
        "<style>"
        "@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');"
        "header,footer,#MainMenu{visibility:hidden!important;}"
        ".block-container{max-width:1350px!important;padding-top:0!important;padding-bottom:0!important;}"
        ".stApp{background:#050816!important;font-family:'DM Sans',sans-serif;}"

        # Aurora blobs
        ".ua1,.ua2,.ua3{position:fixed;border-radius:50%;filter:blur(110px);pointer-events:none;z-index:0;}"
        ".ua1{width:700px;height:700px;background:radial-gradient(circle,rgba(99,102,241,.35),transparent 70%);top:-220px;left:-180px;animation:ud1 18s ease-in-out infinite alternate;}"
        ".ua2{width:580px;height:580px;background:radial-gradient(circle,rgba(16,185,129,.22),transparent 70%);bottom:-160px;right:-160px;animation:ud2 22s ease-in-out infinite alternate;}"
        ".ua3{width:400px;height:400px;background:radial-gradient(circle,rgba(244,114,182,.18),transparent 70%);top:50%;left:38%;transform:translate(-50%,-50%);animation:ud3 14s ease-in-out infinite alternate;}"
        "@keyframes ud1{to{transform:translate(90px,60px);}}"
        "@keyframes ud2{to{transform:translate(-70px,-80px);}}"
        "@keyframes ud3{to{transform:translate(-50%,-50%) scale(1.45);}}"

        # Grid
        ".ugrid{position:fixed;inset:0;z-index:0;pointer-events:none;"
        "background-image:linear-gradient(rgba(99,102,241,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(99,102,241,.05) 1px,transparent 1px);"
        "background-size:60px 60px;"
        "-webkit-mask-image:radial-gradient(ellipse 85% 85% at 50% 50%,black 20%,transparent 100%);}"

        # Page header
        ".uhead{text-align:center;margin-bottom:52px;animation:ufd .7s ease both;position:relative;z-index:10;}"
        ".ubadge{display:inline-flex;align-items:center;gap:8px;padding:6px 20px;border-radius:100px;"
        "border:1px solid rgba(99,102,241,.5);background:rgba(99,102,241,.10);"
        "font-size:11px;letter-spacing:.13em;text-transform:uppercase;color:#a5b4fc;margin-bottom:20px;}"
        ".udot{width:6px;height:6px;border-radius:50%;background:#6366f1;box-shadow:0 0 7px #6366f1;animation:upulse 2s ease-in-out infinite;display:inline-block;}"
        "@keyframes upulse{0%,100%{opacity:1;transform:scale(1);}50%{opacity:.35;transform:scale(.55);}}"
        ".uh1{font-family:'Syne',sans-serif;font-size:clamp(28px,3.5vw,48px);font-weight:800;color:#fff;line-height:1.15;}"
        ".uh1 span{background:linear-gradient(135deg,#818cf8 0%,#34d399 55%,#f472b6 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;background-size:300%;animation:ugrad 6s ease infinite;}"
        "@keyframes ugrad{0%,100%{background-position:0% 50%;}50%{background-position:100% 50%;}}"
        ".usub{font-size:15px;color:rgba(255,255,255,.35);font-weight:300;margin-top:12px;}"

        # Section label
        ".ulabel{font-family:'Syne',sans-serif;font-size:11px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;"
        "display:flex;align-items:center;gap:8px;"
        "margin-top:0;margin-bottom:12px;}"   # margin controlled by wrapper padding
        ".ulabel-t{color:#a5b4fc;}"
        ".ulabel-g{color:#6ee7b7;}"
        ".ulabel-b{color:#93c5fd;}"

        # Section wrapper — gives breathing room between sections
        ".usec{padding:28px 0 0;}"
        ".usec:first-child{padding-top:0;}"

        # Gradient separator
        ".uhr{height:1px;border:none;margin:32px 0;"
        "background:linear-gradient(90deg,rgba(99,102,241,.28),rgba(255,255,255,.05),transparent);}"

        # Layout
        "section.main>div.block-container>div{position:relative;z-index:10;}"
        "div[data-testid='stVerticalBlock']{gap:0px!important;}"
        "[data-testid='column']:first-child{padding-right:20px!important;}"
        "[data-testid='column']:last-child{padding-left:20px!important;}"

        # Text input — bigger, more padding
        "[data-testid='stTextInput'] label{display:none!important;}"
        "[data-testid='stTextInput'] input{"
        "background:rgba(15,20,50,.75)!important;"
        "border:1px solid rgba(99,102,241,.22)!important;"
        "border-radius:14px!important;color:#fff!important;"
        "font-family:'DM Sans',sans-serif!important;"
        "font-size:15px!important;"
        "padding:14px 18px!important;"
        "transition:border-color .3s,box-shadow .3s!important;}"
        "[data-testid='stTextInput'] input:focus{"
        "border-color:rgba(99,102,241,.75)!important;"
        "box-shadow:0 0 0 3px rgba(99,102,241,.15),0 0 20px rgba(99,102,241,.25)!important;"
        "background:rgba(15,20,60,.9)!important;}"
        "[data-testid='stTextInput'] input::placeholder{color:rgba(255,255,255,.22)!important;}"

        # Text area
        "[data-testid='stTextArea'] label{display:none!important;}"
        "[data-testid='stTextArea'] textarea{"
        "background:rgba(15,20,50,.75)!important;"
        "border:1px solid rgba(99,102,241,.22)!important;"
        "border-radius:14px!important;color:#fff!important;"
        "font-family:'DM Sans',sans-serif!important;"
        "font-size:15px!important;min-height:110px!important;"
        "padding:14px 18px!important;"
        "transition:border-color .3s,box-shadow .3s!important;}"
        "[data-testid='stTextArea'] textarea:focus{"
        "border-color:rgba(99,102,241,.75)!important;"
        "box-shadow:0 0 0 3px rgba(99,102,241,.15),0 0 20px rgba(99,102,241,.25)!important;}"
        "[data-testid='stTextArea'] textarea::placeholder{color:rgba(255,255,255,.22)!important;}"

        # File uploader
        "[data-testid='stFileUploader']{"
        "background:rgba(15,20,50,.5)!important;"
        "border:1px dashed rgba(99,102,241,.28)!important;"
        "border-radius:16px!important;padding:14px!important;"
        "transition:border-color .3s,box-shadow .3s!important;}"
        "[data-testid='stFileUploader']:hover{border-color:rgba(99,102,241,.6)!important;box-shadow:0 0 18px rgba(99,102,241,.18)!important;}"
        "[data-testid='stFileUploader'] label{color:rgba(255,255,255,.35)!important;font-family:'DM Sans',sans-serif!important;font-size:13px!important;}"
        "[data-testid='stFileUploader'] button{background:linear-gradient(135deg,#4f46e5,#7c3aed)!important;border:none!important;border-radius:10px!important;color:#fff!important;font-family:'DM Sans',sans-serif!important;font-size:13px!important;}"
        "[data-testid='stFileUploader'] button:hover{box-shadow:0 0 18px rgba(99,102,241,.45)!important;}"

        # Radio
        "[data-testid='stRadio']{margin-top:10px!important;margin-bottom:18px!important;}"
        "[data-testid='stRadio'] label{color:rgba(255,255,255,.6)!important;font-family:'DM Sans',sans-serif!important;font-size:14px!important;}"

        # Start button
        "[data-testid='stButton']>button{"
        "width:100%!important;padding:16px 24px!important;"
        "border-radius:14px!important;"
        "background:linear-gradient(135deg,#4f46e5,#7c3aed)!important;"
        "border:none!important;color:#fff!important;"
        "font-family:'Syne',sans-serif!important;"
        "font-size:16px!important;font-weight:700!important;"
        "letter-spacing:.04em!important;cursor:pointer!important;"
        "transition:transform .25s ease,box-shadow .3s ease!important;}"
        "[data-testid='stButton']>button:hover{transform:translateY(-3px)!important;box-shadow:0 0 40px rgba(99,102,241,.6),0 8px 28px rgba(0,0,0,.4)!important;}"
        "[data-testid='stButton']>button:focus{outline:none!important;box-shadow:none!important;}"

        # misc
        "hr{background:rgba(99,102,241,.18)!important;margin:8px 0!important;}"
        "@keyframes ufd{from{opacity:0;transform:translateY(-18px);}to{opacity:1;transform:translateY(0);}}"
        "</style>",
        unsafe_allow_html=True,
    )

    # Background elements
    st.markdown(
        '<div class="ua1"></div>'
        '<div class="ua2"></div>'
        '<div class="ua3"></div>'
        '<div class="ugrid"></div>',
        unsafe_allow_html=True,
    )

    # Header
    st.markdown(
        '<div class="uhead">'
        '<div class="ubadge"><span class="udot"></span>&nbsp;AI Interview Simulator</div>'
        '<div class="uh1">Set Up Your <span>Interview Session</span></div>'
        '<div class="usub">Fill in your details and let AI craft a personalized interview for you</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1.05, 0.95], gap="small")

    with col1:

        # ── Personal Info ────────────────────────────────────────────────
        st.markdown('<div class="ulabel ulabel-t">&#128100;&nbsp; Personal Info</div>', unsafe_allow_html=True)
        name = st.text_input("n", placeholder="e.g. Alex Johnson", label_visibility="collapsed")

        st.markdown('<div class="uhr"></div>', unsafe_allow_html=True)

        # ── Upload CV ────────────────────────────────────────────────────
        st.markdown('<div class="ulabel ulabel-g">&#128196;&nbsp; Upload CV</div>', unsafe_allow_html=True)
        cv = st.file_uploader("cv", type=["pdf"], label_visibility="collapsed")

        st.markdown('<div class="uhr"></div>', unsafe_allow_html=True)

        # ── Job Description ──────────────────────────────────────────────
        st.markdown('<div class="ulabel ulabel-b">&#128188;&nbsp; Job Description</div>', unsafe_allow_html=True)
        input_type = st.radio("", ["PDF", "Text"], horizontal=True)

        job_text = ""
        job_file = None

        if input_type == "PDF":
            job_file = st.file_uploader("jd", type=["pdf"], label_visibility="collapsed")
            if job_file:
                job_text = "PDF uploaded"
        else:
            job_text = st.text_area(
                "jt",
                placeholder="Paste the full job description here...",
                label_visibility="collapsed",
            )

        st.markdown('<div class="uhr"></div>', unsafe_allow_html=True)

        # ── Start Button ─────────────────────────────────────────────────
        if name and cv and job_text:
            if st.button("&#128640;  Start Interview", use_container_width=True):
                with st.spinner("Preparing your personalized interview..."):
                    cv_text = parse_cv(cv)
                    if "Hata" in cv_text:
                        st.error("CV could not be read")
                        st.stop()
                    if input_type == "PDF":
                        job_clean = parse_job_description(job_file)
                    else:
                        job_clean = parse_job_description(job_text)
                    st.session_state.cv_text = cv_text
                    st.session_state.job_text = job_clean
                    st.session_state.candidate_name = name
                    st.session_state.position = "Software Engineer"
                    try:
                        chat, first_question = start_interview(
                            candidate_name=name,
                            position="Software Engineer",
                            job_text=job_clean,
                            cv_text=cv_text,
                        )
                    except Exception:
                        chat = None
                        first_question = "Tell me about yourself"

                st.session_state.chat = chat
                st.session_state.chat_history = [{"role": "ai", "content": first_question}]
                st.session_state.page = "mode"
                st.rerun()
        else:
            st.markdown(
                '<p style="font-size:13px;color:rgba(255,255,255,.25);text-align:center;margin-top:8px;">'
                "Complete all fields to start your interview</p>",
                unsafe_allow_html=True,
            )

    with col2:
        components.html(RIGHT_CARD_HTML, height=590, scrolling=False)