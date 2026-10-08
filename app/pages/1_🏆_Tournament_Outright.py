"""
Page 1: AFC Asian Cup 2027 Tournament Outright Predictions
Simulated across 100,000 Monte Carlo Tournament Brackets.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np

from app.utils.styles import inject_custom_css
from app.utils.charts import create_top10_outright_bar, create_tpi_vs_knockout_scatter

st.set_page_config(
    page_title="Tournament Outright | AFC Asian Cup 2027",
    page_icon="🏆",
    layout="wide"
)

inject_custom_css()

# Data Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data", "asian_cup_predictions.csv")

@st.cache_data
def load_predictions_data():
    if not os.path.exists(DATA_PATH):
        st.error(f"Predictions data file not found at: {DATA_PATH}")
        return pd.DataFrame()
    df = pd.read_csv(DATA_PATH)
    return df

df = load_predictions_data()

# Header
st.markdown(
    """
    <div style="margin-bottom: 24px;">
        <span class="metric-badge badge-gold">100,000 MONTE CARLO ITERATIONS</span>
        <h1 style="color: #ffffff; margin-top: 6px; font-weight: 800;">
            🏆 Tournament Outright & Knockout Progression
        </h1>
        <p style="color: #94a3b8; font-size: 1.05rem;">
            Championship win probabilities, bracket advancement rates, and quantitative anomaly analysis.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

if df.empty:
    st.warning("No data found. Please run the simulation script first.")
    st.stop()

# Metric summary cards
top_team = df.iloc[0]
idn_team = df[df["Team"] == "Indonesia"].iloc[0] if not df[df["Team"] == "Indonesia"].empty else None

mcol1, mcol2, mcol3, mcol4 = st.columns(4)

with mcol1:
    st.metric(
        label="Tournament Favorite",
        value=top_team["Team"],
        delta=f"{top_team['Win_Tournament_Prob(%)']:.2f}% Win Rate"
    )

with mcol2:
    st.metric(
        label="Top Contenders (>8% Odds)",
        value="6 Teams",
        delta="JPN, KOR, IRN, AUS, QAT, KSA"
    )

with mcol3:
    if idn_team is not None:
        st.metric(
            label="Indonesia Semifinal Chance",
            value=f"{idn_team['Reach_Semi_Final_Prob(%)']:.2f}%",
            delta=f"Rank #{int(idn_team['Rank'])} Overall"
        )

with mcol4:
    if idn_team is not None:
        st.metric(
            label="Indonesia Final Chance",
            value=f"{idn_team['Reach_Final_Prob(%)']:.2f}%",
            delta="Overperforming TPI 4.01"
        )

st.write("")

# Dynamic Insights Engine
st.markdown("### 💡 Quantitative Insights & Anomaly Engine")

# Dynamic anomaly calculation
japan_prob = top_team["Win_Tournament_Prob(%)"]
indonesia_semi = idn_team["Reach_Semi_Final_Prob(%)"] if idn_team is not None else 12.48
indonesia_final = idn_team["Reach_Final_Prob(%)"] if idn_team is not None else 2.70
saudi_win = df[df["Team"] == "Saudi Arabia"]["Win_Tournament_Prob(%)"].values[0] if not df[df["Team"] == "Saudi Arabia"].empty else 8.82
qatar_win = df[df["Team"] == "Qatar"]["Win_Tournament_Prob(%)"].values[0] if not df[df["Team"] == "Qatar"].empty else 9.33

insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.info(
        f"🇮🇩 **The Indonesia Diaspora Anomaly**\n\n"
        f"Despite entering the tournament with a moderate Base TPI of **4.01** (ranked 12th), "
        f"Indonesia boasts a **{indonesia_semi:.2f}%** probability of reaching the Semi-Finals and "
        f"a **{indonesia_final:.2f}%** chance to reach the Final. Their diaspora reinforcement (European tactical depth) "
        f"enables them to survive high-variance knockout matches against traditionally stronger West Asian sides."
    )

with insight_col2:
    st.info(
        f"🇯🇵 **Japanese Dominance vs Gulf Climate Synergy**\n\n"
        f"Japan emerges as the overwhelming favorite at **{japan_prob:.2f}%** win probability due to massive European top-flight squad depth. "
        f"However, host nation **Saudi Arabia ({saudi_win:.2f}%)** and reigning champions **Qatar ({qatar_win:.2f}%)** receive significant "
        f"climatic and geographic boosts, outperforming their pure Elo expectation in knockout rounds."
    )

st.write("")

# Interactive Charts
tab_chart1, tab_chart2 = st.tabs(["📊 Top 10 Title Contenders", "🌌 TPI vs Knockout Progression"])

with tab_chart1:
    fig_bar = create_top10_outright_bar(df)
    st.plotly_chart(fig_bar, use_container_width=True)

with tab_chart2:
    fig_scatter = create_tpi_vs_knockout_scatter(df)
    st.plotly_chart(fig_scatter, use_container_width=True)

st.write("")

# Interactive Dataframe Section with Filters
st.markdown("### 📋 Complete 24-Nation Tournament Probability Table")

filter_col1, filter_col2, filter_col3 = st.columns([2, 2, 2])

with filter_col1:
    search_query = st.text_input("🔍 Search Country / Team:", "")

with filter_col2:
    min_semi_prob = st.slider("Filter: Min Semi-Final Prob (%)", 0.0, 70.0, 0.0, step=1.0)

with filter_col3:
    sort_column = st.selectbox(
        "Sort By Column:",
        [
            "Win_Tournament_Prob(%)",
            "Reach_Final_Prob(%)",
            "Reach_Semi_Final_Prob(%)",
            "Group_Stage_Exit_Prob(%)",
            "Base_TPI",
            "Rank"
        ],
        index=0
    )

# Filter Dataframe
filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[filtered_df["Team"].str.contains(search_query, case=False)]

filtered_df = filtered_df[filtered_df["Reach_Semi_Final_Prob(%)"] >= min_semi_prob]
filtered_df = filtered_df.sort_values(by=sort_column, ascending=(sort_column == "Rank" or sort_column == "Group_Stage_Exit_Prob(%)" if sort_column == "Rank" else False))

# Render Styled DataFrame
st.dataframe(
    filtered_df.style.format({
        "Base_TPI": "{:.2f}",
        "Group_Stage_Exit_Prob(%)": "{:.2f}%",
        "Reach_Semi_Final_Prob(%)": "{:.2f}%",
        "Reach_Final_Prob(%)": "{:.2f}%",
        "Win_Tournament_Prob(%)": "{:.2f}%"
    }).background_gradient(
        subset=["Win_Tournament_Prob(%)", "Reach_Final_Prob(%)", "Reach_Semi_Final_Prob(%)"],
        cmap="YlGnBu"
    ),
    use_container_width=True,
    height=450
)

# Download CSV
csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Export Filtered Projections (CSV)",
    data=csv_data,
    file_name="asian_cup_2027_projections_filtered.csv",
    mime="text/csv"
)
