"""
AFC Asian Cup 2027 Quantitative Prediction Engine
Principal Sports Quantitative Analyst Pipeline
- Feature Engineering & Team Power Index (TPI) for all 24 qualified teams
- Weights: 40% ELO (4-yr), 30% Squad Value/Quality, 10% Host/Geo, 10% Weather, 10% Dynamic Stochastic Luck
- 100,000 Monte Carlo Tournament Simulations (Group Stage -> Knockouts -> Final)
- Output: asian_cup_predictions.csv
"""

import numpy as np
import pandas as pd
import json
import time

print("[STEP 1] Initializing 24 Participating Teams Dataset & Raw Feature Attributes...")

teams_data = [
    # Pot 1 (Top Seeds & Host)
    {
        "team": "Japan", "code": "JPN", "group": "B",
        "elo": 1655, "squad_val_eur": 285_000_000, "top5_league_players": 17,
        "is_host": False, "dist_km": 8700, "home_jan_temp_c": 5.5
    },
    {
        "team": "Iran", "code": "IRN", "group": "C",
        "elo": 1625, "squad_val_eur": 52_000_000, "top5_league_players": 4,
        "is_host": False, "dist_km": 1300, "home_jan_temp_c": 8.0
    },
    {
        "team": "South Korea", "code": "KOR", "group": "D",
        "elo": 1595, "squad_val_eur": 182_000_000, "top5_league_players": 9,
        "is_host": False, "dist_km": 7500, "home_jan_temp_c": -1.0
    },
    {
        "team": "Australia", "code": "AUS", "group": "E",
        "elo": 1570, "squad_val_eur": 43_000_000, "top5_league_players": 3,
        "is_host": False, "dist_km": 12200, "home_jan_temp_c": 28.0
    },
    {
        "team": "Qatar", "code": "QAT", "group": "F",
        "elo": 1520, "squad_val_eur": 21_000_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 500, "home_jan_temp_c": 21.5
    },
    {
        "team": "Saudi Arabia", "code": "KSA", "group": "A",
        "elo": 1495, "squad_val_eur": 36_000_000, "top5_league_players": 0,
        "is_host": True, "dist_km": 0, "home_jan_temp_c": 21.5
    },
    # Pot 2
    {
        "team": "Iraq", "code": "IRQ", "group": "B",
        "elo": 1455, "squad_val_eur": 16_000_000, "top5_league_players": 1,
        "is_host": False, "dist_km": 950, "home_jan_temp_c": 15.0
    },
    {
        "team": "Uzbekistan", "code": "UZB", "group": "E",
        "elo": 1450, "squad_val_eur": 38_000_000, "top5_league_players": 2,
        "is_host": False, "dist_km": 2800, "home_jan_temp_c": 3.0
    },
    {
        "team": "Jordan", "code": "JOR", "group": "A",
        "elo": 1395, "squad_val_eur": 17_000_000, "top5_league_players": 1,
        "is_host": False, "dist_km": 1300, "home_jan_temp_c": 12.0
    },
    {
        "team": "United Arab Emirates", "code": "UAE", "group": "C",
        "elo": 1385, "squad_val_eur": 31_000_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 800, "home_jan_temp_c": 23.5
    },
    {
        "team": "Oman", "code": "OMA", "group": "D",
        "elo": 1345, "squad_val_eur": 8_500_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 1100, "home_jan_temp_c": 24.5
    },
    {
        "team": "Bahrain", "code": "BHR", "group": "F",
        "elo": 1335, "squad_val_eur": 9_200_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 450, "home_jan_temp_c": 20.0
    },
    # Pot 3
    {
        "team": "China PR", "code": "CHN", "group": "A",
        "elo": 1265, "squad_val_eur": 11_500_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 6800, "home_jan_temp_c": 2.0
    },
    {
        "team": "Syria", "code": "SYR", "group": "C",
        "elo": 1255, "squad_val_eur": 9_000_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 1400, "home_jan_temp_c": 11.0
    },
    {
        "team": "Palestine", "code": "PLE", "group": "D",
        "elo": 1245, "squad_val_eur": 7_500_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 1350, "home_jan_temp_c": 13.0
    },
    {
        "team": "Thailand", "code": "THA", "group": "B",
        "elo": 1230, "squad_val_eur": 10_200_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 5700, "home_jan_temp_c": 28.0
    },
    {
        "team": "Tajikistan", "code": "TJK", "group": "F",
        "elo": 1225, "squad_val_eur": 7_200_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 2900, "home_jan_temp_c": 4.0
    },
    {
        "team": "Kyrgyzstan", "code": "KGZ", "group": "E",
        "elo": 1215, "squad_val_eur": 6_400_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 3300, "home_jan_temp_c": -2.0
    },
    # Pot 4
    {
        "team": "Indonesia", "code": "IDN", "group": "A",
        "elo": 1235, "squad_val_eur": 36_500_000, "top5_league_players": 2,
        "is_host": False, "dist_km": 7300, "home_jan_temp_c": 28.5
    },
    {
        "team": "Vietnam", "code": "VIE", "group": "F",
        "elo": 1185, "squad_val_eur": 6_100_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 6300, "home_jan_temp_c": 22.0
    },
    {
        "team": "Lebanon", "code": "LBN", "group": "C",
        "elo": 1178, "squad_val_eur": 6_000_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 1450, "home_jan_temp_c": 14.0
    },
    {
        "team": "North Korea", "code": "PRK", "group": "D",
        "elo": 1172, "squad_val_eur": 5_200_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 7600, "home_jan_temp_c": -4.0
    },
    {
        "team": "Kuwait", "code": "KUW", "group": "B",
        "elo": 1165, "squad_val_eur": 5_500_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 550, "home_jan_temp_c": 18.0
    },
    {
        "team": "India", "code": "IND", "group": "E",
        "elo": 1125, "squad_val_eur": 6_300_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 3000, "home_jan_temp_c": 21.0
    }
]

df = pd.DataFrame(teams_data)

# ------------------------------------------------------------------------------
# STEP 2: FEATURE ENGINEERING & NORMALIZATION SCHEMA
# ------------------------------------------------------------------------------
print("[STEP 2] Executing Feature Engineering & Calculating Team Power Index (TPI)...")

# 1. Historical Match ELO (Weight: 40%)
min_elo = df['elo'].min()
max_elo = df['elo'].max()
df['f_elo'] = (df['elo'] - min_elo) / (max_elo - min_elo)

# 2. Squad Value & Quality (Weight: 30%)
# Log-transform squad value
df['log_squad_val'] = np.log(df['squad_val_eur'])
min_log_val = df['log_squad_val'].min()
max_log_val = df['log_squad_val'].max()
df['norm_log_squad_val'] = (df['log_squad_val'] - min_log_val) / (max_log_val - min_log_val)

# Top 5 league count
max_top5 = df['top5_league_players'].max()
df['norm_top5'] = df['top5_league_players'] / max_top5

# Combined Squad Score (70% log value + 30% top5 elite presence)
df['f_squad'] = 0.70 * df['norm_log_squad_val'] + 0.30 * df['norm_top5']

# 3. Host & Geographic Advantage (Weight: 10%)
# Host boolean: 1 for KSA, 0 otherwise
# Proximity: travel distance to Riyadh (0 km is 1.0, 12200 km is 0.0)
max_dist = df['dist_km'].max()
df['f_proximity'] = 1.0 - (df['dist_km'] / max_dist)
df['f_host_geo'] = np.where(df['is_host'], 1.0, 0.40 * df['f_proximity'])

# 4. Weather & Climate Adaptability (Weight: 10%)
# Host Jan temperature is 21.5°C
host_temp = 21.5
df['temp_diff'] = np.abs(df['home_jan_temp_c'] - host_temp)
max_temp_diff = df['temp_diff'].max()
df['f_climate'] = 1.0 - (df['temp_diff'] / max_temp_diff)

# 5. Base TPI (Static Component)
# Normalized to a 0.0 - 10.0 scale for intuitive quantitative grading
# Weights: 40% ELO, 30% Squad, 10% Host/Geo, 10% Climate (Sum = 0.90 static)
# Re-scaled over static components: (0.40/0.90)*elo + (0.30/0.90)*squad + (0.10/0.90)*geo + (0.10/0.90)*climate
raw_tpi = (
    0.40 * df['f_elo'] +
    0.30 * df['f_squad'] +
    0.10 * df['f_host_geo'] +
    0.10 * df['f_climate']
)

# Rescale Base_TPI to 1.0 - 10.0 rating space
min_raw = raw_tpi.min()
max_raw = raw_tpi.max()
df['Base_TPI'] = np.round(1.5 + (raw_tpi - min_raw) / (max_raw - min_raw) * 7.5, 2)

# Sort and display feature rankings
df_sorted = df.sort_values(by='Base_TPI', ascending=False).reset_index(drop=True)
print("\n--- BASE TEAM POWER INDEX (TPI) RATINGS ---")
for idx, r in df_sorted.iterrows():
    print(f"{idx+1:2d}. {r['team']:<20} | Group {r['group']} | Base TPI: {r['Base_TPI']:5.2f} (ELO: {r['elo']}, Squad: €{r['squad_val_eur']/1e6:5.1f}M, Top5: {r['top5_league_players']})")

# ------------------------------------------------------------------------------
# STEP 3: MONTE CARLO SIMULATION ENGINE (100,000 ITERATIONS)
# ------------------------------------------------------------------------------
N_SIMULATIONS = 100000
print(f"\n[STEP 3] Launching Monte Carlo Tournament Simulation ({N_SIMULATIONS:,} Iterations)...")

# Mapping team index
teams_list = df['team'].tolist()
n_teams = len(teams_list)
team_to_idx = {name: i for i, name in enumerate(teams_list)}
base_tpi_arr = df['Base_TPI'].values

# Groups structure: 6 groups (A-F), 4 teams per group
groups_dict = {}
for g in ['A', 'B', 'C', 'D', 'E', 'F']:
    groups_dict[g] = [team_to_idx[t] for t in df[df['group'] == g]['team'].tolist()]

# Pre-generate group match pairings: 6 matches per group
# (t0, t1), (t2, t3), (t0, t2), (t1, t3), (t0, t3), (t1, t2)
group_matches = []
for g, g_teams in groups_dict.items():
    g_m = [
        (g_teams[0], g_teams[1]),
        (g_teams[2], g_teams[3]),
        (g_teams[0], g_teams[2]),
        (g_teams[1], g_teams[3]),
        (g_teams[0], g_teams[3]),
        (g_teams[1], g_teams[2])
    ]
    group_matches.append(g_m)

# Logistic sensitivity factor k:
# A 2.0 TPI difference equates to ~78% win prob in knockout
K_FACTOR = 0.65
STOCHASTIC_SIGMA = 0.15 # Stochastic Gaussian Noise (Weight: 10% Luck)

# Tracking counters
exit_group_count = np.zeros(n_teams, dtype=np.int32)
reach_semi_count = np.zeros(n_teams, dtype=np.int32)
reach_final_count = np.zeros(n_teams, dtype=np.int32)
win_tourn_count = np.zeros(n_teams, dtype=np.int32)

np.random.seed(42)
start_time = time.time()

# Run simulations in vectorized batches for speed and memory efficiency
BATCH_SIZE = 10000
n_batches = N_SIMULATIONS // BATCH_SIZE

for b in range(n_batches):
    # Dynamic stochastic luck factor for each team in each simulation
    # Luck ~ N(0, 0.15 * Base_TPI)
    # Shape: (BATCH_SIZE, n_teams)
    
    # Track points and goal difference approximation for all 24 teams in batch
    # Shape: (BATCH_SIZE, n_teams)
    batch_points = np.zeros((BATCH_SIZE, n_teams), dtype=np.float32)
    batch_tpi_tiebreak = np.zeros((BATCH_SIZE, n_teams), dtype=np.float32)

    # 1. GROUP STAGE MATCHES
    for g_idx, g_m in enumerate(group_matches):
        for (t_a, t_b) in g_m:
            # Dynamic stochastic noise per match
            noise_a = np.random.normal(0, STOCHASTIC_SIGMA * base_tpi_arr[t_a], BATCH_SIZE)
            noise_b = np.random.normal(0, STOCHASTIC_SIGMA * base_tpi_arr[t_b], BATCH_SIZE)
            
            eff_tpi_a = base_tpi_arr[t_a] + noise_a
            eff_tpi_b = base_tpi_arr[t_b] + noise_b
            delta = eff_tpi_a - eff_tpi_b
            
            # Probability of Draw decays with higher delta
            p_draw = 0.25 * np.exp(-0.25 * (delta ** 2))
            # Conditional Win A prob
            p_win_a_cond = 1.0 / (1.0 + np.exp(-K_FACTOR * delta))
            p_win_a = (1.0 - p_draw) * p_win_a_cond
            p_win_b = 1.0 - p_draw - p_win_a
            
            # Random uniform draw
            u = np.random.rand(BATCH_SIZE)
            
            win_a_mask = u < p_win_a
            draw_mask = (u >= p_win_a) & (u < (p_win_a + p_draw))
            win_b_mask = u >= (p_win_a + p_draw)
            
            # Points update: Win=3, Draw=1, Loss=0
            batch_points[:, t_a] += win_a_mask * 3.0 + draw_mask * 1.0
            batch_points[:, t_b] += win_b_mask * 3.0 + draw_mask * 1.0
            
            # Tiebreak score based on effective performance
            batch_tpi_tiebreak[:, t_a] += delta
            batch_tpi_tiebreak[:, t_b] -= delta

    # 2. ADVANCING TEAMS DETERMINATION
    # For each group, rank teams by Points + 0.01 * Tiebreaker
    # Qualified: top 2 from 6 groups (12 teams) + 4 best 3rd-placed teams (4 teams) = 16 teams
    
    r16_qualifiers = np.zeros((BATCH_SIZE, 16), dtype=np.int32)
    group_3rds = np.zeros((BATCH_SIZE, 6), dtype=np.int32)
    group_3rd_scores = np.zeros((BATCH_SIZE, 6), dtype=np.float32)

    qual_idx = 0
    for g_idx, (g_name, g_teams) in enumerate(groups_dict.items()):
        # Scores for the 4 teams in this group across all batch sims
        g_scores = batch_points[:, g_teams] + 0.001 * batch_tpi_tiebreak[:, g_teams]
        # Sort descending
        order = np.argsort(-g_scores, axis=1) # (BATCH_SIZE, 4)
        
        # 1st and 2nd place advance automatically
        first_place = np.array(g_teams)[order[:, 0]]
        second_place = np.array(g_teams)[order[:, 1]]
        third_place = np.array(g_teams)[order[:, 2]]
        fourth_place = np.array(g_teams)[order[:, 3]]
        
        r16_qualifiers[:, qual_idx] = first_place
        r16_qualifiers[:, qual_idx + 1] = second_place
        qual_idx += 2
        
        group_3rds[:, g_idx] = third_place
        # 3rd place score
        group_3rd_scores[:, g_idx] = np.take_along_axis(g_scores, order[:, 2:3], axis=1).squeeze(1)

    # Pick 4 best 3rd-placed teams
    order_3rds = np.argsort(-group_3rd_scores, axis=1) # (BATCH_SIZE, 6)
    for i in range(4):
        best_3rd = np.take_along_axis(group_3rds, order_3rds[:, i:i+1], axis=1).squeeze(1)
        r16_qualifiers[:, 12 + i] = best_3rd

    # Record group stage exits
    # Any team NOT in r16_qualifiers exited in group stage
    for sim_i in range(BATCH_SIZE):
        qual_set = set(r16_qualifiers[sim_i])
        for t_idx in range(n_teams):
            if t_idx not in qual_set:
                exit_group_count[t_idx] += 1

    # 3. KNOCKOUT STAGE SIMULATION
    # Standard AFC Knockout bracket pairings for 16 teams:
    # 8 matches in Round of 16 -> 8 QF teams -> 4 SF teams -> 2 Finalists -> 1 Champion
    
    def simulate_knockout_round(contenders_matrix):
        """Simulate single elimination round: contenders_matrix has shape (BATCH_SIZE, 2*K)"""
        k = contenders_matrix.shape[1] // 2
        winners = np.zeros((BATCH_SIZE, k), dtype=np.int32)
        for m in range(k):
            t_a = contenders_matrix[:, 2 * m]
            t_b = contenders_matrix[:, 2 * m + 1]
            
            # Base TPIs
            tpi_a = base_tpi_arr[t_a]
            tpi_b = base_tpi_arr[t_b]
            
            noise_a = np.random.normal(0, STOCHASTIC_SIGMA * tpi_a, BATCH_SIZE)
            noise_b = np.random.normal(0, STOCHASTIC_SIGMA * tpi_b, BATCH_SIZE)
            
            delta = (tpi_a + noise_a) - (tpi_b + noise_b)
            p_win_a = 1.0 / (1.0 + np.exp(-K_FACTOR * delta))
            
            u = np.random.rand(BATCH_SIZE)
            win_a = u < p_win_a
            winners[:, m] = np.where(win_a, t_a, t_b)
        return winners

    # Round of 16 (16 teams -> 8 teams)
    # Seed bracket: A1 vs 3rd, B1 vs 3rd, C1 vs 3rd, D1 vs 3rd, etc.
    qf_teams = simulate_knockout_round(r16_qualifiers)

    # Quarter-Finals (8 teams -> 4 teams)
    sf_teams = simulate_knockout_round(qf_teams)
    
    # Record Reached Semi-Finals
    for sim_i in range(BATCH_SIZE):
        for t in sf_teams[sim_i]:
            reach_semi_count[t] += 1

    # Semi-Finals (4 teams -> 2 teams)
    final_teams = simulate_knockout_round(sf_teams)
    
    # Record Reached Final
    for sim_i in range(BATCH_SIZE):
        for t in final_teams[sim_i]:
            reach_final_count[t] += 1

    # Final (2 teams -> 1 Champion)
    champion_team = simulate_knockout_round(final_teams).squeeze(1)
    
    # Record Champion
    for sim_i in range(BATCH_SIZE):
        win_tourn_count[champion_team[sim_i]] += 1

sim_duration = time.time() - start_time
print(f"[SUCCESS] 100,000 Tournament Simulations completed in {sim_duration:.2f} seconds!")

# ------------------------------------------------------------------------------
# STEP 4: DELIVERABLE GENERATION & CSV EXPORT
# ------------------------------------------------------------------------------
print("[STEP 4] Compiling Deliverable: asian_cup_predictions.csv...")

results_df = pd.DataFrame({
    "Team": df['team'],
    "Base_TPI": df['Base_TPI'],
    "Group_Stage_Exit_Prob(%)": np.round((exit_group_count / N_SIMULATIONS) * 100, 2),
    "Reach_Semi_Final_Prob(%)": np.round((reach_semi_count / N_SIMULATIONS) * 100, 2),
    "Reach_Final_Prob(%)": np.round((reach_final_count / N_SIMULATIONS) * 100, 2),
    "Win_Tournament_Prob(%)": np.round((win_tourn_count / N_SIMULATIONS) * 100, 2)
})

# Sort by Win_Tournament_Prob descending
results_df = results_df.sort_values(by="Win_Tournament_Prob(%)", ascending=False).reset_index(drop=True)
results_df.insert(0, "Rank", range(1, n_teams + 1))

# Save to CSV in data/ directory
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
csv_filename = os.path.join(BASE_DIR, "data", "asian_cup_predictions.csv")
os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
results_df.to_csv(csv_filename, index=False)
print(f"[EXPORT COMPLETE] Successfully generated: {csv_filename}\n")

# Display formatted results table
print(results_df.to_string(index=False))
