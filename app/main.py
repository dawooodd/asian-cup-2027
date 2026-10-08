"""
AFC Asian Cup 2027 Analytics & Match Simulation Hub
Main Landing Page & Methodology Center
"""

import os
import streamlit as st
import pandas as pd
from app.utils.styles import inject_custom_css

# Page Configuration
st.set_page_config(
    page_title="AFC Asian Cup 2027 | Predictive Analytics Hub",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_css()

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_PATH = os.path.join(DATA_DIR, "asian_cup_predictions.csv")

# Load high-level tournament dataset
@st.cache_data
def load_quick_stats():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    return pd.DataFrame()

df_preds = load_quick_stats()

# Hero Section
st.markdown(
    """
    <div class="hero-banner">
        <div class="section-tag">AFC ASIAN CUP SAUDI ARABIA 2027 • OFFICIAL ANALYTICS PORTAL</div>
        <h1 style="color: #ffffff; margin-top: 4px; font-weight: 800; font-size: 2.4rem;">
            Predictive Quantitative Engine & Tournament Simulator
        </h1>
        <p style="color: #94a3b8; font-size: 1.1rem; line-height: 1.6; max-width: 950px; margin-top: 10px;">
            A state-of-the-art sports data science platform combining 
            <b>Weighted Poisson Distributions</b>, <b>XGBoost Residual Ensembles</b>, and 
            <b>100,000 Monte Carlo Stochastic Tournaments</b> to forecast championship outcomes, 
            analyze historical tactical telemetry, and simulate head-to-head fixtures in real-time.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# High-Level Metrics Row
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Participating Nations",
        value="24 Teams",
        delta="6 Groups of 4"
    )

with col2:
    st.metric(
        label="Monte Carlo Simulations",
        value="100,000",
        delta="Full Brackets"
    )

with col3:
    st.metric(
        label="Host Nation",
        value="Saudi Arabia",
        delta="10% Proximity Boost"
    )

with col4:
    top_favorite = df_preds.iloc[0]["Team"] if not df_preds.empty else "Japan"
    top_prob = df_preds.iloc[0]["Win_Tournament_Prob(%)"] if not df_preds.empty else 39.17
    st.metric(
        label="Top Title Favorite",
        value=top_favorite,
        delta=f"{top_prob:.1f}% Win Prob",
        delta_color="normal"
    )

with col5:
    idn_row = df_preds[df_preds["Team"] == "Indonesia"] if not df_preds.empty else None
    idn_semi = idn_row.iloc[0]["Reach_Semi_Final_Prob(%)"] if idn_row is not None and not idn_row.empty else 12.48
    st.metric(
        label="Indonesia Semis Odds",
        value=f"{idn_semi:.1f}%",
        delta="TPI 4.01 (#12 Rank)",
        delta_color="normal"
    )

st.write("")

# Navigation Feature Cards
st.markdown("### 🧭 Explore Analytics Modules")
mod_col1, mod_col2, mod_col3 = st.columns(3)

with mod_col1:
    st.markdown(
        """
        <div class="analytics-card">
            <span class="metric-badge badge-gold">Module 01</span>
            <h3 style="color: #f0f6fc; margin-top: 10px;">🏆 Tournament Outright</h3>
            <p style="color: #8b949e; font-size: 0.95rem; line-height: 1.5;">
                Explore championship probabilities, knockout progression matrices, and anomalies 
                across all 24 qualified nations. Filter by progression stage and discover underdogs.
            </p>
            <p style="margin-top: 15px; color: #38bdf8; font-weight: 600;">
                👉 Open via Sidebar: <i>1_🏆_Tournament_Outright</i>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with mod_col2:
    st.markdown(
        """
        <div class="analytics-card">
            <span class="metric-badge badge-idn">Module 02</span>
            <h3 style="color: #f0f6fc; margin-top: 10px;">⚔️ H2H Deep Dive</h3>
            <p style="color: #8b949e; font-size: 0.95rem; line-height: 1.5;">
                Granular tactical autopsy of the epic 120-minute FIFA ASEAN Cup 2026 Final: 
                Spider radar charts, tactical substitution impacts, and cumulative xG line trajectories.
            </p>
            <p style="margin-top: 15px; color: #38bdf8; font-weight: 600;">
                👉 Open via Sidebar: <i>2_⚔️_H2H_Deep_Dive</i>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with mod_col3:
    st.markdown(
        """
        <div class="analytics-card">
            <span class="metric-badge badge-tha">Module 03</span>
            <h3 style="color: #f0f6fc; margin-top: 10px;">🧮 Match Simulator</h3>
            <p style="color: #8b949e; font-size: 0.95rem; line-height: 1.5;">
                Run head-to-head predictive simulations between any two teams. 
                Dynamically adjust the stochastic luck variance factor and view exact scoreline distributions.
            </p>
            <p style="margin-top: 15px; color: #38bdf8; font-weight: 600;">
                👉 Open via Sidebar: <i>3_🧮_Match_Simulator</i>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Methodology & Architectural Deep Dive Tabs
st.write("")
st.markdown("### 🔬 Scientific Methodology & Mathematical Architecture")

tab_math, tab_arch, tab_dataset = st.tabs([
    "📐 Predictive Weighting Schema",
    "🏗️ Modular Repository Architecture",
    "📊 Dataset & Sources"
])

with tab_math:
    st.markdown(
        """
        #### 1. Five-Pillar Team Power Index (TPI)
        Each nation's Base TPI is computed as a weighted harmonic composite score spanning five independent domains:
        
        $$TPI_i = 0.40 \\cdot ELO_i + 0.30 \\cdot \\ln(SquadValue_i) + 0.10 \\cdot Host_i + 0.10 \\cdot Climate_i + 0.10 \\cdot Luck_i$$
        
        - **Historical Match Performance ($W_1 = 40\%$)**: 4-year FIFA/AFC match history translated into Elo ratings adjusted for goal difference and opponent caliber.
        - **Squad Value & European Pedigree ($W_2 = 30\%$)**: Log-transformed Transfermarkt market values combined with UEFA Top-5 League player counts.
        - **Host & Geographic Advantage ($W_3 = 10\%$)**: Travel distance penalty plus host bonus for Saudi Arabia.
        - **Weather & Climate Adaptability ($W_4 = 10\%$)**: Empirical adjustment for Gulf desert conditions (30°C+ heat and low humidity).
        - **Stochastic Tournament Variance ($W_5 = 10\%$)**: Gaussian white noise $\\mathcal{N}(0, \\sigma^2)$ reflecting tournament luck, referee variance, and penalty shootouts.
        
        #### 2. Weighted Poisson + XGBoost Residual Model
        Match scorelines are generated via a Bivariate Poisson distribution parameterized by attack and defense coefficients:
        
        $$P(X = x, Y = y) = \\frac{\\lambda_A^x e^{-\\lambda_A}}{x!} \\times \\frac{\\lambda_B^y e^{-\\lambda_B}}{y!}$$
        
        Residual probabilities are passed through an XGBoost model calibrated on tournament draws, fatigue regressions, and tactical substitutions.
        """
    )

with tab_arch:
    st.markdown(
        """
        #### Clean Modular Repository Architecture
        The repository is organized according to production-grade software engineering standards:
        ```text
        asian-cup-2027/
        │
        ├── data/                  # Standardized data lake (CSV, JSON telemetry)
        │   ├── asian_cup_predictions.csv
        │   ├── indonesia_vs_thailand_analytics.json
        │   └── model_prediction_output.json
        │
        ├── src/                   # Pure python logic, models & pipelines
        │   ├── data_pipeline/     # Data ingestion & schema normalization
        │   ├── models/            # Poisson-XGBoost ensemble & prediction APIs
        │   ├── simulation/        # 100,000 Monte Carlo tournament runner
        │   └── legacy_viz/        # Preserved static matplotlib/seaborn generators
        │
        ├── notebooks/             # Exploratory Jupyter Notebooks
        │   └── match_analysis.ipynb
        │
        ├── viz_outputs/           # Static PNG visual assets
        │
        ├── app/                   # Multipage Streamlit Application
        │   ├── main.py            # Application entry point
        │   ├── pages/             # Dynamic dashboard views
        │   │   ├── 1_🏆_Tournament_Outright.py
        │   │   ├── 2_⚔️_H2H_Deep_Dive.py
        │   │   └── 3_🧮_Match_Simulator.py
        │   └── utils/             # Interactive Plotly charts & styling
        │
        └── requirements.txt       # Pinned production dependencies
        ```
        """
    )

with tab_dataset:
    st.markdown(
        """
        - **Tournament Outright Dataset**: `data/asian_cup_predictions.csv` — Contains 24 qualified nations with Base TPI and probability distributions for Group Exit, Semi-Finals, Finals, and Tournament Championship.
        - **Match Telemetry Dataset**: `data/indonesia_vs_thailand_analytics.json` — 1,600+ lines of granular telemetry capturing Schema A (Team stats), Schema B (Individual player ratings), Schema C (Substitution event log), and H2H match history.
        - **Predictive Model Output**: `data/model_prediction_output.json` — Pre-calibrated Poisson matrix for Indonesia vs Thailand final projection.
        """
    )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #8b949e; font-size: 0.85rem; padding-bottom: 20px;">
        AFC Asian Cup 2027 Quantitative Intelligence Engine • Built with Streamlit & Plotly • © 2026 Sports Science Division
    </div>
    """,
    unsafe_allow_html=True
)
