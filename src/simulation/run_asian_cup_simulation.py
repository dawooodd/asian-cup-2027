"""
Mesin Prediksi Kuantitatif AFC Asian Cup 2027
Pipeline Sains Data Olahraga Profesional & Simulasi Turnamen

Integrasi Model:
1. Machine Learning XGBoost (Extreme Gradient Boosting):
   - Klasifikasi Probabilitas Tiga Arah (Win A, Draw, Win B) berbasis fitur makro & mikro
   - Regresi Selisih Gol Terproyeksi
   - Pembobotan Fitur: Elo Rating, Kualitas Skuad, TPI, Iklim/Tuan Rumah, Skor Clutch, & Pengali Keberuntungan
2. 100.000 Iterasi Simulasi Turnamen Monte Carlo:
   - Pemilihan acak stokastik berbasis matriks probabilitas XGBoost
   - Simulasi lengkap: Babak Fase Grup (A s/d F) -> Babak 16 Besar -> Babak 8 Besar -> Semifinal -> Final
   - Berkas Keluaran: data/asian_cup_predictions.csv
"""

import os
import sys
import time
import json
import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Konfigurasi Direktori Dasar
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

from src.models.weighted_poisson_xgboost_model import get_xgb_model

CSV_OUTPUT_PATH = os.path.join(BASE_DIR, "data", "asian_cup_predictions.csv")
MICRO_DATA_PATH = os.path.join(BASE_DIR, "data", "all_24_teams_squad_micro_analytics.json")

print("=" * 75)
print("🚀 MEMULAI PIPELINE PREDIKSI ENSEMBLE: XGBOOST DIPADUKAN MONTE CARLO (100K ITERASI)")
print("=" * 75)

# ------------------------------------------------------------------------------
# LANGKAH 1: INISIALISASI DATA 24 TIM PESERTA (GRUP A s/d F)
# ------------------------------------------------------------------------------
print("\n[LANGKAH 1] Inisialisasi Dataset 24 Tim Peserta & Parameter Fitur Dasar...")

teams_data = [
    # Grup A (Arab Saudi, Kuwait, Oman, Palestina)
    {
        "team": "Saudi Arabia", "code": "KSA", "group": "A",
        "elo": 1495, "squad_val_eur": 36_000_000, "top5_league_players": 0,
        "is_host": True, "dist_km": 0, "home_jan_temp_c": 21.5
    },
    {
        "team": "Oman", "code": "OMA", "group": "A",
        "elo": 1345, "squad_val_eur": 8_500_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 1100, "home_jan_temp_c": 24.5
    },
    {
        "team": "Palestine", "code": "PLE", "group": "A",
        "elo": 1245, "squad_val_eur": 7_500_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 1350, "home_jan_temp_c": 13.0
    },
    {
        "team": "Kuwait", "code": "KUW", "group": "A",
        "elo": 1165, "squad_val_eur": 5_500_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 550, "home_jan_temp_c": 18.0
    },

    # Grup B (Uzbekistan, Bahrain, Korea Utara, Yordania)
    {
        "team": "Uzbekistan", "code": "UZB", "group": "B",
        "elo": 1450, "squad_val_eur": 38_000_000, "top5_league_players": 2,
        "is_host": False, "dist_km": 2800, "home_jan_temp_c": 3.0
    },
    {
        "team": "Jordan", "code": "JOR", "group": "B",
        "elo": 1395, "squad_val_eur": 17_000_000, "top5_league_players": 1,
        "is_host": False, "dist_km": 1300, "home_jan_temp_c": 12.0
    },
    {
        "team": "Bahrain", "code": "BHR", "group": "B",
        "elo": 1335, "squad_val_eur": 9_200_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 450, "home_jan_temp_c": 20.0
    },
    {
        "team": "North Korea", "code": "PRK", "group": "B",
        "elo": 1172, "squad_val_eur": 5_200_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 7600, "home_jan_temp_c": -4.0
    },

    # Grup C (Iran, Suriah, Kirgizstan, China)
    {
        "team": "Iran", "code": "IRN", "group": "C",
        "elo": 1625, "squad_val_eur": 52_000_000, "top5_league_players": 4,
        "is_host": False, "dist_km": 1300, "home_jan_temp_c": 8.0
    },
    {
        "team": "China PR", "code": "CHN", "group": "C",
        "elo": 1265, "squad_val_eur": 11_500_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 6800, "home_jan_temp_c": 2.0
    },
    {
        "team": "Syria", "code": "SYR", "group": "C",
        "elo": 1255, "squad_val_eur": 9_000_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 1400, "home_jan_temp_c": 11.0
    },
    {
        "team": "Kyrgyzstan", "code": "KGZ", "group": "C",
        "elo": 1215, "squad_val_eur": 6_400_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 3300, "home_jan_temp_c": -2.0
    },

    # Grup D (Australia, Tajikistan, Irak, Singapura)
    {
        "team": "Australia", "code": "AUS", "group": "D",
        "elo": 1570, "squad_val_eur": 43_000_000, "top5_league_players": 3,
        "is_host": False, "dist_km": 12200, "home_jan_temp_c": 28.0
    },
    {
        "team": "Iraq", "code": "IRQ", "group": "D",
        "elo": 1455, "squad_val_eur": 16_000_000, "top5_league_players": 1,
        "is_host": False, "dist_km": 950, "home_jan_temp_c": 15.0
    },
    {
        "team": "Tajikistan", "code": "TJK", "group": "D",
        "elo": 1225, "squad_val_eur": 7_200_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 2900, "home_jan_temp_c": 4.0
    },
    {
        "team": "Singapore", "code": "SGP", "group": "D",
        "elo": 1040, "squad_val_eur": 3_800_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 7000, "home_jan_temp_c": 28.0
    },

    # Grup E (Korea Selatan, Uni Emirat Arab, Vietnam, Yaman)
    {
        "team": "South Korea", "code": "KOR", "group": "E",
        "elo": 1595, "squad_val_eur": 182_000_000, "top5_league_players": 9,
        "is_host": False, "dist_km": 7500, "home_jan_temp_c": -1.0
    },
    {
        "team": "United Arab Emirates", "code": "UAE", "group": "E",
        "elo": 1385, "squad_val_eur": 31_000_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 800, "home_jan_temp_c": 23.5
    },
    {
        "team": "Vietnam", "code": "VIE", "group": "E",
        "elo": 1185, "squad_val_eur": 6_100_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 6300, "home_jan_temp_c": 22.0
    },
    {
        "team": "Yemen", "code": "YEM", "group": "E",
        "elo": 1075, "squad_val_eur": 2_500_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 1100, "home_jan_temp_c": 24.0
    },

    # Grup F (Jepang, Qatar, Thailand, Indonesia)
    {
        "team": "Japan", "code": "JPN", "group": "F",
        "elo": 1655, "squad_val_eur": 285_000_000, "top5_league_players": 17,
        "is_host": False, "dist_km": 8700, "home_jan_temp_c": 5.5
    },
    {
        "team": "Qatar", "code": "QAT", "group": "F",
        "elo": 1520, "squad_val_eur": 21_000_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 500, "home_jan_temp_c": 21.5
    },
    {
        "team": "Indonesia", "code": "IDN", "group": "F",
        "elo": 1235, "squad_val_eur": 36_500_000, "top5_league_players": 2,
        "is_host": False, "dist_km": 7300, "home_jan_temp_c": 28.5
    },
    {
        "team": "Thailand", "code": "THA", "group": "F",
        "elo": 1230, "squad_val_eur": 10_200_000, "top5_league_players": 0,
        "is_host": False, "dist_km": 5700, "home_jan_temp_c": 28.0
    }
]

df = pd.DataFrame(teams_data)

# Integrasi Atribut Mikro Pemain Kunci dari Berkas JSON
micro_clutch_map = {}
micro_luck_map = {}
if os.path.exists(MICRO_DATA_PATH):
    with open(MICRO_DATA_PATH, "r", encoding="utf-8") as f:
        micro_json = json.load(f)
    teams_micro = micro_json.get("teams", {})
    for t_name, t_info in teams_micro.items():
        kps = t_info.get("key_micro_players", [])
        if kps:
            micro_clutch_map[t_name] = max([p.get("clutch_score", 75) for p in kps])
            micro_luck_map[t_name] = max([p.get("micro_luck_multiplier", 1.10) for p in kps])

df["clutch_score"] = df["team"].map(lambda t: micro_clutch_map.get(t, 75))
df["luck_multiplier"] = df["team"].map(lambda t: micro_luck_map.get(t, 1.10))

# ------------------------------------------------------------------------------
# LANGKAH 2: PERHITUNGAN TEAM POWER INDEX (TPI)
# ------------------------------------------------------------------------------
print("[LANGKAH 2] Menghitung Rekayasa Fitur & Indeks Kekuatan Tim (TPI)...")

# 1. Normalisasi Elo Rating (Bobot: 40%)
min_elo, max_elo = df["elo"].min(), df["elo"].max()
df["f_elo"] = (df["elo"] - min_elo) / (max_elo - min_elo)

# 2. Normalisasi Skuad (Bobot: 30%)
df["log_squad_val"] = np.log(df["squad_val_eur"])
min_log, max_log = df["log_squad_val"].min(), df["log_squad_val"].max()
df["norm_log_squad_val"] = (df["log_squad_val"] - min_log) / (max_log - min_log)
df["norm_top5"] = df["top5_league_players"] / df["top5_league_players"].max()
df["f_squad"] = 0.70 * df["norm_log_squad_val"] + 0.30 * df["norm_top5"]

# 3. Tuan Rumah & Proksimitas Geografis (Bobot: 10%)
max_dist = df["dist_km"].max()
df["f_proximity"] = 1.0 - (df["dist_km"] / max_dist)
df["f_host_geo"] = np.where(df["is_host"], 1.0, 0.40 * df["f_proximity"])

# 4. Ketahanan Iklim (Bobot: 10%)
host_temp = 21.5
df["temp_diff"] = np.abs(df["home_jan_temp_c"] - host_temp)
df["f_climate"] = 1.0 - (df["temp_diff"] / df["temp_diff"].max())

# 5. Nilai Base TPI (Skala 1.5 - 9.0)
raw_tpi = (
    0.40 * df["f_elo"] +
    0.30 * df["f_squad"] +
    0.10 * df["f_host_geo"] +
    0.10 * df["f_climate"]
)
df["Base_TPI"] = np.round(1.5 + (raw_tpi - raw_tpi.min()) / (raw_tpi.max() - raw_tpi.min()) * 7.5, 2)

# ------------------------------------------------------------------------------
# LANGKAH 3: MEMPELAJARI POLA DENGAN MACHINE LEARNING XGBOOST
# ------------------------------------------------------------------------------
print("\n[LANGKAH 3] Melatih Model Machine Learning XGBoost & Menghitung Matriks Prediksi...")
xgb_model = get_xgb_model()
print("Bobot Kepentingan Fitur XGBoost:")
for feat, imp in xgb_model.get_feature_importances().items():
    print(f"  - {feat:<16}: {imp:5.2f}%")

n_teams = len(df)
team_names = df["team"].tolist()
team_to_idx = {name: i for i, name in enumerate(team_names)}

# Matriks Probabilitas Hasil Pertandingan XGBoost Pairwise (24 x 24)
pairwise_p_win_a = np.zeros((n_teams, n_teams), dtype=np.float32)
pairwise_p_draw = np.zeros((n_teams, n_teams), dtype=np.float32)
pairwise_p_win_b = np.zeros((n_teams, n_teams), dtype=np.float32)
pairwise_p_ko_a = np.zeros((n_teams, n_teams), dtype=np.float32)

for i in range(n_teams):
    for j in range(n_teams):
        if i == j:
            continue
        row_a = df.iloc[i]
        row_b = df.iloc[j]

        feat_dict = {
            "tpi_diff": float(row_a["Base_TPI"] - row_b["Base_TPI"]),
            "elo_diff": float(row_a["elo"] - row_b["elo"]),
            "log_squad_diff": float(row_a["log_squad_val"] - row_b["log_squad_val"]),
            "top5_diff": float(row_a["top5_league_players"] - row_b["top5_league_players"]),
            "host_diff": 0.50 if row_a["is_host"] else (-0.50 if row_b["is_host"] else 0.0),
            "climate_diff": float(row_a["f_climate"] - row_b["f_climate"]),
            "clutch_diff": float(row_a["clutch_score"] - row_b["clutch_score"]),
            "luck_mult_diff": float(row_a["luck_multiplier"] - row_b["luck_multiplier"]),
        }

        preds = xgb_model.predict_match_proba(feat_dict)
        p_w_a = preds["p_win_a"]
        p_dr = preds["p_draw"]
        p_w_b = preds["p_win_b"]

        pairwise_p_win_a[i, j] = p_w_a
        pairwise_p_draw[i, j] = p_dr
        pairwise_p_win_b[i, j] = p_w_b

        # Di babak gugur (Knockout), hasil imbang diselesaikan lewat Extra Time & Adu Penalti
        # Dipengaruhi oleh skor Clutch dan Pengali Keberuntungan pemain kunci
        clutch_delta = row_a["clutch_score"] - row_b["clutch_score"]
        luck_delta = row_a["luck_multiplier"] - row_b["luck_multiplier"]
        p_et_pk_a = 1.0 / (1.0 + np.exp(-0.045 * clutch_delta - 1.25 * luck_delta))
        pairwise_p_ko_a[i, j] = p_w_a + (p_dr * p_et_pk_a)

# ------------------------------------------------------------------------------
# LANGKAH 4: SIMULASI MONTE CARLO 100.000 ITERASI TURNAMEN
# ------------------------------------------------------------------------------
N_SIMULATIONS = 100000
BATCH_SIZE = 10000
n_batches = N_SIMULATIONS // BATCH_SIZE

print(f"\n[LANGKAH 4] Menjalankan 100.000 Iterasi Simulasi Monte Carlo Berbasis XGBoost...")

groups_dict = {}
for g in ["A", "B", "C", "D", "E", "F"]:
    groups_dict[g] = [team_to_idx[t] for t in df[df["group"] == g]["team"].tolist()]

group_matches = []
for g, g_teams in groups_dict.items():
    g_m = [
        (g_teams[0], g_teams[1]),
        (g_teams[2], g_teams[3]),
        (g_teams[0], g_teams[2]),
        (g_teams[1], g_teams[3]),
        (g_teams[0], g_teams[3]),
        (g_teams[1], g_teams[2]),
    ]
    group_matches.append(g_m)

exit_group_count = np.zeros(n_teams, dtype=np.int32)
reach_r16_count = np.zeros(n_teams, dtype=np.int32)
reach_qf_count = np.zeros(n_teams, dtype=np.int32)
reach_semi_count = np.zeros(n_teams, dtype=np.int32)
reach_final_count = np.zeros(n_teams, dtype=np.int32)
win_tourn_count = np.zeros(n_teams, dtype=np.int32)

np.random.seed(42)
start_time = time.time()

for b in range(n_batches):
    batch_points = np.zeros((BATCH_SIZE, n_teams), dtype=np.float32)
    batch_goal_diff = np.zeros((BATCH_SIZE, n_teams), dtype=np.float32)

    # 1. PERTANDINGAN FASE GRUP
    for g_idx, g_m in enumerate(group_matches):
        for (t_a, t_b) in g_m:
            p_w_a = pairwise_p_win_a[t_a, t_b]
            p_dr = pairwise_p_draw[t_a, t_b]

            u = np.random.rand(BATCH_SIZE)
            win_a = u < p_w_a
            draw = (u >= p_w_a) & (u < (p_w_a + p_dr))
            win_b = u >= (p_w_a + p_dr)

            batch_points[:, t_a] += win_a * 3.0 + draw * 1.0
            batch_points[:, t_b] += win_b * 3.0 + draw * 1.0

            # Selisih gol acak terproyeksi
            gd_sample = np.where(win_a, 1.4, np.where(win_b, -1.4, 0.0))
            batch_goal_diff[:, t_a] += gd_sample
            batch_goal_diff[:, t_b] -= gd_sample

    # 2. PENENTUAN TIM LOLOS DARI FASE GRUP
    r16_qualifiers = np.zeros((BATCH_SIZE, 16), dtype=np.int32)
    group_3rds = np.zeros((BATCH_SIZE, 6), dtype=np.int32)
    group_3rd_scores = np.zeros((BATCH_SIZE, 6), dtype=np.float32)

    qual_idx = 0
    for g_idx, (g_name, g_teams) in enumerate(groups_dict.items()):
        # Skor penentu urutan grup: Poin grup + selisih gol tipis
        g_scores = batch_points[:, g_teams] + 0.01 * batch_goal_diff[:, g_teams]
        order = np.argsort(-g_scores, axis=1)

        first_place = np.array(g_teams)[order[:, 0]]
        second_place = np.array(g_teams)[order[:, 1]]
        third_place = np.array(g_teams)[order[:, 2]]

        r16_qualifiers[:, qual_idx] = first_place
        r16_qualifiers[:, qual_idx + 1] = second_place
        qual_idx += 2

        group_3rds[:, g_idx] = third_place
        group_3rd_scores[:, g_idx] = np.take_along_axis(g_scores, order[:, 2:3], axis=1).squeeze(1)

    # 4 Tim Peringkat Ketiga Terbaik
    order_3rds = np.argsort(-group_3rd_scores, axis=1)
    for i in range(4):
        best_3rd = np.take_along_axis(group_3rds, order_3rds[:, i:i+1], axis=1).squeeze(1)
        r16_qualifiers[:, 12 + i] = best_3rd

    for sim_i in range(BATCH_SIZE):
        qual_set = set(r16_qualifiers[sim_i])
        for t in qual_set:
            reach_r16_count[t] += 1
        for t_idx in range(n_teams):
            if t_idx not in qual_set:
                exit_group_count[t_idx] += 1

    # 3. SIMULASI BABAK GUGUR BERBASIS XGBOOST
    def simulate_ko_pairs(team_a_arr, team_b_arr):
        """Menentukan pemenang babak gugur menggunakan probabilitas pairwise XGBoost."""
        p_win_arr = pairwise_p_ko_a[team_a_arr, team_b_arr]
        u = np.random.rand(BATCH_SIZE)
        return np.where(u < p_win_arr, team_a_arr, team_b_arr)

    # Bagan Resmi 16 Besar AFC Asian Cup
    # Laga 1: 2A vs 2C
    # Laga 2: 1D vs 3rd_1
    # Laga 3: 1B vs 3rd_2
    # Laga 4: 1F vs 2E
    # Laga 5: 1C vs 3rd_3
    # Laga 6: 1E vs 2D
    # Laga 7: 1A vs 3rd_4
    # Laga 8: 2B vs 2F (Runner-up B vs Runner-up F)
    m1_win = simulate_ko_pairs(r16_qualifiers[:, 1], r16_qualifiers[:, 5])
    m2_win = simulate_ko_pairs(r16_qualifiers[:, 6], r16_qualifiers[:, 12])
    m3_win = simulate_ko_pairs(r16_qualifiers[:, 2], r16_qualifiers[:, 13])
    m4_win = simulate_ko_pairs(r16_qualifiers[:, 10], r16_qualifiers[:, 9])
    m5_win = simulate_ko_pairs(r16_qualifiers[:, 4], r16_qualifiers[:, 14])
    m6_win = simulate_ko_pairs(r16_qualifiers[:, 8], r16_qualifiers[:, 7])
    m7_win = simulate_ko_pairs(r16_qualifiers[:, 0], r16_qualifiers[:, 15])
    m8_win = simulate_ko_pairs(r16_qualifiers[:, 3], r16_qualifiers[:, 11])

    # Perempat Final (Babak 8 Besar)
    qf_winners = [m1_win, m2_win, m3_win, m4_win, m5_win, m6_win, m7_win, m8_win]
    for sim_i in range(BATCH_SIZE):
        for q_team in qf_winners:
            reach_qf_count[q_team[sim_i]] += 1

    # Semifinal (Babak 4 Besar)
    qf1_win = simulate_ko_pairs(m1_win, m2_win)
    qf2_win = simulate_ko_pairs(m3_win, m4_win)
    qf3_win = simulate_ko_pairs(m5_win, m6_win)
    qf4_win = simulate_ko_pairs(m7_win, m8_win)

    sf_winners = [qf1_win, qf2_win, qf3_win, qf4_win]
    for sim_i in range(BATCH_SIZE):
        for s_team in sf_winners:
            reach_semi_count[s_team[sim_i]] += 1

    # Final (Babak 2 Besar)
    f1_win = simulate_ko_pairs(qf1_win, qf2_win)
    f2_win = simulate_ko_pairs(qf3_win, qf4_win)

    final_winners = [f1_win, f2_win]
    for sim_i in range(BATCH_SIZE):
        for f_team in final_winners:
            reach_final_count[f_team[sim_i]] += 1

    # Juara Turnamen
    champ = simulate_ko_pairs(f1_win, f2_win)
    for sim_i in range(BATCH_SIZE):
        win_tourn_count[champ[sim_i]] += 1

sim_duration = time.time() - start_time
print(f"[BERHASIL] 100.000 Iterasi Simulasi XGBoost + Monte Carlo Selesai dalam {sim_duration:.2f} detik!")

# ------------------------------------------------------------------------------
# LANGKAH 5: MENULIS DAN MENYIMPAN HASIL PREDIKSI KE CSV
# ------------------------------------------------------------------------------
results_df = pd.DataFrame({
    "Team": df["team"],
    "Group": df["group"],
    "Base_TPI": df["Base_TPI"],
    "Group_Stage_Exit_Prob(%)": np.round((exit_group_count / N_SIMULATIONS) * 100, 2),
    "Reach_Round_16_Prob(%)": np.round((reach_r16_count / N_SIMULATIONS) * 100, 2),
    "Reach_Quarter_Final_Prob(%)": np.round((reach_qf_count / N_SIMULATIONS) * 100, 2),
    "Reach_Semi_Final_Prob(%)": np.round((reach_semi_count / N_SIMULATIONS) * 100, 2),
    "Reach_Final_Prob(%)": np.round((reach_final_count / N_SIMULATIONS) * 100, 2),
    "Win_Tournament_Prob(%)": np.round((win_tourn_count / N_SIMULATIONS) * 100, 2),
})

results_df = results_df.sort_values(by="Win_Tournament_Prob(%)", ascending=False).reset_index(drop=True)
results_df.insert(0, "Rank", range(1, n_teams + 1))

os.makedirs(os.path.dirname(CSV_OUTPUT_PATH), exist_ok=True)
results_df.to_csv(CSV_OUTPUT_PATH, index=False)
print(f"\n[EKSPOR SUKSES] Berkas hasil tersimpan di: {CSV_OUTPUT_PATH}\n")
print(results_df.to_string(index=False))
