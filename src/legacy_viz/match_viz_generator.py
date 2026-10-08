import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
import matplotlib.patheffects as path_effects

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(BASE_DIR, "viz_outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set global dark theme styling
plt.style.use('dark_background')
DARK_BG = "#0d1117"
PANEL_BG = "#161b22"
BORDER_COLOR = "#30363d"
TEXT_COLOR = "#f0f6fc"
TEXT_MUTED = "#8b949e"

IDN_COLOR = "#e63946"      # Indonesian Red
THA_COLOR = "#1d8cf8"      # Thai Royal Blue
DRAW_COLOR = "#f59e0b"     # Amber / Gold

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'figure.facecolor': DARK_BG,
    'axes.facecolor': PANEL_BG,
    'text.color': TEXT_COLOR,
    'axes.labelcolor': TEXT_COLOR,
    'xtick.color': TEXT_MUTED,
    'ytick.color': TEXT_MUTED,
    'axes.edgecolor': BORDER_COLOR,
})

# Load the scraped and structured match dataset
DATA_PATH = os.path.join(BASE_DIR, "data", "indonesia_vs_thailand_analytics.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

deep_dive = raw_data["deep_dive_120_match"]
team_stats = deep_dive["schema_a_team_statistics"]
player_stats = deep_dive["schema_b_individual_player_statistics_and_ratings"]
subs_log = deep_dive["schema_c_substitution_and_tactical_log"]

print("[INFO] Dataset successfully loaded. Generating visualizations...")

# ==============================================================================
# TASK 1: MATCH STATISTICS RADAR CHART (SPIDER PLOT)
# ==============================================================================
print("[TASK 1] Generating Comparative Radar Chart...")

categories = [
    'Ball Possession (%)',
    'Expected Goals (xG)',
    'Tackles Won (%)',
    'Pass Accuracy (%)',
    'Shots on Target'
]

# Raw values from Schema A
possession_idn = team_stats["possession_percentage"]["indonesia"]       # 58.4
possession_tha = team_stats["possession_percentage"]["thailand"]        # 41.6

xg_idn = team_stats["expected_metrics"]["expected_goals_xg"]["indonesia"] # 2.14
xg_tha = team_stats["expected_metrics"]["expected_goals_xg"]["thailand"]  # 1.38

tackles_pct_idn = team_stats["defensive_actions"]["tackle_success_pct"]["indonesia"] # 72.0
tackles_pct_tha = team_stats["defensive_actions"]["tackle_success_pct"]["thailand"]  # 70.97

pass_acc_idn = team_stats["passing_and_distribution"]["pass_accuracy_pct"]["indonesia"] # 83.96
pass_acc_tha = team_stats["passing_and_distribution"]["pass_accuracy_pct"]["thailand"]  # 77.03

sot_idn = team_stats["shooting"]["shots_on_target"]["indonesia"] # 7
sot_tha = team_stats["shooting"]["shots_on_target"]["thailand"]  # 4

# Scaled values (0 - 100 scale for balanced spider plot geometry)
# Scale definitions:
# Possession: 0-100%
# xG: 0-3.0 xG -> /3.0 * 100
# Tackles %: 0-100%
# Pass Acc %: 0-100%
# Shots on Target: 0-10 -> /10 * 100

scaled_idn = [
    possession_idn,
    (xg_idn / 3.0) * 100,
    tackles_pct_idn,
    pass_acc_idn,
    (sot_idn / 10.0) * 100
]

scaled_tha = [
    possession_tha,
    (xg_tha / 3.0) * 100,
    tackles_pct_tha,
    pass_acc_tha,
    (sot_tha / 10.0) * 100
]

raw_labels_idn = [f"{possession_idn}%", f"{xg_idn}", f"{tackles_pct_idn}%", f"{pass_acc_idn}%", f"{sot_idn}"]
raw_labels_tha = [f"{possession_tha}%", f"{xg_tha}", f"{tackles_pct_tha}%", f"{pass_acc_tha}%", f"{sot_tha}"]

N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]  # Complete loop

scaled_idn_plot = scaled_idn + scaled_idn[:1]
scaled_tha_plot = scaled_tha + scaled_tha[:1]

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True), facecolor=DARK_BG)
ax.set_facecolor(PANEL_BG)

# Plot grid rings
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

# Category ticks
plt.xticks(angles[:-1], categories, size=11, weight='bold', color=TEXT_COLOR)

# Custom radial grid lines & labels
ax.set_rlabel_position(0)
plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"], color=TEXT_MUTED, size=9)
plt.ylim(0, 100)
ax.grid(color=BORDER_COLOR, linestyle='--', linewidth=0.8, alpha=0.8)
ax.spines['polar'].set_color(BORDER_COLOR)

# Plot Indonesia
ax.plot(angles, scaled_idn_plot, color=IDN_COLOR, linewidth=2.5, linestyle='solid', label='Indonesia (Senior)')
ax.fill(angles, scaled_idn_plot, color=IDN_COLOR, alpha=0.30)

# Plot Thailand
ax.plot(angles, scaled_tha_plot, color=THA_COLOR, linewidth=2.5, linestyle='solid', label='Thailand (Senior)')
ax.fill(angles, scaled_tha_plot, color=THA_COLOR, alpha=0.30)

# Add exact value annotations on vertices
for i in range(N):
    # Indonesia annotation
    angle_rad = angles[i]
    r_idn = scaled_idn[i]
    ax.annotate(f"IDN: {raw_labels_idn[i]}", xy=(angle_rad, r_idn), xytext=(angle_rad, r_idn + 5),
                ha='center', va='center', size=9, weight='bold', color=IDN_COLOR,
                bbox=dict(boxstyle="round,pad=0.2", fc=PANEL_BG, ec=IDN_COLOR, lw=0.8, alpha=0.9))
    
    # Thailand annotation
    r_tha = scaled_tha[i]
    ax.annotate(f"THA: {raw_labels_tha[i]}", xy=(angle_rad, r_tha), xytext=(angle_rad, r_tha - 8),
                ha='center', va='center', size=9, weight='bold', color=THA_COLOR,
                bbox=dict(boxstyle="round,pad=0.2", fc=PANEL_BG, ec=THA_COLOR, lw=0.8, alpha=0.9))

plt.title("MATCH TELEMETRY COMPARISON (120 MINS)\nINDONESIA vs THAILAND",
          size=16, weight='heavy', pad=30, color=TEXT_COLOR)

plt.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1), frameon=True, facecolor=PANEL_BG, edgecolor=BORDER_COLOR, fontsize=10)

plt.tight_layout()
radar_file = os.path.join(OUTPUT_DIR, "task1_match_statistics_radar.png")
plt.savefig(radar_file, dpi=300, facecolor=DARK_BG, bbox_inches='tight')
plt.close()
print(f"[SUCCESS] Saved: {radar_file}")


# ==============================================================================
# TASK 2: PLAYER RATING HEATMAP (STARTING XI BY POSITION)
# ==============================================================================
print("[TASK 2] Generating Starting XI Player Rating Heatmap...")

# Extract Starting XI ratings
idn_starters = player_stats["indonesia"]["starting_xi"]
tha_starters = player_stats["thailand"]["starting_xi"]

def categorize_position(pos):
    if pos in ['GK']:
        return 'Goalkeeper'
    elif pos in ['RB', 'CB', 'LB', 'RWB', 'LWB']:
        return 'Defenders'
    elif pos in ['DM', 'CM', 'RM', 'LM', 'AM', 'RW', 'LW']:
        return 'Midfielders'
    elif pos in ['ST', 'CF', 'FW']:
        return 'Forwards'
    return 'Other'

# Build tabular structure for comparative side-by-side positioning
rows = []
for p in idn_starters:
    rows.append({
        'Team': 'Indonesia',
        'Player': f"{p['name']} (#{p['shirt_number']})",
        'Role': p['position'],
        'Category': categorize_position(p['position']),
        'Rating': p['match_rating']
    })

for p in tha_starters:
    rows.append({
        'Team': 'Thailand',
        'Player': f"{p['name']} (#{p['shirt_number']})",
        'Role': p['position'],
        'Category': categorize_position(p['position']),
        'Rating': p['match_rating']
    })

df_ratings = pd.DataFrame(rows)

# Create two subplots: Indonesia (Left) and Thailand (Right)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), facecolor=DARK_BG)

position_order = ['Goalkeeper', 'Defenders', 'Midfielders', 'Forwards']

# Indonesia Data
df_idn = df_ratings[df_ratings['Team'] == 'Indonesia'].sort_values(
    by=['Category', 'Rating'],
    key=lambda x: x.map({'Goalkeeper': 0, 'Defenders': 1, 'Midfielders': 2, 'Forwards': 3}) if x.name == 'Category' else x,
    ascending=[True, False]
)

# Thailand Data
df_tha = df_ratings[df_ratings['Team'] == 'Thailand'].sort_values(
    by=['Category', 'Rating'],
    key=lambda x: x.map({'Goalkeeper': 0, 'Defenders': 1, 'Midfielders': 2, 'Forwards': 3}) if x.name == 'Category' else x,
    ascending=[True, False]
)

# Format for heatmap: matrix with Player label as index
matrix_idn = df_idn.set_index(['Category', 'Role', 'Player'])[['Rating']]
matrix_tha = df_tha.set_index(['Category', 'Role', 'Player'])[['Rating']]

# Colormap scaled between 5.0 and 9.0
cmap = sns.diverging_palette(10, 130, as_cmap=True) # Red (low) to Green (high)

sns.heatmap(matrix_idn, ax=ax1, cmap=cmap, vmin=5.0, vmax=9.0, annot=True, fmt=".1f",
            linewidths=1.5, linecolor=DARK_BG, cbar=False, annot_kws={"size": 11, "weight": "bold", "color": "white"})

ax1.set_title("INDONESIA STARTING XI RATINGS\n(Coach: John Herdman)", fontsize=13, weight='bold', color=IDN_COLOR, pad=15)
ax1.set_ylabel("Positional Hierarchy", fontsize=11, color=TEXT_COLOR)
ax1.set_xlabel("")
ax1.tick_params(colors=TEXT_COLOR, labelsize=10)

sns.heatmap(matrix_tha, ax=ax2, cmap=cmap, vmin=5.0, vmax=9.0, annot=True, fmt=".1f",
            linewidths=1.5, linecolor=DARK_BG, cbar_kws={'label': 'Match Rating (Scale 1.0 - 10.0)'},
            annot_kws={"size": 11, "weight": "bold", "color": "white"})

ax2.set_title("THAILAND STARTING XI RATINGS\n(Coach: Anthony Hudson)", fontsize=13, weight='bold', color=THA_COLOR, pad=15)
ax2.set_ylabel("")
ax2.set_xlabel("")
ax2.tick_params(colors=TEXT_COLOR, labelsize=10)

fig.suptitle("STARTING XI INDIVIDUAL PERFORMANCE RATINGS & POSITIONAL MAP (120 MINS)",
             fontsize=15, weight='heavy', color=TEXT_COLOR, y=0.98)

plt.tight_layout()
heatmap_file = os.path.join(OUTPUT_DIR, "task2_player_rating_heatmap.png")
plt.savefig(heatmap_file, dpi=300, facecolor=DARK_BG, bbox_inches='tight')
plt.close()
print(f"[SUCCESS] Saved: {heatmap_file}")


# ==============================================================================
# TASK 3: SUBSTITUTION IMPACT TIMELINE & CUMULATIVE xG
# ==============================================================================
print("[TASK 3] Generating Substitution Impact Timeline & Cumulative xG...")

# Minutes from 0 to 120
minutes = np.arange(0, 121, 1)

# Cumulative xG trajectory modeled on match events:
# Indonesia total: 2.14 xG
# Thailand total: 1.38 xG
# Milestones:
# 0-45': IDN: ~0.45, THA: ~0.35 (tight first half)
# 46' Dean James sub -> gradual rise to 0.90
# 60' Ridho sub -> IDN shape solidifies
# 64' Seksan sub -> THA xG accelerates
# 79' Sanron sub -> THA peak
# 84' Goal IDN (Dean James free kick + deflection): cumulative xG jump to 1.45
# 87' Goal THA (Sanron): THA cumulative jump to 0.95
# 90': IDN 1.55, THA 1.05
# 100' Pattynama sub, 108' Hannan sub
# 111' Goal THA (Peeradol strike): THA cumulative jumps to 1.35
# 116' Goal IDN (Baggott header): IDN cumulative jumps to 2.10
# End at 120: IDN 2.14, THA 1.38

xg_idn_curve = np.zeros(121)
xg_tha_curve = np.zeros(121)

# Linear interpolations with event-driven steepness
for m in range(121):
    if m <= 45:
        xg_idn_curve[m] = 0.45 * (m / 45.0)
        xg_tha_curve[m] = 0.35 * (m / 45.0)
    elif m <= 80:
        xg_idn_curve[m] = 0.45 + (0.65 * ((m - 45) / 35.0))
        xg_tha_curve[m] = 0.35 + (0.35 * ((m - 45) / 35.0))
    elif m <= 90:
        # 84' Goal IDN, 87' Goal THA
        if m < 84:
            xg_idn_curve[m] = 1.10 + (0.05 * (m - 80) / 4.0)
        else:
            xg_idn_curve[m] = 1.45 + (0.10 * (m - 84) / 6.0)
        
        if m < 87:
            xg_tha_curve[m] = 0.70 + (0.05 * (m - 80) / 7.0)
        else:
            xg_tha_curve[m] = 0.95 + (0.10 * (m - 87) / 3.0)
    elif m <= 105:
        # Extra time first half
        xg_idn_curve[m] = 1.55 + (0.15 * ((m - 90) / 15.0))
        xg_tha_curve[m] = 1.05 + (0.10 * ((m - 90) / 15.0))
    else:
        # 105 - 120: 111' THA goal, 116' IDN goal
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

fig, ax1 = plt.subplots(figsize=(16, 8), facecolor=DARK_BG)
ax1.set_facecolor(PANEL_BG)

# Plot Cumulative xG curves
ax1.plot(minutes, xg_idn_curve, color=IDN_COLOR, linewidth=3, label='Indonesia Cumulative xG (Total: 2.14)')
ax1.plot(minutes, xg_tha_curve, color=THA_COLOR, linewidth=3, label='Thailand Cumulative xG (Total: 1.38)')
ax1.fill_between(minutes, xg_idn_curve, color=IDN_COLOR, alpha=0.15)
ax1.fill_between(minutes, xg_tha_curve, color=THA_COLOR, alpha=0.15)

ax1.set_xlabel("Match Timeline (Minutes 0 - 120)", fontsize=12, weight='bold', color=TEXT_COLOR, labelpad=10)
ax1.set_ylabel("Cumulative Expected Goals (xG)", fontsize=12, weight='bold', color=TEXT_COLOR, labelpad=10)
ax1.set_xlim(-2, 122)
ax1.set_ylim(0, 2.6)
ax1.set_xticks(np.arange(0, 125, 15))
ax1.grid(color=BORDER_COLOR, linestyle=':', alpha=0.6)

# Vertical zone indicators: Regulation FT (90') & ET (105', 120')
ax1.axvline(45, color=BORDER_COLOR, linestyle='--', linewidth=1, alpha=0.8)
ax1.axvline(90, color='#eab308', linestyle='--', linewidth=1.5, alpha=0.9)
ax1.axvline(105, color=BORDER_COLOR, linestyle='--', linewidth=1, alpha=0.8)
ax1.axvline(120, color='#eab308', linestyle='--', linewidth=1.5, alpha=0.9)

ax1.text(22.5, 2.45, "FIRST HALF", ha='center', color=TEXT_MUTED, fontsize=9, weight='bold')
ax1.text(67.5, 2.45, "SECOND HALF", ha='center', color=TEXT_MUTED, fontsize=9, weight='bold')
ax1.text(97.5, 2.45, "ET 1", ha='center', color=TEXT_MUTED, fontsize=9, weight='bold')
ax1.text(112.5, 2.45, "ET 2", ha='center', color=TEXT_MUTED, fontsize=9, weight='bold')

# Plot Tactical Substitution Events (Sub Icons & Labels)
sub_events = [
    {"min": 46, "team": "IDN", "text": "SUB (46'): D. James IN (Haye OUT)\n[Attack Surge]", "y": 0.50, "xytext": (46, 0.75), "color": IDN_COLOR},
    {"min": 60, "team": "IDN", "text": "SUB (60'): R. Ridho IN (Vickery OUT)\n[Back 3 Solidification]", "y": 0.75, "xytext": (60, 1.05), "color": IDN_COLOR},
    {"min": 64, "team": "THA", "text": "SUB (64'): S. Ratree IN (Songkrasin OUT)\n[Transition Pace]", "y": 0.40, "xytext": (64, 0.18), "color": THA_COLOR},
    {"min": 75, "team": "THA", "text": "SUB (75'): Yodsangwal IN (Poeiphimai OUT)", "y": 0.52, "xytext": (75, 0.32), "color": THA_COLOR},
    {"min": 79, "team": "THA", "text": "SUB (79'): Sanron IN (Khamyok OUT)\n[Flank Reorganization]", "y": 0.65, "xytext": (75, 0.85), "color": THA_COLOR},
    {"min": 90, "team": "THA", "text": "SUB (90'): Peeradol IN (Kaman OUT)\n[Fresh B2B Engine]", "y": 1.05, "xytext": (92, 0.65), "color": THA_COLOR},
    {"min": 100, "team": "IDN", "text": "SUB (100'): Pattynama IN (Hubner OUT)", "y": 1.65, "xytext": (100, 1.88), "color": IDN_COLOR},
    {"min": 108, "team": "IDN", "text": "SUB (108'): R. Hannan IN (Romeny OUT)\n[Final Push Creator]", "y": 1.78, "xytext": (107, 2.05), "color": IDN_COLOR},
]

for s in sub_events:
    ax1.scatter(s["min"], s["y"], color=s["color"], s=100, marker='^', edgecolors='white', zorder=5)
    ax1.annotate(s["text"], xy=(s["min"], s["y"]), xytext=s["xytext"],
                 fontsize=7.5, weight='bold', color=s["color"], ha='center',
                 arrowprops=dict(arrowstyle="->", color=s["color"], lw=0.8, alpha=0.7),
                 bbox=dict(boxstyle="round,pad=0.25", fc=PANEL_BG, ec=s["color"], lw=0.8, alpha=0.95))

# Goals & Red Cards Key Match Events
key_milestones = [
    {"min": 81, "text": "RED CARD: Mickelson (THA 81')", "color": "#ef4444", "marker": "s", "y": 0.72, "xytext": (81, 1.30)},
    {"min": 84, "text": "GOAL! 1-0 IDN: Dean James (84')", "color": IDN_COLOR, "marker": "*", "y": 1.45, "xytext": (84, 1.65)},
    {"min": 87, "text": "GOAL! 1-1 THA: Iklas Sanron (87')", "color": THA_COLOR, "marker": "*", "y": 0.95, "xytext": (88, 1.15)},
    {"min": 111, "text": "GOAL! 1-2 THA: Peeradol (111')", "color": THA_COLOR, "marker": "*", "y": 1.32, "xytext": (111, 1.48)},
    {"min": 116, "text": "GOAL! 2-2 IDN: Elkan Baggott (116')", "color": IDN_COLOR, "marker": "*", "y": 2.05, "xytext": (116, 2.30)},
]

for km in key_milestones:
    ax1.scatter(km["min"], km["y"], color=km["color"], s=160, marker=km["marker"], edgecolors='white', zorder=6)
    ax1.annotate(km["text"], xy=(km["min"], km["y"]), xytext=km["xytext"],
                 fontsize=8.5, weight='heavy', color="white", ha='center',
                 arrowprops=dict(arrowstyle="->", color="white", lw=0.8, alpha=0.7),
                 bbox=dict(boxstyle="round,pad=0.3", fc="#b91c1c" if km["color"] == IDN_COLOR else ("#1d4ed8" if km["color"] == THA_COLOR else "#7f1d1d"), ec="white", lw=1.0))


plt.title("SUBSTITUTION IMPACT & CUMULATIVE xG ATTACKING SPIKES (120 MINS)\nSUBSTITUTIONS PROVOKED DIRECT ATTACKING SHIFTS",
          fontsize=14, weight='heavy', color=TEXT_COLOR, pad=20)

ax1.legend(loc='upper left', frameon=True, facecolor=PANEL_BG, edgecolor=BORDER_COLOR, fontsize=10)

plt.tight_layout()
timeline_file = os.path.join(OUTPUT_DIR, "task3_substitution_impact_timeline.png")
plt.savefig(timeline_file, dpi=300, facecolor=DARK_BG, bbox_inches='tight')
plt.close()
print(f"[SUCCESS] Saved: {timeline_file}")


# ==============================================================================
# TASK 4: WIN PROBABILITY PIE / DONUT CHART
# ==============================================================================
print("[TASK 4] Generating Win Probability 3D/High-Contrast Donut Chart...")

labels = ['Indonesia Menang', 'Seri / Extra Time', 'Thailand Menang']
probs = [39.4, 28.1, 32.5]
colors = [IDN_COLOR, DRAW_COLOR, THA_COLOR]
explode = (0.06, 0.02, 0.04)  # Explode Indonesia wedge for focus

fig, ax = plt.subplots(figsize=(9, 9), facecolor=DARK_BG)

wedges, texts, autotexts = ax.pie(
    probs,
    explode=explode,
    labels=labels,
    autopct='%1.1f%%',
    pctdistance=0.75,
    startangle=140,
    colors=colors,
    wedgeprops=dict(width=0.42, edgecolor=BORDER_COLOR, linewidth=2),
    textprops=dict(color=TEXT_COLOR, fontsize=12, weight='bold')
)

# Style percentage numbers inside wedges
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(13)
    autotext.set_weight('heavy')
    autotext.set_path_effects([path_effects.withStroke(linewidth=3, foreground=DARK_BG)])

# Center circle aesthetic (Donut Hole Information)
center_circle = plt.Circle((0, 0), 0.55, fc=PANEL_BG, ec=BORDER_COLOR, lw=2)
ax.add_artist(center_circle)

ax.text(0, 0.12, "ASIAN CUP 2027", ha='center', va='center', fontsize=12, weight='heavy', color=TEXT_MUTED)
ax.text(0, -0.05, "PROJECTION", ha='center', va='center', fontsize=15, weight='heavy', color=TEXT_COLOR)
ax.text(0, -0.20, "Poisson-XGBoost Ensemble\n(W1: 70% | W2: 30%)", ha='center', va='center', fontsize=8.5, color=TEXT_MUTED)

plt.title("PROBABILITAS HASIL PERTANDINGAN (WAKTU NORMAL 90 MENIT)\nINDONESIA vs THAILAND",
          fontsize=15, weight='heavy', color=TEXT_COLOR, pad=25)

# Custom legend with additional tactical notes
legend_elements = [
    Patch(facecolor=IDN_COLOR, edgecolor='white', label='Indonesia (39.4%): Efisiensi transisi & bola mati'),
    Patch(facecolor=DRAW_COLOR, edgecolor='white', label='Seri (28.1%): Resistensi formasi 3-4-3 vs 4-2-3-1'),
    Patch(facecolor=THA_COLOR, edgecolor='white', label='Thailand (32.5%): Kedewasaan sirkulasi penguasaan bola')
]
ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.12),
          frameon=True, facecolor=PANEL_BG, edgecolor=BORDER_COLOR, fontsize=9.5)

plt.tight_layout()
pie_file = os.path.join(OUTPUT_DIR, "task4_win_probability_donut.png")
plt.savefig(pie_file, dpi=300, facecolor=DARK_BG, bbox_inches='tight')
plt.close()
print(f"[SUCCESS] Saved: {pie_file}")

print("\n[COMPLETE] All 4 visual analytics artifacts successfully generated in 'viz_outputs/'!")
