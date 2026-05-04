import streamlit as st
import plotly.graph_objects as go
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
    { x:-180, y:-220, r:350, color:'rgba(99,102,241,', a:0.32, dx:0.18, dy:0.12, ox:0, oy:0 },
    { x:W+160, y:H+160, r:290, color:'rgba(16,185,129,', a:0.22, dx:-0.14, dy:-0.16, ox:0, oy:0 },
    { x:W/2, y:H/2, r:200, color:'rgba(244,114,182,', a:0.16, dx:0.10, dy:-0.08, ox:0, oy:0 },
  ];
}
function initParticles() {
  particles = [];
  for (let i=0;i<60;i++) particles.push({ x:Math.random()*W, y:Math.random()*H, r:Math.random()*1.5+0.3, a:Math.random()*0.5+0.1, speedX:(Math.random()-0.5)*0.25, speedY:(Math.random()-0.5)*0.25, twinkle:Math.random()*Math.PI*2 });
}
function draw(ts) {
  const dt = ts - last; last = ts;
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#050816'; ctx.fillRect(0,0,W,H);
  const gs=60; ctx.strokeStyle='rgba(99,102,241,.04)'; ctx.lineWidth=0.5;
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


def _score_color(val: float):
    """Return color tuple (border, bg, text) based on score 0-10."""
    if val >= 7.5:
        return ("rgba(16,185,129,.5)", "rgba(16,185,129,.12)", "#6ee7b7")
    elif val >= 5:
        return ("rgba(234,179,8,.5)", "rgba(234,179,8,.12)", "#fde68a")
    else:
        return ("rgba(239,68,68,.5)", "rgba(239,68,68,.12)", "#fca5a5")


def _recommendation_style(rec: str):
    rec_lower = rec.lower()
    if any(w in rec_lower for w in ["hire", "recommend", "strong", "yes"]):
        return ("rgba(16,185,129,.5)", "rgba(16,185,129,.15)", "#6ee7b7", "✦ HIRE")
    elif any(w in rec_lower for w in ["consider", "maybe", "potential", "review"]):
        return ("rgba(234,179,8,.5)", "rgba(234,179,8,.15)", "#fde68a", "◈ CONSIDER")
    else:
        return ("rgba(239,68,68,.5)", "rgba(239,68,68,.15)", "#fca5a5", "✕ PASS")


def render_score_ui(result: dict):
    if "error" in result:
        st.error("⚠ Scoring failed. Raw output below:")
        st.code(result.get("raw", ""), language="json")
        return

    radar = result["radar"]

    # ── CSS ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

    header, footer { visibility: hidden !important; }
    .stApp { background: #050816 !important; }
    .block-container { padding: 1.5rem 2.5rem 3rem !important; max-width: 1100px !important; position: relative; z-index: 10; }

    /* ── Page header ── */
    .page-badge {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 6px 20px; border-radius: 100px;
        border: 1px solid rgba(99,102,241,.5);
        background: rgba(99,102,241,.12);
        font-size: 11px; letter-spacing: .13em; text-transform: uppercase;
        color: #a5b4fc; font-weight: 500; font-family: 'DM Sans', sans-serif;
        margin-bottom: 16px;
    }
    .badge-dot {
        width: 6px; height: 6px; border-radius: 50%;
        background: #6366f1; box-shadow: 0 0 8px #6366f1;
        display: inline-block; animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse { 0%,100%{opacity:1;transform:scale(1);} 50%{opacity:.4;transform:scale(.6);} }

    .page-title {
        font-family: 'Syne', sans-serif !important;
        font-size: clamp(28px,3.5vw,46px) !important;
        font-weight: 800 !important; line-height: 1.1 !important;
        color: #fff !important; margin-bottom: 6px !important;
    }
    .grad {
        background: linear-gradient(135deg,#818cf8 0%,#34d399 55%,#f472b6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; background-size: 300%; animation: gr 6s ease infinite;
    }
    @keyframes gr { 0%,100%{background-position:0% 50%;} 50%{background-position:100% 50%;} }
    .page-sub {
        font-size: 14px; color: rgba(255,255,255,.38);
        font-family: 'DM Sans', sans-serif; margin-bottom: 36px;
    }

    /* ── Score metric cards ── */
    .score-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 12px;
        margin-bottom: 32px;
    }
    .score-card {
        border-radius: 18px;
        padding: 18px 14px 14px;
        backdrop-filter: blur(20px);
        background: rgba(8,11,35,.85);
        text-align: center;
        transition: transform .3s;
    }
    .score-card:hover { transform: translateY(-4px); }
    .score-num {
        font-family: 'Syne', sans-serif;
        font-size: 32px; font-weight: 800;
        line-height: 1; margin-bottom: 6px;
    }
    .score-label {
        font-size: 10px; letter-spacing: .08em; text-transform: uppercase;
        color: rgba(255,255,255,.4); font-family: 'DM Sans', sans-serif;
    }

    /* ── Section cards ── */
    .section-card {
        background: rgba(8,11,35,.88);
        border: 1px solid rgba(255,255,255,.07);
        border-radius: 20px;
        padding: 24px 28px;
        backdrop-filter: blur(20px);
        margin-bottom: 16px;
    }
    .section-title {
        font-family: 'Syne', sans-serif;
        font-size: 16px; font-weight: 700;
        color: #fff; margin-bottom: 14px;
        display: flex; align-items: center; gap: 10px;
    }
    .section-title-dot {
        width: 8px; height: 8px; border-radius: 50%; display: inline-block;
    }
    .section-body {
        font-size: 14px; color: rgba(255,255,255,.5);
        font-family: 'DM Sans', sans-serif; line-height: 1.8;
    }

    /* ── Strength / Improvement items ── */
    .item-strength {
        display: flex; align-items: flex-start; gap: 10px;
        padding: 12px 16px; border-radius: 12px; margin-bottom: 8px;
        background: rgba(16,185,129,.08);
        border: 1px solid rgba(16,185,129,.2);
        font-size: 13px; color: rgba(255,255,255,.65);
        font-family: 'DM Sans', sans-serif; line-height: 1.6;
    }
    .item-strength-icon { color: #34d399; font-size: 14px; margin-top: 1px; flex-shrink: 0; }

    .item-improve {
        display: flex; align-items: flex-start; gap: 10px;
        padding: 12px 16px; border-radius: 12px; margin-bottom: 8px;
        background: rgba(234,179,8,.08);
        border: 1px solid rgba(234,179,8,.2);
        font-size: 13px; color: rgba(255,255,255,.65);
        font-family: 'DM Sans', sans-serif; line-height: 1.6;
    }
    .item-improve-icon { color: #fbbf24; font-size: 14px; margin-top: 1px; flex-shrink: 0; }

    /* ── Recommendation banner ── */
    .rec-banner {
        border-radius: 20px; padding: 28px 32px;
        backdrop-filter: blur(20px);
        display: flex; align-items: center; justify-content: space-between;
        flex-wrap: wrap; gap: 16px;
        margin-top: 8px;
    }
    .rec-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 13px; color: rgba(255,255,255,.45);
        letter-spacing: .08em; text-transform: uppercase;
        margin-bottom: 6px;
    }
    .rec-value {
        font-family: 'Syne', sans-serif;
        font-size: 22px; font-weight: 800;
    }
    .rec-pill {
        padding: 10px 28px; border-radius: 100px;
        font-family: 'Syne', sans-serif;
        font-size: 13px; font-weight: 700;
        letter-spacing: .12em; text-transform: uppercase;
    }

    .footer-note {
        text-align: center; margin-top: 32px;
        font-size: 11px; color: rgba(255,255,255,.15);
        letter-spacing: .09em; font-family: 'DM Sans', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Arka plan animasyonu ─────────────────────────────────────────────────
    components.html(_BACKGROUND_HTML, height=0)

    # ── Page header ──────────────────────────────────────────────────────────
    total_q = result.get("total_questions", 0)
    st.markdown(f"""
        <div class="page-badge"><span class="badge-dot"></span>&nbsp;Interview Complete</div>
        <div class="page-title">Your <span class="grad">Evaluation Results</span></div>
        <div class="page-sub">{total_q} questions answered &nbsp;·&nbsp; AI-powered analysis</div>
    """, unsafe_allow_html=True)

    # ── Score metric cards ────────────────────────────────────────────────────
    scores_html = '<div class="score-grid">'
    for label, val in radar.items():
        border, bg, color = _score_color(val)
        scores_html += f"""
        <div class="score-card" style="border:1px solid {border}; background:rgba(8,11,35,.85);">
            <div class="score-num" style="color:{color};">{val}<span style="font-size:14px;color:rgba(255,255,255,.25);font-family:'DM Sans',sans-serif;">/10</span></div>
            <div class="score-label">{label}</div>
        </div>"""
    scores_html += '</div>'
    st.markdown(scores_html, unsafe_allow_html=True)

    # ── Radar chart ──────────────────────────────────────────────────────────
    categories = list(radar.keys())
    values = list(radar.values())

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(99,102,241,0.18)',
        line=dict(color='rgba(129,140,248,0.9)', width=2),
        name='Score'
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(8,11,35,0.0)',
            radialaxis=dict(
                visible=True, range=[0, 10],
                tickfont=dict(color='rgba(255,255,255,0.3)', size=10),
                gridcolor='rgba(255,255,255,0.06)',
                linecolor='rgba(255,255,255,0.06)',
            ),
            angularaxis=dict(
                tickfont=dict(color='rgba(255,255,255,0.55)', size=12, family='DM Sans'),
                gridcolor='rgba(255,255,255,0.06)',
                linecolor='rgba(255,255,255,0.06)',
            ),
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(t=40, b=40, l=60, r=60),
        height=380,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Overall comment ──────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">
            <span class="section-title-dot" style="background:#818cf8;box-shadow:0 0 8px #6366f1;"></span>
            Overall Evaluation
        </div>
        <div class="section-body">{result["overall_comment"]}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Strengths + Areas to Improve ─────────────────────────────────────────
    col1, col2 = st.columns(2, gap="large")

    with col1:
        strengths_items = "".join([
            f'<div class="item-strength"><span class="item-strength-icon">✦</span>{s}</div>'
            for s in result["strengths"]
        ])
        st.markdown(f"""
        <div class="section-card" style="height:100%;">
            <div class="section-title">
                <span class="section-title-dot" style="background:#34d399;box-shadow:0 0 8px #10b981;"></span>
                Strengths
            </div>
            {strengths_items}
        </div>
        """, unsafe_allow_html=True)

    with col2:
        improve_items = "".join([
            f'<div class="item-improve"><span class="item-improve-icon">◈</span>{w}</div>'
            for w in result["areas_for_improvement"]
        ])
        st.markdown(f"""
        <div class="section-card" style="height:100%;">
            <div class="section-title">
                <span class="section-title-dot" style="background:#fbbf24;box-shadow:0 0 8px #f59e0b;"></span>
                Areas to Improve
            </div>
            {improve_items}
        </div>
        """, unsafe_allow_html=True)

    # ── Final Recommendation ─────────────────────────────────────────────────
    border, bg, color, label = _recommendation_style(result["recommendation"])
    st.markdown(f"""
    <div class="rec-banner" style="border:1px solid {border}; background:{bg};">
        <div>
            <div class="rec-label">Final Recommendation</div>
            <div class="rec-value" style="color:{color};">{result["recommendation"]}</div>
        </div>
        <div class="rec-pill" style="border:1px solid {border}; background:rgba(8,11,35,.6); color:{color};">
            {label}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="footer-note">✦ &nbsp;Evaluation generated by AI · Results are indicative&nbsp; ✦</div>',
                unsafe_allow_html=True)