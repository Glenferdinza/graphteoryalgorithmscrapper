# Water Ambulance Routing System - Project Summary

## Overview Proyek

Proyek ini mengimplementasikan sistem routing untuk ambulans air di Jakarta dengan menggunakan 9 algoritma pencarian jalur terpendek pada jaringan nyata yang menghubungkan 8 dermaga dengan 8 rumah sakit di wilayah perairan Jakarta.

## File-File Utama

### 1. water_ambulance_routing.py
Script utama yang berisi implementasi lengkap sistem routing ambulans air mencakup:
- Class JakartaWaterwaysNetwork: Definisi graf jaringan perairan Jakarta dengan 16 nodes dan 29 edges
- Class RoutingAlgorithms: Implementasi 9 algoritma (DFS, BFS, Dijkstra, A*, Bellman-Ford, Floyd-Warshall, Johnson, Topological Sort, Multi-Source BFS)
- Main execution: Benchmark performa dan generasi visualisasi dasar
- Output: CSV results dan 4 visualisasi utama

### 2. generate_enhanced_viz.py
Script untuk membuat 5 visualisasi tambahan yang lebih mendalam:
- Multi-metric analysis (4 panel comparison)
- Efficiency scatter plot (computational vs quality)
- Radar complexity chart (multi-dimensional characteristics)
- Comprehensive ranking table (performance scorecard)
- Path complexity analysis (stops vs time trade-off)

### 3. generate_network.py
Script untuk mengkonversi data algoritma menjadi network graph untuk Gephi:
- Generate nodes.csv (algoritma sebagai nodes)
- Generate edges.csv (similarity berdasarkan execution time)
- Threshold: dua algoritma terhubung jika selisih execution time < 3000ms
- Edge weight: 1 / (selisih + 1)

## Hasil Implementasi

### Studi Kasus
Rute: Dermaga Muara Angke (D1) ke RS Siloam Kebon Jeruk (H1)

### Hasil Optimal (50 menit, 3 pemberhentian)
Ditemukan oleh: Dijkstra, Bellman-Ford, Floyd-Warshall, Johnson, Topological Sort
Rute: D1 → D5 (Dermaga Muara Karang) → D6 (Dermaga Pluit) → H1

### Hasil Suboptimal (55 menit, 2 pemberhentian)
Ditemukan oleh: DFS, BFS, A*, Multi-Source BFS
Rute: D1 → H3 (RSPI Puri Indah) → H1

### Best Algorithm: Dijkstra
- Waktu tempuh: 50 menit (optimal)
- Iterations: 11 (efficient)
- Execution time: 0.095 ms (fast)
- Balance terbaik antara optimality dan computational efficiency

## Visualisasi yang Dihasilkan

### Basic Visualizations (dari water_ambulance_routing.py)
1. network_map.png - Peta lengkap jaringan waterways Jakarta
2. optimal_route.png - Visualisasi rute optimal dengan highlighted path
3. algorithm_comparison.png - Bar chart perbandingan waktu tempuh
4. path_details.png - Tabel detail rute setiap algoritma

### Enhanced Visualizations (dari generate_enhanced_viz.py)
5. multi_metric_analysis.png - 4 panel dashboard (time, stops, iterations, exec time)
6. efficiency_scatter.png - Scatter plot computational efficiency vs solution quality
7. radar_complexity.png - Radar chart karakteristik multi-dimensional
8. comprehensive_ranking.png - Tabel ranking dengan color-coded performance tiers
9. path_complexity.png - Grouped bar chart trade-off stops vs travel time

### Network for Gephi (dari generate_network.py)
10. nodes.csv - 9 algoritma sebagai nodes
11. edges.csv - Koneksi berdasarkan similarity execution time

## Dokumentasi

### ROUTING_DOCUMENTATION.md
Dokumentasi lengkap untuk 4 visualisasi dasar dengan penjelasan:
- Deskripsi sistem dan network structure
- Analisis setiap grafik dalam format paragraf deskriptif
- Computational performance comparison
- Kesimpulan implementasi dan rekomendasi

### ENHANCED_VISUALIZATION_DOC.md
Dokumentasi untuk 5 visualisasi enhanced dengan penjelasan:
- Multi-metric analysis interpretation
- Efficiency trade-off insights
- Radar chart profiling
- Comprehensive ranking methodology
- Path complexity paradox explanation

## Data Output

### CSV Files
- csv/ambulance_routing_results.csv - Hasil benchmark 9 algoritma
- csv/nodes.csv - Nodes untuk Gephi
- csv/edges.csv - Edges untuk Gephi
- csv/network_summary.csv - Summary statistik network

## Cara Menjalankan

1. Install dependencies:
```
pip install pandas numpy matplotlib seaborn plotly networkx kaleido
```

2. Jalankan implementasi routing:
```
python water_ambulance_routing.py
```

3. Generate enhanced visualizations:
```
python generate_enhanced_viz.py
```

4. Generate network untuk Gephi:
```
python generate_network.py
```

## Key Findings

1. Dijkstra adalah algoritma terbaik untuk routing ambulans air Jakarta dengan balance optimal antara solution quality dan computational efficiency

2. Rute optimal memerlukan lebih banyak pemberhentian (3 stops) namun total waktu lebih cepat (50 min) dibanding rute sederhana (2 stops, 55 min)

3. Algoritma uninformed search (DFS, BFS) gagal menemukan solusi optimal meskipun sangat cepat secara komputasi

4. A* dengan Euclidean heuristic kurang efektif untuk waterways routing karena jalur air tidak selalu straight-line

5. Floyd-Warshall menggunakan 4096 iterasi untuk menemukan solusi yang sama dengan Dijkstra yang hanya butuh 11 iterasi - clear overkill untuk single-pair shortest path

## Aplikasi Real-World

Sistem ini dapat diaplikasikan untuk:
- Emergency medical response di wilayah perairan Jakarta
- Optimasi rute patrol ambulans air
- Decision support system untuk dispatcher
- Training simulator untuk operator ambulans air
- Basis evaluasi penambahan dermaga atau RS baru dalam network

## Future Development

1. Dynamic routing dengan real-time traffic dan weather conditions
2. Multi-objective optimization (waktu, biaya, kapasitas)
3. Integration dengan GPS dan AIS (Automatic Identification System)
4. Machine learning untuk prediksi congestion patterns
5. Mobile app untuk crew ambulans air

## Kesimpulan

Implementasi ini berhasil mendemonstrasikan aplikasi praktis dari 9 algoritma graph theory dalam solving real-world routing problem untuk ambulans air Jakarta dengan comprehensive analysis dari berbagai perspektif computational dan operational yang menghasilkan actionable insights untuk deployment sistem emergency medical response di wilayah perairan metropolitan.
