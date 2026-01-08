# Dokumentasi Grafik Presentasi
## Water Ambulance Routing - Jakarta Waterways Network

Folder ini berisi visualisasi yang telah disiapkan untuk mendukung presentasi tugas akhir mengenai sistem routing ambulans air di jaringan perairan Jakarta.

## Daftar Grafik dan Penjelasannya

### Grafik 1: Analisis Multi-Metrik Performa 9 Algoritma Routing

File: 1_multi_metric_comparison.png

Grafik ini menampilkan perbandingan komprehensif dari sembilan algoritma routing berdasarkan empat metrik kinerja utama yang disajikan dalam bentuk subplot. Metrik pertama adalah waktu tempuh yang mengukur total durasi perjalanan dari titik awal hingga tujuan, di mana algoritma Dijkstra, Bellman-Ford, Floyd-Warshall, Johnson, dan Topological Sort berhasil mencapai waktu optimal 50 menit yang ditandai dengan warna hijau, sementara DFS, BFS, A*, dan Multi-Source BFS menghasilkan waktu suboptimal 55 menit yang ditandai dengan warna merah. Metrik kedua menunjukkan jumlah pemberhentian atau panjang jalur yang dilewati oleh setiap algoritma, memberikan gambaran tentang kompleksitas rute yang dihasilkan. Metrik ketiga mengukur jumlah iterasi algoritma yang menggambarkan efisiensi komputasi, di mana terlihat perbedaan signifikan antara algoritma yang efisien seperti Dijkstra dengan 11 iterasi dan Floyd-Warshall yang memerlukan 4096 iterasi. Metrik keempat adalah execution time yang mengukur kecepatan komputasi aktual dalam milidetik, menunjukkan bahwa Dijkstra merupakan yang tercepat dengan 0.095 ms sedangkan Floyd-Warshall paling lambat dengan 1.788 ms. Grafik ini sangat berguna untuk menunjukkan bahwa meskipun beberapa algoritma menghasilkan solusi optimal yang sama, efisiensi komputasi mereka sangat berbeda, sehingga pemilihan algoritma tidak hanya bergantung pada kualitas solusi tetapi juga pada kebutuhan kecepatan pemrosesan. Dalam konteks presentasi, grafik ini sebaiknya digunakan setelah menjelaskan metodologi penelitian untuk memberikan gambaran menyeluruh tentang performa setiap algoritma sebelum masuk ke analisis yang lebih detail.

### Grafik 2: Efisiensi Komputasi vs Kualitas Solusi

File: 2_efficiency_scatter.png

Grafik scatter plot ini dirancang untuk memvisualisasikan hubungan antara efisiensi komputasi dan kualitas solusi yang dihasilkan oleh setiap algoritma. Sumbu horizontal menggunakan skala logaritmik untuk menampilkan jumlah iterasi, sementara sumbu vertikal menunjukkan waktu eksekusi dalam milidetik, dengan ukuran marker yang mewakili waktu tempuh perjalanan dan warna yang membedakan antara algoritma optimal berwarna hijau dan suboptimal berwarna merah. Posisi Dijkstra di kuadran kiri bawah menunjukkan sweet spot yaitu kombinasi ideal antara jumlah iterasi rendah, waktu eksekusi cepat, dan menghasilkan solusi optimal. Sebaliknya, Floyd-Warshall berada di kuadran kanan atas yang menandakan pendekatan brute-force dengan iterasi tinggi dan eksekusi lambat meskipun menghasilkan solusi optimal. Algoritma seperti DFS dan BFS menunjukkan kecepatan eksekusi yang baik tetapi gagal menghasilkan jalur optimal, membuktikan bahwa kecepatan komputasi saja tidak menjamin kualitas solusi. Grafik ini memberikan insight visual yang kuat tentang trade-off antara kecepatan komputasi dan kualitas solusi, membantu audiens memahami mengapa Dijkstra unggul tidak hanya dari satu aspek tetapi dari kombinasi optimal antara efisiensi dan akurasi. Dalam presentasi, grafik ini cocok digunakan setelah analisis multi-metrik untuk memperkuat argumen bahwa Dijkstra adalah pilihan terbaik untuk aplikasi real-time routing ambulans air.

### Grafik 3: Radar Perbandingan Karakteristik Algoritma

File: 3_radar_characteristics.png

Grafik radar ini menyajikan perbandingan karakteristik sembilan algoritma berdasarkan empat dimensi yang dinormalisasi ke skala 0-100, di mana skor yang lebih tinggi menunjukkan performa yang lebih baik. Dimensi pertama adalah kecepatan rute yang mengukur seberapa optimal jalur yang dihasilkan dari segi waktu tempuh. Dimensi kedua adalah kesederhanaan path yang mengevaluasi kompleksitas rute berdasarkan jumlah pemberhentian. Dimensi ketiga adalah efisiensi iterasi yang mengukur seberapa efisien algoritma dalam mencapai solusi. Dimensi keempat adalah kecepatan komputasi yang menilai execution time algoritma. Polygon Dijkstra menunjukkan area yang besar dan seimbang di semua dimensi, mengindikasikan performa yang konsisten tinggi di setiap aspek. Bellman-Ford memiliki pola serupa dengan Dijkstra tetapi sedikit lebih kecil terutama di dimensi kecepatan komputasi. Floyd-Warshall menunjukkan keunggulan di kualitas rute tetapi polygon-nya menyempit drastis di dimensi efisiensi iterasi dan kecepatan komputasi. Algoritma DFS dan BFS menunjukkan polygon yang kecil di dimensi kecepatan rute meskipun cukup baik di kecepatan komputasi. Grafik ini efektif untuk menunjukkan profil lengkap setiap algoritma secara visual, memudahkan audiens untuk mengidentifikasi kekuatan dan kelemahan relatif setiap pendekatan. Dalam presentasi, grafik ini dapat digunakan pada tahap mid-presentation untuk memberikan deep dive analysis dan membantu audiens memahami bahwa pemilihan algoritma memerlukan pertimbangan multidimensional, bukan hanya berdasarkan satu metrik saja.

### Grafik 4: Ranking Komprehensif Algoritma Routing Ambulans Air

File: 4_ranking_table.png

Tabel ranking ini menyajikan evaluasi komprehensif dari sembilan algoritma dalam format yang terstruktur dan mudah dibaca dengan sistem color-coding untuk kategori performa. Tabel ini mencakup kolom rank yang menunjukkan posisi keseluruhan, nama algoritma, waktu tempuh dalam menit, jumlah pemberhentian, jumlah iterasi, execution time dalam milidetik, dan overall score yang merupakan skor gabungan dari berbagai metrik. Sistem pewarnaan menggunakan hijau untuk algoritma dengan rank 1-5 yang dikategorikan sebagai excellent, kuning untuk rank 6-7 sebagai good, dan merah untuk rank 8-9 sebagai fair. Dijkstra menduduki peringkat pertama dengan overall score 2.5 yang merupakan hasil kombinasi dari time rank, speed rank, dan setengah dari iteration rank, menunjukkan superioritas yang signifikan dibandingkan peringkat kedua Bellman-Ford dengan score 5.0. Topological Sort berada di peringkat ketiga dengan score 5.5 menunjukkan bahwa meskipun menghasilkan solusi optimal, efisiensi komputasinya sedikit di bawah Dijkstra. Johnson dan Floyd-Warshall melengkapi top 5 dengan score 8.5 dan 13.5, di mana Floyd-Warshall meskipun optimal memiliki score yang lebih rendah karena jumlah iterasi yang sangat tinggi. Tabel ini berfungsi sebagai quick reference yang memungkinkan audiens untuk dengan cepat membandingkan semua metrik penting dan memahami basis objektif dari rekomendasi penggunaan algoritma tertentu. Dalam presentasi, tabel ini sangat efektif digunakan menjelang akhir sebelum kesimpulan untuk memberikan rangkuman komprehensif dan memperkuat argumentasi bahwa Dijkstra adalah pilihan terbaik berdasarkan evaluasi multidimensional.

### Grafik 5: Analisis Kompleksitas Rute Pemberhentian vs Waktu Tempuh

File: 5_path_complexity.png

Grafik bar chart ini menampilkan hubungan antara jumlah pemberhentian dan waktu tempuh untuk setiap algoritma dengan color-coding yang membedakan kategori optimal dan suboptimal. Sumbu horizontal menampilkan nama sembilan algoritma yang diuji, sementara sumbu vertikal menunjukkan jumlah pemberhentian atau path length, dengan label waktu tempuh ditampilkan di atas setiap batang. Warna hijau digunakan untuk algoritma yang menghasilkan waktu optimal 50 menit yaitu Dijkstra, Bellman-Ford, Floyd-Warshall, Johnson, dan Topological Sort, sedangkan warna merah untuk algoritma suboptimal dengan waktu 55 menit yaitu DFS, BFS, A*, dan Multi-Source BFS. Insight penting dari grafik ini adalah bahwa semua algoritma menghasilkan rute dengan jumlah pemberhentian yang sama yaitu 4 lokasi, namun waktu tempuhnya berbeda karena perbedaan jalur yang dipilih dan bobot edge yang dilalui. Grafik ini secara efektif mendemonstrasikan konsep fundamental dalam graph theory bahwa shortest path dalam weighted graph tidak sama dengan minimum hop path, di mana yang optimal adalah yang meminimalkan total bobot bukan jumlah node. Perbedaan 5 menit antara kategori optimal dan suboptimal mungkin terlihat kecil dalam angka, tetapi dalam konteks emergency response ambulans air, perbedaan ini dapat menjadi krusial dalam menyelamatkan nyawa. Grafik ini sebaiknya digunakan setelah menjelaskan optimal path untuk mengklarifikasi kepada audiens bahwa kompleksitas routing tidak hanya soal berapa kali berhenti tetapi juga tentang memilih jalur dengan total waktu minimum, sehingga memperkuat pemahaman tentang pentingnya menggunakan algoritma yang mempertimbangkan edge weights secara tepat.

### Grafik 6: Visualisasi Rute Optimal Jaringan Perairan Jakarta

File: 6_optimal_route_map.png

Grafik peta interaktif ini merupakan visualisasi implementasi nyata dari sistem routing ambulans air di jaringan perairan Jakarta yang menampilkan 8 dermaga sebagai titik awal yang ditandai dengan marker biru, 8 rumah sakit sebagai titik tujuan yang ditandai dengan marker merah, dan jalur air yang menghubungkan lokasi-lokasi tersebut yang digambarkan dengan garis biru muda. Rute optimal yang ditemukan oleh algoritma Dijkstra ditampilkan dengan garis tebal berwarna emas yang menghubungkan Dermaga Muara Angke sebagai start point, melewati Dermaga Ancol, Dermaga Sunda Kelapa, dan berakhir di RS Siloam Kebon Jeruk sebagai finish point. Setiap segmen perjalanan dilengkapi dengan annotation yang menunjukkan nomor step dan waktu tempuh per segmen, yaitu Step 1 dari D1 ke D5 memakan waktu 15 menit, Step 2 dari D5 ke D6 memakan waktu 20 menit, dan Step 3 dari D6 ke H1 memakan waktu 15 menit, menghasilkan total waktu tempuh 50 menit. Marker START dengan ikon bendera hijau ditempatkan di titik awal D1 dan marker FINISH dengan ikon bendera merah di titik akhir H1, sedangkan directional arrows berwarna oranye ditambahkan untuk menunjukkan arah perjalanan secara jelas. Information box di sudut kiri atas peta menampilkan ringkasan rute optimal termasuk sequence path lengkap, total waktu tempuh, dan jumlah pemberhentian. Visualisasi ini memberikan konteks real-world yang konkret dari penelitian, menunjukkan bahwa algoritma tidak hanya bekerja secara teoritis tetapi dapat diimplementasikan pada geografi aktual Jakarta untuk aplikasi emergency response. Peta ini menjadi bukti nyata bahwa sistem routing yang dikembangkan dapat membantu mengurangi response time ambulans air dalam situasi darurat, di mana perbedaan beberapa menit dapat menentukan keselamatan pasien. Dalam presentasi, grafik ini adalah core slide yang wajib ada dan sebaiknya ditempatkan setelah pembahasan analisis performa untuk menunjukkan implementasi praktis dan impact nyata dari penelitian, sehingga audiens dapat melihat aplikasi langsung dari semua analisis teoretis yang telah dijelaskan sebelumnya.

### Grafik 7: Tabel Perbandingan Detail Rute Setiap Algoritma

File: 7_path_details.png

Tabel detail ini menyajikan perbandingan lengkap rute yang dihasilkan oleh setiap algoritma dalam format yang sistematis dengan kolom algorithm name, path sequence, travel time, dan path length. Tabel ini mengungkapkan pola konvergensi yang menarik di mana lima algoritma optimal yaitu Dijkstra, Bellman-Ford, Floyd-Warshall, Johnson, dan Topological Sort semuanya menemukan rute yang identik yaitu D1 menuju D5 menuju D6 menuju H1 dengan waktu tempuh 50 menit. Konvergensi ini merupakan indikator kuat dari correctness solusi karena algoritma yang berbeda dengan pendekatan yang berbeda mencapai hasil yang sama, memvalidasi bahwa rute tersebut memang merupakan true optimal path. Sebaliknya, empat algoritma suboptimal menunjukkan divergensi dengan menghasilkan rute yang berbeda-beda, misalnya DFS menemukan rute D1 menuju D3 menuju D7 menuju H1, sementara BFS, A*, dan Multi-Source BFS menemukan rute D1 menuju D2 menuju H2 menuju H1, keduanya dengan waktu tempuh 55 menit yang lebih lambat 10 persen dari rute optimal. Perbedaan ini menjelaskan mengapa algoritma-algoritma tersebut dikategorikan sebagai suboptimal dalam konteks weighted graph routing, karena mereka tidak mempertimbangkan edge weights dengan tepat atau menggunakan strategi yang tidak cocok untuk masalah shortest path pada graf berbobot. Tabel ini sangat berguna untuk menjawab pertanyaan teknis tentang mengapa beberapa algoritma gagal menemukan rute optimal meskipun semuanya berhasil menemukan path dari start ke goal. Dalam presentasi, tabel ini dapat digunakan sebagai optional slide atau backup slide untuk sesi tanya jawab, terutama jika ada pertanyaan mendalam tentang detail implementasi atau validasi hasil, membantu memperkuat kredibilitas penelitian dengan menunjukkan bahwa hasil telah diverifikasi melalui multiple independent algorithms.

---

### **TIER 3: TECHNICAL DETAILS (Optional/Backup)**

#### **Algorithm Comparison Bar Chart**
**File**: `8_algorithm_comparison.png` (dari `img/algorithm_comparison.html`)

**Deskripsi**:
Simple horizontal bar chart execution time comparison.

**Kapan Digunakan**: Backup slide jika butuh simplifikasi Graph 1

---

## **Panduan Penggunaan di PPT**

### **Struktur PPT yang Direkomendasikan**

```
BAGIAN 1: INTRODUCTION (3-4 slides)
├─ Slide 1: Judul & Identitas
├─ Slide 2: Latar Belakang (Jakarta Waterways + Emergency Response Need)
├─ Slide 3: Problem Statement (Rute D1 → H1 optimal?)
└─ Slide 4: Metodologi (9 Algoritma, Network Structure)

BAGIAN 2: ANALISIS PERFORMA (4-5 slides) ⭐
├─ Slide 5: [GRAPH 1] Multi-Metric Comparison
├─ Slide 6: [GRAPH 2] Efficiency Scatter Plot
├─ Slide 7: [GRAPH 3] Radar Characteristics (Top 5)
├─ Slide 8: [GRAPH 4] Ranking Table
└─ Slide 9: [GRAPH 5] Path Complexity (Optional)

BAGIAN 3: IMPLEMENTASI NYATA (3-4 slides) ⭐⭐⭐
├─ Slide 10: Network Structure Definition
│   └─ 16 nodes, 29 edges, dermaga & RS locations
├─ Slide 11: Dijkstra Implementation
│   └─ Pseudocode/Flowchart
├─ Slide 12: [GRAPH 6] OPTIMAL ROUTE MAP ⭐⭐⭐
│   └─ D1 → D5 → D6 → H1 with annotations
└─ Slide 13: [GRAPH 7] Path Comparison Table

BAGIAN 4: KESIMPULAN (2-3 slides)
├─ Slide 14: Summary Findings
│   ├─ Dijkstra = Best overall
│   ├─ Floyd-Warshall = Optimal tetapi inefficient
│   └─ DFS/BFS/A* = Suboptimal untuk weighted graphs
├─ Slide 15: Rekomendasi & Impact
│   └─ Dijkstra for real-time ambulance routing
└─ Slide 16: Future Work & Q&A

APPENDIX (Backup slides)
├─ Detail hasil benchmark
├─ Code implementation
└─ Additional charts
```

---

## **Tips Presentasi**

### **Untuk Setiap Grafik:**

1. **Build Progression**: 
   - Jangan tampilkan semua data sekaligus
   - Gunakan animation: Reveal bar/line satu per satu
   - Highlight key findings dengan laser pointer atau animation

2. **Color Consistency**:
   - 🟢 **Hijau** = Optimal/Good/Success
   - 🔴 **Merah** = Suboptimal/Warning/Attention
   - 🔵 **Biru** = Neutral/Information
   - 🟡 **Kuning/Gold** = Optimal Path/Best Choice

3. **Annotations**:
   - Tambahkan **callout boxes** untuk key insights
   - Gunakan **arrows** untuk point ke data penting
   - Tambahkan **text highlights** untuk winner algorithm

4. **Timing**:
   - **Graph 1-5**: 1-2 menit per slide
   - **Graph 6 (Optimal Route)**: 3-4 menit (CORE SLIDE) ⭐
   - **Graph 7**: 1 menit
   - **Total visualization time**: ~12-15 menit

---

## **Key Messages untuk Setiap Grafik**

| Grafik | Key Message 1 | Key Message 2 | Key Message 3 |
|--------|---------------|---------------|---------------|
| **Graph 1** | Dijkstra = Fastest (0.095ms) | 5 optimal, 4 suboptimal | Floyd: Optimal but 18x slower |
| **Graph 2** | Dijkstra = Sweet spot | Floyd = Brute force | DFS/BFS = Fast but wrong |
| **Graph 3** | Dijkstra = Balanced | Trade-offs visible | A* failed (bad heuristic) |
| **Graph 4** | Clear ranking: Dijkstra #1 | Overall score: 2.5 vs 5.0 | Top 5 all optimal |
| **Graph 5** | Same hops, different time | Weights matter, not hops | Optimal ≠ Minimum stops |
| **Graph 6** | **REAL IMPLEMENTATION** | D1→D5→D6→H1 = 50 min | Step-by-step visualization |
| **Graph 7** | Optimal converge same path | Suboptimal diverge | Validates correctness |

---

## **Quick Reference: Kapan Pakai Grafik Apa**

### **Jika Waktu Terbatas (10 slides total)**:
**MUST INCLUDE**:
1. Graph 1: Multi-Metric
2. Graph 4: Ranking Table
3. **Graph 6: Optimal Route Map** ⭐⭐⭐
4. Graph 7: Path Details

### **Jika Waktu Cukup (15 slides)**:
**INCLUDE**:
1. Graph 1: Multi-Metric
2. Graph 2: Efficiency Scatter
3. Graph 4: Ranking Table
4. Graph 5: Path Complexity
5. **Graph 6: Optimal Route Map** ⭐⭐⭐
6. Graph 7: Path Details

### **Jika Waktu Banyak (18+ slides)**:
**ALL IN**:
1. Graph 1: Multi-Metric
2. Graph 2: Efficiency Scatter
3. Graph 3: Radar Chart
4. Graph 4: Ranking Table
5. Graph 5: Path Complexity
6. **Graph 6: Optimal Route Map** ⭐⭐⭐
7. Graph 7: Path Details
8. + Additional technical details

---

## **CRITICAL: Graph 6 (Optimal Route) adalah JANTUNG Presentasi!**

**WHY?**
- **Proof of concept**: Showing it actually works in real Jakarta waterways
- **Visual impact**: Maps always engage audience better than charts
- **Non-technical friendly**: Anyone can understand a route on a map
- **Real-world relevance**: Emergency ambulance routing = life-saving application
- **Validates all analysis**: All the benchmarks lead to THIS result

**Tanpa Graph 6**:
- Presentasi terlalu abstrak/theoretical
- Audience bertanya: "Jadi hasilnya gimana?"
- Tidak ada "wow factor"
- Susah jelasin real-world impact

**Dengan Graph 6**:
- "Ini lho rute ambulans air yang optimal!"
- Clear start → steps → finish
- Concrete numbers: 50 menit, 4 locations
- Comparison visible: Why 55 min route is worse

---

## **File Management**

### **Source Files** (jangan hapus):
- `img/multi_metric_analysis.png`
- `img/efficiency_scatter.png`
- `img/radar_complexity.png`
- `img/comprehensive_ranking.png`
- `img/path_complexity.png`
- `img/network_map.html` (interactive)
- `img/optimal_route.html` (interactive)
- `img/path_details.png`

### **Copy ke Folder Ini**:
```bash
# Run untuk copy semua grafik
Copy-Item "img/multi_metric_analysis.png" "ppt_graphs/1_multi_metric_comparison.png"
Copy-Item "img/efficiency_scatter.png" "ppt_graphs/2_efficiency_scatter.png"
Copy-Item "img/radar_complexity.png" "ppt_graphs/3_radar_characteristics.png"
Copy-Item "img/comprehensive_ranking.png" "ppt_graphs/4_ranking_table.png"
Copy-Item "img/path_complexity.png" "ppt_graphs/5_path_complexity.png"
Copy-Item "img/network_map.png" "ppt_graphs/6_optimal_route_map.png"  # After generating
Copy-Item "img/path_details.png" "ppt_graphs/7_path_details.png"
```

---

## **Untuk Sidang/Defense**

### **Antisipasi Pertanyaan**:

**Q1: "Kenapa Dijkstra paling baik?"**
→ Show Graph 1 + Graph 2: Optimal path + Fastest execution + Minimal iterations

**Q2: "Kenapa A* tidak optimal?"**
→ Explain: Euclidean heuristic kurang cocok untuk waterways (not straight-line distance)

**Q3: "Apakah rute ini sudah divalidasi?"**
→ Show Graph 7: 5 optimal algorithms converge ke same path (validates correctness)

**Q4: "Kalau graph-nya lebih besar gimana?"**
→ Graph 3 (jika ada scalability): Dijkstra scales better than Floyd-Warshall

**Q5: "Implementasi nyata di mana?"**
→ **Show Graph 6**: Ini rute konkret di Jakarta Waterways

---

## **Support**

Jika ada pertanyaan tentang grafik atau butuh modifikasi:
1. Check source files di folder `img/`
2. Re-run scripts:
   - `python generate_enhanced_viz.py` (untuk Graph 1-5)
   - `python water_ambulance_routing.py` (untuk Graph 6-7)
3. Adjust layout/colors di source code

---

## **Checklist Sebelum Presentasi**

- [ ] Semua 7 grafik sudah di-copy ke folder `ppt_graphs/`
- [ ] Graph 6 (Optimal Route) sudah di-generate dengan annotations lengkap
- [ ] Sudah cek resolusi semua PNG (minimal 1400x700, scale=2)
- [ ] Sudah prepare backup slides (appendix)
- [ ] Sudah prepare answers untuk anticipated questions
- [ ] Sudah test animation/transitions di PPT
- [ ] Sudah print backup hardcopy grafik (jika diperlukan)

---

_Project: Water Ambulance Routing - Jakarta Waterways Network_
_Algorithms: 9 (Dijkstra, Bellman-Ford, Floyd-Warshall, Johnson, Topological Sort, DFS, BFS, A*, Multi-Source BFS)_
