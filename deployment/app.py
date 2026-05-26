import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# ──────────────────────────────────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Follow the Gold — Who actually bought it in 2022?",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ──────────────────────────────────────────────────────────────────────────
# Styling — light editorial look, no sidebar, wide reading column
# ──────────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: #faf8f3 !important;
    color: #1a1a1a;
    font-family: 'DM Sans', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    max-width: 920px;
    margin: 0 auto;
    padding-top: 3rem;
    padding-bottom: 4rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

h1 {
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    color: #1a1a1a;
    font-size: 2.8rem;
    line-height: 1.1;
}

h2 {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    color: #1a1a1a;
    font-size: 2rem;
    margin-top: 0.5rem;
}

.beat-tag {
    display: inline-block;
    font-size: 0.7rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #8a6534;
    margin-bottom: 12px;
}

.lede {
    font-size: 1.05rem;
    line-height: 1.7;
    color: #2a2a2a;
    margin: 1rem 0 1.8rem;
}

.lede b { color: #1a1a1a; font-weight: 600; }

.caveat {
    font-size: 0.78rem;
    color: #6b6b6b;
    font-style: italic;
    border-left: 2px solid #d4d2cc;
    padding-left: 12px;
    margin: 0.4rem 0 1rem;
    line-height: 1.55;
}

.recap-num {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 900;
    line-height: 1;
    text-align: center;
    margin-bottom: 0.4rem;
}

.recap-label {
    color: #2a2a2a;
    font-size: 0.88rem;
    text-align: center;
    line-height: 1.5;
    margin-bottom: 1.5rem;
}

.verdict {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    line-height: 1.55;
    color: #1a1a1a;
    text-align: center;
    margin: 2.5rem 0 1rem;
    padding: 0 0.5rem;
}

.verdict-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    line-height: 1.65;
    color: #2a2a2a;
    text-align: center;
    margin: 0.5rem 1rem 2rem;
}

hr { border: none; border-top: 1px solid #e0ddd6; margin: 3rem 0; }

.sources {
    font-size: 0.72rem;
    color: #6b6b6b;
    text-align: center;
    line-height: 1.7;
}
</style>
""",
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────────────────────────────────
# Data — restrict story scope to 2017–2024, fix Türkiye encoding inline
# ──────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("data/processed/precious_metals_trade_1988_2024.csv")
    df["country"] = df["country"].replace({"TÃ¼rkiye": "Türkiye"})
    df = df[df["year"].between(2017, 2024)].copy()
    return df


df = load_data()
gold_imp = df[(df["metal_group"] == "Gold") & (df["flow"] == "Import")]


# ──────────────────────────────────────────────────────────────────────────
# Plot defaults — light editorial palette
# ──────────────────────────────────────────────────────────────────────────
BG = "#faf8f3"
GOLD = "#b88a2e"
GOLD_BRIGHT = "#d4a017"
MUTED = "#c8c5bc"
RED = "#b8472a"
BLUE = "#2e6e9b"
TEXT_DIM = "#6b6b6b"
TEXT = "#1a1a1a"
GRID = "#e0ddd6"


def style_fig(fig, height=420):
    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font_family="DM Sans",
        font_color=TEXT,
        font_size=12,
        title_font_color=TEXT,
        title_font_family="Playfair Display",
        title_font_size=16,
        margin=dict(l=10, r=10, t=50, b=40),
        height=height,
        showlegend=False,
        hoverlabel=dict(bgcolor="#ffffff", font_color=TEXT, font_family="DM Sans",
                        bordercolor=GRID),
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID)
    return fig


# ──────────────────────────────────────────────────────────────────────────
# Headline
# ──────────────────────────────────────────────────────────────────────────
st.markdown("# Follow the Gold")
st.markdown(
    '<div class="lede">When inflation hit in 2022 — the worst wave in forty years — the world was supposed to rush into gold. So who actually bought it?</div>',
    unsafe_allow_html=True,
)
st.markdown("<hr>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────
# BEAT 1 — The promise
# ──────────────────────────────────────────────────────────────────────────
st.markdown('<div class="beat-tag">Beat 1 · The promise</div>', unsafe_allow_html=True)
st.markdown("## Buy gold.")
st.markdown(
    '<div class="lede">Every time inflation rises, the advice is the same: buy gold. In 2022, inflation peaked at its highest level in forty years — and gold importers worldwide spent a record <b>$541 billion</b> bringing it across borders. The rule, on the surface, held.</div>',
    unsafe_allow_html=True,
)

global_series = gold_imp.groupby("year")["trade_value_usd"].sum().reset_index()
global_series["value_bn"] = global_series["trade_value_usd"] / 1e9

marker_colors = [GOLD if y == 2022 else MUTED for y in global_series["year"]]
marker_sizes = [16 if y == 2022 else 8 for y in global_series["year"]]

fig1 = go.Figure()
fig1.add_trace(
    go.Scatter(
        x=global_series["year"],
        y=global_series["value_bn"],
        mode="lines+markers",
        line=dict(color=MUTED, width=2),
        marker=dict(color=marker_colors, size=marker_sizes,
                    line=dict(color=marker_colors, width=0)),
        hovertemplate="%{x}: $%{y:.0f} B<extra></extra>",
    )
)
v2022 = float(global_series.loc[global_series["year"] == 2022, "value_bn"].iloc[0])
fig1.add_annotation(
    x=2022, y=v2022,
    text="<b>$541 B in 2022</b><br><span style='font-size:11px'>the year inflation peaked</span>",
    showarrow=True, arrowhead=2, arrowcolor=GOLD, arrowwidth=1.2,
    ax=-60, ay=-55,
    font=dict(color=GOLD, size=13, family="DM Sans"),
    align="left",
)
fig1.update_layout(title="Global gold imports, 2017 – 2024 (USD bn)")
fig1.update_xaxes(dtick=1)
fig1.update_yaxes(title=None)
fig1 = style_fig(fig1, height=380)
st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

st.markdown(
    '<div class="caveat">Sum of all reported gold imports across countries. Source: UN Comtrade HS 7108. Gold price changes, ETFs, and central-bank stocks are not in this number — only physical imports across borders.</div>',
    unsafe_allow_html=True,
)
st.markdown("<hr>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────
# BEAT 2 — The disconfirmation
# ──────────────────────────────────────────────────────────────────────────
st.markdown('<div class="beat-tag">Beat 2 · The disconfirmation</div>', unsafe_allow_html=True)
st.markdown("## But not in Caracas.")
st.markdown(
    '<div class="lede">In Venezuela, where inflation hit 201% in 2022, gold imports were effectively zero. Zimbabwe (105% inflation) imported $77 million. Lebanon (189% inflation) imported $1.1 billion. None of these countries appears on the list of large gold importers. The countries the safe-haven story says should be buying gold the hardest are barely buying it at all.</div>',
    unsafe_allow_html=True,
)

high_inflation = ["Venezuela", "Lebanon", "Sudan", "Zimbabwe", "Argentina", "Iran"]
low_inflation = ["Switzerland", "China", "United Arab Emirates", "India", "United Kingdom"]
curated = high_inflation + low_inflation

g22 = gold_imp[gold_imp["year"] == 2022].groupby("country", as_index=False).agg(
    value=("trade_value_usd", "sum"),
    cpi=("Headline CPI", "first"),
)

cpi22 = (
    df[df["year"] == 2022][["country", "Headline CPI"]]
    .drop_duplicates()
    .rename(columns={"Headline CPI": "cpi"})
)

curated_df = (
    pd.DataFrame({"country": curated})
    .merge(g22[["country", "value"]], on="country", how="left")
    .merge(cpi22, on="country", how="left")
)
curated_df["value"] = curated_df["value"].fillna(0)
curated_df["value_M"] = curated_df["value"] / 1e6
curated_df = curated_df.sort_values("cpi", ascending=True)  # low CPI at top of horizontal chart

def fmt_value(v_M: float) -> str:
    if v_M < 0.5:
        return " ≈ $0"
    if v_M < 1000:
        return f" ${v_M:,.0f} M"
    return f" ${v_M/1000:,.1f} B"

bar_colors = [RED if c in high_inflation else BLUE for c in curated_df["country"]]
y_labels = [f"{c}  ·  CPI {i:.0f}%" for c, i in zip(curated_df["country"], curated_df["cpi"])]

fig2 = go.Figure()
fig2.add_trace(
    go.Bar(
        x=curated_df["value_M"],
        y=y_labels,
        orientation="h",
        marker=dict(color=bar_colors),
        text=[fmt_value(v) for v in curated_df["value_M"]],
        textposition="outside",
        textfont=dict(color=TEXT, size=11, family="DM Sans"),
        cliponaxis=False,
        hovertemplate="%{y}<br>Gold imports 2022: %{text}<extra></extra>",
    )
)
fig2.update_layout(
    title="Gold imports in 2022 — high-inflation (red) vs. low-inflation (blue)",
    bargap=0.35,
)
fig2.update_xaxes(title="Gold imports 2022 (USD millions)", tickformat=",")
fig2.update_yaxes(title=None, automargin=True)
fig2 = style_fig(fig2, height=480)
st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

st.markdown(
    '<div class="caveat">Red bars: 2022 Headline CPI above 20%. Blue bars: below 10%. Trade flows are not the same as ETF investment or jewellery demand — we measure physical gold crossing borders, not gold being hoarded inside a country.</div>',
    unsafe_allow_html=True,
)
st.markdown("<hr>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────
# BEAT 3 — Then who?
# ──────────────────────────────────────────────────────────────────────────
st.markdown('<div class="beat-tag">Beat 3 · Then who?</div>', unsafe_allow_html=True)
st.markdown("## Then who?")
st.markdown(
    '<div class="lede">So who imported the $541 billion of gold the world bought in 2022? At the top of the list: Switzerland, China, the UAE, the UK, India. Five countries took roughly two-thirds of the total. Four of the five had inflation rates of 6% or below — the opposite of what the safe-haven story would predict.</div>',
    unsafe_allow_html=True,
)

top22 = g22.sort_values("value", ascending=False).head(8).copy()
top22["value_bn"] = top22["value"] / 1e9
top22 = top22.sort_values("value_bn", ascending=True)  # ascending so largest is on top

def cpi_label(c: float) -> str:
    if pd.isna(c):
        return "n/a"
    return f"{c:.1f}%"

text_labels = [
    f"  ${v:.0f} B  ·  CPI {cpi_label(c)}"
    for v, c in zip(top22["value_bn"], top22["cpi"])
]

fig3 = go.Figure()
fig3.add_trace(
    go.Bar(
        x=top22["value_bn"],
        y=top22["country"],
        orientation="h",
        marker=dict(
            color=top22["cpi"].fillna(top22["cpi"].mean()),
            colorscale=[[0, BLUE], [0.5, "#bfa97a"], [1, RED]],
            cmin=0, cmax=10,
            line=dict(width=0),
            colorbar=dict(
                title=dict(text="CPI<br>%", font=dict(color=TEXT, size=10)),
                thickness=10, len=0.55, x=1.04,
                tickfont=dict(color=TEXT, size=10),
            ),
        ),
        text=text_labels,
        textposition="outside",
        textfont=dict(color=TEXT, size=11, family="DM Sans"),
        cliponaxis=False,
        hovertemplate="%{y}<br>Imports: $%{x:.1f} B<extra></extra>",
    )
)
fig3.update_layout(title="Top gold importers in 2022, coloured by Headline CPI")
fig3.update_xaxes(title="Gold imports 2022 (USD bn)")
fig3.update_yaxes(title=None, automargin=True)
fig3 = style_fig(fig3, height=420)
st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

st.markdown(
    '<div class="caveat">Five countries — Switzerland, China, UAE, UK, India — together imported about 64% of the world\'s gold in 2022. Most are low-inflation economies. The pattern points away from "consumers fleeing inflation" and toward something else.</div>',
    unsafe_allow_html=True,
)
st.markdown("<hr>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────
# BEAT 4 — The reveal
# ──────────────────────────────────────────────────────────────────────────
st.markdown('<div class="beat-tag">Beat 4 · The reveal</div>', unsafe_allow_html=True)
st.markdown("## China doubled down.")
st.markdown(
    '<div class="lede">China\'s gold imports in 2021: $39 billion. In 2022, the year inflation peaked: <b>$85 billion</b>. A doubling, in one year. That same February, Russia invaded Ukraine — and the United States, the EU, and Japan froze about $300 billion of Russia\'s foreign reserves. The signal to every other central bank was unambiguous: dollar reserves can be switched off. In 2022, central banks worldwide bought <b>1,136 tons of gold</b> — the most since 1950.</div>',
    unsafe_allow_html=True,
)

china = (
    gold_imp[gold_imp["country"] == "China"]
    .groupby("year", as_index=False)["trade_value_usd"]
    .sum()
)
china["value_bn"] = china["trade_value_usd"] / 1e9
china_colors = [GOLD_BRIGHT if y == 2022 else MUTED for y in china["year"]]

fig4 = go.Figure()
fig4.add_trace(
    go.Bar(
        x=china["year"],
        y=china["value_bn"],
        marker_color=china_colors,
        text=[f"${v:.0f} B" for v in china["value_bn"]],
        textposition="outside",
        textfont=dict(color=TEXT, size=11, family="DM Sans"),
        cliponaxis=False,
        hovertemplate="%{x}: $%{y:.1f} B<extra></extra>",
    )
)

v_2020 = float(china.loc[china["year"] == 2020, "value_bn"].iloc[0])
v_2022 = float(china.loc[china["year"] == 2022, "value_bn"].iloc[0])

fig4.add_annotation(
    x=2020, y=v_2020,
    text="<b>COVID</b><br><span style='font-size:10px'>imports collapse</span>",
    showarrow=True, arrowhead=2, arrowcolor=TEXT_DIM, arrowwidth=1,
    ax=-40, ay=-50, font=dict(color=TEXT_DIM, size=11, family="DM Sans"),
    align="left",
)
fig4.add_annotation(
    x=2022, y=v_2022,
    text="<b>+116% vs. 2021</b><br><span style='font-size:10px'>Russia/Ukraine · G7 freezes reserves</span>",
    showarrow=True, arrowhead=2, arrowcolor=GOLD, arrowwidth=1.2,
    ax=-100, ay=-60, font=dict(color=GOLD, size=12, family="DM Sans"),
    align="left",
)

fig4.update_layout(title="China gold imports, 2017 – 2024")
fig4.update_xaxes(dtick=1, title=None)
fig4.update_yaxes(title="Imports (USD bn)")
fig4 = style_fig(fig4, height=420)
st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

st.markdown(
    '<div class="caveat">Gold import data: UN Comtrade HS 7108. Central-bank gold purchases (1,136 tons in 2022, the highest since 1950) and the $300 B reserve freeze figure: World Gold Council, <i>Gold Demand Trends Full Year 2022</i>, and public reporting on the February 2022 G7 sanctions package.</div>',
    unsafe_allow_html=True,
)
st.markdown("<hr>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────
# BEAT 5 — Verdict
# ──────────────────────────────────────────────────────────────────────────
st.markdown('<div class="beat-tag">Beat 5 · Verdict</div>', unsafe_allow_html=True)
st.markdown("## The verdict.")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="recap-num" style="color:#b88a2e">+116%</div>', unsafe_allow_html=True)
    st.markdown('<div class="recap-label">China\'s gold imports<br>2021 → 2022</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="recap-num" style="color:#b8472a">≈ $0</div>', unsafe_allow_html=True)
    st.markdown('<div class="recap-label">Imported by Venezuela<br>in 2022 (CPI 201%)</div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="recap-num" style="color:#b88a2e">1,136 t</div>', unsafe_allow_html=True)
    st.markdown('<div class="recap-label">Central-bank gold buying<br>worldwide, 2022 —<br>highest since 1950</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="verdict">"Buy gold when inflation hits" is a story about consumers.<br>The 2022 data isn\'t.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="verdict-sub">The people in Caracas and Harare didn\'t buy gold. The central banks in Beijing, Abu Dhabi, and Ankara did. Gold\'s safe-haven role is alive — it is just no longer the citizen\'s hedge against inflation. It is the sovereign\'s hedge against the dollar.</div>',
    unsafe_allow_html=True,
)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    '<div class="sources">'
    'Data: UN Comtrade HS 7108 (gold imports, 2017 – 2024) · World Bank Global Inflation Database (Headline CPI). '
    'External citations on this page: World Gold Council, <i>Gold Demand Trends Full Year 2022</i> (central-bank purchase volumes); '
    'public reporting on the February 2022 G7 freeze of Russian foreign reserves. '
    '<br><br>VDSS FS2026 · Gruppe 3 — Schwarz · Omokaro · Thirukumar'
    '</div>',
    unsafe_allow_html=True,
)
