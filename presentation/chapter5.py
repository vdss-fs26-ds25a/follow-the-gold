import streamlit as st


def render():
    # chapter label + title
    st.markdown('<div style="display:inline-block; background:rgba(255,215,0,0.1); color:#FFD700; font-size:0.72rem; letter-spacing:0.15em; text-transform:uppercase; padding:4px 12px; border-radius:20px; border:1px solid rgba(255,215,0,0.25); margin-bottom:12px;">Chapter 5</div>', unsafe_allow_html=True)
    st.markdown("# The Verdict")
    st.markdown("""
    <p style='font-size:1.08rem; color:#8a7d5a; max-width:680px; line-height:1.72; margin-bottom:32px;'>
    We followed gold across 37 years, 245 countries, and $7.5 trillion in trade.
    Here is what the data says — directly, without hedging.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("## The Research Questions — Answered")

    # answer each of the 4 research questions
    _verdict_row(
        "🗺️",
        "Where does gold flow?",
        "Toward refineries, not toward crises.",
        """Switzerland — a country with zero gold mines — is the world's #1 gold importer
        by value at $739.5B. Gold flows from mining nations (South Africa, Australia, Russia)
        to refining hubs first, then on to demand centers. Trade geography follows
        industrial capacity, not just inflation fears.""",
        verdict="Unexpected",
        verdict_color="#a0c4ff",
    )

    _verdict_row(
        "📉",
        "Do high-inflation countries import more gold?",
        "No clear signal in the trade data.",
        """The correlation between a country's Headline CPI and its gold import value
        is essentially zero (r = −0.002). Countries with very high inflation (>5%) actually
        show slightly <em>lower</em> average import values than low-inflation countries —
        likely because high-inflation nations often lack the foreign-exchange reserves
        to buy gold on world markets. The simple narrative doesn't hold.""",
        verdict="Myth Busted",
        verdict_color="#ff9d9d",
    )

    _verdict_row(
        "⚖️",
        "Is gold special among precious metals?",
        "Yes — by a wide margin.",
        """Gold accounts for 71.1% of all precious metals trade value ($7.51T of $10.57T total).
        Silver contributes 17.6%, platinum 7.7%. During the 2008 crisis and COVID-19, gold's
        share grew relative to silver and platinum — confirming that in stress periods,
        investors and institutions specifically reach for gold, not precious metals broadly.""",
        verdict="Confirmed",
        verdict_color="#b9f0a0",
    )

    _verdict_row(
        "🇨🇭",
        "What makes Switzerland the gold hub?",
        "Refining capacity + political neutrality + banking secrecy.",
        """Switzerland's four major refineries (Valcambi, PAMP, Argor-Heraeus, Metalor)
        process an estimated 50–70% of the world's refined gold. The data shows Switzerland
        with 3,469 import records and only 31 export records — a structural imbalance
        that reflects its role as a transformation hub rather than a final destination.
        In the Sankey diagram, this asymmetry is the defining visual feature.""",
        verdict="Confirmed",
        verdict_color="#b9f0a0",
    )

    st.divider()

    # 6 summary numbers as cards (2 rows of 3)
    st.markdown("## By the Numbers")

    metrics = [
        {
            "value": "$7.51T",
            "label": "Total Gold Traded",
            "desc": "37 years of global gold imports and exports combined — equivalent to roughly 3× the annual US GDP at time of peak flows.",
        },
        {
            "value": "71.1%",
            "label": "Gold's PM Trade Share",
            "desc": "Gold dominates precious metals trade. Silver (17.6%) and platinum (7.7%) are significant but secondary.",
        },
        {
            "value": "≈ 0",
            "label": "CPI–Gold Import Correlation",
            "desc": "Across all country-years in the dataset, inflation rate explains essentially none of the variation in gold imports.",
        },
        {
            "value": "#1",
            "label": "Switzerland's Import Rank",
            "desc": "$739.5B imported — ahead of India ($737.1B) and China ($574.2B) — despite having no mines.",
        },
        {
            "value": "+9,798%",
            "label": "Gold Import Growth (1988–2023)",
            "desc": "From $5.9B in 1988 to $579.8B in 2023. The bulk of growth came post-2008 and accelerated sharply post-2020.",
        },
        {
            "value": "2020–23",
            "label": "The Real Inflection Point",
            "desc": "COVID-19 and the geopolitical shock of 2022 drove gold imports to record highs — more than any inflation data point.",
        },
    ]

    for row in range(0, len(metrics), 3):
        cols = st.columns(3)
        for i, col in enumerate(cols):
            if row + i < len(metrics):
                m = metrics[row + i]
                col.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{m['value']}</div>
                    <div class="metric-label">{m['label']}</div>
                    <div class="metric-insight">{m['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    st.divider()

    # final conclusion text
    st.markdown("## So — Is Gold Really the Safe Haven?")

    st.markdown("""
    <div class="insight-box" style="background:rgba(255,215,0,0.04); border-left:3px solid #FFD700; border-radius:0 6px 6px 0; padding:22px 26px; margin:0 0 24px; font-size:0.97rem; color:#c0aa70; line-height:1.75;">
    <strong style='color:#FFD700; font-size:1.05rem;'>The short answer: partly yes, but not in the way the narrative claims.</strong><br><br>
    Gold's <em>price</em> rises during crises — that part of the story is real. Gold broke $3,000/oz
    in 2025, driven by geopolitical uncertainty and record central bank purchases.
    But the <em>trade flow</em> data tells a different story: high-inflation countries do not
    systematically import more gold. In fact, the countries driving record import volumes
    are wealthy, stable economies and refining hubs — not countries fleeing runaway inflation.<br><br>
    The real drivers of the post-2020 gold surge were <strong>geopolitics</strong> (the "weaponized dollar"
    fear after Russia's 2022 sanctions), <strong>central bank diversification</strong> (BRICS nations
    buying over 1,000 tons/year), and <strong>COVID-era uncertainty</strong> — not consumer
    inflation in developing economies.<br><br>
    <strong>Gold is a geopolitical shield first, an inflation hedge second.</strong>
    </div>
    """, unsafe_allow_html=True)

    # known issues with the data
    with st.expander("📋 Data Limitations & Caveats"):
        st.markdown("""
        - **Dataset gap**: The UN trade data runs 1988–2016 for export/re-export flows; import data extends to 2024.
          The 2022–23 inflation wave is therefore only partially visible through imports.
        - **Weight data quality**: 16,765 records have `weight_kg = 0`; weight-based analysis should be treated cautiously.
        - **Switzerland silver only**: Switzerland's silver entries dominate by count;
          the Sankey in Chapter 4 focuses on gold flows specifically.
        - **Correlation ≠ causation**: The near-zero CPI correlation does not mean inflation
          *never* affects gold demand — it means the effect isn't visible at country-year level
          in trade data. Price-level effects may operate through futures markets, not physical trade.
        - **Missing 2022–25 context**: BRICS central bank buying, Russia sanctions, and
          the geopolitical gold surge post-2022 are discussed qualitatively but fall
          partially outside the dataset's full coverage window.
        """)

    st.divider()
    st.markdown("""
    <div style='text-align:center; padding:20px 0; font-size:0.8rem; color:#3a3428; line-height:2;'>
        VDSS Visualisierungsprojekt FS2026 · ZHAW<br>
        Vale Schwarz · Aisosa Omokaro · Thivi Thirukumar<br>
        Data: UN Comtrade · World Bank (Ha, Kose & Ohnsorge, 2023)
    </div>
    """, unsafe_allow_html=True)


# helper function to show one research question + answer block
def _verdict_row(icon, question, headline, body, verdict, verdict_color):
    col1, col2 = st.columns([0.06, 0.94])
    with col1:
        st.markdown(f"<div style='font-size:1.8rem; padding-top:4px;'>{icon}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style='margin-bottom:22px;'>
            <div style='font-size:0.72rem; color:#554d3a; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:4px;'>
                Research Question
            </div>
            <div style='font-size:1.05rem; color:#c0b080; font-weight:500; margin-bottom:6px;'>{question}</div>
            <div style='display:flex; align-items:center; gap:12px; margin-bottom:8px;'>
                <span style='font-size:1rem; color:#FFD700; font-family: Playfair Display, serif;'>{headline}</span>
                <span style='font-size:0.68rem; background:rgba(0,0,0,0.3); color:{verdict_color};
                    border:1px solid {verdict_color}40; padding:2px 10px; border-radius:20px;
                    letter-spacing:0.1em; text-transform:uppercase;'>{verdict}</span>
            </div>
            <div style='font-size:0.875rem; color:#7a7060; line-height:1.65;'>{body}</div>
        </div>
        """, unsafe_allow_html=True)
