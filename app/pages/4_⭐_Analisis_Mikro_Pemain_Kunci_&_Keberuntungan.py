"""
Halaman 4: Analisis Mikro Pemain Kunci (X-Factor) & Faktor Keberuntungan Turnamen
Menganalisis 1-2 Pemain Paling Berpengaruh dari Seluruh 24 Negara Peserta AFC Asian Cup 2027
serta Rekam Jejak Tanpa Batas Pasca Piala Asia 2023 hingga FIFA Matchday Oktober 2026.
Bahasa: Bahasa Indonesia Baku (PUEBI/KBBI).
"""

import os
import json
import streamlit as st
import pandas as pd
import numpy as np

from app.utils.styles import inject_custom_css
from app.utils.charts import create_player_micro_radar_chart, create_clutch_comparison_bar

st.set_page_config(
    page_title="Analisis Mikro & Keberuntungan | AFC Asian Cup 2027",
    page_icon="⭐",
    layout="wide"
)

inject_custom_css()

# Direktori Data Lake
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MICRO_PATH = os.path.join(BASE_DIR, "data", "all_24_teams_squad_micro_analytics.json")

@st.cache_data
def load_micro_data():
    if os.path.exists(MICRO_PATH):
        with open(MICRO_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

data_blob = load_micro_data()
teams_dict = data_blob.get("teams", {})

# Tajuk Halaman
st.markdown(
    """
    <div style="margin-bottom: 24px;">
        <span class="metric-badge badge-gold">FAKTOR MIKRO & DETERMINAN KEBERUNTUNGAN (X-FACTOR)</span>
        <span class="metric-badge badge-tha">DATA PASCA PIALA ASIA 2023 S/D OKTOBER 2026</span>
        <h1 style="color: #ffffff; margin-top: 6px; font-weight: 800;">
            ⭐ Pilar Mikro Penentu Keberuntungan & Performa 24 Negara
        </h1>
        <p style="color: #94a3b8; font-size: 1.05rem; line-height: 1.6;">
            Analisis skuad terbaru 2026 dan peran <b>1–2 pemain paling berpengaruh (X-Factor)</b> yang mampu 
            membalikkan probabilitas matematika melalui aksi penentu (*clutch gene*), penyelamatan penalti, 
            dan ketahanan mental di laga krusial, didukung rekam jejak pertandingan resmi tanpa batas sejak Februari 2024 hingga Oktober 2026.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

if not teams_dict:
    st.error("Data analitika mikro 24 negara tidak ditemukan. Jalankan pipeline data terlebih dahulu.")
    st.stop()

# Edukasi Sederhana: Apa itu Faktor Mikro & Keberuntungan Turnamen?
with st.expander("📚 Memahami 'Faktor Mikro & Keberuntungan' dalam Sains Data Sepak Bola (Panduan Orang Awam)", expanded=True):
    st.markdown(
        """
        Dalam turnamen kompetisi sistem gugur seperti Piala Asia, data statistik makro (seperti penguasaan bola dan peringkat dunia) 
        sering kali ditentukan oleh **momen-momen mikro satu detik**:
        
        1. **Apa itu Faktor 'Clutch' (*Penentu Menit Akhir*)?**
           Pemain tertentu memiliki ketahanan saraf luar biasa ketika berada di bawah tekanan ekstrem. Contohnya **Son Heung-min (Korea Selatan)** 
           atau **Salem Al-Dawsari (Arab Saudi)** yang secara statistik memiliki probabilitas mencetak gol pada menit 85+ jauh lebih tinggi daripada rata-rata pemain.
        2. **Keberuntungan dari Penjaga Gawang (*The Penalty Factor*)**:
           Kiper kelas dunia seperti **Maarten Paes (Indonesia)** yang memiliki rekor penyelamatan penalti dan persentase *shot-stopping* 78,4% 
           dapat menyumbangkan 'keberuntungan ilmiah' bagi timnya saat dipaksa bertahan di bawah gempuran 20 tembakan lawan atau babak adu penalti.
        3. **Bola Mati Pemecah Kebuntuan (*Set-Piece Weapon*)**:
           Ketika pertandingan terkunci 0-0, keberadaan pemain bertinggi 198 cm seperti **Harry Souttar (Australia)** atau penendang bebas melengkung 
           seperti **Mohamed Marhoon (Bahrain)** dan **Akram Afif (Qatar)** menjadi pembeda antara tersingkir atau melaju ke perempat final.
        """
    )

st.write("")

# Tab Navigasi Utama
tab_profil, tab_komparasi, tab_riwayat = st.tabs([
    "🔍 Profil Pemain Kunci per Negara",
    "📊 Peringkat Skor Clutch 24 Negara",
    "📋 Rekam Jejak Laga Resmi (Feb 2024 - Okt 2026)"
])

with tab_profil:
    col_sel1, col_sel2 = st.columns([1, 2])
    
    with col_sel1:
        group_choice = st.selectbox(
            "Pilih Grup Turnamen:",
            ["Semua Grup", "Grup A", "Grup B", "Grup C", "Grup D", "Grup E", "Grup F"]
        )
        
        # Saring daftar tim
        if group_choice == "Semua Grup":
            avail_teams = list(teams_dict.keys())
        else:
            grp_letter = group_choice.split()[-1]
            avail_teams = [t for t, d in teams_dict.items() if d.get("group") == grp_letter]
        
        selected_team = st.selectbox(
            "Pilih Negara Peserta:",
            avail_teams,
            index=avail_teams.index("Indonesia") if "Indonesia" in avail_teams else 0
        )
        
        team_info = teams_dict[selected_team]
        perf = team_info.get("performance_feb2024_oct2026", {})
        
        st.markdown(
            f"""
            <div style="background: rgba(22, 27, 34, 0.85); border: 1px solid #30363d; border-radius: 10px; padding: 16px; margin-top: 15px;">
                <div style="color: #38bdf8; font-weight: 700; font-size: 0.85rem;">RINGKASAN SKUAD 2026</div>
                <div style="color: #f0f6fc; font-size: 1.3rem; font-weight: 800; margin-top: 4px;">{selected_team} (Grup {team_info.get('group')})</div>
                <div style="color: #94a3b8; font-size: 0.9rem; margin-top: 6px;">
                    <b>Pelatih Kepala:</b> {team_info.get('coach', '-')}<br>
                    <b>Jumlah Skuad:</b> {team_info.get('squad_size_2026', 26)} Pemain<br>
                    <b>Nilai Pasar Skuad:</b> €{team_info.get('squad_market_value_eur', 0)/1e6:.1f} Juta
                </div>
                <div style="border-top: 1px solid #30363d; margin-top: 10px; padding-top: 10px; font-size: 0.85rem; color: #cbd5e1;">
                    <b>Rekor Pasca Piala Asia 2023 (s/d Okt 2026):</b><br>
                    {perf.get('matches_played', 0)} Laga: {perf.get('wins', 0)} M - {perf.get('draws', 0)} S - {perf.get('losses', 0)} K<br>
                    <span style="color: #10b981; font-weight: 700;">{perf.get('win_rate_pct', 0)}% Win Rate</span> • 
                    <span style="color: #fbbf24; font-weight: 700;">{perf.get('unbeaten_rate_pct', 0)}% Unbeaten</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_sel2:
        players = team_info.get("key_micro_players", [])
        if not players:
            st.info("Data pemain pilar mikro sedang diperbarui.")
        else:
            st.markdown(f"### ⭐ Pilar Penentu Keberuntungan (X-Factor): {selected_team}")
            
            for p_idx, p in enumerate(players):
                p_col_info, p_col_radar = st.columns([1.2, 1])
                
                with p_col_info:
                    st.markdown(
                        f"""
                        <div style="background: rgba(22, 27, 34, 0.95); border-left: 4px solid {'#e63946' if selected_team == 'Indonesia' else '#38bdf8'}; 
                                    border-radius: 8px; padding: 16px; margin-bottom: 15px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="font-size: 1.2rem; font-weight: 800; color: #f0f6fc;">{p['name']}</div>
                                <span class="metric-badge {'badge-idn' if selected_team == 'Indonesia' else 'badge-gold'}">
                                    Clutch Score: {p['clutch_score']}/100
                                </span>
                            </div>
                            <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">
                                <b>Posisi:</b> {p['position']} • <b>Usia:</b> {p['age_2026']} Thn • <b>Klub:</b> {p['club']}
                            </div>
                            <div style="color: #fbbf24; font-weight: 700; font-size: 0.9rem; margin-top: 8px;">
                                🎯 Peran: {p['x_factor_role']}
                            </div>
                            <div style="color: #cbd5e1; font-size: 0.88rem; line-height: 1.5; margin-top: 6px;">
                                {p['micro_narrative']}
                            </div>
                            <div style="color: #38bdf8; font-size: 0.82rem; margin-top: 8px; font-weight: 600;">
                                🍀 Pengganda Keberuntungan Turnamen: <span style="color:#ffffff;">+{int((p['micro_luck_multiplier'] - 1.0)*100)}% Momentum Boost</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                with p_col_radar:
                    fig_radar = create_player_micro_radar_chart(
                        attributes=p["attributes"],
                        player_name=p["name"],
                        team_name=selected_team
                    )
                    st.plotly_chart(fig_radar, width="stretch")

with tab_komparasi:
    st.markdown("### 📊 Peringkat Skor Clutch 24 Pemain Kunci se-Asia")
    st.caption("Membandingkan tingkat ketenangan, kemampuan mengeksekusi di menit akhir (75+), dan penyelamatan penalti dari 1 pilar utama masing-masing negara.")
    fig_clutch_all = create_clutch_comparison_bar(teams_dict)
    st.plotly_chart(fig_clutch_all, width="stretch")

with tab_riwayat:
    st.markdown("### 📋 Rekam Jejak Performa 24 Negara Pasca Piala Asia 2023 (Februari 2024 s/d Oktober 2026)")
    st.caption("Data dihimpun dari seluruh pertandingan resmi (Kualifikasi Piala Dunia R2 & R3, Kualifikasi Piala Asia, dan FIFA Matchday resmi terbaru).")
    
    summary_rows = []
    for t_name, t_val in teams_dict.items():
        p = t_val.get("performance_feb2024_oct2026", {})
        first_p = t_val.get("key_micro_players", [{}])[0] if t_val.get("key_micro_players") else {}
        summary_rows.append({
            "Negara": t_name,
            "Grup": t_val.get("group", "-"),
            "Pemain Kunci": first_p.get("name", "-"),
            "Skor Clutch": first_p.get("clutch_score", 0),
            "Main": p.get("matches_played", 0),
            "Menang": p.get("wins", 0),
            "Imbang": p.get("draws", 0),
            "Kalah": p.get("losses", 0),
            "Win Rate (%)": p.get("win_rate_pct", 0.0),
            "Tak Terkalahkan (%)": p.get("unbeaten_rate_pct", 0.0),
            "Gol": p.get("goals_for", 0),
            "Kebobolan": p.get("goals_against", 0),
            "Selisih Gol": p.get("goal_difference", 0),
            "Nirbobol": p.get("clean_sheets", 0),
            "Rata-rata xG": p.get("avg_xg_for", 0.0)
        })
    
    df_summary = pd.DataFrame(summary_rows).sort_values(by="Win Rate (%)", ascending=False)
    
    st.dataframe(
        df_summary.style.format({
            "Win Rate (%)": "{:.1f}%",
            "Tak Terkalahkan (%)": "{:.1f}%",
            "Rata-rata xG": "{:.2f}"
        }).background_gradient(subset=["Win Rate (%)", "Tak Terkalahkan (%)", "Skor Clutch"], cmap="YlGnBu"),
        width="stretch",
        height=520
    )
    
    # Unduh CSV
    csv_micro = df_summary.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Unduh Data Analitika Mikro & Performa Laga Pasca Piala Asia 2023 (CSV)",
        data=csv_micro,
        file_name="analisis_mikro_24_negara_piala_asia_2027.csv",
        mime="text/csv"
    )
