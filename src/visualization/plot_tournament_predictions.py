import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('dark_background')
DARK_BG = "#0d1117"
PANEL_BG = "#161b22"
BORDER_COLOR = "#30363d"
TEXT_COLOR = "#f0f6fc"
TEXT_MUTED = "#8b949e"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
csv_path = os.path.join(BASE_DIR, "data", "asian_cup_predictions.csv")
df = pd.read_csv(csv_path)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9), facecolor=DARK_BG)
ax1.set_facecolor(PANEL_BG)
ax2.set_facecolor(PANEL_BG)

# Top 12 Title Contenders
top12 = df.head(12).sort_values(by="Win_Tournament_Prob(%)", ascending=True)
colors = ['#38bdf8' if t != 'Indonesia' else '#ef4444' for t in top12['Team']]

bars = ax1.barh(top12['Team'], top12['Win_Tournament_Prob(%)'], color=colors, edgecolor=BORDER_COLOR, height=0.65)
ax1.set_title("TOP 12 TOURNAMENT WIN PROBABILITIES (%)\n100,000 MONTE CARLO SIMULATIONS", fontsize=13, weight='heavy', color=TEXT_COLOR, pad=15)
ax1.set_xlabel("Championship Probability (%)", fontsize=11, color=TEXT_COLOR)
ax1.grid(color=BORDER_COLOR, linestyle='--', alpha=0.5, axis='x')

for bar in bars:
    w = bar.get_width()
    ax1.text(w + 0.4, bar.get_y() + bar.get_height()/2, f"{w:.2f}%", va='center', ha='left', fontsize=9.5, weight='bold', color=TEXT_COLOR)

# TPI vs Knockout Progression
ax2.scatter(df['Base_TPI'], df['Reach_Semi_Final_Prob(%)'], s=df['Win_Tournament_Prob(%)']*15 + 40, c=df['Win_Tournament_Prob(%)'], cmap='plasma', edgecolors='white', alpha=0.9)
ax2.set_title("BASE TPI vs. REACHING SEMI-FINALS PROBABILITY (%)\nBUBBLE SIZE = CHAMPIONSHIP PROBABILITY", fontsize=13, weight='heavy', color=TEXT_COLOR, pad=15)
ax2.set_xlabel("Base Team Power Index (TPI)", fontsize=11, color=TEXT_COLOR)
ax2.set_ylabel("Probability Reaching Semi-Final (%)", fontsize=11, color=TEXT_COLOR)
ax2.grid(color=BORDER_COLOR, linestyle='--', alpha=0.5)

for idx, r in df.head(10).iterrows():
    ax2.annotate(r['Team'], (r['Base_TPI'], r['Reach_Semi_Final_Prob(%)']),
                 xytext=(r['Base_TPI'] + 0.1, r['Reach_Semi_Final_Prob(%)'] - 1.5),
                 fontsize=8.5, weight='bold', color=TEXT_COLOR)

plt.tight_layout()
output_dir = os.path.join(BASE_DIR, "viz_outputs")
os.makedirs(output_dir, exist_ok=True)
save_target = os.path.join(output_dir, "asian_cup_2027_tournament_predictions.png")
plt.savefig(save_target, dpi=300, facecolor=DARK_BG, bbox_inches='tight')
plt.close()
print(f"Saved {save_target} successfully!")
