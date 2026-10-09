"""
Halaman 1: Prediksi Lengkap Peluang 24 Tim Peserta AFC Asian Cup 2027
Simulasi 100.000 Iterasi Monte Carlo Berdasarkan Rekor Pertandingan 4 Tahun Terakhir.
Bahasa: Bahasa Indonesia Baku (PUEBI/KBBI).
"""

import os
import streamlit as st
import pandas as pd

from app.utils.styles import inject_custom_css
from app.utils.charts import create_top_quarter_final_bar, create_stage_progression_funnel

st.set_page_config(
    page_title="Peluang 24 Tim Peserta | AFC Asian Cup 2027",
    page_icon="🏆",
    layout="wide"
)

inject_custom_css()

# Direktori Data Lake
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data", "asian_cup_predictions.csv")

@st.cache_data
def load_predictions_data():
    if not os.path.exists(DATA_PATH):
        st.error(f"Berkas data prediksi tidak ditemukan: {DATA_PATH}")
        return pd.DataFrame()
    return pd.read_csv(DATA_PATH)

df = load_predictions_data()

# Tajuk Halaman
st.markdown(
    """
    <div style="margin-bottom: 24px;">
        <span class="metric-badge badge-gold">100.000 ITERASI SIMULASI MONTE CARLO</span>
        <span class="metric-badge badge-tha">DATA 4 TAHUN TERAKHIR (2023–2026)</span>
        <h1 style="color: #ffffff; margin-top: 6px; font-weight: 800;">
            🏆 Peta Peluang 24 Negara Peserta Piala Asia 2027
        </h1>
        <p style="color: #94a3b8; font-size: 1.05rem;">
            Analisis bertahap probabilitas kelolosan: <b>Fase Grup ➔ 16 Besar ➔ 8 Besar (Perempat Final) ➔ Semifinal ➔ Final ➔ Juara</b>.
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
        label="Unggulan Teratas Juara",
        value=str(top_team["Team"]),
        delta=f"{float(top_team['Win_Tournament_Prob(%)']):.2f}% Peluang Juara"
    )

with kpi2:
    qf_strong_count = len(df[df["Reach_Quarter_Final_Prob(%)"] >= 50.0])
    st.metric(
        label="Kandidat Kuat 8 Besar (>50%)",
        value=f"{qf_strong_count} Negara",
        delta="JPN, KSA, IRN, AUS, KOR, QAT, UZB"
    )

with kpi3:
    if idn_row is not None:
        st.metric(
            label="Peluang IDN Lolos 16 Besar",
            value=f"{float(idn_row['Reach_Round_16_Prob(%)']):.2f}%",
            delta=f"Grup F (Bersama JPN, QAT, THA)"
        )

with kpi4:
    if idn_row is not None:
        st.metric(
            label="Peluang IDN Lolos 8 Besar",
            value=f"{float(idn_row['Reach_Quarter_Final_Prob(%)']):.2f}%",
            delta="Target Utama (Perempat Final)"
        )

st.write("")

# Edukasi Sederhana: Panduan Membaca Probabilitas
with st.expander("📚 Panduan Membaca Angka Probabilitas Turnamen bagi Orang Awam", expanded=True):
    st.markdown(
        """
        - **Peluang Lolos 16 Besar (`Reach_Round_16_Prob`)**: Kemungkinan tim mengakhiri fase grup di posisi juara grup, runner-up grup, atau termasuk dalam 4 tim peringkat ketiga terbaik. Indonesia di Grup F memiliki peluang **41,00%**, di mana laga menghadapi Thailand menjadi kunci krusial pengumpulan poin.
        - **Peluang Lolos 8 Besar (`Reach_Quarter_Final_Prob`)**: Kemungkinan tim memenangkan laga babak gugur pertama (Babak 16 Besar). Indonesia mencatatkan peluang **11,03%** secara agregat turnamen, dan dapat melonjak hingga **40,5%** apabila mengunci posisi Runner-up Grup F!
        - **Peluang Semifinal dan Final**: Persentase menembus 4 besar Asia yang didominasi oleh kekuatan tradisional Asia seperti Jepang, Arab Saudi, Iran, Korea Selatan, dan Australia.
        """
    )

st.write("")

# Visualisasi Interaktif
tab_chart1, tab_chart2 = st.tabs(["📊 Peringkat Peluang Lolos 8 Besar", "🪜 Piramida Kelolosan Negara Pilihan"])

with tab_chart1:
    st.markdown("#### Siapa Saja yang Berpeluang Lolos ke Babak 8 Besar (Perempat Final)?")
    st.caption("Grafik membandingkan 14 negara dengan probabilitas perempat final tertinggi. Timnas Indonesia disorot dengan warna merah khusus.")
    fig_qf = create_top_quarter_final_bar(df)
    st.plotly_chart(fig_qf, width="stretch")

with tab_chart2:
    st.markdown("#### Piramida Ketahanan Turnamen per Negara")
    selected_team = st.selectbox(
        "Pilih Negara untuk Melihat Piramida Kelolosan:",
        df["Team"].tolist(),
        index=df["Team"].tolist().index("Indonesia") if "Indonesia" in df["Team"].tolist() else 0
    )
    fig_funnel = create_stage_progression_funnel(df, team_name=selected_team)
    st.plotly_chart(fig_funnel, width="stretch")

st.write("")

# Tabel Lengkap 24 Peserta dengan Filter
st.markdown("### 📋 Tabel Probabilitas Komprehensif 24 Negara Peserta")

f_col1, f_col2, f_col3, f_col4 = st.columns([1.5, 1.5, 1.5, 1.5])

with f_col1:
    search_q = st.text_input("🔍 Cari Negara:", "")

with f_col2:
    group_filter = st.selectbox("Pilih Grup:", ["Semua Grup"] + sorted(df["Group"].unique().tolist()))

with f_col3:
    min_qf = st.slider("Batas Minimal Peluang 8 Besar (%):", 0.0, 90.0, 0.0, step=5.0)

with f_col4:
    sort_by = st.selectbox(
        "Urutkan Berdasarkan Kolom:",
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

# Format nama kolom tabel dalam bahasa baku
col_renames = {
    "Rank": "Peringkat",
    "Team": "Negara",
    "Group": "Grup",
    "Base_TPI": "Nilai TPI",
    "Group_Stage_Exit_Prob(%)": "Gugur Fase Grup (%)",
    "Reach_Round_16_Prob(%)": "Lolos 16 Besar (%)",
    "Reach_Quarter_Final_Prob(%)": "Lolos 8 Besar (%)",
    "Reach_Semi_Final_Prob(%)": "Lolos Semifinal (%)",
    "Reach_Final_Prob(%)": "Lolos Final (%)",
    "Win_Tournament_Prob(%)": "Juara Turnamen (%)"
}

styled_table = filtered_df.rename(columns=col_renames).copy()

st.dataframe(
    styled_table.style.format({
        "Nilai TPI": "{:.2f}",
        "Gugur Fase Grup (%)": "{:.2f}%",
        "Lolos 16 Besar (%)": "{:.2f}%",
        "Lolos 8 Besar (%)": "{:.2f}%",
        "Lolos Semifinal (%)": "{:.2f}%",
        "Lolos Final (%)": "{:.2f}%",
        "Juara Turnamen (%)": "{:.2f}%"
    }).background_gradient(
        subset=["Lolos 16 Besar (%)", "Lolos 8 Besar (%)", "Lolos Semifinal (%)", "Juara Turnamen (%)"],
        cmap="YlGnBu"
    ),
    width="stretch",
    height=480
)

# Tombol Unduh Data CSV
csv_dl = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Unduh Data Tabel Prediksi Lengkap (CSV)",
    data=csv_dl,
    file_name="prediksi_piala_asia_2027_24_tim.csv",
    mime="text/csv"
)
