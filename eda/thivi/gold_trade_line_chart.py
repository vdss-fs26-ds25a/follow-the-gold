import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("precious_metals_trade_1988_2024.csv")

# only keep gold rows
gold = df[df["metal_group"] == "Gold"]

# sum up trade value per year and flow type, convert to billions
summary = (
    gold
    .groupby(["year", "flow"])["trade_value_usd"]
    .sum()
    .reset_index()
)
summary["trade_value_bn"] = (summary["trade_value_usd"] / 1e9).round(2)

# reshape so each flow type gets its own column
pivot = summary.pivot(index="year", columns="flow", values="trade_value_bn").reset_index()

years      = pivot["year"].tolist()
imports    = pivot["Import"].tolist()
exports    = pivot["Export"].tolist()
re_exports = pivot["Re-Export"].tolist()
re_imports = pivot["Re-Import"].tolist()

fig = go.Figure()

# import line goes all the way to 2024
fig.add_trace(go.Scatter(
    x=years,
    y=imports,
    name="Import",
    mode="lines+markers",
    line=dict(color="#FFD700", width=3),
    marker=dict(size=5),
    hovertemplate="<b>Import</b><br>Jahr: %{x}<br>Wert: $%{y:.1f}B<extra></extra>"
))

# export only has data until 2016, after that it's NaN so plotly leaves a gap
fig.add_trace(go.Scatter(
    x=years,
    y=exports,
    name="Export",
    mode="lines+markers",
    line=dict(color="#7EB8F7", width=2.5),
    marker=dict(size=5),
    hovertemplate="<b>Export</b><br>Jahr: %{x}<br>Wert: $%{y:.1f}B<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=years,
    y=re_exports,
    name="Re-Export",
    mode="lines+markers",
    line=dict(color="#B39DDB", width=2, dash="dot"),
    marker=dict(size=4),
    hovertemplate="<b>Re-Export</b><br>Jahr: %{x}<br>Wert: $%{y:.1f}B<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=years,
    y=re_imports,
    name="Re-Import",
    mode="lines+markers",
    line=dict(color="#80CBC4", width=1.5, dash="dot"),
    marker=dict(size=4),
    hovertemplate="<b>Re-Import</b><br>Jahr: %{x}<br>Wert: $%{y:.1f}B<extra></extra>"
))

fig.update_layout(
    title=dict(
        text="Globaler Goldhandel 1988–2024",
        font=dict(size=20, color="#FFD700"),
        x=0.02
    ),
    paper_bgcolor="#0f1117",
    plot_bgcolor="#161920",
    font=dict(family="Segoe UI, Arial", color="#cccccc"),
    height=580,
    margin=dict(l=70, r=50, t=70, b=60),

    xaxis=dict(
        title="Jahr",
        tickmode="linear",
        dtick=4,
        gridcolor="#252830",
        zeroline=False,
    ),

    yaxis=dict(
        title="Handelswert (USD Milliarden)",
        tickformat="$.0f",
        ticksuffix="B",
        gridcolor="#252830",
        zeroline=False,
    ),

    legend=dict(
        bgcolor="rgba(22,25,32,0.9)",
        bordercolor="#333",
        borderwidth=1,
        x=0.02,
        y=0.98,
        xanchor="left",
        yanchor="top"
    ),

    hovermode="x unified",

    shapes=[
        # light background to show the area where export data is missing
        dict(
            type="rect",
            xref="x", yref="paper",
            x0=2016.5, x1=2024.5,
            y0=0, y1=1,
            fillcolor="rgba(255,255,255,0.03)",
            line=dict(width=0)
        ),
        # dashed line at 2016 to mark the data cutoff
        dict(
            type="line",
            xref="x", yref="paper",
            x0=2016.5, x1=2016.5,
            y0=0, y1=1,
            line=dict(color="#555555", width=1.5, dash="dash")
        ),
    ],

    # labels for the key events on the timeline
    annotations=[
        dict(
            x=2008, y=70,
            text="2008<br>Finanzkrise",
            showarrow=True, arrowhead=2,
            arrowcolor="#555555", ax=0, ay=-45,
            font=dict(size=10, color="#aaaaaa"),
            bgcolor="rgba(30,33,45,0.85)",
            bordercolor="#444444", borderwidth=1
        ),
        dict(
            x=2011, y=210,
            text="2011<br>Gold-Preis Peak",
            showarrow=True, arrowhead=2,
            arrowcolor="#555555", ax=40, ay=-40,
            font=dict(size=10, color="#aaaaaa"),
            bgcolor="rgba(30,33,45,0.85)",
            bordercolor="#444444", borderwidth=1
        ),
        dict(
            x=2020, y=495,
            text="2020<br>COVID-19",
            showarrow=True, arrowhead=2,
            arrowcolor="#555555", ax=0, ay=-40,
            font=dict(size=10, color="#aaaaaa"),
            bgcolor="rgba(30,33,45,0.85)",
            bordercolor="#444444", borderwidth=1
        ),
        dict(
            x=2020.5, y=30,
            xref="x", yref="y",
            text="Export-Daten nicht verfügbar",
            showarrow=False,
            font=dict(size=9.5, color="#666666"),
            align="center"
        ),
    ]
)

fig.show()

# uncomment to save as html file
# fig.write_html("gold_trade_line_chart.html")
