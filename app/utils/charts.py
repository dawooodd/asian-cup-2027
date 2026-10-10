"""
Modul Utilitas Visualisasi Plotly untuk Dashboard AFC Asian Cup 2027.
Visualisasi interaktif bertema gelap (dark-mode), edukatif, dan mudah dipahami oleh publik umum.
Menerapkan prinsip kode bersih dan tata bahasa Indonesia baku (PUEBI/KBBI).
"""

from typing import List, Dict, Any
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Palet Warna Tema Gelap Modern
DARK_BG = "#0d1117"
CARD_BG = "#161b22"
BORDER_COLOR = "#30363d"
TEXT_COLOR = "#f0f6fc"
TEXT_MUTED = "#8b949e"

IDN_COLOR = "#e63946"      # Merah Crimson Garuda
GOLD_COLOR = "#fbbf24"     # Emas Juara
CYAN_COLOR = "#38bdf8"     # Biru Langit Elektrik
GREEN_COLOR = "#10b981"    # Hijau Daun
PURPLE_COLOR = "#a855f7"   # Ungu Elegan
ORANGE_COLOR = "#f97316"   # Oranye Cerah


def apply_dark_layout(fig: go.Figure, title: str = "", height: int = 450) -> go.Figure:
    """Menerapkan konfigurasi tata letak standar bertema gelap pada objek grafik Plotly."""
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(family="Inter, Segoe UI, sans-serif", size=15, color=TEXT_COLOR),
            x=0.02,
            y=0.96
        ),
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(family="Inter, Segoe UI, sans-serif", color=TEXT_COLOR),
        margin=dict(l=40, r=40, t=50 if title else 25, b=40),
        height=height,
        hoverlabel=dict(
            bgcolor="#1f2937",
            font_size=13,
            font_family="Inter, Segoe UI, sans-serif",
            bordercolor=BORDER_COLOR
        ),
        legend=dict(
            bgcolor="rgba(22, 27, 34, 0.7)",
            bordercolor=BORDER_COLOR,
            borderwidth=1,
            font=dict(color=TEXT_COLOR, size=11)
        )
    )
    return fig


def create_stage_progression_funnel(df: pd.DataFrame, team_name: str = "Indonesia") -> go.Figure:
    """
    Membuat diagram piramida kelolosan bertahap turnamen untuk negara pilihan.
    Sangat mudah dipahami orang awam untuk melihat di babak mana rintangan terbesar berada.
    """
    row = df[df["Team"] == team_name]
    if row.empty:
        row = df.iloc[0:1]
        team_name = str(row["Team"].iloc[0])
    
    r = row.iloc[0]
    stages = [
        "Fase Grup (Awal)",
        "Lolos 16 Besar",
        "Lolos 8 Besar (Perempat Final)",
        "Lolos Semifinal (4 Besar)",
        "Lolos Final (2 Besar)",
        "Juara Turnamen"
    ]
    
    probs = [
        100.0,
        float(r.get("Reach_Round_16_Prob(%)", 41.00)),
        float(r.get("Reach_Quarter_Final_Prob(%)", 11.03)),
        float(r.get("Reach_Semi_Final_Prob(%)", 2.54)),
        float(r.get("Reach_Final_Prob(%)", 0.43)),
        float(r.get("Win_Tournament_Prob(%)", 0.06))
    ]

    colors = [
        "#94a3b8",      # 100% Start (Abu-abu)
        "#38bdf8",      # 16 Besar (Sian)
        IDN_COLOR if team_name == "Indonesia" else "#f59e0b", # 8 Besar (Sorotan)
        "#10b981",      # Semifinal (Hijau)
        "#a855f7",      # Final (Ungu)
        GOLD_COLOR      # Juara (Emas)
    ]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=stages[::-1],
        x=probs[::-1],
        orientation="h",
        marker=dict(color=colors[::-1], line=dict(color=BORDER_COLOR, width=1.5)),
        text=[f"<b>{p:.2f}%</b>" for p in probs[::-1]],
        textposition="outside",
        textfont=dict(color=TEXT_COLOR, size=12),
        hovertemplate="Tahapan: <b>%{y}</b><br>Peluang Lolos: <b>%{x:.2f}%</b><extra></extra>"
    ))

    apply_dark_layout(fig, title=f"Piramida Probabilitas Kelolosan Bertahap: {team_name}", height=380)
    fig.update_xaxes(title="Peluang Kumulatif (%)", range=[0, 115], gridcolor="#21262d", zerolinecolor="#30363d", color=TEXT_MUTED)
    fig.update_yaxes(color=TEXT_COLOR, tickfont=dict(size=11, weight="bold"))
    return fig


def create_top_quarter_final_bar(df: pd.DataFrame) -> go.Figure:
    """
    Membuat diagram batang horizontal komparatif peluang melaju ke Babak 8 Besar (Perempat Final).
    Menyorot Timnas Indonesia dengan warna merah khas.
    """
    top_qf = df.sort_values(by="Reach_Quarter_Final_Prob(%)", ascending=False).head(14).copy()
    top_qf = top_qf.sort_values(by="Reach_Quarter_Final_Prob(%)", ascending=True)

    colors = []
    for team in top_qf["Team"]:
        if team == "Indonesia":
            colors.append(IDN_COLOR)
        elif team in ["Japan", "Saudi Arabia", "Iran", "South Korea"]:
            colors.append(GOLD_COLOR)
        elif team in ["Australia", "Qatar", "Iraq", "United Arab Emirates", "Uzbekistan", "Jordan"]:
            colors.append(CYAN_COLOR)
        else:
            colors.append("#818cf8")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top_qf["Team"],
        x=top_qf["Reach_Quarter_Final_Prob(%)"],
        orientation="h",
        marker=dict(color=colors, line=dict(color=BORDER_COLOR, width=1.2)),
        text=[f"<b>{val:.1f}%</b>" for val in top_qf["Reach_Quarter_Final_Prob(%)"]],
        textposition="outside",
        textfont=dict(color=TEXT_COLOR, size=11),
        customdata=np.stack((
            top_qf["Base_TPI"],
            top_qf["Reach_Round_16_Prob(%)"],
            top_qf["Reach_Semi_Final_Prob(%)"],
            top_qf["Win_Tournament_Prob(%)"]
        ), axis=-1),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Peluang Lolos 8 Besar: <b>%{x:.2f}%</b><br>"
            "Indeks TPI: <b>%{customdata[0]:.2f}</b><br>"
            "Peluang 16 Besar: <b>%{customdata[1]:.2f}%</b><br>"
            "Peluang Semifinal: <b>%{customdata[2]:.2f}%</b><br>"
            "Peluang Juara: <b>%{customdata[3]:.2f}%</b><extra></extra>"
        )
    ))

    apply_dark_layout(fig, title="Peringkat Peluang Lolos Babak 8 Besar (Perempat Final) Piala Asia 2027", height=500)
    fig.update_xaxes(title="Peluang Menembus Babak 8 Besar (%)", gridcolor="#21262d", zerolinecolor="#30363d", color=TEXT_MUTED)
    fig.update_yaxes(color=TEXT_COLOR, tickfont=dict(size=11, weight="bold"))
    return fig


def create_indonesia_squad_value_evolution_chart(yearly_data: List[Dict[str, Any]]) -> go.Figure:
    """
    Menampilkan pertumbuhan eksponensial nilai pasar skuad Timnas Indonesia (2023 - 2026/2027).
    Membantu orang awam memahami korelasi investasi talenta dengan peningkatan probabilitas kemenangan.
    """
    years = [d["year"] for d in yearly_data]
    vals = [d["market_value_eur"] / 1_000_000 for d in yearly_data]
    ranks = [d["rank_in_asia"] for d in yearly_data]
    notes = [d["notes"] for d in yearly_data]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=years,
        y=vals,
        mode="lines+markers+text",
        name="Nilai Pasar Skuad (€ Juta)",
        line=dict(color=IDN_COLOR, width=3.5),
        marker=dict(size=12, color=GOLD_COLOR, line=dict(color="white", width=2)),
        fill="tozeroy",
        fillcolor="rgba(230, 57, 70, 0.18)",
        text=[f"<b>€{v:.1f}M</b><br>(Peringkat #{r} Asia)" for v, r in zip(vals, ranks)],
        textposition="top center",
        textfont=dict(color=TEXT_COLOR, size=11),
        customdata=notes,
        hovertemplate="Periode: <b>%{x}</b><br>Nilai Skuad: <b>€%{y:.2f} Juta</b><br>Konteks: <i>%{customdata}</i><extra></extra>"
    ))

    apply_dark_layout(fig, title="Evolusi Nilai Pasar Skuad Timnas Indonesia (2023 - 2026)", height=380)
    fig.update_xaxes(gridcolor="#21262d", zerolinecolor="#30363d", color=TEXT_MUTED)
    fig.update_yaxes(title="Nilai Pasar Skuad (€ Juta)", range=[0, 45], gridcolor="#21262d", zerolinecolor="#30363d", color=TEXT_MUTED)
    return fig


def create_scenario_comparison_bar(scenarios: List[Dict[str, Any]]) -> go.Figure:
    """
    Memvisualisasikan 3 jalur taktis Indonesia menuju Babak 8 Besar (Perempat Final).
    Membandingkan probabilitas terjadinya skenario di fase grup vs peluang menang di Babak 16 Besar.
    """
    names = [s["scenario"] for s in scenarios]
    r16_win = [float(s["r16_win_probability"].replace("%", "")) for s in scenarios]
    occur = [float(s["likelihood_to_occur"].replace("%", "")) for s in scenarios]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Kemungkinan Terjadi di Fase Grup",
        x=names,
        y=occur,
        marker=dict(color="#38bdf8", line=dict(color=BORDER_COLOR, width=1)),
        text=[f"<b>{o:.1f}%</b>" for o in occur],
        textposition="outside",
        textfont=dict(color=TEXT_COLOR, size=11)
    ))

    fig.add_trace(go.Bar(
        name="Peluang Menang di 16 Besar Menuju 8 Besar",
        x=names,
        y=r16_win,
        marker=dict(color=IDN_COLOR, line=dict(color=BORDER_COLOR, width=1)),
        text=[f"<b>{w:.1f}%</b>" for w in r16_win],
        textposition="outside",
        textfont=dict(color=TEXT_COLOR, size=11)
    ))

    apply_dark_layout(fig, title="Bedah 3 Skenario Menuju Babak 8 Besar (Perempat Final)", height=420)
    fig.update_layout(
        barmode="group",
        legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="center", x=0.5)
    )
    fig.update_xaxes(color=TEXT_COLOR, tickfont=dict(size=10, weight="bold"))
    fig.update_yaxes(title="Probabilitas (%)", range=[0, 78], gridcolor="#21262d", color=TEXT_MUTED)
    return fig


def create_matches_xg_trajectory_chart(matches: List[Dict[str, Any]]) -> go.Figure:
    """
    Memplot tren Expected Goals (xG Dibuat vs xG Lawan) Timnas Indonesia selama 4 tahun terakhir.
    Memvisualisasikan kematangan taktik: pertahanan kian rapat dan ancaman konversi kian tajam.
    """
    df_m = pd.DataFrame(matches)
    df_m["match_idx"] = range(1, len(df_m) + 1)
    df_m["label"] = df_m["opponent"] + " (" + df_m["score"] + ")"

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_m["match_idx"],
        y=df_m["xg_for"],
        mode="lines+markers",
        name="xG Indonesia (Kualitas Peluang Dibuat)",
        line=dict(color=IDN_COLOR, width=2.5),
        marker=dict(size=8, color=IDN_COLOR),
        hovertemplate="Laga #%{x}: <b>%{text}</b><br>xG Indonesia: <b>%{y:.2f}</b><extra></extra>",
        text=df_m["label"]
    ))

    fig.add_trace(go.Scatter(
        x=df_m["match_idx"],
        y=df_m["xg_against"],
        mode="lines+markers",
        name="xG Lawan (Kualitas Peluang Kebobolan)",
        line=dict(color="#64748b", width=2.0, dash="dash"),
        marker=dict(size=7, color="#94a3b8"),
        hovertemplate="Laga #%{x}: <b>%{text}</b><br>xG Lawan: <b>%{y:.2f}</b><extra></extra>",
        text=df_m["label"]
    ))

    apply_dark_layout(fig, title="Tren Expected Goals (xG) Timnas Indonesia di 20 Laga Kunci (2023 - 2026)", height=420)
    fig.update_xaxes(
        title="Urutan Pertandingan (Kronologis 2023–2026)",
        gridcolor="#21262d",
        zerolinecolor="#30363d",
        color=TEXT_MUTED
    )
    fig.update_yaxes(
        title="Expected Goals (xG)",
        gridcolor="#21262d",
        zerolinecolor="#30363d",
        color=TEXT_MUTED
    )
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5))
    return fig


def create_match_donut_chart(win_a: float, draw: float, win_b: float, team_a: str, team_b: str) -> go.Figure:
    """Membangun diagram donat modern yang merepresentasikan probabilitas hasil pertandingan."""
    labels = [f"{team_a} Menang", "Imbang (Seri)", f"{team_b} Menang"]
    values = [win_a, draw, win_b]
    color_a = IDN_COLOR if team_a == "Indonesia" else "#3b82f6"
    color_b = "#10b981" if team_b != "Indonesia" else IDN_COLOR

    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.62,
        marker=dict(colors=[color_a, "#f59e0b", color_b], line=dict(color=BORDER_COLOR, width=2)),
        textinfo="label+percent", textfont=dict(color=TEXT_COLOR, size=13),
        hoverinfo="label+value+percent", direction="clockwise", sort=False
    )])
    fig.add_annotation(
        text=f"<b>PROYEKSI</b><br><span style='font-size:11px;color:{TEXT_MUTED}'>90 Menit Penuh</span>",
        x=0.5, y=0.5, showarrow=False, font=dict(size=14, color=TEXT_COLOR)
    )
    apply_dark_layout(fig, title=f"Matriks Peluang Hasil Pertandingan: {team_a} vs {team_b}", height=420)
    fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=50, b=20))
    return fig


def create_scoreline_bar_chart(scorelines: List[Dict[str, Any]], team_a: str, team_b: str) -> go.Figure:
    """Membangun diagram batang horizontal yang menampilkan tebakan skor akhir paling mungkin."""
    scores = [s["score"] for s in scorelines]
    probs = [s["probability_pct"] for s in scorelines]

    fig = go.Figure(data=[go.Bar(
        y=scores[::-1], x=probs[::-1], orientation="h",
        marker=dict(color="#38bdf8", line=dict(color=BORDER_COLOR, width=1)),
        text=[f"<b>{p:.1f}%</b>" for p in probs[::-1]], textposition="outside",
        textfont=dict(color=TEXT_COLOR, size=12),
        hovertemplate=f"Skor: <b>%{{y}}</b> ({team_a} - {team_b})<br>Peluang: <b>%{{x:.2f}}%</b><extra></extra>"
    )])
    apply_dark_layout(fig, title="Distribusi Skor Akhir Paling Mungkin", height=380)
    fig.update_xaxes(title="Peluang Terjadi (%)", gridcolor="#21262d", zerolinecolor="#30363d", color=TEXT_MUTED)
    fig.update_yaxes(title="Skor", color=TEXT_COLOR, tickfont=dict(size=12, weight="bold"))
    return fig


def create_player_micro_radar_chart(attributes: Dict[str, int], player_name: str, team_name: str) -> go.Figure:
    """
    Membangun diagram radar spider plot untuk profil atribut mikro penentu keberuntungan pemain kunci.
    Kategori: Ketenangan (Composure), Dampak Penalti, Ketajaman Bola Mati, Kepemimpinan, Penentu Menit 75+.
    """
    categories = [
        "Ketenangan di Bawah Tekanan",
        "Dampak Penalti (Tepis/Eksekusi)",
        "Ketajaman Bola Mati",
        "Karisma & Kepemimpinan",
        "Penentu Laga Menit 75+"
    ]
    raw_keys = ["composure", "penalty_impact", "set_piece_lethality", "leadership", "late_game_decisiveness"]
    values = [attributes.get(k, 80) for k in raw_keys]

    # Tutup poligon radar
    cat_closed = categories + [categories[0]]
    val_closed = values + [values[0]]

    color = IDN_COLOR if team_name == "Indonesia" else CYAN_COLOR

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=val_closed,
        theta=cat_closed,
        fill="toself",
        name=player_name,
        line=dict(color=color, width=2.5),
        fillcolor=f"rgba(230, 57, 70, 0.25)" if team_name == "Indonesia" else "rgba(56, 189, 248, 0.25)",
        marker=dict(size=7, color=color),
        hovertemplate="Atribut: <b>%{theta}</b><br>Nilai: <b>%{r}/100</b><extra></extra>"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10, color=TEXT_MUTED),
                gridcolor="#21262d",
                linecolor="#30363d"
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color=TEXT_COLOR, family="Inter, Segoe UI, sans-serif"),
                gridcolor="#21262d",
                linecolor="#30363d"
            ),
            bgcolor=CARD_BG
        ),
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_COLOR, family="Inter, Segoe UI, sans-serif"),
        height=380,
        margin=dict(l=40, r=40, t=40, b=40),
        title=dict(
            text=f"<b>Radar Atribut Mikro (X-Factor): {player_name} ({team_name})</b>",
            font=dict(size=14, color=TEXT_COLOR),
            x=0.02,
            y=0.98
        ),
        showlegend=False
    )
    return fig


def create_clutch_comparison_bar(teams_data: Dict[str, Any]) -> go.Figure:
    """Membangun diagram perbandingan Clutch Score pemain paling berpengaruh dari 24 negara peserta."""
    team_names = []
    player_names = []
    clutch_scores = []
    colors = []

    for t_name, t_info in teams_data.items():
        players = t_info.get("key_micro_players", [])
        if players:
            p = players[0]
            team_names.append(t_name)
            player_names.append(f"{p['name']} ({t_name})")
            clutch_scores.append(p["clutch_score"])
            colors.append(IDN_COLOR if t_name == "Indonesia" else ("#fbbf24" if p["clutch_score"] >= 94 else CYAN_COLOR))

    df_clutch = pd.DataFrame({
        "label": player_names,
        "score": clutch_scores,
        "team": team_names,
        "color": colors
    }).sort_values(by="score", ascending=True)

    fig = go.Figure(data=[go.Bar(
        y=df_clutch["label"],
        x=df_clutch["score"],
        orientation="h",
        marker=dict(color=df_clutch["color"], line=dict(color=BORDER_COLOR, width=1)),
        text=[f"<b>{s}</b>" for s in df_clutch["score"]],
        textposition="outside",
        textfont=dict(color=TEXT_COLOR, size=10),
        hovertemplate="Pilar Kunci: <b>%{y}</b><br>Skor Clutch: <b>%{x}/100</b><extra></extra>"
    )])

    apply_dark_layout(fig, title="Peringkat Clutch Score Pemain Kunci 24 Negara Peserta (Skala 1 - 100)", height=650)
    fig.update_xaxes(title="Clutch Score (Tingkat Penentu Kemenangan / Keberuntungan)", range=[70, 105], gridcolor="#21262d", color=TEXT_MUTED)
    fig.update_yaxes(color=TEXT_COLOR, tickfont=dict(size=10, weight="bold"))
    return fig

