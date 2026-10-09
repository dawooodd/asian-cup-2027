# ⚽ AFC Asian Cup 2027: Platform Prediksi Sains Data & Simulasi Turnamen

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.20%2B-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0%2B-EB5424.svg)](https://xgboost.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](#)

Repositori analitika sains data olahraga profesional dan pemodelan prediktif kuantitatif untuk memproyeksikan peta kompetisi **Piala Asia (AFC Asian Cup) Arab Saudi 2027**.

Platform ini mengintegrasikan **100.000 Iterasi Simulasi Monte Carlo**, **Model Distribusi Bivariate Poisson dengan Kalibrasi Residual XGBoost**, **Rekam Jejak 20 Pertandingan 4 Tahun Terakhir (2023–2026)**, serta **Evolusi Nilai Pasar Skuad (€36,5 Juta)** dengan fokus analisis utama: **Membedah Peluang Tim Nasional Indonesia Menembus Babak 8 Besar (Perempat Final)** dari persaingan sengit **Grup F (bersama Jepang, Qatar, dan Thailand)** serta probabilitas kelolosan seluruh 24 negara peserta.

---

## 📑 Daftar Isi
1. [Ringkasan Eksekutif: Sejauh Mana Timnas Indonesia Melangkah?](#-1-ringkasan-eksekutif-sejauh-mana-timnas-indonesia-melangkah)
2. [Peta Lengkap Probabilitas 24 Negara Peserta (Grup A s/d F)](#-2-peta-lengkap-probabilitas-24-negara-peserta-grup-a-sd-f)
3. [Bedah Taktis & 3 Skenario Timnas Indonesia Menuju 8 Besar](#-3-bedah-taktis--3-skenario-timnas-indonesia-menuju-8-besar)
4. [Edukasi Sains Data bagi Orang Awam: Cara Kerja Model Prediksi](#-4-edukasi-sains-data-bagi-orang-awam-cara-kerja-model-prediksi)
5. [Evolusi Kualitas Skuad & Rekor 20 Pertandingan Resmi (2023–2026)](#-5-evolusi-kualitas-skuad--rekor-20-pertandingan-resmi-20232026)
6. [Arsitektur Direktori Repositori](#-6-arsitektur-direktori-repositori)
7. [Panduan Instalasi & Menjalankan Dashboard Streamlit](#-7-panduan-instalasi--menjalankan-dashboard-streamlit)
8. [Uji Kualitas & Verifikasi Otomatis](#-8-uji-kualitas--verifikasi-otomatis)

---

## 🇮🇩 1. Ringkasan Eksekutif: Sejauh Mana Timnas Indonesia Melangkah?

Berdasarkan hasil komputasi **100.000 simulasi bagan turnamen penuh** menggunakan data performa 4 tahun terakhir:

| Tahapan Turnamen | Peluang Timnas Indonesia (%) | Makna Praktis bagi Suporter & Publik |
| :--- | :---: | :--- |
| **Lolos Fase Grup (16 Besar)** | **41,00%** | **Peluang Terbuka Nyata.** Indonesia berada di Grup F bersama Jepang, Qatar, dan Thailand. Kunci kelolosan adalah mengamankan poin penuh atas Thailand serta meminimalkan selisih gol. |
| **Lolos Babak 8 Besar (Perempat Final)** | **11,03% (Agregat)<br>s/d 40,50% (via Runner-up)** | **Target Sejarah Utama.** Apabila Indonesia mengamankan posisi Runner-up Grup F, lawan di 16 Besar adalah Runner-up Grup B (Yordania/Uzbekistan/Bahrain), sehingga peluang lolos ke 8 Besar melonjak menjadi **40,5%**! |
| **Lolos Semifinal (4 Besar)** | **2,54%** | **Pencapaian Fantastis.** Mengharuskan kemenangan beruntun atas dua raksasa Pot 1 dan Pot 2 Asia. |
| **Lolos ke Final (2 Besar)** | **0,43%** | **Kejutan Bersejarah Asia.** Peluang tembus partai puncak di Riyadh. |
| **Juara Piala Asia 2027** | **0,06%** | Kemungkinan matematis (~60 kali dari 100.000 simulasi turnamen). |

> **Kesimpulan Utama:** Target ilmiah paling terukur dan rasional bagi Timnas Indonesia di Piala Asia 2027 adalah **mengunci tiket Babak 16 Besar dan bertarung menembus Babak 8 Besar (Perempat Final)**, mencatatkan tinta emas pencapaian tertinggi dalam sejarah sepak bola Indonesia di tingkat Asia.

---

## 🏆 2. Peta Lengkap Probabilitas 24 Negara Peserta (Grup A s/d F)

Pembagian grup turnamen resmi terdiri dari 24 negara yang terbagi dalam 6 grup:
- **Grup A**: Arab Saudi, Kuwait, Oman, Palestina
- **Grup B**: Uzbekistan, Bahrain, Korea Utara, Yordania
- **Grup C**: Iran, Suriah, Kirgizstan, China
- **Grup D**: Australia, Tajikistan, Irak, Singapura
- **Grup E**: Korea Selatan, Uni Emirat Arab, Vietnam, Yaman
- **Grup F**: Jepang, Qatar, Thailand, Indonesia

Berikut adalah tabel hasil simulasi kuantitatif 100.000 iterasi Monte Carlo secara menyeluruh:

| Peringkat | Negara | Grup | Nilai TPI | Gugur Grup (%) | Lolos 16 Besar (%) | **Lolos 8 Besar (%)** | Semifinal (%) | Final (%) | **Juara (%)** |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | 🇯🇵 **Jepang** | F | 9.00 | 0.18% | 99.82% | **84.75%** | 73.34% | 59.07% | **42.84%** |
| **2** | 🇸🇦 **Arab Saudi** | A | 7.42 | 0.40% | 99.60% | **89.39%** | 57.63% | 29.90% | **13.66%** |
| **3** | 🇮🇷 **Iran** | C | 7.48 | 0.22% | 99.78% | **86.60%** | 50.34% | 27.98% | **13.15%** |
| **4** | 🇰🇷 **Korea Selatan** | E | 7.56 | 0.17% | 99.83% | **66.59%** | 39.92% | 23.39% | **11.26%** |
| **5** | 🇦🇺 **Australia** | D | 6.80 | 0.27% | 99.73% | **68.64%** | 49.34% | 19.21% | **8.07%** |
| **6** | 🇶🇦 **Qatar** | F | 6.61 | 4.18% | 95.82% | **63.91%** | 32.56% | 14.76% | **5.01%** |
| **7** | 🇮🇶 **Irak** | D | 5.71 | 1.29% | 98.71% | **41.45%** | 20.25% | 6.02% | **1.66%** |
| **8** | 🇺🇿 **Uzbekistan** | B | 5.56 | 2.97% | 97.03% | **52.31%** | 14.29% | 5.21% | **1.38%** |
| **9** | 🇦🇪 **UAE** | E | 5.67 | 2.25% | 97.75% | **26.78%** | 12.08% | 4.90% | **1.34%** |
| **10** | 🇯🇴 **Yordania** | B | 5.14 | 5.09% | 94.91% | **40.99%** | 10.81% | 3.04% | **0.64%** |
| **11** | 🇴🇲 **Oman** | A | 4.64 | 14.71% | 85.29% | **48.79%** | 14.64% | 2.68% | **0.44%** |
| **12** | 🇧🇭 **Bahrain** | B | 4.70 | 8.66% | 91.34% | **31.60%** | 8.18% | 1.90% | **0.33%** |
| **13** | 🇮🇩 **INDONESIA** | **F** | **4.26** | **59.00%** | **41.00%** | **11.03%** | **2.54%** | **0.43%** | **0.06%** |
| **14** | 🇸🇾 **Suriah** | C | 3.62 | 23.85% | 76.15% | **25.01%** | 4.59% | 0.55% | **0.06%** |
| **15** | 🇵🇸 **Palestina** | A | 3.55 | 44.72% | 55.28% | **17.13%** | 3.05% | 0.31% | **0.04%** |
| **16** | 🇨🇳 **China PR** | C | 3.20 | 37.47% | 62.53% | **15.14%** | 2.32% | 0.27% | **0.02%** |
| **17** | 🇹🇭 **Thailand** | F | 3.52 | 83.60% | 16.40% | **3.40%** | 0.59% | 0.07% | **0.01%** |
| **18** | 🇻🇳 **Vietnam** | E | 3.16 | 51.98% | 48.02% | **5.53%** | 0.88% | 0.11% | **0.01%** |
| **19** | 🇰🇵 **Korea Utara** | B | 1.77 | 92.54% | 7.46% | **0.54%** | 0.03% | 0.00% | **0.00%** |
| **20** | 🇰🇼 **Kuwait** | A | 3.03 | 67.84% | 32.16% | **8.28%** | 1.21% | 0.11% | **0.00%** |
| **21** | 🇸🇬 **Singapura** | D | 1.50 | 92.27% | 7.73% | **0.39%** | 0.03% | 0.00% | **0.00%** |
| **22** | 🇹🇯 **Tajikistan** | D | 2.90 | 47.42% | 52.58% | **5.93%** | 0.75% | 0.07% | **0.00%** |
| **23** | 🇰🇬 **Kirgizstan** | C | 2.47 | 68.56% | 31.44% | **5.34%** | 0.60% | 0.03% | **0.00%** |
| **24** | 🇾🇪 **Yaman** | E | 1.96 | 90.35% | 9.64% | **0.48%** | 0.05% | 0.00% | **0.00%** |

---

## 🗺️ 3. Bedah Taktis & 3 Skenario Timnas Indonesia Menuju 8 Besar

Di Piala Asia 2027, Indonesia ditempatkan di **Grup F** yang sering dijuluki sebagai grup neraka:
1. **Jepang** (Unggulan #1 Asia, Nilai Skuad €285 Juta, Pot 1)
2. **Qatar** (Juara Bertahan 2 Edisi Beruntun, Tuan Rumah 2023, Pot 1/2)
3. **Indonesia** (Kekuatan Baru Berbasis Diaspora Eropa, Nilai Skuad €36,5 Juta)
4. **Thailand** (Rival Tradisional Asia Tenggara)

Format kompetisi meloloskan **Juara Grup**, **Runner-up Grup**, serta **4 Tim Peringkat Ketiga Terbaik** ke Babak 16 Besar. Berikut adalah pemetaan 3 skenario taktis kelolosan Indonesia:

```text
                                       [FASE GRUP F]
                                (Jepang, Qatar, Thailand, IDN)
                   ┌──────────────────────────┼──────────────────────────┐
                   ▼                          ▼                          ▼
         [SKENARIO UTAMA: 28.5%]    [SKENARIO EMAS: 11.8%]     [SKENARIO KEJUTAN: 0.7%]
           Peringkat 3 Terbaik           Runner-up Grup F            Juara Grup F
                   │                          │                          │
                   ▼                          ▼                          ▼
          [Babak 16 Besar]           [Babak 16 Besar]           [Babak 16 Besar]
           vs Juara C / D             vs Runner-up B             vs Runner-up E
           (Iran / Australia)      (Yordania / Uzbekistan)       (UAE / Vietnam)
                   │                          │                          │
       Peluang Menang: 18.5%      Peluang Menang: 40.5%      Peluang Menang: 58.0%
                   │                          │                          │
                   └──────────────────────────┼──────────────────────────┘
                                              ▼
                              [BABAK 8 BESAR / PEREMPAT FINAL]
                                 (Peluang Agregat: 11.03%)
```

### 1. Skenario Utama: Peringkat 3 Terbaik Grup F (Kemungkinan Terjadi: 28,5%)
- **Prasyarat Taktis**: Mengalahkan Thailand pada laga pembuka/kunci dan menjaga selisih gol agar tidak defisit besar saat bersua Jepang dan Qatar (mengoleksi 3–4 poin).
- **Calon Lawan di 16 Besar**: Juara Grup C (**Iran**) atau Juara Grup D (**Australia**).
- **Peluang Menang Menuju 8 Besar**: **18,5%**.
- **Analisis**: Jalur yang paling mungkin dilewati. Menghadapi raksasa Asia menuntut kedisiplinan skema pertahanan blok rendah (*low-block*) dan kecepatan serangan balik seperti kemenangan 2-0 atas Arab Saudi.

### 2. Skenario Emas: Runner-up Grup F (Kemungkinan Terjadi: 11,8%)
- **Prasyarat Taktis**: Mengalahkan Thailand serta berhasil menahan imbang atau menaklukkan Qatar untuk mengunci posisi ke-2 di bawah Jepang (mengoleksi 4–6 poin).
- **Calon Lawan di 16 Besar**: Runner-up Grup B (kemungkinan besar **Yordania**, **Uzbekistan**, atau **Bahrain**).
- **Peluang Menang Menuju 8 Besar**: **40,5%**!
- **Analisis**: Ini adalah rute terbaik bagi Indonesia menuju sejarah 8 Besar. Menghadapi tim sekelas Yordania atau Uzbekistan memberikan peluang berimbang karena Indonesia terhindar dari unggulan teratas Asia.

### 3. Skenario Kejutan Bersejarah: Juara Grup F (Kemungkinan Terjadi: 0,7%)
- **Prasyarat Taktis**: Kejutan sensasional di mana Indonesia menyapu poin penuh atas Thailand dan Qatar serta menahan imbang Jepang.
- **Calon Lawan di 16 Besar**: Runner-up Grup E (**Uni Emirat Arab** atau **Vietnam**).
- **Peluang Menang Menuju 8 Besar**: **58,0%**.

---

## 🎓 4. Edukasi Sains Data bagi Orang Awam: Cara Kerja Model Prediksi

Bagi masyarakat dan pecinta sepak bola umum, platform ini dibangun menggunakan 3 metodologi sains data teruji:

### 1. Apa itu Simulasi Monte Carlo? (Analogi Lemparan Dadu 100.000 Kali)
> *Jika Anda melempar sepasang dadu satu kali, hasilnya tampak acak. Namun jika Anda melemparnya **100.000 kali**, Anda akan mengetahui secara pasti persentase kemungkinan munculnya setiap kombinasi angka.*

Dalam sepak bola nyata, sebuah pertandingan tidak bisa dipastikan hanya dari sejarah nama besar. Kartu merah tak terduga, benturan bola ke tiang gawang, atau kesalahan penjaga gawang dapat terjadi. Superkomputer kami **memainkan turnamen Piala Asia 2027 sebanyak 100.000 kali secara virtual**. Angka persentase pada aplikasi ini adalah akumulasi probabilitas dari 100.000 kali percobaan turnamen tersebut.

### 2. Apa itu Team Power Index (TPI) 5-Pilar?
Setiap negara peserta diberi indeks kekuatan dasar (*Base TPI*) berskala 1,0 hingga 10,0 yang dihitung dari:
1. **Rating Elo 4 Tahun Terakhir (Bobot: 40%)**: Menilai performa pertandingan nyata. Kemenangan atas Arab Saudi berperingkat FIFA 50 besar memberi poin jauh lebih tinggi dibanding kemenangan atas tim semenjana.
2. **Kualitas & Nilai Pasar Skuad (Bobot: 30%)**: Berdasarkan data Transfermarkt. Pemain di liga elite Eropa terbukti memiliki ketahanan fisik, pemahaman taktik, dan kecepatan pengambilan keputusan yang unggul.
3. **Faktor Tuan Rumah & Jarak Tempuh (Bobot: 10%)**: Keunggulan tuan rumah bagi Arab Saudi serta penalti kelelahan perjalanan penerbangan benua.
4. **Adaptasi Iklim Gurun (Bobot: 10%)**: Daya tahan fisik bertanding dalam cuaca musim dingin gurun di Arab Saudi (~21,5°C).
5. **Varians Stokastik (Bobot: 10%)**: Faktor kejutan lapangan hijau dan dinamika adu penalti (*Gaussian Noise*).

### 3. Apa itu Expected Goals (xG)?
xG (*Expected Goals*) mengukur seberapa berbahaya peluang tembakan yang diciptakan (skala 0,0 sampai 1,0). Tembakan dari titik penalti bernilai ~0,79 xG, sementara tendangan spekulatif dari jarak 35 meter bernilai ~0,02 xG. xG menjadi bukti sahih apakah kemenangan suatu tim merupakan buah dari skema permainan yang matang atau sekadar keberuntungan.

---

## 📈 5. Evolusi Kualitas Skuad & Rekor 20 Pertandingan Resmi (2023–2026)

### Lonjakan Nilai Pasar Skuad Timnas Indonesia
Peningkatan daya saing Indonesia merupakan buah dari integrasi talenta terukur:

```text
2023 (Tahap Awal Integrasi)     : €  5,85 Juta  (Peringkat 18 di Asia)
2024 (Piala Asia Qatar)         : € 12,40 Juta  (Peringkat 13 di Asia)
2025 (Kualifikasi PD Putaran 3) : € 26,85 Juta  (Peringkat 8 di Asia)
2026/2027 (Skuad Matang)        : € 36,50 Juta  (Peringkat 6 Tertinggi di Seluruh Asia!)
```

### Rekam Jejak 20 Laga Kunci 4 Tahun Terakhir
- **Total Laga**: 20 Pertandingan Resmi
- **Hasil**: 9 Menang, 4 Imbang, 7 Kalah (65% Rekor Tak Terkalahkan)
- **Gol & Pertahanan**: 27 Gol Dibuat, 27 Kebobolan, 8 Nirbobol (*Clean Sheet*, 40%)
- **vs Raksasa Pot 1 Asia**: 
  - Menang **2-0 atas Arab Saudi** di Stadion Gelora Bung Karno (xG 2,15 vs 0,95)
  - Imbang **1-1 melawan Arab Saudi** di Stadion King Abdullah Sports City Jeddah
  - Imbang **0-0 melawan Australia** di GBK (Maarten Paes mencatat 5 penyelamatan gemilang)
- **vs Tim Pot 2 & 3 Asia**: 
  - Sapu bersih tiga kemenangan atas Vietnam (1-0, 1-0, 3-0 di Hanoi)
  - Menang 1-0 atas Bahrain di GBK, imbang 2-2 di Riffa
  - Menang 2-0 atas Filipina & 2-0 atas China PR

---

## 🏗️ 6. Arsitektur Direktori Repositori

```text
asian-cup-2027/
│
├── data/                                         # Pusat Data Lake Resmi
│   ├── asian_cup_predictions.csv                 # Luaran simulasi 100k Monte Carlo 24 tim
│   └── indonesia_4yr_match_analytics.json        # Telemetri match 4 tahun & evolusi skuad
│
├── src/                                          # Kode Sumber Logika & Pemodelan
│   ├── data_pipeline/
│   │   └── build_indonesia_analytics.py          # Generator analitika 4 tahun Timnas IDN
│   ├── models/
│   │   └── weighted_poisson_xgboost_model.py     # Model Bivariate Poisson + Koreksi XGBoost
│   ├── simulation/
│   │   └── run_asian_cup_simulation.py           # Mesin simulasi 100.000 turnamen
│   └── visualization/
│       └── plot_tournament_predictions.py        # Generator visualisasi turnamen resmi
│
├── app/                                          # Aplikasi Web Multipage Streamlit
│   ├── main.py                                   # Beranda utama & pusat edukasi publik
│   ├── pages/
│   │   ├── 1_🏆_Peluang_24_Tim_Peserta.py        # Peta probabilitas lengkap 24 negara
│   │   ├── 2_🇮🇩_Peluang_8_Besar_Timnas_Indonesia.py # Bedah mendalam peluang 8 besar IDN
│   │   └── 3_🧮_Simulator_Pertandingan_Interaktif.py # Simulator pertandingan interaktif
│   └── utils/
│       ├── charts.py                             # Utilitas visualisasi Plotly interaktif
│       └── styles.py                             # Desain CSS, lencana, & antarmuka modern
│
├── notebooks/                                    # Eksplorasi Interaktif Jupyter Notebook
│   └── match_analysis.ipynb
│
├── viz_outputs/                                  # Ekspor gambar visualisasi statis PNG
│   └── asian_cup_2027_tournament_predictions.png
│
├── .gitignore                                    # Berkas pengecualian Git
├── README.md                                     # Dokumentasi resmi berbahasa Indonesia baku
└── requirements.txt                              # Daftar dependensi pustaka Python
```

---

## 🚀 7. Panduan Instalasi & Menjalankan Dashboard Streamlit

### 1. Salin Repositori (Clone)
```bash
git clone https://github.com/dawooodd/asian-cup-2027.git
cd asian-cup-2027
```

### 2. Siapkan Lingkungan Virtual (Virtual Environment)
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
Aplikasi akan secara otomatis terbuka di peramban web pada alamat `http://localhost:8501`.

---

## 🧪 8. Uji Kualitas & Verifikasi Otomatis

Seluruh halaman aplikasi web telah melalui proses pengujian nir-antarmuka (*headless testing*) resmi Streamlit `AppTest`:

```powershell
.\asiancup_env\Scripts\python.exe -c "
from streamlit.testing.v1 import AppTest
pages = [
    'app/main.py',
    'app/pages/1_🏆_Peluang_24_Tim_Peserta.py',
    'app/pages/2_🇮🇩_Peluang_8_Besar_Timnas_Indonesia.py',
    'app/pages/3_🧮_Simulator_Pertandingan_Interaktif.py'
]
for p in pages:
    at = AppTest.from_file(p).run(timeout=25)
    assert not at.exception, f'Kendala pada {p}: {at.exception}'
    print(f'Terverifikasi Berhasil: {p}')
print('Seluruh halaman aplikasi lolos pengujian: 0 Exceptions!')
"
```

---

## 📄 Lisensi
Hak Cipta © 2026 Divisi Sains Data & Analitika Kuantitatif Olahraga. Dilisensikan di bawah [Lisensi MIT](LICENSE).
