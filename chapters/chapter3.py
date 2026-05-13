import streamlit as st
import pandas as pd
import plotly.express as px

def render():
    st.markdown('<div class="chapter-badge">Chapter 3</div>', unsafe_allow_html=True)
    st.title("Gold vs. Silver vs. Platinum")
    st.markdown("Does gold really stand apart from other precious metals — or do they all move together?")

    # load data
    df = pd.read_csv("data/processed/precious_metals_trade_1988_2024.csv")
    df = df[df["metal_group"] != "Other precious"]

    # --- Chart 1: Total Trade Value by Metal ---
    st.subheader("Total Trade Value by Metal (1988–2024)")

    bar_data = df.groupby("metal_group")["trade_value_usd"].sum().reset_index()

    fig1 = px.bar(
        bar_data,
        x="metal_group",
        y="trade_value_usd",
        color="metal_group",
        color_discrete_map={"Gold": "#FFD700", "Silver": "#C0C0C0", "Platinum": "#E5E4E2"},
        labels={"metal_group": "Metal", "trade_value_usd": "Total Trade Value (USD)"},
    )
    fig1.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#d4c5a0",
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    Gold dominates with $7.5 trillion in total trade value (1988–2024) — nearly 4x more than Silver ($1.9T) 
    and 9x more than Platinum ($815B). This confirms Gold's unique role as the primary precious metal in global trade.
    </div>
    """, unsafe_allow_html=True)

    # --- Chart 2: Trade Value over Time by Metal ---
    st.subheader("Trade Value Over Time")

    time_data = df.groupby(["year", "metal_group"])["trade_value_usd"].sum().reset_index()

    fig2 = px.line(
        time_data,
        x="year",
        y="trade_value_usd",
        color="metal_group",
        color_discrete_map={"Gold": "#FFD700", "Silver": "#C0C0C0", "Platinum": "#E5E4E2"},
        labels={"year": "Year", "trade_value_usd": "Trade Value (USD)", "metal_group": "Metal"},
    )
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#d4c5a0",
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    Gold trade surged after the 2008 financial crisis and again during the COVID-19 pandemic (2020) 
    and inflation wave (2022). Silver and Platinum follow similar but much smaller patterns — 
    suggesting all precious metals react to crises, but Gold reacts most strongly.
    </div>
    """, unsafe_allow_html=True)
