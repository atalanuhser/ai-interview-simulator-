import streamlit as st
import streamlit.components.v1 as components

_BACKGROUND_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body{width:100%;height:100%;background:transparent;overflow:hidden;}
canvas#bg{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;}
</style>
</head>
<body>
<canvas id="bg"></canvas>
<script>
const canvas = document.getElementById('bg');
const ctx = canvas.getContext('2d');
let W, H, orbs, particles, last = 0;
function resize() { W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight; }
function initOrbs() {
  orbs = [
    { x:-180, y:-220, r:350, color:'rgba(99,102,241,', a:0.38, dx:0.18, dy:0.12, ox:0, oy:0 },
    { x:W+160, y:H+160, r:290, color:'rgba(16,185,129,', a:0.25, dx:-0.14, dy:-0.16, ox:0, oy:0 },
    { x:W/2, y:H/2, r:200, color:'rgba(244,114,182,', a:0.20, dx:0.10, dy:-0.08, ox:0, oy:0 },
  ];
}
function initParticles() {
  particles = [];
  for (let i=0;i<60;i++) particles.push({ x:Math.random()*W, y:Math.random()*H, r:Math.random()*1.5+0.3, a:Math.random()*0.6+0.1, speedX:(Math.random()-0.5)*0.25, speedY:(Math.random()-0.5)*0.25, twinkle:Math.random()*Math.PI*2 });
}
function draw(ts) {
  const dt = ts - last; last = ts;
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#050816'; ctx.fillRect(0,0,W,H);
  const gs=60; ctx.strokeStyle='rgba(99,102,241,.045)'; ctx.lineWidth=0.5;
  for(let x=0;x<W;x+=gs){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}
  for(let y=0;y<H;y+=gs){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}
  orbs.forEach(o=>{
    o.ox+=o.dx*(dt/1000); o.oy+=o.dy*(dt/1000);
    const px=o.x+Math.sin(o.ox*0.6)*120, py=o.y+Math.cos(o.oy*0.6)*90;
    const gr=ctx.createRadialGradient(px,py,0,px,py,o.r);
    gr.addColorStop(0,o.color+o.a+')'); gr.addColorStop(1,'transparent');
    ctx.beginPath(); ctx.arc(px,py,o.r,0,Math.PI*2); ctx.fillStyle=gr; ctx.fill();
  });
  const t=ts/1000;
  particles.forEach(p=>{
    p.x+=p.speedX; p.y+=p.speedY;
    if(p.x<0)p.x=W; if(p.x>W)p.x=0; if(p.y<0)p.y=H; if(p.y>H)p.y=0;
    const tw=Math.sin(t*1.5+p.twinkle)*0.4+0.6;
    ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
    ctx.fillStyle=`rgba(165,180,252,${p.a*tw})`; ctx.fill();
  });
  requestAnimationFrame(draw);
}
resize(); initOrbs(); initParticles();
window.addEventListener('resize',()=>{resize();initOrbs();initParticles();});
requestAnimationFrame(draw);
</script>
</body>
</html>"""


def render_mode_selection():
    if "page" not in st.session_state:
        st.session_state.page = "mode"
    if "interview_mode" not in st.session_state:
        st.session_state.interview_mode = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ── Global CSS ──────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

    header, footer { visibility: hidden !important; }
    .stApp { background: #050816 !important; }
    .block-container { padding: 1.5rem 2.5rem 2rem !important; max-width: 980px !important; position: relative; z-index: 10; }

    /* ── Top bar ── */
    .top-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    .badge {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 6px 20px; border-radius: 100px;
        border: 1px solid rgba(99,102,241,.5);
        background: rgba(99,102,241,.12);
        font-size: 11px; letter-spacing: .13em; text-transform: uppercase;
        color: #a5b4fc; font-weight: 500; font-family: 'DM Sans', sans-serif;
    }
    .badge-dot {
        width: 6px; height: 6px; border-radius: 50%;
        background: #6366f1; box-shadow: 0 0 8px #6366f1;
        display: inline-block; animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse { 0%,100%{opacity:1;transform:scale(1);} 50%{opacity:.4;transform:scale(.6);} }

    /* ── Back button (Streamlit) ── */
    div[data-testid="stButton"]:has(button[kind="secondary"]#back_btn) button,
    .back-area button {
        background: rgba(255,255,255,.05) !important;
        border: 1px solid rgba(255,255,255,.12) !important;
        color: rgba(255,255,255,.6) !important;
        border-radius: 100px !important;
        padding: 4px 18px !important;
        font-size: 12px !important;
        font-family: 'DM Sans', sans-serif !important;
        letter-spacing: .06em !important;
        transition: all .3s ease !important;
    }

    /* ── All Streamlit buttons global override ── */
    .stButton > button {
        font-family: 'DM Sans', sans-serif !important;
        transition: all .3s ease !important;
        cursor: pointer !important;
    }

    /* ── Back button specific ── */
    .back-area .stButton > button {
        background: rgba(255,255,255,.05) !important;
        border: 1px solid rgba(255,255,255,.12) !important;
        color: rgba(255,255,255,.6) !important;
        border-radius: 100px !important;
        font-size: 12px !important;
        letter-spacing: .06em !important;
    }
    .back-area .stButton > button:hover {
        background: rgba(255,255,255,.1) !important;
        border-color: rgba(99,102,241,.5) !important;
        color: #fff !important;
    }

    /* ── Title ── */
    .main-title {
        font-family: 'Syne', sans-serif !important;
        font-size: clamp(32px,4vw,52px) !important;
        font-weight: 800 !important; line-height: 1.1 !important;
        color: #fff !important; margin-bottom: 10px !important;
    }
    .grad {
        background: linear-gradient(135deg,#818cf8 0%,#34d399 55%,#f472b6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; background-size: 300%; animation: gr 6s ease infinite;
    }
    @keyframes gr { 0%,100%{background-position:0% 50%;} 50%{background-position:100% 50%;} }
    .sub-title {
        font-size: 15px; color: rgba(255,255,255,.4);
        font-weight: 300; margin-bottom: 32px;
        font-family: 'DM Sans', sans-serif;
    }

    /* ── Cards ── */
    .card-inner {
        position: relative; border-radius: 24px; padding: 32px 28px 24px;
        background: rgba(8,11,35,.88);
        border: 1px solid rgba(255,255,255,.07);
        backdrop-filter: blur(28px);
        display: flex; flex-direction: column; text-align: left;
        transition: transform .35s cubic-bezier(.22,.61,.36,1), box-shadow .35s, border-color .35s;
        margin-bottom: 0;
    }
    .card-inner:hover { transform: translateY(-6px); }
    .text-card:hover { box-shadow: 0 0 60px rgba(99,102,241,.4); border-color: rgba(99,102,241,.4) !important; }
    .voice-card:hover { box-shadow: 0 0 60px rgba(16,185,129,.35); border-color: rgba(16,185,129,.35) !important; }

    .card-icon { font-size: 40px; margin-bottom: 16px; line-height: 1; }
    .card-title-text { font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 700; margin-bottom: 8px; }
    .text-card .card-title-text { color: #c7d2fe; }
    .voice-card .card-title-text { color: #a7f3d0; }

    .card-divider { height: 1px; width: 36px; margin-bottom: 12px; border-radius: 2px; opacity: .55; }
    .text-card .card-divider { background: linear-gradient(90deg,#6366f1,transparent); }
    .voice-card .card-divider { background: linear-gradient(90deg,#10b981,transparent); }

    .card-desc { font-size: 13px; color: rgba(255,255,255,.4); font-weight: 300; line-height: 1.7; margin-bottom: 18px; }

    .tags { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 18px; }
    .tag { font-size: 10px; letter-spacing: .08em; text-transform: uppercase; padding: 3px 10px; border-radius: 100px; font-weight: 500; }
    .text-card .tag { background: rgba(99,102,241,.15); border: 1px solid rgba(99,102,241,.3); color: #a5b4fc; }
    .voice-card .tag { background: rgba(16,185,129,.15); border: 1px solid rgba(16,185,129,.3); color: #6ee7b7; }

    /* ── Select buttons under cards ── */
    .text-area .stButton > button {
        width: 100% !important;
        background: rgba(99,102,241,.15) !important;
        border: 1px solid rgba(99,102,241,.4) !important;
        color: #a5b4fc !important;
        border-radius: 100px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        letter-spacing: .1em !important;
        text-transform: uppercase !important;
        padding: 10px 0 !important;
        margin-top: 8px !important;
    }
    .text-area .stButton > button:hover {
        background: rgba(99,102,241,.3) !important;
        border-color: rgba(99,102,241,.7) !important;
        color: #fff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 0 20px rgba(99,102,241,.3) !important;
    }

    .voice-area .stButton > button {
        width: 100% !important;
        background: rgba(16,185,129,.15) !important;
        border: 1px solid rgba(16,185,129,.4) !important;
        color: #6ee7b7 !important;
        border-radius: 100px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        letter-spacing: .1em !important;
        text-transform: uppercase !important;
        padding: 10px 0 !important;
        margin-top: 8px !important;
    }
    .voice-area .stButton > button:hover {
        background: rgba(16,185,129,.3) !important;
        border-color: rgba(16,185,129,.7) !important;
        color: #fff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 0 20px rgba(16,185,129,.3) !important;
    }

    .footer-note {
        text-align: center; margin-top: 28px;
        font-size: 11px; color: rgba(255,255,255,.18);
        letter-spacing: .09em; font-family: 'DM Sans', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Arka plan animasyonu ─────────────────────────────────────────────────
    components.html(_BACKGROUND_HTML, height=0)

    # ── Top bar: Back butonu (sol) + Badge (sağ) ────────────────────────────
    col_back, col_badge = st.columns([3, 2])
    with col_back:
        st.markdown('<div class="back-area">', unsafe_allow_html=True)
        if st.button("← Back to Upload", key="back_to_upload"):
            st.session_state.page = "upload"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_badge:
        st.markdown("""
        <div style="display:flex;justify-content:flex-end;align-items:center;padding-top:6px;">
            <div class="badge"><span class="badge-dot"></span>&nbsp;AI-Powered Simulator</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Başlık ───────────────────────────────────────────────────────────────
    st.markdown("""
        <div class="main-title">Choose Your <span class="grad">Interview Mode</span></div>
        <div class="sub-title">Select the format that matches how you want to practice today</div>
    """, unsafe_allow_html=True)

    # ── Kartlar + Butonlar ───────────────────────────────────────────────────
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="card-inner text-card">
            <div class="card-icon">📝</div>
            <div class="card-title-text">Written Interview</div>
            <div class="card-divider"></div>
            <div class="card-desc">Classic text-based simulation designed to help you craft precise, structured answers. Review your responses and refine your written communication at your own pace.</div>
            <div class="tags">
                <span class="tag">Text-based</span>
                <span class="tag">Self-paced</span>
                <span class="tag">Editable</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="text-area">', unsafe_allow_html=True)
        if st.button("● Select Written Interview", key="btn_text", use_container_width=True):
            st.session_state.interview_mode = "text"
            st.session_state.page = "interview"
            st.session_state.chat_history = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card-inner voice-card">
            <div class="card-icon">🎤</div>
            <div class="card-title-text">Voice Interview</div>
            <div class="card-divider"></div>
            <div class="card-desc">Real-time spoken simulation that mirrors a live interview room. Practice your delivery, pacing, and tone — then get instant AI feedback on your verbal performance.</div>
            <div class="tags">
                <span class="tag">Real-time</span>
                <span class="tag">Speech AI</span>
                <span class="tag">Feedback</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="voice-area">', unsafe_allow_html=True)
        if st.button("● Select Voice Interview", key="btn_voice", use_container_width=True):
            st.session_state.interview_mode = "voice"
            st.session_state.page = "interview"
            st.session_state.chat_history = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="footer-note">✦ &nbsp;Responses are evaluated in real time by AI&nbsp; ✦</div>',
                unsafe_allow_html=True)


# ── Doğrudan çalıştırma ───────────────────────────────────────────────────
if __name__ == "__main__":
    st.set_page_config(page_title="Interview Simulator", layout="wide")

    if "page" not in st.session_state:
        st.session_state.page = "mode"
    if "interview_mode" not in st.session_state:
        st.session_state.interview_mode = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if st.session_state.page == "mode":
        render_mode_selection()
    elif st.session_state.page == "upload":
        st.title("Upload Page")
        st.write("CV yükleme sayfası.")
        if st.button("← Mode Seçimine Dön"):
            st.session_state.page = "mode"
            st.rerun()
    elif st.session_state.page == "interview":
        mode = st.session_state.get("interview_mode", "text")
        st.title(f"{'Written' if mode == 'text' else 'Voice'} Interview")
        st.write(f"Mülakat modu: **{mode}**")
        if st.button("← Geri"):
            st.session_state.page = "mode"
            st.rerun()