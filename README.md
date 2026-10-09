# ⚽ AFC Asian Cup 2027: Platform Prediksi Sains Data & Simulasi Turnamen

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.20%2B-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0%2B-EB5424.svg)](https://xgboost.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](#)

Repositori sains data sepak bola dan pemodelan prediktif kuantitatif untuk memproyeksikan peta kompetisi **Piala Asia (AFC Asian Cup) Arab Saudi 2027**. 

Platform ini menggabungkan **100.000 Iterasi Simulasi Monte Carlo**, **Model Distribusi Bivariate Poisson + Koreksi XGBoost**, **Data Pertandingan 4 Tahun Terakhir (2023–2026)**, serta **Evolusi Nilai Pasar Skuad (€36.5 Juta)** dengan fokus utama: **Membedah Peluang Timnas Indonesia Menembus Babak 8 Besar (Quarter-Finals)** serta memprediksi kelolosan seluruh 24 negara peserta.

---

## 📑 Daftar Isi
1. [Ringkasan Eksekutif: Sejauh Mana Timnas Indonesia Bisa Melangkah?](#-1-ringkasan-eksekutif-sejauh-mana-timnas-indonesia-bisa-melangkah)
2. [Peta Lengkap Probabilitas 24 Negara Peserta](#-2-peta-lengkap-probabilitas-24-negara-peserta)
3. [Bedah Taktis & 3 Skenario Timnas Indonesia Menuju 8 Besar](#-3-bedah-taktis--3-skenario-timnas-indonesia-menuju-8-besar)
4. [Edukasi Sains Data bagi Orang Awam: Cara Kerja Model Prediksi](#-4-edukasi-sains-data-bagi-orang-awam-cara-kerja-model-prediksi)
5. [Evolusi Kualitas Skuad & Rekor 20 Laga 4 Tahun Terakhir (2023–2026)](#-5-evolusi-kualitas-skuad--rekor-20-laga-4-tahun-terakhir-20232026)
6. [Arsitektur Direktori Repositori](#-6-arsitektur-direktori-repositori)
7. [Panduan Instalasi & Menjalankan Dashboard Streamlit](#-7-panduan-instalasi--menjalankan-dashboard-streamlit)
8. [Uji Kualitas & Verifikasi Otomatis](#-8-uji-kualitas--verifikasi-otomatis)

---

## 🇮🇩 1. Ringkasan Eksekutif: Sejauh Mana Timnas Indonesia Bisa Melangkah?

Berdasarkan hasil komputasi **100.000 simulasi braket turnamen penuh** menggunakan data performa 4 tahun terakhir:

| Tahapan Turnamen | Peluang Timnas Indonesia (%) | Makna Praktis bagi Suporter & Publik |
| :--- | :---: | :--- |
| **Lolos Fase Grup (16 Besar)** | **67.74%** | **Sangat Terbuka Lebar.** Dalam 2 dari 3 skenario simulasi, Indonesia berhasil lolos dari Grup A (baik via Runner-up maupun Peringkat 3 Terbaik). |
| **Lolos Babak 8 Besar (Quarter-Final)** | **16.18% (Agregat)<br>s/d 42.50% (via Runner-up)** | **Target Paling Realistis.** Jika Indonesia mengunci posisi Runner-up Grup A, peluang menembus 8 Besar melonjak menjadi **42.5%** karena terhindar dari juara grup unggulan. |
| **Lolos Semifinal (4 Besar)** | **4.11%** | **Pencapaian Luar Biasa.** Membutuhkan kemenangan atas raksasa Asia di perempat final. |
| **Lolos ke Final** | **0.65%** | **Kejutan Bersejarah Asia.** Skenario di mana Indonesia menumbangkan 2 tim raksasa Pot 1 berturut-turut. |
| **Juara Piala Asia 2027** | **0.07%** | Peluang juara ada secara matematis (~70 kali dari 100.000 turnamen simulasi). |

> **Kesimpulan Utama:** Target ilmiah paling rasional dan dapat dicapai bagi Timnas Indonesia di Piala Asia 2027 adalah **menembus Babak 8 Besar (Quarter-Finals)**, mencatatkan rekor terbaik sepanjang sejarah sepak bola Indonesia di kancah Asia.

---

## 🏆 2. Peta Lengkap Probabilitas 24 Negara Peserta

Berikut adalah tabel hasil simulasi 100.000 iterasi Monte Carlo yang memproyeksikan seluruh 24 peserta di setiap babak:

| Rank | Negara | Grup | Base TPI | Gugur Grup (%) | Lolos 16 Besar (%) | **Lolos 8 Besar (%)** | Semifinal (%) | Final (%) | **Juara (%)** |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | 🇯🇵 **Jepang** | B | 9.00 | 0.04% | 99.96% | **93.01%** | 76.45% | 56.61% | **42.22%** |
| **2** | 🇰🇷 **Korea Selatan** | D | 7.59 | 0.08% | 99.92% | **84.86%** | 62.62% | 27.99% | **15.74%** |
| **3** | 🇮🇷 **Iran** | C | 7.47 | 0.32% | 99.68% | **86.69%** | 56.47% | 33.60% | **14.89%** |
| **4** | 🇸🇦 **Arab Saudi** | A | 7.17 | 0.74% | 99.26% | **85.67%** | 59.60% | 31.50% | **12.53%** |
| **5** | 🇦🇺 **Australia** | E | 6.77 | 0.50% | 99.50% | **72.90%** | 34.01% | 18.14% | **6.43%** |
| **6** | 🇶🇦 **Qatar** | F | 6.45 | 0.66% | 99.34% | **62.62%** | 19.68% | 8.71% | **3.36%** |
| **7** | 🇮🇶 **Irak** | B | 5.53 | 4.46% | 95.54% | **58.60%** | 23.48% | 7.72% | **1.63%** |
| **8** | 🇦🇪 **UAE** | C | 5.44 | 4.63% | 95.37% | **53.44%** | 18.46% | 4.88% | **1.23%** |
| **9** | 🇺🇿 **Uzbekistan** | E | 5.47 | 2.82% | 97.18% | **44.85%** | 11.71% | 4.00% | **0.98%** |
| **10** | 🇯🇴 **Yordania** | A | 4.93 | 12.29% | 87.71% | **37.86%** | 12.28% | 2.64% | **0.52%** |
| **11** | 🇧🇭 **Bahrain** | F | 4.39 | 10.17% | 89.83% | **30.26%** | 7.48% | 1.56% | **0.21%** |
| **12** | 🇴🇲 **Oman** | D | 4.35 | 7.40% | 92.60% | **23.14%** | 6.01% | 1.24% | **0.16%** |
| **13** | 🇮🇩 **INDONESIA** | **A** | **3.95** | **34.08%** | **65.92%** | **15.32%** | **3.79%** | **0.58%** | **0.06%** |
| **14** | 🇸🇾 **Suriah** | C | 3.31 | 50.58% | 49.42% | **8.30%** | 1.48% | 0.17% | **0.01%** |
| **15** | 🇹🇭 **Thailand** | B | 3.18 | 66.80% | 33.20% | **6.55%** | 1.12% | 0.12% | **0.01%** |
| **16** | 🇵🇸 **Palestina** | D | 3.21 | 28.20% | 71.80% | **8.47%** | 1.53% | 0.19% | **0.01%** |
| **17** | 🇲🇾 **Malaysia** | E | 3.05 | 48.84% | 51.16% | **6.11%** | 0.89% | 0.10% | **0.00%** |
| **18** | 🇨🇳 **China PR** | A | 2.98 | 73.81% | 26.19% | **4.07%** | 0.63% | 0.05% | **0.00%** |
| **19** | 🇹🇯 **Tajikistan** | F | 2.60 | 60.96% | 39.04% | **4.51%** | 0.62% | 0.05% | **0.00%** |
| **20** | 🇻🇳 **Vietnam** | F | 2.75 | 53.63% | 46.37% | **5.74%** | 0.81% | 0.08% | **0.00%** |
| **21** | 🇰🇼 **Kuwait** | B | 2.60 | 84.78% | 15.22% | **2.69%** | 0.37% | 0.03% | **0.00%** |
| **22** | 🇱🇧 **Lebanon** | C | 2.56 | 80.83% | 19.17% | **2.58%** | 0.30% | 0.02% | **0.00%** |
| **23** | 🇰🇬 **Kyrgyzstan** | E | 2.20 | 83.32% | 16.68% | **1.30%** | 0.14% | 0.01% | **0.00%** |
| **24** | 🇰🇵 **Korea Utara** | D | 1.50 | 90.03% | 9.97% | **0.48%** | 0.05% | 0.00% | **0.00%** |

---

## 🗺️ 3. Bedah Taktis & 3 Skenario Timnas Indonesia Menuju 8 Besar

Di Piala Asia 2027, Indonesia berada di **Grup A** bersama:
1. **Arab Saudi** (Tuan Rumah, Pot 1)
2. **Yordania** (Runner-up Piala Asia 2023, Pot 2)
3. **China PR** (Pot 3)
4. **Indonesia** (Pot 4)

Format turnamen meloloskan **Juara Grup**, **Runner-up Grup**, serta **4 Tim Peringkat Ketiga Terbaik** ke Babak 16 Besar. Berikut adalah 3 skenario kelolosan Indonesia:

```text
                                       [FASE GRUP A]
                  ┌──────────────────────────┼──────────────────────────┐
                  ▼                          ▼                          ▼
        [SKENARIO A: 38.5%]        [SKENARIO B: 29.2%]        [SKENARIO C: 5.4%]
          Runner-up Grup A        Peringkat 3 Terbaik          Juara Grup A
                  │                          │                          │
                  ▼                          ▼                          ▼
         [Babak 16 Besar]           [Babak 16 Besar]           [Babak 16 Besar]
         vs Runner-up C             vs Juara B / C             vs Peringkat 3
          (UAE / Suriah)            (Jepang / Iran)            (C / D / E)
                  │                          │                          │
      Peluang Menang: 42.5%      Peluang Menang: 14.5%      Peluang Menang: 65.0%
                  │                          │                          │
                  └──────────────────────────┼──────────────────────────┘
                                             ▼
                             [BABAK 8 BESAR / PEREMPAT FINAL]
                                (Peluang Agregat: 16.18%)
```

### 1. Skenario Emas: Runner-up Grup A (Peluang Terjadinya: 38.5%)
- **Syarat**: Indonesia mengalahkan China PR, menahan imbang Yordania, atau mencuri poin dari Arab Saudi.
- **Calon Lawan di 16 Besar**: Runner-up Grup C (kemungkinan besar **UAE** atau **Suriah**).
- **Peluang Menang Menuju 8 Besar**: **42.5%**!
- **Analisis Taktis**: Menghindari raksasa seperti Jepang dan Iran. Level Indonesia dengan nilai skuad €36.5M sangat kompetitif menghadapi UAE (TPI 5.46) dan Suriah (TPI 3.33).

### 2. Skenario Realistis: Peringkat 3 Terbaik Grup A (Peluang Terjadinya: 29.2%)
- **Syarat**: Indonesia finis posisi ke-3 dengan raihan 3–4 poin (misal menang atas China namun kalah dari Saudi & Yordania).
- **Calon Lawan di 16 Besar**: Juara Grup B (**Jepang**) atau Juara Grup C (**Iran**).
- **Peluang Menang Menuju 8 Besar**: **14.5%**.
- **Analisis Taktis**: Pertandingan babak gugur yang sangat berat, membutuhkan strategi *ultra low-block* dan efisiensi *counter-attack* mutlak seperti saat menundukkan Arab Saudi 2-0 di GBK.

### 3. Skenario Kejutan: Juara Grup A (Peluang Terjadinya: 5.4%)
- **Syarat**: Indonesia menumbangkan Arab Saudi dan Yordania untuk memuncaki Grup A.
- **Calon Lawan di 16 Besar**: Peringkat 3 dari Grup C/D/E.
- **Peluang Menang Menuju 8 Besar**: **65.0%**.

---

## 🎓 4. Edukasi Sains Data bagi Orang Awam: Cara Kerja Model Prediksi

Bagi masyarakat dan pecinta sepak bola awam, platform ini bekerja menggunakan metode data science modern:

### 1. Apa itu Simulasi Monte Carlo? (Analogi Lempar Dadu)
> *Jika Anda melempar sepasang dadu sekali, hasilnya bisa acak. Namun jika Anda melemparnya **100.000 kali**, Anda akan tahu persis probabilitas setiap kombinasi angka yang keluar.*

Dalam turnamen sepak bola, hasil pertandingan tidak pernah pasti 100%. Wasit, tiang gawang, dan kartu merah bisa mengubah jalannya laga. Komputer kami **memainkan turnamen Piala Asia 2027 secara virtual sebanyak 100.000 kali**. Angka persentase yang Anda lihat adalah kompilasi dari 100.000 turnamen simulasi tersebut.

### 2. Apa itu Team Power Index (TPI) 5-Pilar?
Setiap tim diberi skor kekuatan (Base TPI) yang dihitung dari:
1. **Rating Elo 4 Tahun Terakhir (40%)**: Menghitung hasil tanding riil. Menang atas Arab Saudi memberi poin jauh lebih tinggi dibanding menang atas tim lemah.
2. **Nilai Pasar Skuad / Squad Value (30%)**: Berdasarkan data Transfermarkt. Pemain di liga elite Eropa terbukti memiliki ketahanan fisik dan pemahaman taktis superior.
3. **Faktor Tuan Rumah (10%)**: Keuntungan Arab Saudi sebagai tuan rumah turnamen.
4. **Adaptasi Iklim Teluk (10%)**: Ketahanan fisik bertanding dalam suhu panas gurun (>30°C).
5. **Varians Stokastik (10%)**: Faktor keberuntungan acak turnamen (*Gaussian Noise*).

### 3. Apa itu Expected Goals (xG)?
xG (*Expected Goals*) mengukur seberapa berbahaya peluang tembakan diciptakan (skala 0.0 sampai 1.0). Tembakan penalti bernilai ~0.79 xG, sementara tendangan spekulatif dari tengah lapangan bernilai ~0.02 xG. xG membuktikan apakah suatu tim menang karena bermain bagus atau sekadar beruntung.

---

## 📈 5. Evolusi Kualitas Skuad & Rekor 20 Laga 4 Tahun Terakhir (2023–2026)

### Lonjakan Nilai Pasar Skuad Timnas Indonesia
Peningkatan performa Indonesia bukan kebetulan, melainkan hasil transformasi skuad terukur:

```text
2023 (Pra-Diaspora Penuh)  : € 5.85 Juta   (Peringkat 18 di Asia)
2024 (Piala Asia Qatar)    : € 12.40 Juta  (Peringkat 13 di Asia)
2025 (Kualifikasi PD R3)   : € 26.85 Juta  (Peringkat 8 di Asia)
2026/2027 (Skuad Matang)   : € 36.50 Juta  (Peringkat 6 Tertinggi di Seluruh Asia!)
```

### Rekam Jejak 20 Laga Kunci 4 Tahun Terakhir
- **Total Laga**: 20 Pertandingan Resmi
- **Hasil**: 9 Menang, 4 Seri, 7 Kalah (65% Rekor Tak Terkalahkan)
- **Gol & xG**: 27 Gol Dibuat, 27 Kebobolan, 8 Clean Sheets (40% Clean Sheet Rate)
- **vs Raksasa Pot 1 Asia**: 
  - Menang **2-0 vs Arab Saudi** di GBK (xG 2.15 vs 0.95)
  - Imbang **1-1 vs Arab Saudi** di King Abdullah Sports City Jeddah
  - Imbang **0-0 vs Australia** di GBK (xG 0.65 vs 1.55, Maarten Paes masterclass)
- **vs Tim Pot 2 & 3 Asia**: 
  - Sapu bersih atas Vietnam (1-0, 1-0, 3-0 di Hanoi)
  - Menang 1-0 vs Bahrain di GBK, imbang 2-2 di Riffa
  - Menang 2-0 vs Filipina & 2-0 vs China PR

---

## 🏗️ 6. Arsitektur Direktori Repositori

```text
asian-cup-2027/
│
├── data/                                         # Data Lake Resmi
│   ├── asian_cup_predictions.csv                 # Output simulasi 100k Monte Carlo 24 tim
│   ├── indonesia_4yr_match_analytics.json        # Telemetri match 4 tahun & evolusi skuad
│   └── model_prediction_output.json             # Matriks bivariate poisson terkalibrasi
│
├── src/                                          # Kode Sumber Logika & Model
│   ├── data_pipeline/
│   │   ├── build_sports_data.py                  # Pipeline scraping & standarisasi
│   │   └── build_indonesia_analytics.py          # Generator analitika 4 tahun Timnas IDN
│   ├── models/
│   │   └── weighted_poisson_xgboost_model.py     # Model Bivariate Poisson + XGBoost
│   ├── simulation/
│   │   ├── run_asian_cup_simulation.py           # Engine simulasi 100.000 turnamen
│   │   └── benchmark_sim.py                      # Uji kecepatan komputasi vektor
│   └── legacy_viz/
│       ├── match_viz_generator.py                # Visualisasi statis (arsip)
│       └── plot_tournament_predictions.py        # Visualisasi turnamen statis (arsip)
│
├── app/                                          # Aplikasi Web Multipage Streamlit
│   ├── main.py                                   # Landing page & pusat edukasi publik
│   ├── pages/
│   │   ├── 1_🏆_Peluang_24_Tim_Peserta.py        # Peta probabilitas lengkap 24 negara
│   │   ├── 2_🇮🇩_Peluang_8_Besar_Timnas_Indonesia.py # Bedah mendalam 8 besar Indonesia
│   │   └── 3_🧮_Simulator_Pertandingan_Interaktif.py # Simulator laga interaktif
│   └── utils/
│       ├── charts.py                             # Modul grafik Plotly interaktif dark-theme
│       └── styles.py                             # CSS, badge, dan kartu UI glassmorphism
│
├── notebooks/                                    # Eksplorasi Jupyter Notebook
│   └── match_analysis.ipynb
│
├── viz_outputs/                                  # Aset ekspor gambar statis PNG
├── .gitignore                                    # Pengecualian git (venv, cache, checkpoints)
├── README.md                                     # Dokumentasi resmi berbahasa Indonesia
└── requirements.txt                              # Dependensi produksi
```

---

## 🚀 7. Panduan Instalasi & Menjalankan Dashboard Streamlit

### 1. Clone Repositori
```bash
git clone https://github.com/dawooodd/asian-cup-2027.git
cd asian-cup-2027
```

### 2. Siapkan Virtual Environment
```bash
# Windows (PowerShell):
python -m venv asiancup_env
.\asiancup_env\Scripts\activate

# Linux / macOS:
python3 -m venv asiancup_env
source asiancup_env/bin/activate
```

### 3. Pasang Dependensi
```bash
pip install -r requirements.txt
```

### 4. Jalankan Dashboard Streamlit
```bash
streamlit run app/main.py
```
Aplikasi akan terbuka secara otomatis di peramban web pada alamat `http://localhost:8501`.

---

## 🧪 8. Uji Kualitas & Verifikasi Otomatis

Seluruh halaman aplikasi web telah lolos pengujian *headless testing* resmi Streamlit `AppTest`:

```powershell
.\asiancup_env\Scripts\python.exe -c "
from streamlit.testing.v1 import AppTest
for p in ['app/main.py', 'app/pages/1_🏆_Peluang_24_Tim_Peserta.py', 'app/pages/2_🇮🇩_Peluang_8_Besar_Timnas_Indonesia.py', 'app/pages/3_🧮_Simulator_Pertandingan_Interaktif.py']:
    at = AppTest.from_file(p).run(timeout=25)
    assert not at.exception, f'Error in {p}: {at.exception}'
    print(f'Lolos: {p}')
print('Seluruh halaman terverifikasi: 0 Exceptions!')
"
```

---

## 📄 Lisensi
Hak Cipta © 2026 Sports Science & Quantitative Analytics Division. Dilisensikan di bawah [Lisensi MIT](LICENSE).
