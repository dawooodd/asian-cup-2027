"""
Halaman 1: Prediksi Lengkap Peluang 24 Tim Peserta AFC Asian Cup 2027
Simulasi 100.000 Iterasi Monte Carlo Berdasarkan Data 4 Tahun Terakhir.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np

from app.utils.styles import inject_custom_css
from app.utils.charts import create_top_quarter_final_bar, create_stage_progression_funnel

st.set_page_config(
    page_title="Peluang 24 Tim Peserta | AFC Asian Cup 2027",
    page_icon="🏆",
    layout="wide"
)

inject_custom_css()

# Path Data Lake
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data", "asian_cup_predictions.csv")

@st.cache_data
def load_predictions_data():
    if not os.path.exists(DATA_PATH):
        st.error(f"File data prediksi tidak ditemukan: {DATA_PATH}")
        return pd.DataFrame()
    return pd.read_csv(DATA_PATH)

df = load_predictions_data()

# Header Halaman
st.markdown(
    """
    <div style="margin-bottom: 24px;">
        <span class="metric-badge badge-gold">100.000 ITERASI SIMULASI MONTE CARLO</span>
        <span class="metric-badge badge-tha">DATA 4 TAHUN TERAKHIR (2023 - 2026)</span>
        <h1 style="color: #ffffff; margin-top: 6px; font-weight: 800;">
            🏆 Peta Peluang 24 Negara Peserta Piala Asia 2027
        </h1>
        <p style="color: #94a3b8; font-size: 1.05rem;">
            Analisis bertahap probabilitas kelolosan: <b>Fase Grup ➔ 16 Besar ➔ 8 Besar (Quarter-Finals) ➔ Semifinal ➔ Final ➔ Juara</b>.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

if df.empty:
    st.warning("Data prediksi belum tersedia. Silakan jalankan simulasi terlebih dahulu.")
    st.stop()

# Baris Metrik Sorotan
top_team = df.iloc[0]
idn_row = df[df["Team"] == "Indonesia"].iloc[0] if not df[df["Team"] == "Indonesia"].empty else None

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        label="Favorit Juara Teratas",
        value=top_team["Team"],
        delta=f"{top_team['Win_Tournament_Prob(%)']:.2f}% Peluang Juara"
    )

with kpi2:
    st.metric(
        label="Kandidat Kuat 8 Besar (>50%)",
        value="8 Negara",
        delta="JPN, KOR, IRN, KSA, AUS, QAT, IRQ, UAE"
    )

with kpi3:
    if idn_row is not None:
        st.metric(
            label="Peluang IDN Lolos 16 Besar",
            value=f"{idn_row['Reach_Round_16_Prob(%)']:.2f}%",
            delta=f"Peringkat #{int(idn_row['Rank'])} di Asia"
        )

with kpi4:
    if idn_row is not None:
        st.metric(
            label="Peluang IDN Lolos 8 Besar",
            value=f"{idn_row['Reach_Quarter_Final_Prob(%)']:.2f}%",
            delta="Target Utama (Perempat Final)"
        )

st.write("")

# Edukasi Sederhana: Penjelasan Tahapan
with st.expander("📚 Pelajari Cara Membaca Angka-Angka Probabilitas Ini (Panduan Orang Awam)", expanded=True):
    st.markdown(
        """
        - **Peluang Lolos 16 Besar (`Reach_Round_16_Prob`)**: Kemungkinan tim mengakhiri babak grup di peringkat 1, 2, atau termasuk dalam 4 tim peringkat ketiga terbaik. Indonesia memiliki peluang **67.74%**, artinya dalam 2 dari 3 simulasi, Indonesia berhasil melangkah keluar dari fase grup!
        - **Peluang Lolos 8 Besar (`Reach_Quarter_Final_Prob`)**: Kemungkinan tim memenangkan laga babak gugur pertama (Babak 16 Besar). Indonesia memiliki peluang **16.18%** secara umum, dan bisa melonjak hingga **42.5%** jika mengamankan posisi Runner-up Grup A!
        - **Peluang Semifinal & Final**: Persentase menembus 4 besar Asia yang biasanya didominasi oleh raksasa tradisional seperti Jepang, Korea Selatan, Iran, dan Arab Saudi.
        """
    )

st.write("")

# Visualisasi Interaktif
tab_chart1, tab_chart2 = st.tabs(["📊 Peringkat Peluang Lolos 8 Besar", "🪜 Piramida Kelolosan Tim Pilihan"])

with tab_chart1:
    st.markdown("#### Siapa Saja yang Berpeluang Lolos ke Babak 8 Besar (Quarter-Finals)?")
    st.caption("Grafik membandingkan 14 negara dengan probabilitas perempat final tertinggi. Timnas Indonesia disorot dengan warna merah.")
    fig_qf = create_top_quarter_final_bar(df)
    st.plotly_chart(fig_qf, use_container_width=True)

with tab_chart2:
    st.markdown("#### Piramida Ketahanan Turnamen per Negara")
    selected_team = st.selectbox(
        "Pilih Negara untuk Melihat Piramida Kelolosan:",
        df["Team"].tolist(),
        index=df["Team"].tolist().index("Indonesia") if "Indonesia" in df["Team"].tolist() else 0
    )
    fig_funnel = create_stage_progression_funnel(df, team_name=selected_team)
    st.plotly_chart(fig_funnel, use_container_width=True)

st.write("")

# Tabel Lengkap 24 Peserta dengan Filter
st.markdown("### 📋 Tabel Probabilitas Komprehensif 24 Negara Peserta")

f_col1, f_col2, f_col3, f_col4 = st.columns([1.5, 1.5, 1.5, 1.5])

with f_col1:
    search_q = st.text_input("🔍 Cari Negara:", "")

with f_col2:
    group_filter = st.selectbox("Filter Grup:", ["Semua Grup"] + sorted(df["Group"].unique().tolist()))

with f_col3:
    min_qf = st.slider("Min Peluang 8 Besar (%):", 0.0, 95.0, 0.0, step=5.0)

with f_col4:
    sort_by = st.selectbox(
        "Urutkan Berdasarkan:",
        [
            "Reach_Quarter_Final_Prob(%)",
            "Reach_Round_16_Prob(%)",
            "Win_Tournament_Prob(%)",
            "Reach_Semi_Final_Prob(%)",
            "Group_Stage_Exit_Prob(%)",
            "Base_TPI"
        ],
        index=0
    )

# Filter dataframe
filtered_df = df.copy()
if search_q:
    filtered_df = filtered_df[filtered_df["Team"].str.contains(search_q, case=False)]

if group_filter != "Semua Grup":
    filtered_df = filtered_df[filtered_df["Group"] == group_filter]

filtered_df = filtered_df[filtered_df["Reach_Quarter_Final_Prob(%)"] >= min_qf]
filtered_df = filtered_df.sort_values(by=sort_by, ascending=False)

# Format kolom tabel untuk pembacaan nyaman
col_renames = {
    "Rank": "Peringkat",
    "Team": "Negara",
    "Group": "Grup",
    "Base_TPI": "Nilai TPI",
    "Group_Stage_Exit_Prob(%)": "Gugur Grup (%)",
    "Reach_Round_16_Prob(%)": "Lolos 16 Besar (%)",
    "Reach_Quarter_Final_Prob(%)": "Lolos 8 Besar (%)",
    "Reach_Semi_Final_Prob(%)": "Lolos Semifinal (%)",
    "Reach_Final_Prob(%)": "Lolos Final (%)",
    "Win_Tournament_Prob(%)": "Juara (%)"
}

styled_table = filtered_df.rename(columns=col_renames).copy()

st.dataframe(
    styled_table.style.format({
        "Nilai TPI": "{:.2f}",
        "Gugur Grup (%)": "{:.2f}%",
        "Lolos 16 Besar (%)": "{:.2f}%",
        "Lolos 8 Besar (%)": "{:.2f}%",
        "Lolos Semifinal (%)": "{:.2f}%",
        "Lolos Final (%)": "{:.2f}%",
        "Juara (%)": "{:.2f}%"
    }).background_gradient(
        subset=["Lolos 16 Besar (%)", "Lolos 8 Besar (%)", "Lolos Semifinal (%)", "Juara (%)"],
        cmap="YlGnBu"
    ),
    use_container_width=True,
    height=480
)

# Unduh Data CSV
csv_dl = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Unduh Data Tabel Prediksi (CSV)",
    data=csv_dl,
    file_name="prediksi_piala_asia_2027_24_tim.csv",
    mime="text/csv"
)
