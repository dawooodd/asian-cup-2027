"""
Page 3: Interactive AFC Asian Cup Match Simulator
Powered by Weighted Poisson + XGBoost Residual Model.
"""

import os
import sys
import streamlit as st
import pandas as pd
import numpy as np

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.models.weighted_poisson_xgboost_model import predict_match
from app.utils.styles import inject_custom_css
from app.utils.charts import create_match_donut_chart, create_scoreline_bar_chart

st.set_page_config(
    page_title="Match Simulator | AFC Asian Cup 2027",
    page_icon="🧮",
    layout="wide"
)

inject_custom_css()

# Load team data for TPI and selections
CSV_PATH = os.path.join(BASE_DIR, "data", "asian_cup_predictions.csv")

@st.cache_data
def load_teams():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        return dict(zip(df["Team"], df["Base_TPI"]))
    # Default fallback
    return {
        "Japan": 9.00, "South Korea": 7.57, "Iran": 7.42, "Australia": 6.73,
        "Qatar": 6.43, "Saudi Arabia": 7.20, "Uzbekistan": 5.45, "Iraq": 5.52,
        "United Arab Emirates": 5.46, "Jordan": 4.93, "Bahrain": 4.41,
        "Indonesia": 4.01, "Oman": 4.36, "Palestine": 3.23, "Syria": 3.33,
        "Thailand": 3.22, "China PR": 2.98, "Vietnam": 2.79, "India": 2.44,
        "Kyrgyzstan": 2.20, "Tajikistan": 2.62, "Lebanon": 2.60,
        "North Korea": 1.50, "Kuwait": 2.65
    }

team_tpi_map = load_teams()
team_names = list(team_tpi_map.keys())

# Page Title
st.markdown(
    """
    <div style="margin-bottom: 24px;">
        <span class="metric-badge badge-tha">BIVARIATE POISSON + XGBOOST RESIDUALS</span>
        <h1 style="color: #ffffff; margin-top: 6px; font-weight: 800;">
            🧮 Interactive Match Engine & Scoreline Simulator
        </h1>
        <p style="color: #94a3b8; font-size: 1.05rem;">
            Simulate any fixture with customizable stochastic luck variance, xG projections, and scoreline probability matrices.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Configuration Panel (Columns)
st.markdown("### ⚙️ Fixture Setup & Simulation Parameters")

cfg_col1, cfg_col2, cfg_col3 = st.columns([1.2, 1.2, 1.6])

with cfg_col1:
    team_a = st.selectbox(
        "Select Team A (Home / Pot 1):",
        team_names,
        index=team_names.index("Indonesia") if "Indonesia" in team_names else 0
    )
    tpi_a = team_tpi_map.get(team_a, 4.0)
    st.caption(f"🛡️ **{team_a}** Base TPI: `{tpi_a:.2f}`")

with cfg_col2:
    # Filter team_b choices to avoid identical team simulation by default
    team_b_options = [t for t in team_names if t != team_a]
    default_b = "Thailand" if "Thailand" in team_b_options else team_b_options[0]
    team_b = st.selectbox(
        "Select Team B (Away / Pot 2):",
        team_b_options,
        index=team_b_options.index(default_b) if default_b in team_b_options else 0
    )
    tpi_b = team_tpi_map.get(team_b, 3.2)
    st.caption(f"⚔️ **{team_b}** Base TPI: `{tpi_b:.2f}`")

with cfg_col3:
    luck_factor = st.slider(
        "Stochastic / Luck Factor (Variance Injection):",
        min_value=-0.50,
        max_value=0.50,
        value=0.00,
        step=0.05,
        help="Simulates external stochastic events: referee decisions, red cards, weather spikes, or home crowd surges. Negative favors Team B; Positive favors Team A."
    )
    if luck_factor > 0:
        st.caption(f"📈 Momentum skew: **+{luck_factor:.2f}** favoring **{team_a}**")
    elif luck_factor < 0:
        st.caption(f"📉 Momentum skew: **{luck_factor:.2f}** favoring **{team_b}**")
    else:
        st.caption("⚖️ Neutral baseline conditions (Zero stochastic distortion)")

st.write("")
simulate_btn = st.button("🚀 Run Match Simulation", type="primary", use_container_width=True)

# Run Simulation
if simulate_btn or "last_sim" not in st.session_state:
    with st.spinner(f"Computing Bivariate Poisson Matrix for {team_a} vs {team_b}..."):
        sim_result = predict_match(
            team_a_name=team_a,
            team_b_name=team_b,
            tpi_a=tpi_a,
            tpi_b=tpi_b,
            luck_factor=luck_factor
        )
        st.session_state["last_sim"] = sim_result
else:
    sim_result = st.session_state.get("last_sim")

if sim_result:
    st.markdown("---")
    st.markdown(f"### 🎯 Simulation Output: {sim_result['team_a']} vs {sim_result['team_b']}")

    # Metric Scorecard
    res_col1, res_col2, res_col3, res_col4 = st.columns(4)

    with res_col1:
        st.metric(
            label=f"{sim_result['team_a']} Win Prob",
            value=f"{sim_result['win_prob_a']}%",
            delta=f"xG: {sim_result['projected_xg_a']}"
        )

    with res_col2:
        st.metric(
            label="Draw Probability",
            value=f"{sim_result['draw_prob']}%",
            delta="Deadlock Rate"
        )

    with res_col3:
        st.metric(
            label=f"{sim_result['team_b']} Win Prob",
            value=f"{sim_result['win_prob_b']}%",
            delta=f"xG: {sim_result['projected_xg_b']}"
        )

    with res_col4:
        st.metric(
            label="Most Likely Scoreline",
            value=sim_result["most_likely_score"],
            delta=f"{sim_result['most_likely_score_prob']}% Likelihood",
            delta_color="normal"
        )

    st.write("")

    # Visualizations Row: Donut Chart & Scoreline Bar
    vcol1, vcol2 = st.columns([1, 1.2])

    with vcol1:
        fig_donut = create_match_donut_chart(
            win_a=sim_result["win_prob_a"],
            draw=sim_result["draw_prob"],
            win_b=sim_result["win_prob_b"],
            team_a=sim_result["team_a"],
            team_b=sim_result["team_b"]
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with vcol2:
        fig_scores = create_scoreline_bar_chart(
            scorelines=sim_result["top_scorelines"],
            team_a=sim_result["team_a"],
            team_b=sim_result["team_b"]
        )
        st.plotly_chart(fig_scores, use_container_width=True)

    # Tactical Analysis Box
    st.write("")
    st.markdown("### 📋 Automated Tactical Projection Summary")
    
    tpi_diff = sim_result["tpi_a"] - sim_result["tpi_b"]
    luck = sim_result["luck_factor"]
    
    analysis_text = (
        f"**Match Archetype:** "
    )
    if abs(tpi_diff) < 0.5:
        analysis_text += (
            f"Equally matched tactical deadlock. With a razor-thin TPI gap of **{abs(tpi_diff):.2f}**, "
            f"this contest exhibits high draw probability (**{sim_result['draw_prob']}%**). "
            f"Both managers are expected to deploy mid-blocks, with transitional counter-attacks deciding the outcome."
        )
    elif tpi_diff > 0:
        analysis_text += (
            f"Dominant favorite setup. **{sim_result['team_a']}** (TPI {sim_result['tpi_a']}) holds an offensive advantage, "
            f"generating a projected **{sim_result['projected_xg_a']} xG** against **{sim_result['team_b']}'s {sim_result['projected_xg_b']} xG**. "
            f"They possess a **{sim_result['win_prob_a']}%** win probability."
        )
    else:
        analysis_text += (
            f"Underdog dynamic. **{sim_result['team_b']}** (TPI {sim_result['tpi_b']}) outclasses **{sim_result['team_a']}**, "
            f"carrying a projected **{sim_result['win_prob_b']}%** chance of victory. "
            f"**{sim_result['team_a']}** must rely on low-block defensive resilience and set-pieces to salvage points."
        )
        
    if abs(luck) > 0.1:
        analysis_text += (
            f"\n\n**Stochastic Shock Alert:** The injected luck variance ({luck:+.2f}) noticeably alters the standard Poisson curve, "
            f"simulating irregular match conditions (e.g., early red card, referee intervention, or severe meteorological factors)."
        )

    st.info(analysis_text)

    # Detailed Scorelines Table in Expander
    with st.expander("🔍 View Detailed Scoreline Probabilities Table", expanded=False):
        df_top_scores = pd.DataFrame(sim_result["top_scorelines"])
        df_top_scores.rename(columns={
            "score": "Scoreline",
            "goals_a": f"Goals ({sim_result['team_a']})",
            "goals_b": f"Goals ({sim_result['team_b']})",
            "probability_pct": "Probability (%)"
        }, inplace=True)
        st.dataframe(df_top_scores, use_container_width=True)
