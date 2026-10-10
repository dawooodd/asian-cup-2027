"""
Modul Model Prediksi Ensemble: Weighted Poisson & Machine Learning XGBoost
Engine Kuantitatif Simulasi Pertandingan Sepak Bola AFC Asian Cup 2027

Model ini memadukan dua paradigma sains data olahraga:
1. Distribusi Bivariate Poisson: Menghitung distribusi probabilitas skor eksak (0-0, 1-0, 2-1, dll.)
   berdasarkan laju ekspektasi gol (Expected Goals / lambda).
2. Model Klasifikasi & Regresi XGBoost (Extreme Gradient Boosting):
   Mempelajari pola non-linear dari fitur makro (Elo, nilai pasar, TPI, iklim, tuan rumah)
   dan fitur mikro (faktor clutch pemain kunci, pengali keberuntungan).
"""

import os
import json
import numpy as np
import scipy.stats as stats
import xgboost as xgb

# Direktori proyek
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MICRO_PATH = os.path.join(BASE_DIR, "data", "all_24_teams_squad_micro_analytics.json")


class XGBoostMatchModel:
    """
    Model Machine Learning XGBoost untuk memprediksi probabilitas hasil pertandingan
    (Menang Tim A, Imbang, Menang Tim B) serta estimasi selisih gol.
    """

    def __init__(self):
        self.clf = None
        self.reg = None
        self.feature_names = [
            "tpi_diff",
            "elo_diff",
            "log_squad_diff",
            "top5_diff",
            "host_diff",
            "climate_diff",
            "clutch_diff",
            "luck_mult_diff",
        ]
        self._train_model()

    def _generate_synthetic_training_dataset(self, n_samples: int = 600):
        """
        Membangkitkan data pelatihan realistis berbasis domain sains data sepak bola Asia,
        mencakup variasi selisih kekuatan tim dari laga timpang hingga duel ketat selevel.
        """
        np.random.seed(42)

        # Selisih fitur antar tim
        tpi_diff = np.random.uniform(-5.0, 5.0, n_samples)
        elo_diff = tpi_diff * 75.0 + np.random.normal(0, 40, n_samples)
        log_squad_diff = tpi_diff * 0.70 + np.random.normal(0, 0.35, n_samples)
        top5_diff = np.clip(np.round(tpi_diff * 1.5 + np.random.normal(0, 1.2, n_samples)), -15, 15)
        host_diff = np.random.choice([0.0, 0.4, 0.8, -0.4, -0.8], size=n_samples)
        climate_diff = np.random.uniform(-0.5, 0.5, n_samples)
        clutch_diff = tpi_diff * 3.5 + np.random.normal(0, 4.0, n_samples)
        luck_mult_diff = tpi_diff * 0.04 + np.random.normal(0, 0.05, n_samples)

        X = np.column_stack([
            tpi_diff,
            elo_diff,
            log_squad_diff,
            top5_diff,
            host_diff,
            climate_diff,
            clutch_diff,
            luck_mult_diff,
        ])

        # Penentuan label target berbasis probabilitas logistik dengan varians sepak bola
        latent_strength = (
            0.45 * tpi_diff +
            0.003 * elo_diff +
            0.20 * log_squad_diff +
            0.05 * top5_diff +
            0.15 * host_diff +
            0.08 * climate_diff +
            0.02 * clutch_diff +
            1.20 * luck_mult_diff
        )

        p_draw_base = 0.28 * np.exp(-0.18 * (latent_strength ** 2))
        p_win_a_cond = 1.0 / (1.0 + np.exp(-0.85 * latent_strength))
        p_win_a = (1.0 - p_draw_base) * p_win_a_cond
        p_win_b = np.maximum(0.01, 1.0 - p_draw_base - p_win_a)

        # Normalisasi
        p_total = p_win_a + p_draw_base + p_win_b
        p_win_a /= p_total
        p_draw_base /= p_total
        p_win_b /= p_total

        y_clf = np.zeros(n_samples, dtype=int)
        y_reg = np.zeros(n_samples, dtype=float)

        for i in range(n_samples):
            outcome = np.random.choice([0, 1, 2], p=[p_win_a[i], p_draw_base[i], p_win_b[i]])
            y_clf[i] = outcome
            if outcome == 0:  # Tim A Menang
                y_reg[i] = np.random.choice([1.0, 2.0, 3.0, 4.0], p=[0.55, 0.28, 0.12, 0.05])
            elif outcome == 1:  # Imbang
                y_reg[i] = 0.0
            else:  # Tim B Menang
                y_reg[i] = -np.random.choice([1.0, 2.0, 3.0, 4.0], p=[0.55, 0.28, 0.12, 0.05])

        return X, y_clf, y_reg

    def _train_model(self):
        """Melatih model XGBClassifier dan XGBRegressor."""
        X, y_clf, y_reg = self._generate_synthetic_training_dataset(n_samples=800)

        # 1. Model Klasifikasi Probabilitas (Win A, Draw, Win B)
        self.clf = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=3,
            learning_rate=0.08,
            subsample=0.85,
            colsample_bytree=0.85,
            objective="multi:softprob",
            eval_metric="mlogloss",
            random_state=42,
        )
        self.clf.fit(X, y_clf)

        # 2. Model Regresi Selisih Gol
        self.reg = xgb.XGBRegressor(
            n_estimators=80,
            max_depth=3,
            learning_rate=0.08,
            subsample=0.85,
            colsample_bytree=0.85,
            random_state=42,
        )
        self.reg.fit(X, y_reg)

    def predict_match_proba(self, features_dict: dict) -> dict:
        """
        Memprediksi probabilitas pertandingan menggunakan XGBoost.
        Mengembalikan probabilitas Win A, Draw, dan Win B.
        """
        x_vec = np.array([[
            features_dict.get("tpi_diff", 0.0),
            features_dict.get("elo_diff", 0.0),
            features_dict.get("log_squad_diff", 0.0),
            features_dict.get("top5_diff", 0.0),
            features_dict.get("host_diff", 0.0),
            features_dict.get("climate_diff", 0.0),
            features_dict.get("clutch_diff", 0.0),
            features_dict.get("luck_mult_diff", 0.0),
        ]])

        probs = self.clf.predict_proba(x_vec)[0]  # [p_win_a, p_draw, p_win_b]
        goal_diff = float(self.reg.predict(x_vec)[0])

        return {
            "p_win_a": float(probs[0]),
            "p_draw": float(probs[1]),
            "p_win_b": float(probs[2]),
            "predicted_goal_diff": goal_diff,
        }

    def get_feature_importances(self) -> dict:
        """Mengembalikan tingkat kepentingan fitur dari pohon keputusan XGBoost."""
        importances = self.clf.feature_importances_
        return {name: round(float(imp) * 100, 2) for name, imp in zip(self.feature_names, importances)}


# Model Singleton Instance
_xgb_model_instance = None


def get_xgb_model() -> XGBoostMatchModel:
    global _xgb_model_instance
    if _xgb_model_instance is None:
        _xgb_model_instance = XGBoostMatchModel()
    return _xgb_model_instance


def _load_team_micro_attributes(team_name: str) -> dict:
    """Memuat atribut mikro pemain kunci suatu tim jika tersedia di berkas JSON."""
    if not os.path.exists(MICRO_PATH):
        return {"clutch_score": 75, "luck_multiplier": 1.10}

    try:
        with open(MICRO_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        teams = data.get("teams", {})
        if team_name in teams:
            tinfo = teams[team_name]
            kps = tinfo.get("key_micro_players", [])
            if kps:
                top_clutch = max([p.get("clutch_score", 75) for p in kps])
                top_luck = max([p.get("micro_luck_multiplier", 1.10) for p in kps])
                return {"clutch_score": top_clutch, "luck_multiplier": top_luck}
    except Exception:
        pass
    return {"clutch_score": 75, "luck_multiplier": 1.10}


def predict_match(
    team_a_name: str,
    team_b_name: str,
    tpi_a: float,
    tpi_b: float,
    luck_factor: float = 0.0,
    max_goals: int = 6,
    clutch_a: float = None,
    clutch_b: float = None,
    luck_mult_a: float = None,
    luck_mult_b: float = None
) -> dict:
    """
    Mensimulasikan pertandingan antara Tim A dan Tim B menggunakan model ensemble:
    Bivariate Poisson yang dikalibrasi oleh Machine Learning XGBoost.
    """
    xgb_model = get_xgb_model()

    # Muat atribut mikro jika belum disuplai
    if clutch_a is None or luck_mult_a is None:
        micro_a = _load_team_micro_attributes(team_a_name)
        clutch_a = micro_a["clutch_score"]
        luck_mult_a = micro_a["luck_multiplier"]

    if clutch_b is None or luck_mult_b is None:
        micro_b = _load_team_micro_attributes(team_b_name)
        clutch_b = micro_b["clutch_score"]
        luck_mult_b = micro_b["luck_multiplier"]

    # Selisih TPI dan faktor keberuntungan
    delta_tpi = (tpi_a - tpi_b) + luck_factor
    clutch_delta = float(clutch_a - clutch_b)
    luck_mult_delta = float(luck_mult_a - luck_mult_b) + (luck_factor * 0.1)

    # Susun vektor fitur untuk XGBoost
    features = {
        "tpi_diff": float(delta_tpi),
        "elo_diff": float(delta_tpi * 70.0),
        "log_squad_diff": float(delta_tpi * 0.65),
        "top5_diff": float(np.clip(delta_tpi * 1.2, -10, 10)),
        "host_diff": 0.40 if team_a_name == "Saudi Arabia" else (-0.40 if team_b_name == "Saudi Arabia" else 0.0),
        "climate_diff": 0.0,
        "clutch_diff": clutch_delta,
        "luck_mult_diff": luck_mult_delta,
    }

    # 1. Prediksi Berbasis XGBoost
    xgb_preds = xgb_model.predict_match_proba(features)
    p_win_a_xgb = xgb_preds["p_win_a"]
    p_draw_xgb = xgb_preds["p_draw"]
    p_win_b_xgb = xgb_preds["p_win_b"]
    goal_diff_xgb = xgb_preds["predicted_goal_diff"]

    # 2. Kalibrasi Distribusi Poisson dengan Output XGBoost
    # Rata-rata gol internasional per tim ~1.30 gol/pertandingan
    # Koreksi lambda berbasis selisih gol yang diproyeksikan XGBoost
    lambda_a = max(0.20, 1.28 * np.exp(0.14 * delta_tpi + 0.08 * goal_diff_xgb))
    lambda_b = max(0.20, 1.28 * np.exp(-0.14 * delta_tpi - 0.08 * goal_diff_xgb))

    # Matriks Probabilitas Poisson Eksak
    poisson_matrix = np.zeros((max_goals + 1, max_goals + 1))
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            poisson_matrix[i, j] = stats.poisson.pmf(i, lambda_a) * stats.poisson.pmf(j, lambda_b)

    poisson_matrix /= poisson_matrix.sum()

    # Probabilitas dasar Poisson murni
    p_win_a_poisson = float(np.sum(np.tril(poisson_matrix, -1)))
    p_draw_poisson = float(np.sum(np.diag(poisson_matrix)))
    p_win_b_poisson = float(np.sum(np.triu(poisson_matrix, 1)))

    # 3. Ensemble Berbobot (60% XGBoost ML + 40% Poisson Probability Matrix)
    W_XGB = 0.60
    W_POI = 0.40
    p_win_a_ens = W_XGB * p_win_a_xgb + W_POI * p_win_a_poisson
    p_draw_ens = W_XGB * p_draw_xgb + W_POI * p_draw_poisson
    p_win_b_ens = W_XGB * p_win_b_xgb + W_POI * p_win_b_poisson

    tot_ens = p_win_a_ens + p_draw_ens + p_win_b_ens
    p_win_a = p_win_a_ens / tot_ens
    p_draw = p_draw_ens / tot_ens
    p_win_b = p_win_b_ens / tot_ens

    # Kompilasi distribusi skor terurut
    score_probs = []
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            prob = poisson_matrix[i, j]
            score_probs.append({
                "score": f"{i} - {j}",
                "goals_a": i,
                "goals_b": j,
                "probability_pct": round(float(prob) * 100, 2)
            })

    score_probs.sort(key=lambda x: x["probability_pct"], reverse=True)

    return {
        "team_a": team_a_name,
        "team_b": team_b_name,
        "tpi_a": round(float(tpi_a), 2),
        "tpi_b": round(float(tpi_b), 2),
        "clutch_a": clutch_a,
        "clutch_b": clutch_b,
        "luck_mult_a": round(float(luck_mult_a), 2),
        "luck_mult_b": round(float(luck_mult_b), 2),
        "luck_factor": round(float(luck_factor), 2),
        "projected_xg_a": round(float(lambda_a), 2),
        "projected_xg_b": round(float(lambda_b), 2),
        "win_prob_a": round(p_win_a * 100, 1),
        "draw_prob": round(p_draw * 100, 1),
        "win_prob_b": round(p_win_b * 100, 1),
        "xgboost_pure_win_a": round(p_win_a_xgb * 100, 1),
        "xgboost_pure_draw": round(p_draw_xgb * 100, 1),
        "xgboost_pure_win_b": round(p_win_b_xgb * 100, 1),
        "xgboost_predicted_goal_diff": round(goal_diff_xgb, 2),
        "model_architecture": "Ensemble Bivariate Poisson (40%) + XGBoost Machine Learning (60%)",
        "top_scorelines": score_probs[:6],
        "most_likely_score": score_probs[0]["score"],
        "most_likely_score_prob": score_probs[0]["probability_pct"],
        "feature_importances": xgb_model.get_feature_importances(),
    }


if __name__ == "__main__":
    res = predict_match("Indonesia", "Qatar", 4.26, 6.61, luck_factor=0.0)
    print("=" * 60)
    print("UJI COBA ENSEMBLE WEIGHTED POISSON + XGBOOST MACHINE LEARNING")
    print("=" * 60)
    print(f"Pertandingan: {res['team_a']} vs {res['team_b']}")
    print(f"Model: {res['model_architecture']}")
    print(f"Probabilitas Akhir: {res['team_a']} {res['win_prob_a']}% | Imbang {res['draw_prob']}% | {res['team_b']} {res['win_prob_b']}%")
    print(f"Prediksi XGBoost Murni: {res['xgboost_pure_win_a']}% / {res['xgboost_pure_draw']}% / {res['xgboost_pure_win_b']}%")
    print(f"Proyeksi xG: {res['projected_xg_a']} vs {res['projected_xg_b']}")
    print(f"Skor Paling Mungkin: {res['most_likely_score']} ({res['most_likely_score_prob']}%)")
    print("Kepentingan Fitur XGBoost:", res["feature_importances"])
