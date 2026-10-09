"""
Halaman 3: Simulator Pertandingan Interaktif AFC Asian Cup 2027
Didukung oleh Model Bivariate Poisson + Koreksi Residual XGBoost.
"""

import os
import sys
import streamlit as st
import pandas as pd
import numpy as np

# Pastikan project root ada di sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.models.weighted_poisson_xgboost_model import predict_match
from app.utils.styles import inject_custom_css
from app.utils.charts import create_match_donut_chart, create_scoreline_bar_chart

st.set_page_config(
    page_title="Simulator Pertandingan | AFC Asian Cup 2027",
    page_icon="🧮",
    layout="wide"
)

inject_custom_css()

# Memuat data tim dan nilai TPI dari CSV
CSV_PATH = os.path.join(BASE_DIR, "data", "asian_cup_predictions.csv")

@st.cache_data
def load_teams():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        return dict(zip(df["Team"], df["Base_TPI"]))
    return {
        "Japan": 9.00, "South Korea": 7.57, "Iran": 7.42, "Saudi Arabia": 7.20,
        "Australia": 6.73, "Qatar": 6.43, "Iraq": 5.52, "United Arab Emirates": 5.46,
        "Uzbekistan": 5.45, "Jordan": 4.93, "Bahrain": 4.41, "Oman": 4.36,
        "Indonesia": 4.01, "Syria": 3.33, "Palestine": 3.23, "Thailand": 3.22,
        "China PR": 2.98, "Vietnam": 2.79, "Kuwait": 2.65, "Tajikistan": 2.62,
        "Lebanon": 2.56, "Malaysia": 3.05, "Kyrgyzstan": 2.20, "North Korea": 1.50
    }

team_tpi_map = load_teams()
team_names = list(team_tpi_map.keys())

# Header
st.markdown(
    """
    <div style="margin-bottom: 24px;">
        <span class="metric-badge badge-tha">DISTRIBUSI BIVARIATE POISSON & XGBOOST</span>
        <h1 style="color: #ffffff; margin-top: 6px; font-weight: 800;">
            🧮 Simulator Laga Head-to-Head Interaktif
        </h1>
        <p style="color: #94a3b8; font-size: 1.05rem;">
            Simulasikan duel antara dua tim mana pun dengan slider faktor keberuntungan/stokastik untuk melihat peluang hasil dan distribusi skor tepat.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Panel Konfigurasi Pertandingan
st.markdown("### ⚙️ Konfigurasi Pertandingan & Parameter Taktis")

c1, c2, c3 = st.columns([1.2, 1.2, 1.6])

with c1:
    team_a = st.selectbox(
        "Pilih Tim A (Tuan Rumah / Pot 1):",
        team_names,
        index=team_names.index("Indonesia") if "Indonesia" in team_names else 0
    )
    tpi_a = team_tpi_map.get(team_a, 4.01)
    st.caption(f"🛡️ **{team_a}** Base TPI: `{tpi_a:.2f}`")

with c2:
    team_b_options = [t for t in team_names if t != team_a]
    default_b = "Saudi Arabia" if "Saudi Arabia" in team_b_options else team_b_options[0]
    team_b = st.selectbox(
        "Pilih Tim B (Tamu / Pot 2):",
        team_b_options,
        index=team_b_options.index(default_b) if default_b in team_b_options else 0
    )
    tpi_b = team_tpi_map.get(team_b, 7.20)
    st.caption(f"⚔️ **{team_b}** Base TPI: `{tpi_b:.2f}`")

with c3:
    luck_factor = st.slider(
        "Faktor Keberuntungan / Kejutan Stokastik:",
        min_value=-0.50,
        max_value=0.50,
        value=0.00,
        step=0.05,
        help="Mensimulasikan insiden tidak terduga: kartu merah awal, blunder wasit, cuaca ekstrem, atau dorongan suporter. Nilai positif menguntungkan Tim A; nilai negatif menguntungkan Tim B."
    )
    if luck_factor > 0:
        st.caption(f"📈 Momentum kejutan: **+{luck_factor:.2f}** menguntungkan **{team_a}**")
    elif luck_factor < 0:
        st.caption(f"📉 Momentum kejutan: **{luck_factor:.2f}** menguntungkan **{team_b}**")
    else:
        st.caption("⚖️ Kondisi netral (Kekuatan murni berdasarkan statistik)")

st.write("")
sim_button = st.button("🚀 Simulasikan Pertandingan Sekarang", type="primary", use_container_width=True)

# Eksekusi Simulasi
if sim_button or "current_sim" not in st.session_state:
    with st.spinner(f"Menghitung Matriks Poisson untuk {team_a} vs {team_b}..."):
        sim_res = predict_match(
            team_a_name=team_a,
            team_b_name=team_b,
            tpi_a=tpi_a,
            tpi_b=tpi_b,
            luck_factor=luck_factor
        )
        st.session_state["current_sim"] = sim_res
else:
    sim_res = st.session_state.get("current_sim")

if sim_res:
    st.markdown("---")
    st.markdown(f"### 🎯 Hasil Proyeksi: {sim_res['team_a']} vs {sim_res['team_b']}")

    # Baris Metrik Skor & xG
    r1, r2, r3, r4 = st.columns(4)

    with r1:
        st.metric(
            label=f"Peluang {sim_res['team_a']} Menang",
            value=f"{sim_res['win_prob_a']}%",
            delta=f"xG Dibuat: {sim_res['projected_xg_a']}"
        )

    with r2:
        st.metric(
            label="Peluang Imbang (Seri)",
            value=f"{sim_res['draw_prob']}%",
            delta="Deadlock Rate"
        )

    with r3:
        st.metric(
            label=f"Peluang {sim_res['team_b']} Menang",
            value=f"{sim_res['win_prob_b']}%",
            delta=f"xG Dibuat: {sim_res['projected_xg_b']}"
        )

    with r4:
        st.metric(
            label="Skor Paling Mungkin",
            value=sim_res["most_likely_score"],
            delta=f"{sim_res['most_likely_score_prob']}% Kemungkinan",
            delta_color="normal"
        )

    st.write("")

    # Visualisasi Donut & Bar Skor
    v1, v2 = st.columns([1, 1.2])

    with v1:
        fig_donut = create_match_donut_chart(
            win_a=sim_res["win_prob_a"],
            draw=sim_res["draw_prob"],
            win_b=sim_res["win_prob_b"],
            team_a=sim_res["team_a"],
            team_b=sim_res["team_b"]
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with v2:
        fig_bar = create_scoreline_bar_chart(
            scorelines=sim_res["top_scorelines"],
            team_a=sim_res["team_a"],
            team_b=sim_res["team_b"]
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Analisis Taktis Otomatis
    st.write("")
    st.markdown("### 📋 Narasi Taktis Berbasis Data untuk Suporter")

    delta_tpi = sim_res["tpi_a"] - sim_res["tpi_b"]
    luck = sim_res["luck_factor"]

    if abs(delta_tpi) < 0.5:
        narasi = (
            f"**Pertarungan Sangat Berimbang:** Selisih TPI kedua tim sangat tipis ({abs(delta_tpi):.2f}). "
            f"Pertandingan ini memiliki peluang seri cukup tinggi ({sim_res['draw_prob']}%), "
            f"di mana laga berpotensi berlanjut ke babak perpanjangan waktu atau adu penalti jika terjadi di fase gugur."
        )
    elif delta_tpi > 0:
        narasi = (
            f"**{sim_res['team_a']} Lebih Diunggulkan:** Dengan TPI {sim_res['tpi_a']} berbanding {sim_res['tpi_b']}, "
            f"{sim_res['team_a']} diproyeksikan menguasai tempo laga dan menghasilkan ancaman lebih tinggi "
            f"({sim_res['projected_xg_a']} xG vs {sim_res['projected_xg_b']} xG). Peluang menang: {sim_res['win_prob_a']}%."
        )
    else:
        narasi = (
            f"**{sim_res['team_a']} Menghadapi Lawan Berat:** {sim_res['team_b']} memiliki keunggulan kualitas dasar "
            f"(TPI {sim_res['tpi_b']}). Kunci bagi {sim_res['team_a']} adalah menerapkan strategi bertahan rapat (*low-block*) "
            f"dan memaksimalkan serangan balik cepat (*counter-attack*) seperti saat Indonesia menundukkan Arab Saudi 2-0."
        )

    if abs(luck) > 0.1:
        narasi += (
            f"\n\n**Efek Faktor Keberuntungan ({luck:+.2f}):** Varians acak yang disuntikkan secara nyata menggeser kurva peluang, "
            f"mensimulasikan laga turnamen dengan dinamika dramatis di lapangan."
        )

    st.info(narasi)

    # Tabel Rincian Skor
    with st.expander("🔍 Lihat Tabel Lengkap 6 Skor Paling Mungkin"):
        df_scores = pd.DataFrame(sim_res["top_scorelines"])
        df_scores.rename(columns={
            "score": "Tebakan Skor",
            "goals_a": f"Gol ({sim_res['team_a']})",
            "goals_b": f"Gol ({sim_res['team_b']})",
            "probability_pct": "Peluang Terjadi (%)"
        }, inplace=True)
        st.dataframe(df_scores, use_container_width=True)
