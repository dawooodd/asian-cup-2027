"""
Halaman 3: Simulator Pertandingan Interaktif AFC Asian Cup 2027
Didukung oleh Distribusi Bivariate Poisson dan Koreksi Residual XGBoost.
Bahasa: Bahasa Indonesia Baku (PUEBI/KBBI).
"""

import os
import sys
import streamlit as st
import pandas as pd

# Menambahkan direktori utama repositori ke sys.path
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

# Memuat data tim dan nilai TPI dari CSV hasil simulasi
CSV_PATH = os.path.join(BASE_DIR, "data", "asian_cup_predictions.csv")

@st.cache_data
def load_teams():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        return dict(zip(df["Team"], df["Base_TPI"]))
    # Peta cadangan terkalibrasi resmi 24 tim
    return {
        "Japan": 9.00, "South Korea": 7.56, "Iran": 7.48, "Saudi Arabia": 7.42,
        "Australia": 6.80, "Qatar": 6.61, "Iraq": 5.71, "United Arab Emirates": 5.67,
        "Uzbekistan": 5.56, "Jordan": 5.14, "Bahrain": 4.70, "Oman": 4.64,
        "Indonesia": 4.26, "Syria": 3.62, "Palestine": 3.55, "Thailand": 3.52,
        "China PR": 3.20, "Vietnam": 3.16, "Kuwait": 3.03, "Tajikistan": 2.90,
        "Kyrgyzstan": 2.47, "Yemen": 1.96, "North Korea": 1.77, "Singapore": 1.50
    }

team_tpi_map = load_teams()
team_names = list(team_tpi_map.keys())

# Tajuk Halaman
st.markdown(
    """
    <div style="margin-bottom: 24px;">
        <span class="metric-badge badge-tha">DISTRIBUSI BIVARIATE POISSON & XGBOOST</span>
        <h1 style="color: #ffffff; margin-top: 6px; font-weight: 800;">
            🧮 Simulator Laga Head-to-Head Interaktif
        </h1>
        <p style="color: #94a3b8; font-size: 1.05rem;">
            Simulasikan duel antara dua tim mana pun dengan slider faktor keberuntungan/kejutan lapangan untuk melihat peluang hasil serta distribusi skor akhir.
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
        "Pilih Tim A (Tuan Rumah / Tim Pertama):",
        team_names,
        index=team_names.index("Indonesia") if "Indonesia" in team_names else 0
    )
    tpi_a = float(team_tpi_map.get(team_a, 4.26))
    st.caption(f"🛡️ **{team_a}** Base TPI: `{tpi_a:.2f}`")

with c2:
    team_b_options = [t for t in team_names if t != team_a]
    default_b = "Thailand" if "Thailand" in team_b_options else team_b_options[0]
    team_b = st.selectbox(
        "Pilih Tim B (Tim Tamu / Tim Kedua):",
        team_b_options,
        index=team_b_options.index(default_b) if default_b in team_b_options else 0
    )
    tpi_b = float(team_tpi_map.get(team_b, 3.52))
    st.caption(f"⚔️ **{team_b}** Base TPI: `{tpi_b:.2f}`")

with c3:
    luck_preset = st.selectbox(
        "Pemicu Keberuntungan Mikro (X-Factor Pemain Kunci):",
        [
            "Kondisi Netral (0.00)",
            f"🌟 Performa Puncak Pemain Kunci {team_a} (+0.20)",
            f"🔥 Momentum Luar Biasa & Penyelamatan Gemilang {team_a} (+0.35)",
            f"⚡ Performa Puncak Pemain Kunci {team_b} (-0.20)",
            f"💥 Serangan Balik Kilat & Keberuntungan {team_b} (-0.35)",
            "Kustomisasi Manual (Gunakan Slider)"
        ]
    )
    
    preset_val = 0.00
    if "+0.20" in luck_preset:
        preset_val = 0.20
    elif "+0.35" in luck_preset:
        preset_val = 0.35
    elif "-0.20" in luck_preset:
        preset_val = -0.20
    elif "-0.35" in luck_preset:
        preset_val = -0.35

    luck_factor = st.slider(
        "Slider Nilai Keberuntungan / Kejutan Lapangan:",
        min_value=-0.50,
        max_value=0.50,
        value=preset_val if "Kustomisasi" not in luck_preset else 0.00,
        step=0.05,
        help="Mensimulasikan insiden tak terduga: aksi clutch pemain bintang, penyelamatan penalti kiper, atau kartu merah awal. Nilai positif menguntungkan Tim A; nilai negatif menguntungkan Tim B."
    )
    if luck_factor > 0:
        st.caption(f"📈 Momentum kejutan: **+{luck_factor:.2f}** menguntungkan **{team_a}**")
    elif luck_factor < 0:
        st.caption(f"📉 Momentum kejutan: **{luck_factor:.2f}** menguntungkan **{team_b}**")
    else:
        st.caption("⚖️ Kondisi netral (Kekuatan murni berdasarkan statistik)")

st.write("")
sim_button = st.button("🚀 Simulasikan Pertandingan Sekarang", type="primary", width="stretch")

# Eksekusi Simulasi
if sim_button or "current_sim" not in st.session_state:
    with st.spinner(f"Menghitung Matriks Peluang Poisson untuk {team_a} vs {team_b}..."):
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
            delta=f"Proyeksi xG: {sim_res['projected_xg_a']}"
        )

    with r2:
        st.metric(
            label="Peluang Imbang (Seri)",
            value=f"{sim_res['draw_prob']}%",
            delta="Potensi Perpanjangan Waktu"
        )

    with r3:
        st.metric(
            label=f"Peluang {sim_res['team_b']} Menang",
            value=f"{sim_res['win_prob_b']}%",
            delta=f"Proyeksi xG: {sim_res['projected_xg_b']}"
        )

    with r4:
        st.metric(
            label="Skor Paling Mungkin",
            value=sim_res["most_likely_score"],
            delta=f"{sim_res['most_likely_score_prob']}% Kemungkinan",
            delta_color="normal"
        )

    st.write("")

    # Visualisasi Donut dan Batang Skor
    v1, v2 = st.columns([1, 1.2])

    with v1:
        fig_donut = create_match_donut_chart(
            win_a=sim_res["win_prob_a"],
            draw=sim_res["draw_prob"],
            win_b=sim_res["win_prob_b"],
            team_a=sim_res["team_a"],
            team_b=sim_res["team_b"]
        )
        st.plotly_chart(fig_donut, width="stretch")

    with v2:
        fig_bar = create_scoreline_bar_chart(
            scorelines=sim_res["top_scorelines"],
            team_a=sim_res["team_a"],
            team_b=sim_res["team_b"]
        )
        st.plotly_chart(fig_bar, width="stretch")

    # Analisis Taktis Otomatis
    st.write("")
    st.markdown("### 📋 Narasi Taktis Berbasis Data")

    delta_tpi = sim_res["tpi_a"] - sim_res["tpi_b"]
    luck = sim_res["luck_factor"]

    if abs(delta_tpi) < 0.5:
        narasi = (
            f"**Pertandingan Sangat Berimbang:** Selisih TPI kedua tim sangat tipis ({abs(delta_tpi):.2f}). "
            f"Laga ini memiliki peluang imbang cukup tinggi ({sim_res['draw_prob']}%), "
            f"yang berpotensi berlanjut ke babak perpanjangan waktu atau adu penalti jika terjadi pada fase gugur."
        )
    elif delta_tpi > 0:
        narasi = (
            f"**{sim_res['team_a']} Lebih Diunggulkan:** Dengan TPI {sim_res['tpi_a']} berbanding {sim_res['tpi_b']}, "
            f"{sim_res['team_a']} diproyeksikan mendikte jalannya pertandingan dan menghasilkan ancaman ofensif lebih tinggi "
            f"({sim_res['projected_xg_a']} xG vs {sim_res['projected_xg_b']} xG). Peluang kemenangan: {sim_res['win_prob_a']}%."
        )
    else:
        narasi = (
            f"**{sim_res['team_a']} Menghadapi Lawan Tangguh:** {sim_res['team_b']} memiliki keunggulan kualitas dasar "
            f"(TPI {sim_res['tpi_b']}). Kunci taktis bagi {sim_res['team_a']} adalah menerapkan strategi pertahanan blok rendah (*low-block*) "
            f"dan memaksimalkan serangan balik cepat (*counter-attack*) berpresisi tinggi."
        )

    if abs(luck) > 0.1:
        narasi += (
            f"\n\n**Pengaruh Faktor Keberuntungan ({luck:+.2f}):** Varians acak yang disuntikkan secara nyata menggeser kurva probabilitas, "
            f"mensimulasikan dinamika tak terduga yang kerap mewarnai atmosfer turnamen sepak bola."
        )

    st.info(narasi)

    # Tabel Rincian Skor
    with st.expander("🔍 Rincian Tabel 6 Skor Paling Mungkin"):
        df_scores = pd.DataFrame(sim_res["top_scorelines"])
        df_scores.rename(columns={
            "score": "Tebakan Skor",
            "goals_a": f"Gol ({sim_res['team_a']})",
            "goals_b": f"Gol ({sim_res['team_b']})",
            "probability_pct": "Peluang Terjadi (%)"
        }, inplace=True)
        st.dataframe(df_scores, width="stretch")

    # Diagnostik Machine Learning XGBoost
    with st.expander("🤖 Diagnostik Machine Learning XGBoost & Penjelasan bagi Orang Awam", expanded=False):
        st.markdown(
            f"""
            #### 🧠 Bagaimana Pohon Keputusan XGBoost Menghitung Laga Ini?
            Model **XGBoost (Extreme Gradient Boosting)** tidak sekadar melihat nama besar atau peringkat dunia, melainkan 
            mengevaluasi **pola interaksi non-linear** antara kekuatan tim (*TPI*), kedalaman materi liga top Eropa, 
            ketahanan iklim, hingga **faktor mentalitas (*Clutch Score*)** dan **pengali keberuntungan (*Luck Multiplier*)**.

            - **Prediksi Probabilitas Murni XGBoost**: 
              - Menang {sim_res['team_a']}: **{sim_res.get('xgboost_pure_win_a', sim_res['win_prob_a'])}%**
              - Hasil Imbang: **{sim_res.get('xgboost_pure_draw', sim_res['draw_prob'])}%**
              - Menang {sim_res['team_b']}: **{sim_res.get('xgboost_pure_win_b', sim_res['win_prob_b'])}%**
            - **Proyeksi Selisih Gol XGBoost**: **{sim_res.get('xgboost_predicted_goal_diff', 0.0):+.2f} Gol**
            - **Model Ensemble**: {sim_res.get('model_architecture', 'Bivariate Poisson + XGBoost')}
            """
        )

        feat_imp = sim_res.get("feature_importances", {})
        if feat_imp:
            st.markdown("##### 📊 Kontribusi Pembobotan Fitur (*Feature Importance*):")
            feat_df = pd.DataFrame([
                {"Fitur Analisis": k, "Tingkat Pengaruh (%)": v}
                for k, v in feat_imp.items()
            ]).sort_values(by="Tingkat Pengaruh (%)", ascending=False)
            st.dataframe(feat_df, hide_index=True, width="stretch")
            st.caption("💡 *Tingkat Pengaruh (%) menunjukkan seberapa dominan faktor tersebut dalam menentukan arah prediksi model XGBoost.*")
