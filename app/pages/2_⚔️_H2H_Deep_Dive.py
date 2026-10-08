"""
Page 2: Indonesia vs Thailand Head-to-Head Deep Dive
Granular 120-Minute Tactical Autopsy & Telemetry Analysis.
"""

import os
import json
import streamlit as st
import pandas as pd
import numpy as np

from app.utils.styles import inject_custom_css
from app.utils.charts import create_radar_chart, create_substitution_timeline_chart

st.set_page_config(
    page_title="H2H Deep Dive | Indonesia vs Thailand",
    page_icon="⚔️",
    layout="wide"
)

inject_custom_css()

# Data Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data", "indonesia_vs_thailand_analytics.json")

@st.cache_data
def load_match_analytics():
    if not os.path.exists(DATA_PATH):
        st.error(f"Analytics file not found at: {DATA_PATH}")
        return {}
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

data = load_match_analytics()
deep_dive = data.get("deep_dive_120_match", {})
team_stats = deep_dive.get("schema_a_team_statistics", {})
player_stats = deep_dive.get("schema_b_individual_player_statistics_and_ratings", {})
subs_log = deep_dive.get("schema_c_substitution_and_tactical_log", [])
match_history = data.get("match_history_summary", [])

# Page Title
st.markdown(
    """
    <div style="margin-bottom: 24px;">
        <span class="metric-badge badge-idn">FIFA ASEAN CUP 2026 FINAL</span>
        <span class="metric-badge badge-gold">120-MINUTE THRILLER</span>
        <h1 style="color: #ffffff; margin-top: 6px; font-weight: 800;">
            ⚔️ Indonesia vs Thailand: Tactical Telemetry Deep Dive
        </h1>
        <p style="color: #94a3b8; font-size: 1.05rem;">
            Exhaustive analytical breakdown of the most intense regional final in ASEAN history.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Match Scoreboard Banner
st.markdown(
    """
    <div style="background: linear-gradient(90deg, rgba(230,57,70,0.15) 0%, rgba(15,23,42,0.85) 50%, rgba(29,140,248,0.15) 100%);
                border: 1px solid #30363d; border-radius: 12px; padding: 20px 28px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div style="text-align: left;">
                <div style="font-size: 1.5rem; font-weight: 800; color: #ef4444;">🇮🇩 INDONESIA</div>
                <div style="color: #94a3b8; font-size: 0.9rem;">Coach: John Herdman</div>
                <div style="color: #cbd5e1; font-size: 0.85rem; margin-top: 4px;">Goals: Dean James 84', Elkan Baggott 116'</div>
            </div>
            <div style="text-align: center; padding: 10px 20px;">
                <div style="font-size: 2.2rem; font-weight: 900; letter-spacing: 2px; color: #ffffff;">
                    2 - 2
                </div>
                <div style="color: #fbbf24; font-weight: 700; font-size: 1rem;">
                    (PENALTIES: 4 - 2 INDONESIA)
                </div>
                <div style="color: #64748b; font-size: 0.8rem; margin-top: 2px;">
                    FT: 1-1 • AET: 2-2 • Gelora Bung Karno (70,098 Att.)
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 1.5rem; font-weight: 800; color: #3b82f6;">THAILAND 🇹🇭</div>
                <div style="color: #94a3b8; font-size: 0.9rem;">Coach: Anthony Hudson</div>
                <div style="color: #cbd5e1; font-size: 0.85rem; margin-top: 4px;">Goals: Iklas Sanron 87', Peeradol 111'</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Core Telemetry Metrics Row
col1, col2, col3, col4, col5 = st.columns(5)

pos_idn = team_stats.get("possession_percentage", {}).get("indonesia", 58.4)
pos_tha = team_stats.get("possession_percentage", {}).get("thailand", 41.6)

xg_idn = team_stats.get("expected_metrics", {}).get("expected_goals_xg", {}).get("indonesia", 2.14)
xg_tha = team_stats.get("expected_metrics", {}).get("expected_goals_xg", {}).get("thailand", 1.38)

sot_idn = team_stats.get("shooting", {}).get("shots_on_target", {}).get("indonesia", 7)
sot_tha = team_stats.get("shooting", {}).get("shots_on_target", {}).get("thailand", 4)

tackles_idn = team_stats.get("defensive_actions", {}).get("tackle_success_pct", {}).get("indonesia", 72.0)
tackles_tha = team_stats.get("defensive_actions", {}).get("tackle_success_pct", {}).get("thailand", 70.97)

pass_idn = team_stats.get("passing_and_distribution", {}).get("pass_accuracy_pct", {}).get("indonesia", 83.96)
pass_tha = team_stats.get("passing_and_distribution", {}).get("pass_accuracy_pct", {}).get("thailand", 77.03)

with col1:
    st.metric("Possession", f"{pos_idn}% vs {pos_tha}%", delta="+16.8% IDN Domination")
with col2:
    st.metric("Expected Goals (xG)", f"{xg_idn} vs {xg_tha}", delta="+0.76 xG IDN Quality")
with col3:
    st.metric("Shots on Target", f"{sot_idn} vs {sot_tha}", delta="7/18 vs 4/11 Total")
with col4:
    st.metric("Tackles Won %", f"{tackles_idn}% vs {tackles_tha}%", delta="High Press Intensity")
with col5:
    st.metric("Pass Accuracy", f"{pass_idn}% vs {pass_tha}%", delta="607 vs 418 Passes")

st.write("")

# Visualizations Section
st.markdown("### 📊 Interactive Tactical Visualizations")

chart_col1, chart_col2 = st.columns([1, 1.3])

with chart_col1:
    st.markdown("#### 🕸️ Match Attributes Spider Radar")
    st.caption("Normalized metric index comparing both squads across 5 core tactical vectors.")
    fig_radar = create_radar_chart(team_stats)
    st.plotly_chart(fig_radar, use_container_width=True)

with chart_col2:
    st.markdown("#### 📈 Cumulative xG & Substitution Impact")
    st.caption("Substitutions mapped directly over minute-by-minute cumulative xG curve.")
    fig_timeline = create_substitution_timeline_chart()
    st.plotly_chart(fig_timeline, use_container_width=True)

st.write("")

# Detailed Tabs: Player Ratings & Tactical Substitutions
tab_subs, tab_players, tab_history = st.tabs([
    "🔄 Substitution & Tactical Log",
    "⭐ Starting XI Player Ratings",
    "📜 Head-to-Head History (2020-2026)"
])

with tab_subs:
    st.markdown("#### Detailed Substitution Impact Registry")
    if subs_log:
        subs_rows = []
        for s in subs_log:
            subs_rows.append({
                "Minute": f"{s.get('minute')}'",
                "Team": s.get("team"),
                "Player Out": s.get("player_out"),
                "Player In": s.get("player_in"),
                "Tactical Objective": s.get("tactical_purpose"),
                "Impact Observed": s.get("post_sub_impact")
            })
        df_subs = pd.DataFrame(subs_rows)
        st.dataframe(df_subs, use_container_width=True, height=340)
    else:
        st.info("No substitution data available.")

with tab_players:
    st.markdown("#### Top Performers & Starting XI Ratings (Scale 1.0 - 10.0)")
    
    idn_starters = player_stats.get("indonesia", {}).get("starting_xi", [])
    tha_starters = player_stats.get("thailand", {}).get("starting_xi", [])
    
    p_col1, p_col2 = st.columns(2)
    
    with p_col1:
        st.markdown("##### 🇮🇩 Indonesia Squad Ratings")
        if idn_starters:
            df_idn_p = pd.DataFrame([
                {
                    "Player": f"{p['name']} (#{p['shirt_number']})",
                    "Pos": p["position"],
                    "Rating": p["match_rating"],
                    "Key Metric": f"xG: {p.get('xg', 0.0)} | Pass: {p.get('pass_accuracy_pct', 0)}%"
                }
                for p in idn_starters
            ]).sort_values(by="Rating", ascending=False)
            st.dataframe(df_idn_p, use_container_width=True, height=360)
            
    with p_col2:
        st.markdown("##### 🇹🇭 Thailand Squad Ratings")
        if tha_starters:
            df_tha_p = pd.DataFrame([
                {
                    "Player": f"{p['name']} (#{p['shirt_number']})",
                    "Pos": p["position"],
                    "Rating": p["match_rating"],
                    "Key Metric": f"xG: {p.get('xg', 0.0)} | Pass: {p.get('pass_accuracy_pct', 0)}%"
                }
                for p in tha_starters
            ]).sort_values(by="Rating", ascending=False)
            st.dataframe(df_tha_p, use_container_width=True, height=360)

with tab_history:
    st.markdown("#### Head-to-Head Encounters (2020 - 2026)")
    if match_history:
        h2h_rows = []
        for m in match_history:
            h2h_rows.append({
                "Date": m.get("date")[:10] if m.get("date") else "N/A",
                "Tournament": m.get("competition"),
                "Stadium": m.get("stadium"),
                "Scoreline": m.get("outcome")
            })
        df_h2h = pd.DataFrame(h2h_rows)
        st.dataframe(df_h2h, use_container_width=True)
    else:
        st.info("H2H summary history not found.")
