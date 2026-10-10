# ⚽ AFC Asian Cup 2027: Platform Prediksi Sains Data & Simulasi Turnamen

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.20%2B-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0%2B-EB5424.svg)](https://xgboost.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](#)

Repositori analitika sains data olahraga profesional dan pemodelan prediktif kuantitatif untuk memproyeksikan peta kompetisi **Piala Asia (AFC Asian Cup) Arab Saudi 2027**.

Platform ini mengintegrasikan **100.000 Iterasi Simulasi Monte Carlo**, **Model Distribusi Bivariate Poisson dengan Kalibrasi Residual XGBoost**, **Analisis Mikro X-Factor Pemain Kunci & Pengali Keberuntungan (*Luck Multiplier*) untuk 24 Negara**, **Rekam Jejak Tanpa Batas Pasca Piala Asia 2023 hingga FIFA Matchday Oktober 2026 (27 Laga Resmi)**, serta **Evolusi Nilai Pasar Skuad (€36,5 Juta)** dengan fokus utama: **Membedah Peluang Tim Nasional Indonesia Menembus Babak 8 Besar (Perempat Final)** dari persaingan sengit **Grup F (bersama Jepang, Qatar, dan Thailand)**.

---

## 📑 Daftar Isi
1. [Ringkasan Eksekutif: Sejauh Mana Timnas Indonesia Melangkah?](#-1-ringkasan-eksekutif-sejauh-mana-timnas-indonesia-melangkah)
2. [Peta Lengkap Probabilitas 24 Negara Peserta (Grup A s/d F)](#-2-peta-lengkap-probabilitas-24-negara-peserta-grup-a-sd-f)
3. [Analisis Mikro X-Factor Pemain Kunci & Varians Keberuntungan (24 Negara)](#-3-analisis-mikro-x-factor-pemain-kunci--varians-keberuntungan-24-negara)
4. [Bedah Taktis & 3 Skenario Timnas Indonesia Menuju 8 Besar](#-4-bedah-taktis--3-skenario-timnas-indonesia-menuju-8-besar)
5. [Evolusi Kualitas Skuad & Rekor Lengkap Pasca Piala Asia 2023 s.d. Oktober 2026](#-5-evolusi-kualitas-skuad--rekor-lengkap-pasca-piala-asia-2023-sd-oktober-2026)
6. [Edukasi Sains Data bagi Orang Awam: Cara Kerja Model Prediksi](#-6-edukasi-sains-data-bagi-orang-awam-cara-kerja-model-prediksi)
7. [Arsitektur Direktori Repositori](#-7-arsitektur-direktori-repositori)
8. [Panduan Instalasi & Menjalankan Dashboard Streamlit](#-8-panduan-instalasi--menjalankan-dashboard-streamlit)
9. [Uji Kualitas & Verifikasi Otomatis](#-9-uji-kualitas--verifikasi-otomatis)

---

## 🇮🇩 1. Ringkasan Eksekutif: Sejauh Mana Timnas Indonesia Melangkah?

Berdasarkan hasil komputasi **100.000 simulasi bagan turnamen penuh** menggunakan data performa menyeluruh:

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

## ⭐ 3. Analisis Mikro X-Factor Pemain Kunci & Varians Keberuntungan (24 Negara)

Dalam turnamen sistem gugur (*single-elimination*), statistik makro (seperti penguasaan bola atau total tembakan) kerap kali dinetralkan oleh **varians mikro** — momen magis satu pemain, keahlian kiper menepis penalti, atau kepemimpinan di menit-menit akhir (*injury time*).

### Rumusan Skor Mikro Pemain (Clutch Score & Luck Multiplier)
Setiap pemain kunci dianalisis menggunakan 5 atribut mikro (skala 0–100):
1. **Ketenangan di Bawah Tekanan (*Composure Under Pressure*)**: Akurasi pengambilan keputusan saat lawan melakukan *high-press*.
2. **Dampak Situasi Penalti (*Penalty Clutch Impact*)**: Rasio konversi penalti atau penyelamatan kiper.
3. **Efisiensi Bola Mati (*Set-Piece Lethality*)**: Konversi tendangan bebas, sepak pojok, atau lemparan ke dalam berbahaya.
4. **Kepemimpinan & Resiliensi (*Leadership & Resilience*)**: Kemampuan mengangkat mentalitas tim saat tertinggal.
5. **Daya Penentu Menit Akhir (*Late-Game Decisiveness*)**: Produktivitas gol/asist/blok krusial di atas menit ke-75.

$$\text{Clutch Score} = 0.25 C + 0.25 P + 0.15 S + 0.15 L + 0.20 D$$

$$\text{Micro Luck Multiplier} = 1.0 + \left(\frac{\text{Clutch Score} - 50}{150}\right)$$

### Profil Dua Pemain Pembeda Timnas Indonesia
- 🧤 **Maarten Paes (Penjaga Gawang, FC Dallas - MLS)**
  - *Clutch Score*: **94/100** | *Pengali Keberuntungan*: **1.30x**
  - *Peran Mikro*: Penyelamat penalti ulung (*Penalty Stopper*), penyelamatan *post-shot xG* positif (+3.8), dan ketenangan distribusi bola di bawah *pressing* tinggi. Paes terbukti menggagalkan penalti kapten Arab Saudi di Jeddah dan menepis 5 tembakan akurat Australia.
- 🛡️ **Jay Idzes (Bek Tengah / Kapten, Venezia FC - Serie A)**
  - *Clutch Score*: **92/100** | *Pengali Keberuntungan*: **1.25x**
  - *Peran Mikro*: Tembok pertahanan berdarah dingin (*Clearance Magnet*), pemimpin vokal organisasi garis pertahanan, memenangkan 78% duel udara di kotak penalti, serta ancaman bola mati ofensif (gol sundulan vs Vietnam di Hanoi).

### Peta Komparasi Pemain Kunci 24 Negara Peserta

| Grup | Negara | Pemain 1 (Peran Mikro) | Pemain 2 (Peran Mikro) | Skor Clutch Tertinggi | Pengali Keberuntungan |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **A** | 🇸🇦 Arab Saudi | Salem Al-Dawsari (Winger/Kreator) | Firas Al-Buraikan (Striker) | **93** | 1.26x |
| **A** | 🇴🇲 Oman | Issam Al-Sabhi (Target Man) | Jameel Al-Yahmadi (Gelandang) | **82** | 1.15x |
| **A** | 🇵🇸 Palestina | Oday Dabbagh (Striker Tajam) | Rami Hamadeh (Kiper) | **84** | 1.18x |
| **A** | 🇰🇼 Kuwait | Shabaib Al-Khaldi (Finisher) | Fahad Al-Hajeri (Bek Senior) | **76** | 1.10x |
| **B** | 🇺🇿 Uzbekistan | Abbosbek Fayzullaev (Playmaker CSKA) | Eldor Shomurodov (Target Man Serie A) | **91** | 1.25x |
| **B** | 🇯🇴 Yordania | Mousa Al-Tamari (Penyerang Sayap Ligue 1) | Yazan Al-Naimat (Striker Gesit) | **94** | 1.28x |
| **B** | 🇧🇭 Bahrain | Mohamed Marhoon (Spesialis Set-Piece) | Ali Madan (Winger Cepat) | **83** | 1.17x |
| **B** | 🇰🇵 Korea Utara | Han Kwang-song (Striker Berbakat) | Kang Ju-hyok (Kiper Tangguh) | **78** | 1.11x |
| **C** | 🇮🇷 Iran | Mehdi Taremi (Striker Inter Milan) | Alireza Beiranvand (Kiper Spesialis Penalti) | **95** | 1.29x |
| **C** | 🇸🇾 Suriah | Omar Khribin (Finisher Haus Gol) | Ahmad Madania (Kiper Penyelamat) | **85** | 1.18x |
| **C** | 🇨🇳 China PR | Wu Lei (Striker Pencari Ruang) | Wang Dalei (Kiper Vokal) | **82** | 1.15x |
| **C** | 🇰🇬 Kirgizstan | Joel Kojo (Striker Naturalisasi) | Valery Kichin (Bek Pemimpin) | **80** | 1.13x |
| **D** | 🇦🇺 Australia | Harry Souttar (Bek 198cm Senjata Set-Piece) | Mathew Ryan (Kiper & Kapten Berpengalaman) | **91** | 1.24x |
| **D** | 🇮🇶 Irak | Aymen Hussein (Finisher Udara Mematikan) | Ali Jasim (Winger Dribel Licin) | **90** | 1.23x |
| **D** | 🇹🇯 Tajikistan | Rustam Soirov (Striker Penekan) | Rustam Yatimov (Kiper Pahlawan Adu Penalti) | **81** | 1.14x |
| **D** | 🇸🇬 Singapura | Ikhsan Fandi (Target Man Postur Tinggi) | Hassan Sunny (Kiper Senior Tembok Terakhir) | **74** | 1.09x |
| **E** | 🇰🇷 Korea Selatan | Son Heung-min (Bintang Dunia & Algojo Clutch) | Kim Min-jae (Bek Monster Bayern Munich) | **97** | 1.33x |
| **E** | 🇦🇪 UAE | Fabio Lima (Kreator Serangan & Algojo FK) | Ali Mabkhout (Pencetak Gol Bersejarah) | **87** | 1.20x |
| **E** | 🇻🇳 Vietnam | Nguyen Quang Hai (Maestro Tendangan Bebas) | Filip Nguyen (Kiper Postur Eropa) | **80** | 1.13x |
| **E** | 🇾🇪 Yaman | Abdulwasea Al-Matari (Kapten & Gelandang) | Ahmed Al-Sarori (Winger Cepat) | **72** | 1.07x |
| **F** | 🇯🇵 Jepang | Kaoru Mitoma (Spesialis 1v1 Premier League) | Wataru Endo (Gelandang Jangkar Liverpool) | **96** | 1.32x |
| **F** | 🇶🇦 Qatar | Akram Afif (Penyihir Sayap & 2x MVP Asia) | Almoez Ali (Top Skor Bersejarah) | **96** | 1.32x |
| **F** | 🇮🇩 Indonesia | Maarten Paes (Kiper Penepis Penalti MLS) | Jay Idzes (Tembok Pertahanan Serie A) | **94** | 1.30x |
| **F** | 🇹🇭 Thailand | Chanathip Songkrasin (Maestro Visi Dribel) | Theerathon Bunmathan (Spesialis Bola Mati) | **86** | 1.19x |

---

## 🗺️ 4. Bedah Taktis & 3 Skenario Timnas Indonesia Menuju 8 Besar

Di Piala Asia 2027, Indonesia ditempatkan di **Grup F** yang sangat kompetitif:
1. **Jepang** (Unggulan #1 Asia, Nilai Skuad €285 Juta, Pot 1)
2. **Qatar** (Juara Bertahan 2 Edisi Beruntun, Nilai Skuad €18,5 Juta, Pot 1/2)
3. **Indonesia** (Kekuatan Baru Berbasis Diaspora Eropa, Nilai Skuad €36,5 Juta)
4. **Thailand** (Rival Tradisional Asia Tenggara)

```text
                                       [FASE GRUP F]
                                (Jepang, Qatar, Thailand, IDN)
                   ┌──────────────────────────┼──────────────────────────┐
                   ▼                          ▼                          ▼
         [SKENARIO UTAMA: 28.5%]    [SKENARIO EMAS: 11.8%]     [SKENARIO KEJUTAN: 0.7%]
            Peringkat 3 Terbaik            Runner-up Grup F               Juara Grup F
                   │                          │                          │
                   ▼                          ▼                          ▼
            [BABAK 16 BESAR]           [BABAK 16 BESAR]           [BABAK 16 BESAR]
           vs Juara Grup A/B          vs Runner-up Grup B        vs Peringkat 3 A/B/C
        (Arab Saudi/Uzbekistan)     (Yordania/Bahrain/Uzbek)     (Palestina/Suriah/KWT)
                   │                          │                          │
                   ▼                          ▼                          ▼
           [PELUANG MENANG]           [PELUANG MENANG]           [PELUANG MENANG]
                 21.0%                      40.5%                      68.0%
                   │                          │                          │
                   └──────────────────────────┼──────────────────────────┘
                                              ▼
                                   [BABAK 8 BESAR (QF)]
                              Probabilitas Kumulatif: 11.03%
```

- **Skenario Emas (Pintu Masuk Terbuka Lebar)**: Mengalahkan Thailand (3 poin) dan menahan imbang Qatar (1 poin), lolos sebagai **Runner-up Grup F**. Di 16 Besar bertemu Runner-up Grup B (Yordania/Bahrain), di mana rekam jejak Indonesia sangat kompetitif (peluang menang **40,5%**).
- **Skenario Realistis (Peringkat 3 Terbaik)**: Menang atas Thailand, lolos dengan 3–4 poin. Menghadapi Juara Grup A (Arab Saudi) atau Juara Grup B (Uzbekistan) dengan peluang menang **21,0%**.

---

## 📈 5. Evolusi Kualitas Skuad & Rekor Lengkap Pasca Piala Asia 2023 s.d. Oktober 2026

### Lonjakan Nilai Pasar Skuad Timnas Indonesia
Peningkatan daya saing Indonesia merupakan buah dari integrasi talenta diaspora di liga top Eropa:

```text
2023 (Tahap Awal Integrasi)     : €  5,85 Juta  (Peringkat 18 di Asia)
2024 (Piala Asia Qatar)         : € 12,40 Juta  (Peringkat 13 di Asia)
2025 (Kualifikasi PD Putaran 3) : € 26,85 Juta  (Peringkat 8 di Asia)
2026/2027 (Skuad Matang)        : € 36,50 Juta  (Peringkat 6 Tertinggi di Seluruh Asia!)
```

### Rekor Menyeluruh Tanpa Batas: 27 Pertandingan Resmi (Maret 2024 – Oktober 2026)
Analisis pertandingan diperluas tanpa batasan buatan, mencakup seluruh **27 pertandingan resmi FIFA/AFC** sejak berakhirnya Piala Asia 2023 di Qatar hingga **FIFA Matchday Oktober 2026**:
- **Total Laga**: 27 Pertandingan Resmi
- **Hasil**: 15 Kemenangan, 6 Hasil Imbang, 6 Kekalahan
- **Persentase Kemenangan**: **55,56%** | **Rekor Tak Terkalahkan**: **77,78%**
- **Produktivitas Gol**: 41 Gol Dibuat, 23 Kebobolan (Selisih Gol: **+18**)
- **Pertahanan Kokoh**: 13 Nirbobol (*Clean Sheet*, **48,15%**)

#### Sorotan Prestasi vs Kekuatan Asia (2024–2026):
1. **vs Pot 1 Asia**:
   - Menang **2-0 atas Arab Saudi** di Stadion Utama Gelora Bung Karno (xG 2,15 vs 0,95)
   - Imbang **1-1 melawan Arab Saudi** di King Abdullah Sports City, Jeddah
   - Imbang **0-0 melawan Australia** di GBK (Maarten Paes menepis 5 peluang emas)
2. **vs Pot 2 & 3 Asia**:
   - Menang **2-1 atas Bahrain** di GBK (Oktober 2026) & imbang **2-2** di Riffa
   - Menang **1-0 atas Oman** di Muscat (September 2026)
   - Menang **2-1 atas Thailand** di Bangkok
   - Menang **2-0 atas China PR** di GBK
   - Tiga kemenangan beruntun atas Vietnam (1-0, 1-0, dan 3-0 di My Dinh Hanoi)

---

## 🧠 6. Edukasi Sains Data bagi Orang Awam: Cara Kerja Model Prediksi

Bagi masyarakat umum yang awam terhadap matematika tingkat lanjut, berikut cara kerja model komputer dalam memprediksi pertandingan:

1. **Simulasi Monte Carlo (100.000 Putaran)**:
   Komputer memutar turnamen layaknya permainan digital sebanyak 100.000 kali dari laga pertama hingga final. Probabilitas adalah persentase seberapa sering suatu tim mencapai babak tertentu dari 100.000 turnamen tersebut.
2. **Distribusi Bivariate Poisson**:
   Menghitung probabilitas setiap skor spesifik (1-0, 2-1, 0-0) berdasarkan kekuatan serang (*attacking strength*) dan ketangguhan pertahanan (*defensive strength*).
3. **Penyempurnaan Machine Learning (XGBoost)**:
   Mengoreksi angka Poisson dengan membaca faktor non-linear: kelelahan pemain, jadwal pemulihan, dan dampak pergantian pemain di babak kedua.
4. **Expected Goals (xG)**:
   Mengukur kualitas peluang tembakan (skala 0,0 hingga 1,0). Penalti bernilai ~0,79 xG, sedangkan tembakan spekulatif dari luar kotak bernilai ~0,02 xG. xG membuktikan bahwa performa solid Indonesia didasari skema peluang berkualitas tinggi, bukan keberuntungan semata.

---

## 🏗️ 7. Arsitektur Direktori Repositori

```text
asian-cup-2027/
│
├── data/                                         # Pusat Data Lake Resmi
│   ├── asian_cup_predictions.csv                 # Luaran simulasi 100k Monte Carlo 24 tim
│   ├── indonesia_4yr_match_analytics.json        # 27 laga resmi pasca 2023 s.d. Okt 2026
│   └── all_24_teams_squad_micro_analytics.json   # Skuad 2026, profil clutch & luck 24 tim
│
├── src/                                          # Kode Sumber Logika & Pemodelan
│   ├── data_pipeline/
│   │   ├── build_indonesia_analytics.py          # Generator analitika 27 laga resmi IDN
│   │   └── build_squad_micro_analytics.py        # Generator analitika mikro 24 negara
│   ├── models/
│   │   └── weighted_poisson_xgboost_model.py     # Model Bivariate Poisson + Koreksi XGBoost
│   ├── simulation/
│   │   └── run_asian_cup_simulation.py           # Mesin simulasi 100.000 turnamen
│   └── visualization/
│       └── plot_tournament_predictions.py        # Generator visualisasi turnamen resmi
│
├── app/                                          # Aplikasi Web Multipage Streamlit
│   ├── main.py                                   # Beranda utama & pengantar modul
│   ├── pages/
│   │   ├── 1_🏆_Peluang_24_Tim_Peserta.py        # Peta probabilitas lengkap 24 negara
│   │   ├── 2_🇮🇩_Peluang_8_Besar_Timnas_Indonesia.py # Bedah mendalam peluang 8 besar IDN
│   │   ├── 3_🧮_Simulator_Pertandingan_Interaktif.py # Simulator pertandingan & adu penalti
│   │   └── 4_⭐_Analisis_Mikro_Pemain_Kunci_&_Keberuntungan.py # Bedah mikro pemain & keberuntungan
│   └── utils/
│       ├── charts.py                             # Utilitas visualisasi Plotly & Radar interaktif
│       └── styles.py                             # Desain CSS, lencana, & antarmuka modern
│
├── notebooks/                                    # Eksplorasi Interaktif Jupyter Notebook
│   └── match_analysis.ipynb                      # Notebook komprehensif 6 bagian analitika
│
├── viz_outputs/                                  # Ekspor gambar visualisasi statis PNG
│   └── asian_cup_2027_tournament_predictions.png
│
├── .gitignore                                    # Berkas pengecualian Git
├── README.md                                     # Dokumentasi resmi berbahasa Indonesia baku
└── requirements.txt                              # Daftar dependensi pustaka Python
```

---

## 🚀 8. Panduan Instalasi & Menjalankan Dashboard Streamlit

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

## 🧪 9. Uji Kualitas & Verifikasi Otomatis

Seluruh 5 modul halaman aplikasi web telah melalui proses pengujian nir-antarmuka (*headless testing*) resmi Streamlit `AppTest` dengan hasil **0 Exception**:

```powershell
.\asiancup_env\Scripts\python.exe -c "
from streamlit.testing.v1 import AppTest
pages = [
    'app/main.py',
    'app/pages/1_🏆_Peluang_24_Tim_Peserta.py',
    'app/pages/2_🇮🇩_Peluang_8_Besar_Timnas_Indonesia.py',
    'app/pages/3_🧮_Simulator_Pertandingan_Interaktif.py',
    'app/pages/4_⭐_Analisis_Mikro_Pemain_Kunci_&_Keberuntungan.py'
]
for p in pages:
    at = AppTest.from_file(p).run(timeout=35)
    assert not at.exception, f'Kendala pada {p}: {at.exception}'
    print(f'Terverifikasi Berhasil: {p}')
print('Seluruh 5 modul halaman aplikasi lolos pengujian: 0 Exceptions!')
"
```

---

## 📄 Lisensi
Hak Cipta © 2026 Divisi Sains Data & Analitika Kuantitatif Olahraga. Dilisensikan di bawah [Lisensi MIT](LICENSE).
