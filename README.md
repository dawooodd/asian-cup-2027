# ⚽ AFC Asian Cup 2027: Quantitative Intelligence & Tournament Simulation Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.20%2B-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0%2B-EB5424.svg)](https://xgboost.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](#)

A production-grade sports data engineering and quantitative modeling repository designed to forecast outcomes for the **AFC Asian Cup Saudi Arabia 2027**. 

The platform integrates a **Five-Pillar Team Power Index (TPI)**, **Bivariate Poisson-XGBoost Residual Ensembles**, **100,000 Monte Carlo Tournament Simulations**, and a modern, high-impact **Multipage Streamlit Dashboard**.

---

## 📑 Table of Contents
1. [Executive Summary](#-executive-summary)
2. [Modular Repository Architecture](#-modular-repository-architecture)
3. [Mathematical Methodology & Modeling Framework](#-mathematical-methodology--modeling-framework)
4. [Streamlit Multipage Dashboard](#-streamlit-multipage-dashboard)
5. [Key Tournament Forecasts & Insights](#-key-tournament-forecasts--insights)
6. [Getting Started & Installation](#-getting-started--installation)
7. [Running Simulations & Pipeline Scripts](#-running-simulations--pipeline-scripts)
8. [Automated Quality Audit & Verification](#-automated-quality-audit--verification)
9. [Technology Stack](#-technology-stack)

---

## 🌟 Executive Summary

Predicting international cup tournaments requires capturing both long-term team strength and extreme single-match variance. This project provides:
- **Comprehensive 24-Nation Power Indexing**: Combining 4-year Elo ratings, European top-flight squad values, geographic proximity, and Gulf climate adaptation.
- **Micro-Tactical Telemetry**: An exhaustive 1,600+ line dataset analyzing the 120-minute FIFA ASEAN Cup 2026 Final (Indonesia vs Thailand), including substitution impact timestamps and minute-by-minute cumulative expected goals (xG).
- **Interactive Simulation Engine**: Real-time fixture simulation allowing sports analysts to test custom stochastic variance ("luck factor") scenarios.

---

## 🏗️ Modular Repository Architecture

The project adheres to GitHub open-source and data engineering best practices:

```text
asian-cup-2027/
│
├── data/                                      # Structured Data Lake
│   ├── asian_cup_predictions.csv              # 100,000 Monte Carlo tournament simulation outputs
│   ├── indonesia_vs_thailand_analytics.json   # 120-min match telemetry (Schemas A, B, and C)
│   └── model_prediction_output.json          # Pre-calibrated Bivariate Poisson matrix
│
├── src/                                       # Core Python Source Code
│   ├── data_pipeline/
│   │   ├── __init__.py
│   │   └── build_sports_data.py               # Data ingestion, schemas, and telemetry builder
│   ├── models/
│   │   ├── __init__.py
│   │   └── weighted_poisson_xgboost_model.py  # Poisson model + XGBoost residual adjustments
│   ├── simulation/
│   │   ├── __init__.py
│   │   ├── run_asian_cup_simulation.py        # 100,000 Monte Carlo tournament bracket runner
│   │   └── benchmark_sim.py                   # Vectorized simulation benchmark utility
│   └── legacy_viz/
│       ├── match_viz_generator.py             # Static Matplotlib/Seaborn match generator (archived)
│       └── plot_tournament_predictions.py     # Static Matplotlib tournament chart generator (archived)
│
├── app/                                       # Streamlit Web Application
│   ├── __init__.py
│   ├── main.py                                # Application landing page & methodology center
│   ├── pages/                                 # Multipage navigation views
│   │   ├── 1_🏆_Tournament_Outright.py        # 24-team probabilities, charts, and anomaly filters
│   │   ├── 2_⚔️_H2H_Deep_Dive.py              # IDN vs THA 120-min telemetry, radar & xG timeline
│   │   └── 3_🧮_Match_Simulator.py            # Real-time Poisson fixture simulation engine
│   └── utils/
│       ├── __init__.py
│       ├── charts.py                          # Reusable interactive Plotly charts module
│       └── styles.py                          # Bespoke CSS, glassmorphism cards & design tokens
│
├── notebooks/                                 # Exploratory Data Science
│   └── match_analysis.ipynb                   # Jupyter notebook for exploratory telemetry analysis
│
├── viz_outputs/                               # High-Resolution Static Visual Exports
│   ├── asian_cup_2027_tournament_predictions.png
│   ├── task1_match_statistics_radar.png
│   ├── task2_player_rating_heatmap.png
│   ├── task3_substitution_impact_timeline.png
│   └── task4_win_probability_donut.png
│
├── .gitignore                                 # Production ignore rules (venv, cache, checkpoints)
└── requirements.txt                           # Pinned dependencies
```

---

## 🔬 Mathematical Methodology & Modeling Framework

### 1. Five-Pillar Team Power Index (TPI)
Each qualified nation is ranked using a composite index:

$$\text{TPI}_i = 0.40 \cdot \text{ELO}_i + 0.30 \cdot \ln(\text{SquadValue}_i) + 0.10 \cdot \text{Host}_i + 0.10 \cdot \text{Climate}_i + 0.10 \cdot \text{Luck}_i$$

| Pillar | Weight | Description | Metric Specification |
| :--- | :---: | :--- | :--- |
| **Historical Elo** | **40%** | 4-year FIFA/AFC match history | Elo system adjusted for margin of victory and opponent strength |
| **Squad Value & Pedigree** | **30%** | Transfermarkt squad market value | Log-transformed Euro valuation + Top-5 European league player tally |
| **Host / Proximity** | **10%** | Home and travel advantage | Binary bonus for Saudi Arabia + inverted flight travel distance |
| **Climate Adaptability** | **10%** | High heat and low humidity resilience | Historical performance index in Gulf desert climate conditions |
| **Tournament Stochastic Variance** | **10%** | Knockout unpredictability | Gaussian white noise $\mathcal{N}(0, \sigma^2)$ simulating referee variance, injuries, and penalty shootouts |

### 2. Weighted Poisson-XGBoost Ensemble
Match scorelines are calculated via a **Bivariate Poisson Distribution**:

$$P(X = x, Y = y) = \frac{\lambda_A^x e^{-\lambda_A}}{x!} \times \frac{\lambda_B^y e^{-\lambda_B}}{y!}$$

Where $\lambda_A$ and $\lambda_B$ represent attack rates derived from the TPI delta:
$$\lambda_A = 1.30 \cdot \exp(0.16 \cdot (\text{TPI}_A - \text{TPI}_B + \epsilon_{\text{luck}}))$$
$$\lambda_B = 1.30 \cdot \exp(-0.16 \cdot (\text{TPI}_A - \text{TPI}_B + \epsilon_{\text{luck}}))$$

An **XGBoost Residual Classifier** recalibrates the raw Poisson matrix to account for:
- International tournament draw tendencies in tight knockout games.
- Player fatigue decay curves over 90 and 120 minutes.
- Second-half tactical substitution impacts.

### 3. 100,000 Monte Carlo Tournament Simulations
The simulator processes all 24 qualified teams across 6 groups of 4:
1. **Group Stage**: Round-robin format (3 matches per team); top 2 teams per group + 4 best 3rd-placed teams advance (16 teams).
2. **Knockout Stage**: Round of 16 $\rightarrow$ Quarter-Finals $\rightarrow$ Semi-Finals $\rightarrow$ Final.
3. Every knockout deadlock triggers extra-time and penalty shootout weighting.

---

## 🖥️ Streamlit Multipage Dashboard

The web dashboard is designed with dark-mode sports science aesthetics:

### 1. Main Landing Hub (`app/main.py`)
- Hero section detailing the scientific simulation methodology.
- Executive KPI cards: Total Teams (24), Iterations (100K), Host (Saudi Arabia), Top Contenders.
- Modular navigation cards and architectural documentation.

### 2. 🏆 Tournament Outright (`app/pages/1_🏆_Tournament_Outright.py`)
- **Interactive Plotly Horizontal Bar**: Top 10 nations sorted by championship probability.
- **TPI vs Knockout Bubble Scatter**: Evaluates overachieving underdogs vs underperforming heavyweights.
- **Anomaly Detection Engine**:
  - *Indonesia Diaspora Anomaly*: Highlights Indonesia's **12.48% Semifinal probability** and **2.70% Final odds** despite a Base TPI of 4.01.
  - *Gulf Synergy*: Identifies Saudi Arabia (8.82%) and Qatar (9.33%) tournament boosts due to climate adaptation.
- **Filterable Data Table**: Search by nation, filter by minimum progression odds, and export filtered data to CSV.

### 3. ⚔️ H2H Deep Dive (`app/pages/2_⚔️_H2H_Deep_Dive.py`)
- Tactical autopsy of **Indonesia 2-2 Thailand (4-2 on Penalties, AET)** in the FIFA ASEAN Cup 2026 Final.
- **Spider Radar Plot**: Compares Possession (58.4% vs 41.6%), xG (2.14 vs 1.38), Tackles Won % (72.0% vs 70.9%), Pass Accuracy (83.9% vs 77.0%), and Shots on Target (7 vs 4).
- **Interactive xG & Substitution Timeline**: Minute-by-minute cumulative xG trajectory showing exact substitution entry points (46' Dean James, 60' Rizky Ridho, 79' Sanron, 116' Elkan Baggott goal).
- **Player Rating Tables**: Starters and substitutes ranked on a 1.0 - 10.0 scale.

### 4. 🧮 Match Simulator (`app/pages/3_🧮_Match_Simulator.py`)
- Select any two teams from the 24 qualified nations.
- Interactive slider to inject **Stochastic Luck Factor** ($-0.50$ to $+0.50$).
- Real-time output:
  - 3D-styled Plotly Donut Chart of Win/Draw/Loss probabilities.
  - Projected Expected Goals ($\text{xG}$) per squad.
  - Most likely full-time scoreline (e.g., `1-1` or `2-1`).
  - Bar chart showing the Top 6 scoreline probabilities.
  - Automated tactical narrative projection based on team power differential.

---

## 📊 Key Tournament Forecasts & Insights

Simulated across 100,000 full tournament brackets:

| Rank | Team | Base TPI | Group Exit % | Reaching Semis % | Reaching Final % | **Win Tournament %** |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **1** | 🇯🇵 **Japan** | **9.00** | 0.05% | 68.09% | 47.98% | **39.17%** |
| **2** | 🇰🇷 **South Korea** | **7.57** | 0.08% | 51.51% | 21.34% | **14.53%** |
| **3** | 🇮🇷 **Iran** | **7.42** | 0.35% | 42.24% | 17.27% | **11.24%** |
| **4** | 🇦🇺 **Australia** | **6.73** | 0.38% | 43.27% | 33.22% | **11.05%** |
| **5** | 🇶🇦 **Qatar** | **6.43** | 0.71% | 42.08% | 31.20% | **9.33%** |
| **6** | 🇸🇦 **Saudi Arabia** | **7.20** | 0.74% | 28.63% | 14.29% | **8.82%** |
| **7** | 🇺🇿 **Uzbekistan** | **5.45** | 2.04% | 18.01% | 10.12% | **1.99%** |
| **8** | 🇮🇶 **Iraq** | **5.52** | 4.72% | 10.85% | 3.81% | **1.03%** |
| **9** | 🇦🇪 **UAE** | **5.46** | 4.63% | 13.40% | 3.89% | **1.00%** |
| **10** | 🇯🇴 **Jordan** | **4.93** | 12.52% | 11.69% | 3.52% | **0.63%** |
| **11** | 🇧🇭 **Bahrain** | **4.41** | 10.20% | 10.56% | 3.84% | **0.45%** |
| **12** | 🇮🇩 **Indonesia** | **4.01** | 32.26% | **12.48%** | **2.70%** | **0.26%** |
| **13** | 🇴🇲 **Oman** | **4.36** | 7.29% | 8.63% | 1.84% | **0.24%** |
| **14** | 🇵🇸 **Palestine** | **3.23** | 26.83% | 8.88% | 1.27% | **0.08%** |
| **15** | 🇸🇾 **Syria** | **3.33** | 48.78% | 7.60% | 1.14% | **0.07%** |
| **16** | 🇹🇭 **Thailand** | **3.22** | 64.70% | 4.52% | 0.65% | **0.04%** |

---

## 🚀 Getting Started & Installation

### Prerequisites
- Python 3.10 or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/dawooodd/asian-cup-2027.git
cd asian-cup-2027
```

### 2. Set Up Virtual Environment
```bash
# On Linux / macOS:
python3 -m venv asiancup_env
source asiancup_env/bin/activate

# On Windows (PowerShell):
python -m venv asiancup_env
.\asiancup_env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Streamlit Dashboard
```bash
streamlit run app/main.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## ⚙️ Running Simulations & Pipeline Scripts

### Run 100,000 Monte Carlo Simulations
To re-run the full tournament bracket simulation and regenerate `data/asian_cup_predictions.csv`:
```bash
python src/simulation/run_asian_cup_simulation.py
```

### Run Simulation Performance Benchmark
```bash
python src/simulation/benchmark_sim.py
```
*(Evaluates 5.1 Million vectorized match outcome evaluations in ~0.15s).*

### Rebuild Historical Sports Telemetry
```bash
python src/data_pipeline/build_sports_data.py
```

---

## 🧪 Automated Quality Audit & Verification

The codebase includes automated verification to ensure zero runtime regressions:

```bash
# Verify headless compilation and rendering of all Streamlit pages
python -c "
from streamlit.testing.v1 import AppTest
for path in ['app/main.py', 'app/pages/1_🏆_Tournament_Outright.py', 'app/pages/2_⚔️_H2H_Deep_Dive.py', 'app/pages/3_🧮_Match_Simulator.py']:
    at = AppTest.from_file(path).run()
    assert not at.exception, f'Failed on {path}: {at.exception}'
print('All Streamlit pages verified: ZERO exceptions!')
"
```

---

## 🛠️ Technology Stack

| Domain | Technologies |
| :--- | :--- |
| **Web Application** | Streamlit (Multipage, wide layout, responsive styling) |
| **Visualization** | Plotly Graph Objects & Plotly Express (Interactive dark theme) |
| **Machine Learning** | XGBoost, Scikit-learn, Scipy Stats (Bivariate Poisson) |
| **Data Processing** | Pandas, NumPy (Vectorized Monte Carlo) |
| **Legacy Visuals** | Matplotlib, Seaborn |
| **Version Control** | Git, Modular GitHub Standard Architecture |

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

© 2026 Sports Science & Quantitative Analytics Division.
