import streamlit as st
import streamlit.components.v1 as components


def render():
    # big title section at the top
    st.markdown("""
    <div style="padding: 60px 0 40px; text-align: center;">
        <div style="
            font-family: 'DM Sans', sans-serif;
            font-size: 0.8rem;
            letter-spacing: 0.25em;
            text-transform: uppercase;
            color: #554d3a;
            margin-bottom: 18px;
        ">VDSS Visualisierungsprojekt · FS2026</div>

        <h1 style="
            font-family: 'Playfair Display', Georgia, serif;
            font-size: clamp(2.4rem, 6vw, 4.2rem);
            font-weight: 900;
            color: #FFD700;
            line-height: 1.12;
            margin: 0 0 16px;
            text-shadow: 0 0 60px rgba(255,215,0,0.15);
        ">Is Gold Really<br>the Safe Haven?</h1>

        <p style="
            font-size: 1.15rem;
            color: #8a7d5a;
            max-width: 620px;
            margin: 0 auto 50px;
            line-height: 1.7;
            font-weight: 300;
        ">When inflation strikes and markets tremble, everyone says the same thing:
        <em style='color:#b0956a;'>buy gold.</em>
        But what does the trade data actually show?
        We followed 37 years of physical gold flows across 245 countries to find out.</p>
    </div>
    """, unsafe_allow_html=True)

    # 3 animated numbers that count up when the page loads
    # used components.html because normal streamlit cant do javascript animations
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: transparent;
            font-family: 'DM Sans', 'Segoe UI', sans-serif;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            padding: 0 4px 30px;
        }

        .metric-card {
            background: linear-gradient(160deg, #13161f 0%, #1a1d28 100%);
            border: 1px solid #252830;
            border-top: 3px solid #FFD700;
            border-radius: 10px;
            padding: 32px 20px 26px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        /* subtle gold glow at the top of each card */
        .metric-card::before {
            content: '';
            position: absolute;
            inset: 0;
            background: radial-gradient(ellipse at top, rgba(255,215,0,0.04) 0%, transparent 65%);
            pointer-events: none;
        }

        .metric-icon {
            font-size: 1.6rem;
            margin-bottom: 12px;
            display: block;
        }

        .metric-value {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 2.8rem;
            font-weight: 900;
            color: #FFD700;
            line-height: 1;
            margin-bottom: 8px;
            letter-spacing: -0.02em;
        }

        .metric-unit {
            font-size: 1.3rem;
            color: #a08040;
            font-weight: 300;
        }

        .metric-label {
            font-size: 0.72rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: #554d3a;
            margin-bottom: 14px;
        }

        .metric-desc {
            font-size: 0.85rem;
            color: #7a7060;
            line-height: 1.55;
        }

        /* cards fade in one after the other */
        .metric-card {
            opacity: 0;
            transform: translateY(18px);
            animation: fadeUp 0.7s ease forwards;
        }
        .metric-card:nth-child(1) { animation-delay: 0.1s; }
        .metric-card:nth-child(2) { animation-delay: 0.28s; }
        .metric-card:nth-child(3) { animation-delay: 0.46s; }

        @keyframes fadeUp {
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
    </head>
    <body>
    <div class="metrics-grid">

        <div class="metric-card">
            <span class="metric-icon">📈</span>
            <div class="metric-value">
                $<span id="price">0</span><span class="metric-unit">+</span>
            </div>
            <div class="metric-label">Gold Price Record (per oz)</div>
            <div class="metric-desc">In early 2025, gold broke the $3,000 barrier for the first time in history — driven by geopolitical tension and central bank buying.</div>
        </div>

        <div class="metric-card">
            <span class="metric-icon">🌍</span>
            <div class="metric-value">
                $<span id="trade">0</span><span class="metric-unit">T</span>
            </div>
            <div class="metric-label">Total Gold Traded (1988–2024)</div>
            <div class="metric-desc">Over 37 years, gold worth $7.51 trillion crossed international borders — dwarfing silver and platinum combined.</div>
        </div>

        <div class="metric-card">
            <span class="metric-icon">🏦</span>
            <div class="metric-value">
                <span id="countries">0</span>
            </div>
            <div class="metric-label">Countries in Dataset</div>
            <div class="metric-desc">From small island states to global powers — 245 countries appear in the data, revealing an unexpectedly concentrated trade network.</div>
        </div>

    </div>

    <script>
    // counts a number up from 0 to the target value
    function countUp(id, target, duration, decimals) {
        const el = document.getElementById(id);
        const start = performance.now();
        function step(now) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            // makes it slow down at the end
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = eased * target;
            el.textContent = decimals
                ? current.toFixed(decimals)
                : Math.round(current).toLocaleString();
            if (progress < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
    }

    // wait a bit so the cards are visible before counting starts
    setTimeout(() => {
        countUp('price', 3000, 1800, 0);
        countUp('trade', 7.51, 2000, 2);
        countUp('countries', 245, 1500, 0);
    }, 500);
    </script>
    </body>
    </html>
    """, height=280)

    st.divider()

    # list of the 5 research questions we answer in the chapters
    st.markdown('<div class="chapter-badge" style="display:inline-block; background:rgba(255,215,0,0.1); color:#FFD700; font-size:0.72rem; letter-spacing:0.15em; text-transform:uppercase; padding:4px 12px; border-radius:20px; border:1px solid rgba(255,215,0,0.25); margin-bottom:16px;">Five Questions</div>', unsafe_allow_html=True)
    st.markdown("## What We Set Out to Answer")

    questions = [
        ("🗺️ **Where does gold flow?**", "Ch. 1", "Does gold move toward safety — or toward refining capacity? The map reveals a surprising answer."),
        ("📉 **When inflation strikes, do countries import more gold?**", "Ch. 2", "The classic narrative says yes. The scatter plot tells a more nuanced story."),
        ("⚖️ **Is gold special — or do all precious metals behave the same?**", "Ch. 3", "Gold dominates at 71% of trade value. But in a crisis, does silver catch up?"),
        ("🇨🇭 **Why does Switzerland — with zero mines — top the import charts?**", "Ch. 4", "50–70% of the world's refined gold passes through Swiss hands. The Sankey shows the flows."),
        ("📋 **So: is gold actually a safe haven?**", "Ch. 5", "We answer the question directly, with numbers. No hedging."),
    ]

    for i, (q, chapter, desc) in enumerate(questions):
        col1, col2 = st.columns([0.08, 0.92])
        with col1:
            st.markdown(f"<div style='font-size:1.3rem; padding-top:4px;'>{q.split('**')[0]}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style='margin-bottom: 16px;'>
                <span style='font-size:0.7rem; color:#554d3a; letter-spacing:0.1em; text-transform:uppercase;'>{chapter}</span><br>
                <span style='font-size:1rem; color:#c0aa70; font-weight:500;'>{"**".join(q.split("**")[1:]).replace("**","")}</span><br>
                <span style='font-size:0.87rem; color:#6a6050;'>{desc}</span>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # short info about where the data comes from
    st.markdown("## The Data")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="insight-box" style="background:rgba(255,215,0,0.04); border-left:3px solid #FFD700; border-radius:0 6px 6px 0; padding:18px 22px; font-size:0.88rem; color:#a09070; line-height:1.65;">
            <strong style='color:#FFD700;'>UN Global Commodity Trade Statistics</strong><br>
            ~83,000 rows after filtering to precious metals<br>
            Period: 1988–2024 · 245 countries<br>
            Variables: country, year, metal type, trade flow,<br>value (USD), weight (kg)<br>
            <span style='font-size:0.8rem; color:#5a5040;'>Source: UN Comtrade via Kaggle · HS Codes 7106–7112</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="insight-box" style="background:rgba(255,215,0,0.04); border-left:3px solid #FFD700; border-radius:0 6px 6px 0; padding:18px 22px; font-size:0.88rem; color:#a09070; line-height:1.65;">
            <strong style='color:#FFD700;'>World Bank Global Inflation Database</strong><br>
            ~50,000 rows (209 countries × 6 inflation types)<br>
            Period: 1970–2025<br>
            Variables: country, inflation type (Headline, Food,<br>Energy, Core CPI, PPI, GDP Deflator), year<br>
            <span style='font-size:0.8rem; color:#5a5040;'>Source: Ha, Kose & Ohnsorge (2023) · World Bank</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; padding: 30px 0 10px; font-size:0.88rem; color:#4a4438;'>
        Use the sidebar to navigate through the five chapters →
    </div>
    """, unsafe_allow_html=True)
