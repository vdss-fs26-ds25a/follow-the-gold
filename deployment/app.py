import streamlit as st

# basic page settings
st.set_page_config(
    page_title="Is Gold Really the Safe Haven?",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# all the css styling for the dark theme
# i put it here so every page uses the same colors
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0a0c10 !important;
    color: #d4c5a0;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #0f1117 !important;
    border-right: 1px solid #1e2130;
}
[data-testid="stSidebar"] * { color: #b0a080 !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 0.9rem; }

/* hide the default streamlit menu and footer */
#MainMenu, footer, header { visibility: hidden; }

h1, h2, h3 {
    font-family: 'Playfair Display', Georgia, serif;
    color: #FFD700;
}

hr { border-color: #1e2130; }

/* card style used in chapter 5 */
.metric-card {
    background: linear-gradient(135deg, #13161f 0%, #1a1d28 100%);
    border: 1px solid #2a2d3a;
    border-top: 3px solid #FFD700;
    border-radius: 8px;
    padding: 28px 24px 22px;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(255,215,0,0.08);
}
.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 900;
    color: #FFD700;
    line-height: 1;
    margin-bottom: 6px;
}
.metric-label {
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #7a7060;
    margin-bottom: 10px;
}
.metric-insight {
    font-size: 0.88rem;
    color: #a09070;
    line-height: 1.5;
}

/* the yellow left-border box used for insights */
.insight-box {
    background: rgba(255,215,0,0.04);
    border-left: 3px solid #FFD700;
    border-radius: 0 6px 6px 0;
    padding: 16px 20px;
    margin: 20px 0;
    font-size: 0.93rem;
    color: #c0b080;
    line-height: 1.65;
}

.chapter-badge {
    display: inline-block;
    background: rgba(255,215,0,0.1);
    color: #FFD700;
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid rgba(255,215,0,0.25);
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# sidebar with navigation
with st.sidebar:
    st.markdown("### 🪙 Gold Safe Haven?")
    st.markdown("<small style='color:#554d3a;'>VDSS · FS2026</small>", unsafe_allow_html=True)
    st.divider()
    page = st.radio(
        "Navigate",
        options=[
            "Intro",
            "Ch. 1 — Where Does Gold Flow?",
            "Ch. 2 — When Inflation Strikes",
            "Ch. 3 — Gold vs. Silver vs. Platinum",
            "Ch. 4 — The Swiss Connection",
            "Ch. 5 — The Verdict",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("<small style='color:#3a3428;'>Data: UN Trade Statistics 1988–2024<br>World Bank Inflation Database</small>",
                unsafe_allow_html=True)

# load the right page depending on what's selected
if page == "Intro":
    from pages.intro import render
    render()
elif page == "Ch. 1 — Where Does Gold Flow?":
    st.markdown('<div class="chapter-badge">Chapter 1</div>', unsafe_allow_html=True)
    st.title("Where Does Gold Flow?")
    st.info("🚧 Vale's chapter — coming soon")
elif page == "Ch. 2 — When Inflation Strikes":
    st.markdown('<div class="chapter-badge">Chapter 2</div>', unsafe_allow_html=True)
    st.title("When Inflation Strikes")
    st.info("🚧 Vale's chapter — coming soon")
elif page == "Ch. 3 — Gold vs. Silver vs. Platinum":
    st.markdown('<div class="chapter-badge">Chapter 3</div>', unsafe_allow_html=True)
    st.title("Gold vs. Silver vs. Platinum")
    st.info("🚧 Aisosa's chapter — coming soon")
elif page == "Ch. 4 — The Swiss Connection":
    st.markdown('<div class="chapter-badge">Chapter 4</div>', unsafe_allow_html=True)
    st.title("The Swiss Connection")
    st.info("🚧 Aisosa's chapter — coming soon")
elif page == "Ch. 5 — The Verdict":
    from pages.chapter5 import render
    render()
