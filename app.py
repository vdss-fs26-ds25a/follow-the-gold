
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="Is Gold Really the Safe Haven?",
    page_icon="🪙",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0b0d11 !important;
    color: #c0ab9a;
    font-family: 'DM Sans', sans-serif;
}

#MainMenu, footer, header {
    visibility: hidden;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif;
    color: #d3b099;
}

hr {
    border-color: #1c2029;
}

.chapter-badge {
    display: inline-block;
    background: rgba(211,176,153,0.08);
    color: #d3b099;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid rgba(211,176,153,0.18);
    margin-bottom: 12px;
}

.metric-card {
    background: linear-gradient(135deg, #13161f 0%, #1b1f29 100%);
    border: 1px solid #262b36;
    border-top: 3px solid #d3b099;
    border-radius: 10px;
    padding: 24px 20px;
    text-align: center;
}

.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #d3b099;
    margin-bottom: 6px;
}

.metric-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #6f6f70;
    margin-bottom: 8px;
}

.metric-insight {
    font-size: 0.88rem;
    color: #c0ab9a;
    line-height: 1.5;
}

.insight-box {
    background: rgba(211,176,153,0.04);
    border-left: 3px solid #d3b099;
    border-radius: 0 6px 6px 0;
    padding: 14px 18px;
    margin: 18px 0;
    font-size: 0.92rem;
    line-height: 1.6;
    color: #c0ab9a;
}

.caveat-box {
    background: rgba(111,111,112,0.06);
    border-left: 3px solid #6f6f70;
    border-radius: 0 6px 6px 0;
    padding: 12px 16px;
    margin: 14px 0;
    font-size: 0.82rem;
    line-height: 1.5;
    color: #6f6f70;
}

.source-note {
    font-size: 0.75rem;
    color: #6f6f70;
    margin-top: 4px;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/precious_metals_trade_1988_2024.csv")

df = load_data()

gold = df[df["metal_group"] == "Gold"]
gold_import = gold[gold["flow"] == "Import"]

st.sidebar.title("Exploration Controls")

selected_country = st.sidebar.selectbox(
    "Highlight Country",
    ["All Countries"] + sorted(df["country"].dropna().unique().tolist())
)

selected_year_range = st.sidebar.slider(
    "Global Year Range",
    1988,
    2024,
    (1988, 2024)
)

# ── INTRO ──────────────────────────────────────────────────────────────────
st.markdown("# Is Gold Really the Safe Haven?")
st.markdown("""
#### Gold prices hit record highs during inflation crises — but do physical trade flows support the safe haven narrative?

This project investigates global precious metals trade flows across 193 countries between 1988 and 2024.
""")
st.markdown("<small style='color:#6f6f70;'>Pre-2017 trade data: UN Comtrade HS 7106–7112 · Post-2016: BACI CEPII HS17 V202601</small>", unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""<div class="metric-card">
        <div class="metric-value">$3,000+</div>
        <div class="metric-label">Gold Price 2024</div>
        <div class="metric-insight">Highest recorded modern gold price per ounce</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="metric-card">
        <div class="metric-value">85%</div>
        <div class="metric-label">Turkey Inflation 2022</div>
        <div class="metric-insight">One of the highest inflation rates during the 2022–23 wave</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="metric-card">
        <div class="metric-value">70%</div>
        <div class="metric-label">Swiss Refining Share</div>
        <div class="metric-insight">Estimated share of globally refined gold processed in Switzerland</div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── CHAPTER 1 ──────────────────────────────────────────────────────────────
st.markdown('<div class="chapter-badge">Chapter 1</div>', unsafe_allow_html=True)
st.markdown("## Geographic Concentration of Gold Imports")

map_metric = st.radio(
    "Display Metric",
    ["Absolute Trade Value", "Share of Global Total (%)"],
    horizontal=True
)

country_totals = gold_import.groupby("country")["trade_value_usd"].sum().reset_index()

if map_metric == "Share of Global Total (%)":
    country_totals["value"] = (country_totals["trade_value_usd"] / country_totals["trade_value_usd"].sum()) * 100
    color_label = "Share (%)"
else:
    country_totals["value"] = country_totals["trade_value_usd"]
    color_label = "Trade Value (USD)"

fig1 = px.choropleth(
    country_totals,
    locations="country",
    locationmode="country names",
    color="value",
    hover_name="country",
    color_continuous_scale=[
        [0, "#111319"],
        [0.4, "#6f6f70"],
        [1, "#d3b099"]
    ],
    labels={"value": color_label},
    title="Gold Import Activity by Country"
)
fig1.update_layout(
    paper_bgcolor="#0b0d11",
    geo=dict(
        bgcolor="#0b0d11",
        showframe=False,
        showcoastlines=True,
        coastlinecolor="#1c2029",
        projection_type="natural earth",
        showland=True,
        landcolor="#1a1d24",
        scope="world"
    ),
    font_color="#c0ab9a",
    title_font_color="#d3b099"
)
st.plotly_chart(fig1, use_container_width=True)
st.markdown('<div class="source-note">Source: UN Comtrade + BACI CEPII. The choropleth emphasizes spatial concentration patterns rather than exact quantitative comparison.</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box">Large economies such as China, India, and Hong Kong dominate by absolute value. Switching to percentage share highlights Switzerland\'s disproportionate role relative to its population size.</div>', unsafe_allow_html=True)
st.markdown("---")

# ── CHAPTER 2 ──────────────────────────────────────────────────────────────
st.markdown('<div class="chapter-badge">Chapter 2</div>', unsafe_allow_html=True)
st.markdown("## Inflation and Crisis Dynamics")

gold_time = gold_import[
    (gold_import["year"] >= selected_year_range[0]) &
    (gold_import["year"] <= selected_year_range[1])
]

if selected_country != "All Countries":
    gold_time = gold_time[gold_time["country"] == selected_country]

gold_time = gold_time.groupby("year")["trade_value_usd"].sum().reset_index()
gold_time["trade_bn"] = gold_time["trade_value_usd"] / 1e9

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=gold_time["year"],
    y=gold_time["trade_bn"],
    mode="lines+markers",
    line=dict(color="#d3b099", width=3),
    marker=dict(size=5),
    name="Gold Imports"
))
for year, label in [(2008, "2008 Crisis"), (2020, "COVID-19"), (2022, "Inflation Wave")]:
    if selected_year_range[0] <= year <= selected_year_range[1]:
        fig2.add_vline(x=year, line_dash="dash", line_color="#6f6f70",
                      annotation_text=label, annotation_font_color="#6f6f70")
fig2.update_layout(
    title="Gold Import Value Over Time",
    paper_bgcolor="#0b0d11",
    plot_bgcolor="#10141c",
    font_color="#c0ab9a",
    title_font_color="#d3b099",
    xaxis=dict(gridcolor="#1c2029"),
    yaxis=dict(gridcolor="#1c2029", title="Trade Value (Billion USD)")
)
st.plotly_chart(fig2, use_container_width=True)
st.markdown('<div class="insight-box">Gold trade activity increases during major crisis periods including the 2008 financial crisis, COVID-19, and the 2022 inflation wave. The pattern is broadly consistent with safe-haven behavior.</div>', unsafe_allow_html=True)

st.markdown("### Inflation vs. Gold Imports")

scatter_year = st.slider("Scatterplot Year", 1988, 2024, 2022)

scatter_data = gold_import[gold_import["year"] == scatter_year].groupby("country")["trade_value_usd"].sum().reset_index()
scatter_data.columns = ["country", "trade_value"]
cpi_data = df[df["year"] == scatter_year][["country", "Headline CPI"]].drop_duplicates()
scatter_merged = scatter_data.merge(cpi_data, on="country", how="inner")
scatter_merged = scatter_merged[
    (scatter_merged["trade_value"] > 0) &
    (scatter_merged["Headline CPI"].between(-20, 200))
]

if len(scatter_merged) > 5:
    corr = scatter_merged["Headline CPI"].corr(np.log10(scatter_merged["trade_value"]))
    if abs(corr) < 0.2:
        strength = "Very Weak"
    elif abs(corr) < 0.4:
        strength = "Weak"
    elif abs(corr) < 0.6:
        strength = "Moderate"
    else:
        strength = "Strong"

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Correlation", f"{corr:.2f}")
    with m2:
        st.metric("Relationship Strength", strength)
    with m3:
        st.metric("Countries", len(scatter_merged))

    fig_scatter = px.scatter(
        scatter_merged,
        x="Headline CPI",
        y="trade_value",
        hover_name="country",
        log_y=True,
        trendline="ols",
        labels={"Headline CPI": "Headline CPI (%)", "trade_value": "Gold Imports (log USD)"},
        title=f"Inflation vs. Gold Imports ({scatter_year})",
        color_discrete_sequence=["#5298c2"]
    )
    fig_scatter.update_layout(
        paper_bgcolor="#0b0d11",
        plot_bgcolor="#10141c",
        font_color="#c0ab9a",
        title_font_color="#d3b099",
        xaxis=dict(gridcolor="#1c2029"),
        yaxis=dict(gridcolor="#1c2029")
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('<div class="source-note">Source: World Bank Global Inflation Database matched with UN Comtrade/BACI. Countries with CPI > 200% excluded.</div>', unsafe_allow_html=True)

st.markdown('<div class="insight-box">Inflation alone explains relatively little variation in gold import activity. The relationship is generally weak and differs across countries, suggesting that geopolitical factors, industrial demand, and financial market dynamics also play important roles.</div>', unsafe_allow_html=True)
st.markdown('<div class="caveat-box">⚠️ Correlation does not imply causation. Trade volumes reflect multiple overlapping forces beyond inflation alone.</div>', unsafe_allow_html=True)
st.markdown("---")

# ── CHAPTER 3 ──────────────────────────────────────────────────────────────
st.markdown('<div class="chapter-badge">Chapter 3</div>', unsafe_allow_html=True)
st.markdown("## Precious Metals Comparison")
st.markdown("Is gold's dominant position unique — or do all precious metals behave similarly during crises?")

metal_filter = st.multiselect(
    "Select Metals",
    ["Gold", "Silver", "Platinum"],
    default=["Gold", "Silver", "Platinum"]
)

df3 = df[
    (df["metal_group"].isin(metal_filter)) &
    (df["year"] >= selected_year_range[0]) &
    (df["year"] <= selected_year_range[1])
]

bar_data = df3.groupby("metal_group")["trade_value_usd"].sum().reset_index()
fig3a = px.bar(
    bar_data,
    x="metal_group",
    y="trade_value_usd",
    color="metal_group",
    color_discrete_map={
        "Gold": "#d3b099",
        "Silver": "#a3c1d0",
        "Platinum": "#c0ab9a"
    },
    labels={"metal_group": "Metal", "trade_value_usd": "Total Trade Value (USD)"},
    title="Total Trade Value by Metal"
)
fig3a.update_layout(
    showlegend=False,
    paper_bgcolor="#0b0d11",
    plot_bgcolor="#10141c",
    font_color="#c0ab9a",
    title_font_color="#d3b099",
    xaxis=dict(gridcolor="#1c2029"),
    yaxis=dict(gridcolor="#1c2029")
)
st.plotly_chart(fig3a, use_container_width=True)

time_data = df3.groupby(["year", "metal_group"])["trade_value_usd"].sum().reset_index()
fig3b = px.line(
    time_data,
    x="year",
    y="trade_value_usd",
    color="metal_group",
    color_discrete_map={
        "Gold": "#d3b099",
        "Silver": "#a3c1d0",
        "Platinum": "#c0ab9a"
    },
    labels={"year": "Year", "trade_value_usd": "Trade Value (USD)", "metal_group": "Metal"},
    title="Trade Value Over Time by Metal"
)
fig3b.update_layout(
    paper_bgcolor="#0b0d11",
    plot_bgcolor="#10141c",
    font_color="#c0ab9a",
    title_font_color="#d3b099",
    xaxis=dict(gridcolor="#1c2029"),
    yaxis=dict(gridcolor="#1c2029")
)
st.plotly_chart(fig3b, use_container_width=True)
st.markdown('<div class="source-note">Source: UN Comtrade HS 7106 (Silver), 7108 (Gold), 7110 (Platinum) + BACI CEPII 2017–2024.</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box">Gold accounts for ~$7.5T in total trade value — approximately 4× Silver ($1.9T) and 9× Platinum ($815B). While all metals show increased activity during crises, Gold\'s response is disproportionately larger.</div>', unsafe_allow_html=True)
st.markdown("---")

# ── CHAPTER 4 ──────────────────────────────────────────────────────────────
st.markdown('<div class="chapter-badge">Chapter 4</div>', unsafe_allow_html=True)
st.markdown("## The Swiss Connection")
st.markdown("Why does a landlocked country of 8 million sit at the center of global gold flows?")

swiss_data = df[(df["metal_group"] == "Gold") & (df["country"] == "Switzerland")]
global_gold = gold_import.groupby("year")["trade_value_usd"].sum().reset_index()
global_gold.columns = ["year", "global_total"]

flow_type = st.radio("Flow Type", ["Import", "Export", "Both"], horizontal=True)

if flow_type != "Both":
    swiss_data = swiss_data[swiss_data["flow"] == flow_type]

swiss_time = swiss_data.groupby("year")["trade_value_usd"].sum().reset_index()
swiss_time["trade_bn"] = swiss_time["trade_value_usd"] / 1e9

swiss_vs_global = swiss_time.merge(global_gold, on="year", how="left")
swiss_vs_global["share"] = (swiss_vs_global["trade_value_usd"] / swiss_vs_global["global_total"]) * 100

fig4a = go.Figure()
fig4a.add_trace(go.Bar(
    x=swiss_time["year"],
    y=swiss_time["trade_bn"],
    marker_color="#d3b099",
    hovertemplate="Year: %{x}<br>Value: $%{y:.2f}B<extra></extra>"
))
for year, label in [(2008, "2008"), (2020, "COVID"), (2022, "Inflation")]:
    fig4a.add_vline(x=year, line_dash="dash", line_color="#6f6f70",
                   annotation_text=label, annotation_font_color="#6f6f70")
fig4a.update_layout(
    title=f"Switzerland Gold Trade ({flow_type}) Over Time",
    paper_bgcolor="#0b0d11",
    plot_bgcolor="#10141c",
    font_color="#c0ab9a",
    title_font_color="#d3b099",
    xaxis=dict(gridcolor="#1c2029"),
    yaxis=dict(gridcolor="#1c2029", title="Trade Value (Billion USD)")
)
st.plotly_chart(fig4a, use_container_width=True)

fig4b = px.line(
    swiss_vs_global,
    x="year",
    y="share",
    title="Switzerland's Share of Global Gold Imports (%)",
    labels={"share": "Share (%)", "year": "Year"},
    color_discrete_sequence=["#5298c2"]
)
fig4b.update_layout(
    paper_bgcolor="#0b0d11",
    plot_bgcolor="#10141c",
    font_color="#c0ab9a",
    title_font_color="#d3b099",
    xaxis=dict(gridcolor="#1c2029"),
    yaxis=dict(gridcolor="#1c2029")
)
st.plotly_chart(fig4b, use_container_width=True)
st.markdown('<div class="source-note">Source: BACI CEPII HS17 (2017–2024) + UN Comtrade pre-2017.</div>', unsafe_allow_html=True)
st.markdown('<div class="insight-box">Switzerland\'s share of global gold trade fluctuates notably during crisis periods, suggesting its refining hub role intensifies when global demand spikes. Four major refineries in Ticino — Valcambi, PAMP, Argor-Heraeus, and Metalor — process raw gold and redistribute refined bars globally.</div>', unsafe_allow_html=True)
st.markdown("---")

# ── CHAPTER 5 ──────────────────────────────────────────────────────────────
st.markdown('<div class="chapter-badge">Chapter 5</div>', unsafe_allow_html=True)
st.markdown("## The Verdict")
st.markdown("#### What does the data tell us — and what remains uncertain?")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""<div class="metric-card">
        <div class="metric-value">Weak</div>
        <div class="metric-label">Inflation Correlation</div>
        <div class="metric-insight">Inflation alone explains relatively little variation in gold imports</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="metric-card">
        <div class="metric-value">4×</div>
        <div class="metric-label">Larger than Silver</div>
        <div class="metric-insight">Gold trade volume substantially exceeds other precious metals</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class="metric-card">
        <div class="metric-value">🇨🇭 Central</div>
        <div class="metric-label">Swiss Role</div>
        <div class="metric-insight">Switzerland becomes more prominent during crisis periods</div>
    </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
<b>Conclusion:</b> The analysis provides evidence broadly consistent with gold's safe-haven role during periods of economic uncertainty. 
However, inflation alone appears insufficient to explain global gold trade dynamics, indicating that additional geopolitical and financial mechanisms are likely involved.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="caveat-box">
⚠️ <b>Limitations:</b> This analysis relies on trade-flow data rather than investor-level behavior or ETF flows. 
Combining UN Comtrade and BACI datasets may introduce minor methodological discontinuities.
Future work could integrate gold price volatility, central bank reserves, and financial market indicators.
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<small style='color:#6f6f70;'>Data: UN Comtrade HS 7106–7112 (1988–2016) · BACI CEPII HS17 V202601 (2017–2024) · World Bank Global Inflation Database · VDSS FS2026</small>", unsafe_allow_html=True)
