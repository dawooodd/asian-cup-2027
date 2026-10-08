"""
Plotly Chart Utility Module for AFC Asian Cup 2027 Dashboard.
High-impact, interactive visualizations with dark-mode aesthetic.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Theme palette matching IDE / GitHub dark mode
DARK_BG = "#0d1117"
CARD_BG = "#161b22"
BORDER_COLOR = "#30363d"
TEXT_COLOR = "#f0f6fc"
TEXT_MUTED = "#8b949e"

IDN_COLOR = "#e63946"      # Indonesian Vibrant Crimson
THA_COLOR = "#1d8cf8"      # Thai Royal Azure
DRAW_COLOR = "#f59e0b"     # Amber Gold
ACCENT_GREEN = "#10b981"   # Mint Green
ACCENT_PURPLE = "#a855f7"  # Electric Purple


def apply_dark_layout(fig, title="", height=450):
    """Applies standardized dark theme styling to Plotly figures."""
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(family="Inter, Segoe UI, sans-serif", size=16, color=TEXT_COLOR),
            x=0.02,
            y=0.95
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


def create_top10_outright_bar(df: pd.DataFrame) -> go.Figure:
    """
    Builds an interactive horizontal bar chart showing the top 10 teams
    most likely to win the AFC Asian Cup 2027.
    """
    top10 = df.sort_values(by="Win_Tournament_Prob(%)", ascending=False).head(10).copy()
    top10 = top10.sort_values(by="Win_Tournament_Prob(%)", ascending=True)

    # Highlight Indonesia with crimson, others with azure/gold gradient
    colors = []
    for team in top10["Team"]:
        if team == "Indonesia":
            colors.append(IDN_COLOR)
        elif team == "Japan":
            colors.append("#fbbf24") # Golden for favorite
        elif team in ["South Korea", "Iran", "Australia", "Saudi Arabia"]:
            colors.append("#38bdf8")
        else:
            colors.append("#818cf8")

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=top10["Team"],
        x=top10["Win_Tournament_Prob(%)"],
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(color=BORDER_COLOR, width=1.2)
        ),
        text=[f"<b>{val:.2f}%</b>" for val in top10["Win_Tournament_Prob(%)"]],
        textposition="outside",
        textfont=dict(color=TEXT_COLOR, size=12),
        customdata=np.stack((
            top10["Base_TPI"],
            top10["Reach_Semi_Final_Prob(%)"],
            top10["Reach_Final_Prob(%)"],
            top10["Group_Stage_Exit_Prob(%)"]
        ), axis=-1),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Win Tournament: <b>%{x:.2f}%</b><br>"
            "Base TPI: <b>%{customdata[0]:.2f}</b><br>"
            "Reach Semis: <b>%{customdata[1]:.2f}%</b><br>"
            "Reach Finals: <b>%{customdata[2]:.2f}%</b><br>"
            "Group Exit: <b>%{customdata[3]:.2f}%</b>"
            "<extra></extra>"
        )
    ))

    apply_dark_layout(fig, title="Top 10 Tournament Win Probabilities (100k Monte Carlo)", height=450)
    fig.update_xaxes(
        title="Championship Probability (%)",
        gridcolor="#21262d",
        zerolinecolor="#30363d",
        color=TEXT_MUTED
    )
    fig.update_yaxes(
        color=TEXT_COLOR,
        tickfont=dict(size=12, weight="bold")
    )
    return fig


def create_tpi_vs_knockout_scatter(df: pd.DataFrame) -> go.Figure:
    """
    Builds a bubble chart comparing Base TPI vs Reach Semi-Final Probability,
    with bubble size proportional to Tournament Win Probability.
    """
    fig = px.scatter(
        df,
        x="Base_TPI",
        y="Reach_Semi_Final_Prob(%)",
        size="Win_Tournament_Prob(%)",
        color="Win_Tournament_Prob(%)",
        hover_name="Team",
        text="Team",
        color_continuous_scale="Viridis",
        size_max=38,
        custom_data=["Win_Tournament_Prob(%)", "Reach_Final_Prob(%)", "Group_Stage_Exit_Prob(%)"]
    )

    fig.update_traces(
        textposition="top center",
        textfont=dict(size=10, color=TEXT_COLOR),
        marker=dict(line=dict(width=1, color="rgba(255,255,255,0.7)")),
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Base TPI: <b>%{x:.2f}</b><br>"
            "Semi-Final Prob: <b>%{y:.2f}%</b><br>"
            "Finals Prob: <b>%{customdata[1]:.2f}%</b><br>"
            "Win Tournament: <b>%{customdata[0]:.2f}%</b><extra></extra>"
        )
    )

    apply_dark_layout(fig, title="Base TPI vs. Deep Knockout Progression Odds", height=480)
    fig.update_xaxes(
        title="Base Team Power Index (TPI)",
        gridcolor="#21262d",
        zerolinecolor="#30363d",
        color=TEXT_MUTED
    )
    fig.update_yaxes(
        title="Probability of Reaching Semi-Finals (%)",
        gridcolor="#21262d",
        zerolinecolor="#30363d",
        color=TEXT_MUTED
    )
    fig.update_coloraxes(colorbar=dict(title="Win Prob (%)", tickfont=dict(color=TEXT_MUTED)))
    return fig


def create_radar_chart(team_stats: dict) -> go.Figure:
    """
    Builds an interactive Radar/Spider chart comparing Indonesia vs Thailand match metrics.
    Categories: Ball Possession (%), Expected Goals (xG), Tackles Won (%), Pass Accuracy (%), Shots on Target.
    """
    categories = [
        'Ball Possession (%)',
        'Expected Goals (xG)',
        'Tackles Won (%)',
        'Pass Accuracy (%)',
        'Shots on Target'
    ]

    # Raw metrics
    pos_idn = team_stats.get("possession_percentage", {}).get("indonesia", 58.4)
    pos_tha = team_stats.get("possession_percentage", {}).get("thailand", 41.6)

    xg_idn = team_stats.get("expected_metrics", {}).get("expected_goals_xg", {}).get("indonesia", 2.14)
    xg_tha = team_stats.get("expected_metrics", {}).get("expected_goals_xg", {}).get("thailand", 1.38)

    tac_idn = team_stats.get("defensive_actions", {}).get("tackle_success_pct", {}).get("indonesia", 72.0)
    tac_tha = team_stats.get("defensive_actions", {}).get("tackle_success_pct", {}).get("thailand", 70.97)

    pass_idn = team_stats.get("passing_and_distribution", {}).get("pass_accuracy_pct", {}).get("indonesia", 83.96)
    pass_tha = team_stats.get("passing_and_distribution", {}).get("pass_accuracy_pct", {}).get("thailand", 77.03)

    sot_idn = team_stats.get("shooting", {}).get("shots_on_target", {}).get("indonesia", 7)
    sot_tha = team_stats.get("shooting", {}).get("shots_on_target", {}).get("thailand", 4)

    # Scaled 0 - 100 for radar visual symmetry
    scaled_idn = [
        pos_idn,
        (xg_idn / 3.0) * 100,
        tac_idn,
        pass_idn,
        (sot_idn / 10.0) * 100
    ]

    scaled_tha = [
        pos_tha,
        (xg_tha / 3.0) * 100,
        tac_tha,
        pass_tha,
        (sot_tha / 10.0) * 100
    ]

    raw_idn = [f"{pos_idn}%", f"{xg_idn} xG", f"{tac_idn}%", f"{pass_idn}%", f"{sot_idn} shots"]
    raw_tha = [f"{pos_tha}%", f"{xg_tha} xG", f"{tac_tha}%", f"{pass_tha}%", f"{sot_tha} shots"]

    # Close the polygon loop
    cat_loop = categories + [categories[0]]
    idn_loop = scaled_idn + [scaled_idn[0]]
    tha_loop = scaled_tha + [scaled_tha[0]]
    raw_idn_loop = raw_idn + [raw_idn[0]]
    raw_tha_loop = raw_tha + [raw_tha[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=idn_loop,
        theta=cat_loop,
        fill='toself',
        fillcolor='rgba(230, 57, 70, 0.35)',
        line=dict(color=IDN_COLOR, width=2.8),
        name='Indonesia',
        customdata=raw_idn_loop,
        hovertemplate="<b>Indonesia</b><br>%{theta}: <b>%{customdata}</b> (Index: %{r:.1f})<extra></extra>"
    ))

    fig.add_trace(go.Scatterpolar(
        r=tha_loop,
        theta=cat_loop,
        fill='toself',
        fillcolor='rgba(29, 140, 248, 0.35)',
        line=dict(color=THA_COLOR, width=2.8),
        name='Thailand',
        customdata=raw_tha_loop,
        hovertemplate="<b>Thailand</b><br>%{theta}: <b>%{customdata}</b> (Index: %{r:.1f})<extra></extra>"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                linecolor="#30363d",
                gridcolor="#21262d"
            ),
            angularaxis=dict(
                linecolor="#30363d",
                gridcolor="#21262d",
                tickfont=dict(color=TEXT_COLOR, size=11, family="Inter, Segoe UI, sans-serif")
            ),
            bgcolor="#161b22"
        ),
        paper_bgcolor=CARD_BG,
        font=dict(family="Inter, Segoe UI, sans-serif", color=TEXT_COLOR),
        height=480,
        margin=dict(l=60, r=60, t=40, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color=TEXT_COLOR)
        )
    )
    return fig


def create_substitution_timeline_chart() -> go.Figure:
    """
    Builds an interactive Timeline mapping substitution minutes and goals against
    the cumulative Expected Goals (xG) line curves for Indonesia (2.14 xG) and Thailand (1.38 xG).
    """
    minutes = np.arange(0, 121, 1)
    xg_idn_curve = np.zeros(121)
    xg_tha_curve = np.zeros(121)

    for m in range(121):
        if m <= 45:
            xg_idn_curve[m] = 0.45 * (m / 45.0)
            xg_tha_curve[m] = 0.35 * (m / 45.0)
        elif m <= 80:
            xg_idn_curve[m] = 0.45 + (0.65 * ((m - 45) / 35.0))
            xg_tha_curve[m] = 0.35 + (0.35 * ((m - 45) / 35.0))
        elif m <= 90:
            if m < 84:
                xg_idn_curve[m] = 1.10 + (0.05 * (m - 80) / 4.0)
            else:
                xg_idn_curve[m] = 1.45 + (0.10 * (m - 84) / 6.0)

            if m < 87:
                xg_tha_curve[m] = 0.70 + (0.05 * (m - 80) / 7.0)
            else:
                xg_tha_curve[m] = 0.95 + (0.10 * (m - 87) / 3.0)
        elif m <= 105:
            xg_idn_curve[m] = 1.55 + (0.15 * ((m - 90) / 15.0))
            xg_tha_curve[m] = 1.05 + (0.10 * ((m - 90) / 15.0))
        else:
            if m < 111:
                xg_tha_curve[m] = 1.15 + (0.05 * (m - 105) / 6.0)
            else:
                xg_tha_curve[m] = 1.32 + (0.06 * (m - 111) / 9.0)

            if m < 116:
                xg_idn_curve[m] = 1.70 + (0.08 * (m - 105) / 11.0)
            else:
                xg_idn_curve[m] = 2.05 + (0.09 * (m - 116) / 4.0)

    xg_idn_curve[-1] = 2.14
    xg_tha_curve[-1] = 1.38

    fig = go.Figure()

    # Indonesia xG Curve
    fig.add_trace(go.Scatter(
        x=minutes,
        y=xg_idn_curve,
        mode="lines",
        name="Indonesia Cumulative xG (2.14)",
        line=dict(color=IDN_COLOR, width=3.2),
        fill="tozeroy",
        fillcolor="rgba(230, 57, 70, 0.12)",
        hovertemplate="Minute %{x}'<br>Indonesia xG: <b>%{y:.2f}</b><extra></extra>"
    ))

    # Thailand xG Curve
    fig.add_trace(go.Scatter(
        x=minutes,
        y=xg_tha_curve,
        mode="lines",
        name="Thailand Cumulative xG (1.38)",
        line=dict(color=THA_COLOR, width=3.2),
        fill="tozeroy",
        fillcolor="rgba(29, 140, 248, 0.12)",
        hovertemplate="Minute %{x}'<br>Thailand xG: <b>%{y:.2f}</b><extra></extra>"
    ))

    # Match Phase Vertical Guides
    phases = [(45, "HT (0-0)"), (90, "FT (1-1)"), (105, "ET HT"), (120, "AET (2-2)")]
    for p_min, p_label in phases:
        fig.add_vline(
            x=p_min,
            line_width=1.5,
            line_dash="dash",
            line_color="#f59e0b" if p_min in [90, 120] else "#475569"
        )
        fig.add_annotation(
            x=p_min,
            y=2.5,
            text=f"<b>{p_label}</b>",
            showarrow=False,
            font=dict(color="#f59e0b" if p_min in [90, 120] else TEXT_MUTED, size=10),
            bgcolor="rgba(15, 23, 42, 0.7)"
        )

    # Goal Markers
    goals = [
        (84, 1.45, "⚽ 84' Dean James (IDN 1-0)", IDN_COLOR),
        (87, 0.95, "⚽ 87' Sanron (THA 1-1)", THA_COLOR),
        (111, 1.32, "⚽ 111' Peeradol (THA 2-1)", THA_COLOR),
        (116, 2.08, "⚽ 116' Elkan Baggott (IDN 2-2)", IDN_COLOR)
    ]
    for g_min, g_val, g_text, g_color in goals:
        fig.add_trace(go.Scatter(
            x=[g_min],
            y=[g_val],
            mode="markers+text",
            marker=dict(symbol="star", size=14, color=g_color, line=dict(color="white", width=1.5)),
            name=g_text,
            text=[g_text],
            textposition="top center" if "IDN" in g_text else "bottom center",
            textfont=dict(size=10, color=g_color),
            showlegend=False,
            hoverinfo="text",
            hovertext=f"<b>GOAL!</b> {g_text} at {g_min}'"
        ))

    # Tactical Substitution Annotations (Impact Points)
    substitutions = [
        (46, 0.48, "🔄 46' Sub: Dean James IN", IDN_COLOR),
        (60, 0.75, "🔄 60' Sub: Rizky Ridho IN", IDN_COLOR),
        (64, 0.52, "🔄 64' Sub: Seksan Ratree IN", THA_COLOR),
        (79, 0.72, "🔄 79' Sub: Iklas Sanron IN", THA_COLOR),
        (100, 1.63, "🔄 100' Sub: Shayne Pattynama IN", IDN_COLOR),
        (108, 1.20, "🔄 108' Sub: Rayhan Hannan IN", IDN_COLOR),
        (115, 1.85, "🔄 115' Sub: Ramadhan Sananta IN", IDN_COLOR)
    ]
    for s_min, s_val, s_text, s_color in substitutions:
        fig.add_trace(go.Scatter(
            x=[s_min],
            y=[s_val],
            mode="markers",
            marker=dict(symbol="triangle-up", size=10, color=s_color, line=dict(color="#ffffff", width=1)),
            showlegend=False,
            hoverinfo="text",
            hovertext=f"Tactical Change: {s_text}"
        ))

    apply_dark_layout(fig, title="120-Minute Cumulative xG Trajectory & Tactical Impact Timeline", height=500)
    fig.update_xaxes(
        title="Match Timeline (Minutes 0' to 120')",
        gridcolor="#21262d",
        zerolinecolor="#30363d",
        dtick=15,
        range=[-2, 124],
        color=TEXT_MUTED
    )
    fig.update_yaxes(
        title="Cumulative Expected Goals (xG)",
        gridcolor="#21262d",
        zerolinecolor="#30363d",
        range=[0, 2.7],
        color=TEXT_MUTED
    )
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.22,
            xanchor="center",
            x=0.5
        )
    )
    return fig


def create_match_donut_chart(win_a: float, draw: float, win_b: float, team_a: str, team_b: str) -> go.Figure:
    """
    Builds a modern 3D-styled Donut Chart representing simulated match outcome probabilities.
    """
    labels = [f"{team_a} Win", "Draw", f"{team_b} Win"]
    values = [win_a, draw, win_b]

    # Assign team-appropriate colors
    color_a = IDN_COLOR if team_a == "Indonesia" else "#3b82f6"
    color_b = THA_COLOR if team_b == "Thailand" else "#10b981"
    colors = [color_a, DRAW_COLOR, color_b]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.62,
        marker=dict(
            colors=colors,
            line=dict(color=BORDER_COLOR, width=2)
        ),
        textinfo="label+percent",
        textfont=dict(color=TEXT_COLOR, size=13, family="Inter, Segoe UI, sans-serif"),
        hoverinfo="label+value+percent",
        direction="clockwise",
        sort=False
    )])

    # Center text annotation
    fig.add_annotation(
        text=f"<b>PROJECTION</b><br><span style='font-size:11px;color:{TEXT_MUTED}'>90 Mins FT</span>",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=14, color=TEXT_COLOR, family="Inter, Segoe UI, sans-serif")
    )

    apply_dark_layout(fig, title=f"Win Probability Matrix: {team_a} vs {team_b}", height=420)
    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig


def create_scoreline_bar_chart(scorelines: list, team_a: str, team_b: str) -> go.Figure:
    """
    Builds a horizontal bar chart displaying the top 6 most likely scorelines.
    """
    scores = [s["score"] for s in scorelines]
    probs = [s["probability_pct"] for s in scorelines]

    fig = go.Figure(data=[go.Bar(
        y=scores[::-1],
        x=probs[::-1],
        orientation="h",
        marker=dict(
            color="#38bdf8",
            line=dict(color=BORDER_COLOR, width=1)
        ),
        text=[f"<b>{p:.1f}%</b>" for p in probs[::-1]],
        textposition="outside",
        textfont=dict(color=TEXT_COLOR, size=12),
        hovertemplate=f"Scoreline: <b>%{{y}}</b> ({team_a} - {team_b})<br>Probability: <b>%{{x:.2f}}%</b><extra></extra>"
    )])

    apply_dark_layout(fig, title="Most Probable Full-Time Scorelines", height=380)
    fig.update_xaxes(
        title="Probability (%)",
        gridcolor="#21262d",
        zerolinecolor="#30363d",
        color=TEXT_MUTED
    )
    fig.update_yaxes(
        title="Scoreline",
        color=TEXT_COLOR,
        tickfont=dict(size=12, weight="bold")
    )
    return fig
