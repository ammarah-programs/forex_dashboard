import streamlit as st
from config import FOREX_PAIRS
from news import collect_pair_news
from ai import analyze_news, ask_dashboard_ai
from price import get_price_movement
import streamlit.components.v1 as components
from daily_calendar import build_daily_calendar




# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="THE EDGEFLOW",
    layout="wide"
)

# --------------------------------------------------
# GLOBAL STYLING (DARK THEME — FIXED)
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&display=swap');

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700;800&display=swap');

/* ------------------------------
   CONFIDENCE BAR
------------------------------ */

.confidence {
    margin-top: 0.8rem;
    font-size: 0.85rem;
    color: var(--text-muted);
}

.confidence-bar {
    margin-top: 0.4rem;
    height: 6px;
    width: 100%;
    background: rgba(255,255,255,0.08);
    border-radius: 6px;
    overflow: hidden;
}

.confidence-fill {
    height: 100%;
    background: linear-gradient(
        90deg,
        #3b82f6,
        #60a5fa
    );
    border-radius: 6px;
    transition: width 0.4s ease;
}

.pair-card {
    background: #171b21;
    border: 2px solid rgba(255,255,255,0.25);
    border-radius: 18px;
    padding: 1.4rem;
    margin-bottom: 1.6rem;
    box-shadow: 0 20px 50px rgba(0,0,0,0.7);
}

.pair-card h3 {
    margin-top: 0;
    margin-bottom: 0.6rem;
}

.confidence {
    margin-top: 0.6rem;
    color: var(--text-muted);
}

/* --------------------------------------------------
   FORCE STREAMLIT CONTAINER BORDERS TO SHOW
-------------------------------------------------- */

div[data-testid="stContainer"][data-border="true"] {
    border: 1.6px solid rgba(255, 255, 255, 0.22) !important;
    border-radius: 18px !important;
    background: #171b21;
    padding: 1.4rem;
    box-shadow: 0 18px 45px rgba(0,0,0,0.65);
}

/* --------------------------------------------------
   EXPLICIT PAIR CARD (STREAMLIT-PROOF)
-------------------------------------------------- */

.pair-card {
    background: #171b21;
    border: 1.5px solid rgba(255,255,255,0.18);
    border-radius: 18px;
    padding: 1.4rem 1.4rem 1.6rem;
    margin-bottom: 1.8rem;

    box-shadow:
        inset 0 0 0 1px rgba(255,255,255,0.04),
        0 18px 45px rgba(0,0,0,0.7);

    transition: all 0.25s ease;
}

.pair-card:hover {
    transform: translateY(-3px);
    border-color: rgba(255,255,255,0.28);
    box-shadow:
        inset 0 0 0 1px rgba(255,255,255,0.08),
        0 26px 65px rgba(0,0,0,0.85);
}



:root {
    --bg-main: #121417;
    --bg-card: #171b21;
    --border-soft: rgba(255,255,255,0.06);
    --text-main: #e6e6e6;
    --text-muted: #9aa0aa;
}

.stApp {
    background: radial-gradient(circle at top, #262a30, var(--bg-main));
    color: var(--text-main);
    font-family: 'Source Sans 3', sans-serif;
}

h3 {
    color: #ffffff !important;
}

.edgeflow-title {
    text-align: center;
    font-size: 2.6rem;
    font-weight: 700;
    color: #ffffff;
}

.edgeflow-subtitle {
    text-align: center;
    font-size: 0.95rem;
    color: var(--text-muted);
    margin-bottom: 3rem;
}

.pos { color: #2ecc71; font-weight: 600; }
.neg { color: #e74c3c; font-weight: 600; }
.neu { color: #f1c40f; font-weight: 600; }

/* ------------------------------
   RIGHT SIDE DAILY BRIEF PANEL
------------------------------ */

.right-panel {
    background: #171b21;
    border: 2px solid rgba(255,255,255,0.22);
    border-radius: 20px;
    padding: 1.4rem;
    box-shadow: 0 18px 45px rgba(0,0,0,0.7);
}

.panel-section {
    margin-bottom: 1.6rem;
}

.panel-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 0.6rem;
}

.focus-pair {
    font-size: 1.9rem;
    font-weight: 800;
    color: #00ffb3;
    text-align: center;
}

.panel-muted {
    text-align: center;
    font-size: 0.8rem;
    color: var(--text-muted);
}

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700;800&display=swap');

.daily-focus-pair {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 32px;
    font-weight: 800;
    color: #9AD7FF;
    letter-spacing: 1.2px;
}
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 0.6px;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
}
/* ------------------------------
   ASK AI BUTTON FIX
------------------------------ */

button[kind="primary"], 
div.stButton > button {
    background: #1e3a8a !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    border: none !important;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
    color: #ffffff !important;
}

div.stButton > button:disabled {
    background: rgba(255,255,255,0.2) !important;
    color: rgba(255,255,255,0.6) !important;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("""
<div class="edgeflow-title">THE EDGEFLOW</div>
<div class="edgeflow-subtitle">
Macro intelligence & FX bias — distilled
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# GRID
left_col, right_col = st.columns([3.6, 1.4])

# --------------------------------------------------
with left_col:
    pairs = list(FOREX_PAIRS.items())

    for i in range(0, len(pairs), 3):
        cols = st.columns(3)

        for col, (pair, keywords) in zip(cols, pairs[i:i+3]):
            with col:
                with st.container(border=True):
                    news = collect_pair_news(pair, keywords)
                    analysis = analyze_news(pair, news)

                impact = analysis["impact"]
                conf = analysis["confidence"]

                # ---- Bias style
                if impact == "Bullish":
                    cls, arrow = "pos", "▲"
                elif impact == "Bearish":
                    cls, arrow = "neg", "▼"
                else:
                    cls, arrow = "neu", "→"

                # ---- Price movement
                movement = get_price_movement(pair)

                st.markdown(f"""
                <div class="pair-card">

                <h3>{pair}</h3>
                <div class="{cls}">{arrow} Bias: {impact}</div>

                {f"<div class='pos'>▲ +{movement['percent']}%</div>" if movement and movement["direction"] == "up" else ""}
                {f"<div class='neg'>▼ -{movement['percent']}%</div>" if movement and movement["direction"] == "down" else ""}

                <div class="confidence">
                Confidence: {conf}%
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {conf}%;"></div>
                </div>
                </div>

                <p>{analysis["summary"]}</p>

                </div>
                """, unsafe_allow_html=True)

                with st.expander("🔍 Deep View"):
                    st.write(analysis["deep_view"])

# --------------------------------------------------
# AGGREGATE ALL NEWS FOR AI ASSISTANT (SAFE / READ-ONLY)
# --------------------------------------------------
all_dashboard_news = []

for pair, keywords in FOREX_PAIRS.items():
    try:
        items = collect_pair_news(pair, keywords)
        if isinstance(items, list):
            all_dashboard_news.extend(items)
    except Exception:
        pass


with right_col:
    with st.container(border=True):

        st.markdown("""
<div class="section-title">
    📅 TODAY
</div>
""", unsafe_allow_html=True)

        st.markdown(
    "<div style='height:1px;background:rgba(255,255,255,0.08);margin:8px 0 12px;'></div>",
    unsafe_allow_html=True
)

        calendar_news = collect_pair_news(
            "CALENDAR",
            [],
            calendar_mode=True
        )

        calendar = build_daily_calendar(calendar_news)

        # ---- DATE
        st.markdown(
            f"<div style='color:#9aa0aa;font-size:13px;margin-bottom:10px;'>"
            f"{calendar['date']}</div>",
            unsafe_allow_html=True
        )

        # ---- CALENDAR ITEMS
        if calendar["pinned_news"]:
            for item in calendar["pinned_news"]:
                st.markdown(f"""
<div style="
    background:#101418;
    border-left:4px solid #f59e0b;
    border-radius:10px;
    padding:10px 12px;
    margin-bottom:8px;
    font-size:13px;
">
<b>{item['currency']}</b> — {item['text']}
</div>
""", unsafe_allow_html=True)

        else:
            st.markdown("""
<div style="
    background:#101418;
    border:1px solid rgba(255,255,255,0.08);
    border-radius:12px;
    padding:12px;
    font-size:13px;
    color:#9aa0aa;
">
🟢 <b>Quiet session</b><br>
No high-impact macro events scheduled
</div>
""", unsafe_allow_html=True)

    

        # ---- DAILY FOCUS (static for now)
        st.markdown("""
<div class="section-title">
    🎯 Daily Focus
</div>
""", unsafe_allow_html=True)

        st.markdown(f"""
<div style="
background:#101418;
border:1px solid rgba(255,255,255,0.10);
border-radius:16px;
padding:18px;
text-align:center;
">

<div style="
font-size:12px;
color:#9aa0aa;
letter-spacing:1px;
margin-bottom:6px;
">
PRIMARY PAIR
</div>

<div style="
font-size:34px;
font-weight:700;
color:#d4b15f;
font-family:'Source Sans 3', sans-serif;
margin-bottom:6px;
">
{calendar["focus_pair"] if calendar["focus_pair"] else "—"}
</div>

<div style="
font-size:13px;
color:#9aa0aa;
">
⚡ High-impact volatility expected
</div>

</div>
""", unsafe_allow_html=True)

    

        # ---- KEY NEWS
        st.markdown("""
<div class="section-title">
    📰 Key News
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div style="
    background:#101418;
    border:1px solid rgba(255,255,255,0.10);
    border-radius:16px;
    padding:14px;
">

<div style="margin-bottom:10px;">
🟡 <b>USD CPI</b><br>
<span style="color:#9aa0aa;font-size:13px;">
Inflation risk remains elevated
</span>
</div>

<div style="margin-bottom:10px;">
🔵 <b>ECB</b><br>
<span style="color:#9aa0aa;font-size:13px;">
Tone remains slightly cautious
</span>
</div>

<div>
🔴 <b>Risk Sentiment</b><br>
<span style="color:#9aa0aa;font-size:13px;">
Markets remain fragile
</span>
</div>

</div>
""", unsafe_allow_html=True)

# ---- EDGEFLOW AI ASSISTANT
        st.markdown("""
        <div class="section-title">
            🤖 Ask EdgeFlow AI
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):

            user_q = st.text_input(
                "Ask about today's FX bias, macro risk, or sentiment",
                placeholder="Ask Edgeflow about today's market sentiment.",
                label_visibility="collapsed"
            )

            if st.button("Ask AI") and user_q.strip():
                with st.spinner("Analyzing macro context..."):
                    answer = ask_dashboard_ai(user_q, all_dashboard_news)

                st.markdown(f"""
        <div style="
            background:#101418;
            border:1px solid rgba(255,255,255,0.10);
            border-radius:14px;
            padding:14px;
            font-size:14px;
            color:#e6e6e6;
            line-height:1.5;
        ">
        {answer}
        </div>
        """, unsafe_allow_html=True)


