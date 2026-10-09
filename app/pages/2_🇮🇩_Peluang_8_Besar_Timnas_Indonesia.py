"""
Halaman 2: Bedah Peluang Timnas Indonesia Lolos ke Babak 8 Besar (Quarter-Finals)
Piala Asia 2027 Berdasarkan Data Pertandingan 4 Tahun Terakhir (2023 - 2026),
Evolusi Nilai Skuad (€36.5 Juta), dan Model Taktis Bivariate Poisson.
"""

import os
import json
import streamlit as st
import pandas as pd
import numpy as np

from app.utils.styles import inject_custom_css
from app.utils.charts import (
    create_stage_progression_funnel,
    create_indonesia_squad_value_evolution_chart,
    create_scenario_comparison_bar,
    create_matches_xg_trajectory_chart
)

st.set_page_config(
    page_title="Peluang 8 Besar Timnas Indonesia | AFC Asian Cup 2027",
    page_icon="🇮🇩",
    layout="wide"
)

inject_custom_css()

# Path Data Lake
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ANALYTICS_PATH = os.path.join(BASE_DIR, "data", "indonesia_4yr_match_analytics.json")
PREDS_PATH = os.path.join(BASE_DIR, "data", "asian_cup_predictions.csv")

@st.cache_data
def load_data():
    analytics = {}
    preds_df = pd.DataFrame()
    if os.path.exists(ANALYTICS_PATH):
        with open(ANALYTICS_PATH, "r", encoding="utf-8") as f:
            analytics = json.load(f)
    if os.path.exists(PREDS_PATH):
        preds_df = pd.read_csv(PREDS_PATH)
    return analytics, preds_df

analytics, df_preds = load_data()

# Header Halaman
st.markdown(
    """
    <div style="margin-bottom: 24px;">
        <span class="metric-badge badge-idn">FOKUS UTAMA: TIMNAS INDONESIA</span>
        <span class="metric-badge badge-gold">TARGET: BABAK 8 BESAR (QUARTER-FINALS)</span>
        <h1 style="color: #ffffff; margin-top: 6px; font-weight: 800;">
            🇮🇩 Peluang Timnas Indonesia Lolos ke 8 Besar Piala Asia 2027
        </h1>
        <p style="color: #94a3b8; font-size: 1.05rem; line-height: 1.6;">
            Analisis kuantitatif berbasis <b>20 Laga Kunci 4 Tahun Terakhir (2023–2026)</b>, 
            lonjakan nilai skuad diaspora <b>(€36.5 Juta / Peringkat #6 Asia)</b>, serta pemetaan 3 skenario taktis menuju perempat final.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

if not analytics:
    st.error("Data analitika Timnas Indonesia tidak ditemukan. Harap pastikan pipeline data telah dijalankan.")
    st.stop()

# Scorecard KPI Peluang Indonesia
r8 = analytics.get("road_to_quarter_final_8_besar", {})
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric(
        label="Peluang Lolos Fase Grup",
        value=f"{r8.get('reach_round_of_16_prob', 67.74)}%",
        delta="Lolos ke Babak 16 Besar"
    )

with kpi2:
    st.metric(
        label="Peluang Lolos 8 Besar (Agregat)",
        value=f"{r8.get('reach_quarter_final_8_besar_prob', 16.18)}%",
        delta="Target Utama Sejarah Baru",
        delta_color="normal"
    )

with kpi3:
    st.metric(
        label="Peluang 8 Besar via Runner-up",
        value="42.5%",
        delta="Skenario Emas Grup A",
        delta_color="normal"
    )

with kpi4:
    st.metric(
        label="Nilai Pasar Skuad Terbaru",
        value="€36.5 Juta",
        delta="Peringkat #6 Tertinggi Asia"
    )

with kpi5:
    agg = analytics.get("aggregate_performance_summary", {})
    st.metric(
        label="Rekor Tak Terkalahkan 4 Thn",
        value=f"{agg.get('unbeaten_rate_pct', 65.0)}%",
        delta=f"9 M - 4 S - 7 K (20 Laga)"
    )

st.write("")

# Banner Edukasi Utama
st.info(
    "💡 **Kesimpulan Sains Data untuk Suporter & Publik:**\n\n"
    "Secara probabilitas umum turnamen, peluang Timnas Indonesia menembus Babak 8 Besar adalah **16.18%** (peringkat 13 dari 24 negara). "
    "Namun, kunci keberhasilan Indonesia terletak pada **posisi akhir di Grup A**! "
    "Jika Indonesia berhasil mengunci posisi **Runner-up Grup A**, lawan di babak 16 besar adalah Runner-up Grup C (seperti UAE atau Suriah). "
    "Dalam skenario ini, peluang Indonesia mengalahkan lawannya dan lolos ke **Babak 8 Besar melonjak drastis hingga 42.5%**!"
)

st.write("")

# Bagian 1: 3 Skenario Menuju 8 Besar
st.markdown("### 🗺️ Peta Jalur & Bedah 3 Skenario Menuju Babak 8 Besar")
scenarios = r8.get("scenario_breakdown_to_8_besar", [])

col_scen_chart, col_scen_text = st.columns([1.3, 1])

with col_scen_chart:
    fig_scen = create_scenario_comparison_bar(scenarios)
    st.plotly_chart(fig_scen, use_container_width=True)

with col_scen_text:
    st.markdown("#### Penjelasan Skenario:")
    for s in scenarios:
        st.markdown(
            f"""
            <div style="background: rgba(22, 27, 34, 0.85); border-left: 4px solid {'#e63946' if 'Emas' in s['scenario'] else '#38bdf8'}; 
                        padding: 12px 16px; border-radius: 6px; margin-bottom: 12px;">
                <div style="font-weight: 700; color: #f0f6fc; font-size: 0.95rem;">{s['scenario']}</div>
                <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">
                    <b>Kemungkinan:</b> {s['likelihood_to_occur']} • <b>Peluang Menang 16 Besar:</b> <span style="color:#fbbf24;font-weight:700;">{s['r16_win_probability']}</span>
                </div>
                <div style="color: #cbd5e1; font-size: 0.85rem; margin-top: 4px;">
                    <b>Calon Lawan:</b> {s['opponent_in_r16']}<br>
                    <i>{s['verdict']}</i>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")

# Bagian 2: Nilai Skuad & Pilar Diaspora
st.markdown("### 💶 Lonjakan Kualitas Skuad: Mengapa Peluang Indonesia Naik Pesat?")
col_val_chart, col_val_desc = st.columns([1.2, 1])

yearly_vals = analytics.get("squad_market_value_evolution", {}).get("yearly_trajectory", [])
diaspora_pillars = analytics.get("squad_market_value_evolution", {}).get("top_diaspora_pillars", [])

with col_val_chart:
    fig_val = create_indonesia_squad_value_evolution_chart(yearly_vals)
    st.plotly_chart(fig_val, use_container_width=True)

with col_val_desc:
    st.markdown(
        """
        #### Bukti Ilmiah: Korelasi Nilai Skuad & Performa
        Pada Piala Asia 2023 (Januari 2024), nilai skuad Indonesia baru berkisar **€12.4 Juta** (peringkat 13 Asia) dan berhasil mencapai babak 16 besar untuk pertama kalinya dalam sejarah.
        
        Kini menuju 2026/2027, nilai skuad melonjak menjadi **€36.5 Juta** (Peringkat #6 di Asia, melampaui Arab Saudi, Irak, dan Qatar) berkat hadirnya pemain-pemain inti di kompetisi elite Eropa:
        - **Jay Idzes (Venezia)**: Tampil reguler di Serie A Italia melawan striker kelas dunia.
        - **Mees Hilgers (FC Twente)**: Bertanding di kompetisi kasta tertinggi Belanda & UEFA Europa League.
        - **Kevin Diks (FC Copenhagen)**: Berpengalaman di UEFA Champions League.
        - **Maarten Paes (FC Dallas)**: Kiper dengan reflek dan penyelamatan penalti terbukti vs Arab Saudi.
        
        Peningkatan fisik, disiplin formasi, dan kedalaman bangku cadangan (*squad depth*) membuat Indonesia mampu bertahan dengan intensitas tinggi selama 90 hingga 120 menit.
        """
    )

with st.expander("⭐ Lihat Tabel Rincian 9 Pemain Pilar & Metrik Kuncinya"):
    df_pillars = pd.DataFrame(diaspora_pillars)
    df_pillars.rename(columns={
        "name": "Nama Pemain",
        "position": "Posisi",
        "club": "Klub & Liga",
        "market_value_eur": "Nilai Pasar (€)",
        "key_metric": "Metrik Keunggulan Taktis"
    }, inplace=True)
    st.dataframe(
        df_pillars.style.format({"Nilai Pasar (€)": "€{:,.0f}"}),
        use_container_width=True
    )

st.write("")

# Bagian 3: Statistik Pertandingan 4 Tahun Terakhir (2023 - 2026)
st.markdown("### 📊 Rekam Jejak 20 Laga Kunci 4 Tahun Terakhir (2023 - 2026)")
matches_data = analytics.get("matches_4_years_history", [])

col_xg_chart, col_tier_summary = st.columns([1.4, 1])

with col_xg_chart:
    fig_xg = create_matches_xg_trajectory_chart(matches_data)
    st.plotly_chart(fig_xg, use_container_width=True)

with col_tier_summary:
    st.markdown("#### Rangkuman vs Level Lawan:")
    t1 = agg.get("tier_1_heavyweights_record", {})
    t2 = agg.get("tier_2_and_3_record", {})
    
    st.markdown(
        f"""
        <div style="background: rgba(22, 27, 34, 0.85); border: 1px solid #30363d; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
            <div style="color: #ef4444; font-weight: 700; font-size: 0.95rem;">⚔️ vs Raksasa Pot 1 Asia (Arab Saudi, Australia, Jepang)</div>
            <div style="color: #f0f6fc; font-size: 1.1rem; font-weight: 800; margin-top: 4px;">{t1.get('wins', 1)} Menang - {t1.get('draws', 2)} Seri - {t1.get('losses', 5)} Kalah</div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 6px;">
                <b>Sorotan:</b> Menang 2-0 vs Arab Saudi di GBK, Imbang 1-1 di Jeddah, Imbang 0-0 vs Australia. Bukti nyata Indonesia mampu menahan tim ber-ranking FIFA 50 besar!
            </div>
        </div>
        
        <div style="background: rgba(22, 27, 34, 0.85); border: 1px solid #30363d; border-radius: 8px; padding: 14px;">
            <div style="color: #38bdf8; font-weight: 700; font-size: 0.95rem;">🛡️ vs Pot 2 & 3 Asia (Bahrain, Vietnam, China, Burundi)</div>
            <div style="color: #f0f6fc; font-size: 1.1rem; font-weight: 800; margin-top: 4px;">{t2.get('wins', 7)} Menang - {t2.get('draws', 1)} Seri - {t2.get('losses', 2)} Kalah ({t2.get('win_rate_pct', 70.0)}% Win Rate)</div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 6px;">
                <b>Sorotan:</b> Sapu bersih kemenangan atas Vietnam (1-0, 1-0, 3-0), menang vs Bahrain (1-0). Dominasi atas tim level menengah Asia.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Tabel Riwayat Pertandingan dengan Filter
st.write("")
st.markdown("#### 📋 Telusuri Riwayat 20 Pertandingan Lengkap")

filter_tier = st.selectbox(
    "Filter Berdasarkan Level Lawan:",
    ["Semua Pertandingan", "Pot 1 (Raksasa Asia)", "Pot 2 & 3", "Pot 4"]
)

df_matches = pd.DataFrame(matches_data)

if filter_tier == "Pot 1 (Raksasa Asia)":
    df_matches = df_matches[df_matches["tier"].isin(["Pot 1", "World #1"])]
elif filter_tier == "Pot 2 & 3":
    df_matches = df_matches[df_matches["tier"].isin(["Pot 2", "Pot 3"])]
elif filter_tier == "Pot 4":
    df_matches = df_matches[df_matches["tier"] == "Pot 4"]

table_view = df_matches[[
    "date", "opponent", "competition", "tier", "score", "result",
    "possession_pct", "xg_for", "xg_against", "clean_sheet", "notes"
]].rename(columns={
    "date": "Tanggal",
    "opponent": "Lawan",
    "competition": "Ajang",
    "tier": "Level Lawan",
    "score": "Skor",
    "result": "Hasil",
    "possession_pct": "Possession (%)",
    "xg_for": "xG Indonesia",
    "xg_against": "xG Lawan",
    "clean_sheet": "Clean Sheet",
    "notes": "Catatan Taktis"
})

st.dataframe(
    table_view.style.format({
        "Possession (%)": "{:.1f}%",
        "xG Indonesia": "{:.2f}",
        "xG Lawan": "{:.2f}"
    }),
    use_container_width=True,
    height=400
)

# Faktor Taktis Penutup
st.write("")
st.markdown("### 🧠 4 Alasan Taktis Mengapa Target 8 Besar Sangat Masuk Akal")
factors = r8.get("tactical_scientific_factors_why_8_besar_is_achievable", [])

f_cols = st.columns(2)
for idx, f in enumerate(factors):
    target_col = f_cols[idx % 2]
    with target_col:
        st.markdown(
            f"""
            <div style="background: rgba(22, 27, 34, 0.9); border: 1px solid #30363d; border-radius: 8px; padding: 16px; margin-bottom: 14px;">
                <div style="color: #fbbf24; font-weight: 700; font-size: 1rem;">✅ {f['factor']}</div>
                <div style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.5; margin-top: 6px;">
                    {f['explanation']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
