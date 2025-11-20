# Graph Theory Algorithms Implementation

Water Ambulance Routing System - Jakarta Waterways Network

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)

Implementasi dan analisis komprehensif 9 algoritma pencarian jalur terpendek untuk sistem routing ambulans air di Jakarta. Project ini mencakup benchmark performance analysis, implementasi real-world network, visualisasi interaktif, dan network analysis menggunakan Gephi.

## Quick Links

📚 **[FAQ - Frequently Asked Questions](FAQ_PROJECT.md)** - Penjelasan detail tentang routing paths, algoritma, network specifications, dan struktur file  
📖 **[Routing Documentation](ROUTING_DOCUMENTATION.md)** - Panduan lengkap sistem routing ambulans air  
📊 **[Enhanced Visualization Docs](ENHANCED_VISUALIZATION_DOC.md)** - Dokumentasi visualisasi lanjutan  
🔧 **[Gephi Guide](GEPHI_GUIDE.md)** - Tutorial lengkap Gephi network visualization  
⚡ **[Gephi Quickstart](GEPHI_QUICKSTART.md)** - Quick reference untuk Gephi  
📝 **[Project Summary](PROJECT_SUMMARY.md)** - Ringkasan komprehensif project

## Deskripsi Project

Project ini terdiri dari 3 komponen utama:

### 1. Benchmark Performance Analysis
Analisis komparatif mendalam terhadap 9 algoritma graf:

- **DFS (Depth-First Search)** - Traversal dengan eksplorasi mendalam
- **BFS (Breadth-First Search)** - Traversal level-by-level  
- **Dijkstra** - Single-source shortest path untuk weighted graph
- **Bellman-Ford** - Shortest path dengan support negative weights
- **A*** - Heuristic-based optimal pathfinding
- **Topological Sort** - Linearization untuk directed acyclic graphs
- **Multi-Source BFS** - Multiple starting points untuk multi-ambulance
- **Floyd-Warshall** - All-pairs shortest path
- **Johnson's Algorithm** - Efficient all-pairs untuk sparse graphs

Dataset: 2,152 benchmark records dengan 3 graph sizes (small, medium, large)

### 2. Real-World Implementation: Jakarta Waterways Network
Implementasi sistem routing ambulans air dengan:
- **16 Nodes**: 8 dermaga + 8 rumah sakit
- **26 Edges**: Jalur air dengan waktu tempuh real
- **Network Density**: 0.217 (connected graph)
- **Studi Kasus**: Dermaga Muara Angke → RS Siloam Kebon Jeruk

**Hasil Optimal Route:**
- Path: D1 (Muara Angke) → D5 (Muara Karang) → D6 (Pluit) → H1 (Siloam)
- Total Time: 50 menit
- Stops: 3 pemberhentian
- Best Algorithm: Dijkstra (optimal + efficient)

### 3. Network Analysis & Visualization
- Machine Learning modeling (Random Forest R² ~0.94)
- 14 visualisasi profesional (static PNG + interactive HTML)
- Gephi network files untuk advanced graph analysis
- Comprehensive documentation dengan paragraf deskriptif

## Analisis Mencakup

### Performance Metrics
- Waktu eksekusi (execution time)
- Penggunaan memori (memory usage)
- Jumlah iterasi (iterations count)
- Kualitas jalur (path length)
- Skalabilitas pada berbagai ukuran graf

### Advanced Analysis
- Multi-metric comparison (4-panel dashboard)
- Efficiency scatter plot (computational vs quality trade-off)
- Radar chart (multi-dimensional characteristics)
- Comprehensive ranking scorecard
- Path complexity analysis

### Machine Learning
- Random Forest Regressor untuk prediksi execution time
- Feature importance analysis
- Model evaluation (R², RMSE, MAE)
- Training accuracy: ~0.94

## Instalasi dan Cara Menjalankan

### Prerequisites
- Python 3.13+ atau lebih tinggi
- pip (Python package manager)
- Jupyter Notebook atau VS Code dengan Jupyter extension

### Langkah Instalasi

1. **Clone repository**
```bash
git clone https://github.com/Glenferdinza/graphteoryalgorithmscrapper.git
cd graphteoryalgorithmscrapper
```

2. **Buat virtual environment** (opsional tapi disarankan)

Kalau ada folder `.venv` hasil clone, hapus dulu:
```bash
# Windows
rmdir /s .venv

# Linux/Mac
rm -rf .venv
```

Buat virtual environment baru:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Cara Menjalankan

#### 1. Generate Benchmark Data
```bash
python scraper.py
```
Output: `csv/data.csv` dengan 2,152 benchmark records

#### 2. Analisis Performance (Notebook)
Buka Jupyter atau VS Code:
```bash
jupyter notebook analysis.ipynb
```

Atau di VS Code:
- Buka `analysis.ipynb`
- Pilih kernel: `.venv` (Python 3.13+)
- Run all cells (Ctrl + Shift + K untuk select kernel)

Output:
- `csv/processed_data.csv` - Data processed
- `csv/algorithm_performance_summary.csv` - Summary statistics
- `execution_time_predictor.pkl` - ML model
- `img/ppt_graph_*.png` - 6 grafik presentasi

#### 3. Implementasi Routing Ambulans Air
```bash
python water_ambulance_routing.py
```

Output:
- `csv/ambulance_routing_results.csv` - Hasil routing 9 algoritma
- `img/network_map.png` & `.html` - Peta waterways Jakarta
- `img/optimal_route.png` & `.html` - Rute optimal
- `img/algorithm_comparison.png` - Performance comparison
- `img/path_details.png` - Detail rute per algoritma

#### 4. Generate Enhanced Visualizations
```bash
python generate_enhanced_viz.py
```

Output 5 visualisasi tambahan:
- `img/multi_metric_analysis.png` - 4-panel dashboard
- `img/efficiency_scatter.png` - Computational vs quality
- `img/radar_complexity.png` - Multi-dimensional radar
- `img/comprehensive_ranking.png` - Performance scorecard
- `img/path_complexity.png` - Stops vs time analysis

#### 5. Generate Network untuk Gephi

**Algorithm Similarity Network:**
```bash
python generate_network.py
```
Output:
- `csv/nodes.csv` - 9 algoritma
- `csv/edges.csv` - 6 koneksi (similarity < 3000ms)
- `csv/network_summary.csv` - Network statistics

**Waterways Network:**
```bash
python generate_waterways_gephi.py
```
Output:
- `csv/waterways_nodes.csv` - 16 lokasi (8 dermaga + 8 RS)
- `csv/waterways_edges.csv` - 26 jalur air
- `csv/optimal_path_nodes.csv` - Rute optimal highlight
- `csv/waterways_network_stats.csv` - Network metrics

### Import ke Gephi
Lihat panduan lengkap: `GEPHI_QUICKSTART.md` atau `GEPHI_GUIDE.md`

## Struktur Project

```
tugasakhir/
│
├── csv/                                   # Data Files
│   ├── data.csv                              # Raw benchmark data (2,152 records)
│   ├── processed_data.csv                    # Processed benchmark data
│   ├── algorithm_performance_summary.csv     # Performance summary statistics
│   ├── ambulance_routing_results.csv         # Routing results (9 algorithms)
│   │
│   ├── nodes.csv                             # Gephi: Algorithm nodes (9 nodes)
│   ├── edges.csv                             # Gephi: Algorithm edges (6 edges)
│   ├── network_summary.csv                   # Gephi: Algorithm network stats
│   │
│   ├── waterways_nodes.csv                   # Gephi: Waterways nodes (16 nodes)
│   ├── waterways_edges.csv                   # Gephi: Waterways edges (26 edges)
│   ├── optimal_path_nodes.csv                # Gephi: Optimal path highlight
│   └── waterways_network_stats.csv           # Gephi: Waterways network stats
│
├── img/                                   # Visualizations
│   ├── ppt_graph_1_execution_time.png        # Bar chart: Execution time comparison
│   ├── ppt_graph_2_multi_metric.png          # Grouped bar: Multi-metric normalized
│   ├── ppt_graph_3_scalability.png           # Line chart: Scalability analysis
│   ├── ppt_graph_4_heatmap.png               # Heatmap: Performance matrix
│   ├── ppt_graph_5_radar_top5.png            # Radar: Top 5 algorithms
│   ├── ppt_graph_6_summary_table.png         # Table: Comprehensive ranking
│   │
│   ├── network_map.png & .html               # Jakarta waterways network map
│   ├── optimal_route.png & .html             # Optimal route visualization
│   ├── algorithm_comparison.png & .html      # Algorithm performance bars
│   ├── path_details.png & .html              # Detailed path table
│   │
│   ├── multi_metric_analysis.png & .html     # 4-panel dashboard
│   ├── efficiency_scatter.png & .html        # Computational efficiency scatter
│   ├── radar_complexity.png & .html          # Multi-dimensional radar
│   ├── comprehensive_ranking.png & .html     # Performance scorecard
│   └── path_complexity.png & .html           # Path stops vs time analysis
│
├── Core Scripts
│   ├── scraper.py                            # Benchmark data generator
│   ├── analysis.ipynb                        # Main analysis notebook (Jupyter)
│   ├── water_ambulance_routing.py            # Real-world routing implementation
│   ├── generate_enhanced_viz.py              # Enhanced visualizations generator
│   ├── generate_network.py                   # Gephi algorithm network generator
│   └── generate_waterways_gephi.py           # Gephi waterways network generator
│
├── Documentation
│   ├── README.md                             # This file
│   ├── ROUTING_DOCUMENTATION.md              # Routing system documentation
│   ├── ENHANCED_VISUALIZATION_DOC.md         # Enhanced viz documentation
│   ├── PROJECT_SUMMARY.md                    # Comprehensive project summary
│   ├── GEPHI_GUIDE.md                        # Detailed Gephi tutorial
│   └── GEPHI_QUICKSTART.md                   # Quick Gephi reference
│
├── Configuration & Model
│   ├── requirements.txt                      # Python dependencies
│   ├── execution_time_predictor.pkl          # Trained ML model (Random Forest)
│   └── LICENSE                               # MIT License
│
└── .venv/                                 # Virtual environment (not in repo)
```

## File Details

### Data Files (csv/)

| File | Description | Size | Format |
|------|-------------|------|--------|
| `data.csv` | Raw benchmark data | 2,152 rows | algorithm, graph_size, nodes, edges, execution_time_ms, memory_usage_mb, path_length, iterations, complexity, source, timestamp |
| `processed_data.csv` | Processed with engineered features | 2,152 rows | Adds: graph_density, time_per_node, memory_per_node, iteration_efficiency, performance_score |
| `ambulance_routing_results.csv` | Routing results for D1→H1 | 9 rows | Algorithm, Path, Time (minutes), Path Length, Iterations, Execution Time (ms) |
| `nodes.csv` | Algorithm similarity nodes | 9 rows | Id, Label, AvgExecutionTime, StdExecutionTime, SampleCount |
| `edges.csv` | Algorithm similarity edges | 6 edges | Source, Target, Weight, ExecutionTimeDiff, Type |
| `waterways_nodes.csv` | Jakarta waterways nodes | 16 rows | Id, Label, Type, Latitude, Longitude, NodeSize, Color |
| `waterways_edges.csv` | Jakarta waterways edges | 26 edges | Source, Target, Type, Distance, Time, Weight, Label |

### Visualizations (img/)

**Benchmark Analysis (6 files):**
1. Execution time comparison - Horizontal bar chart
2. Multi-metric comparison - Grouped bars (normalized)
3. Scalability analysis - Line chart with markers
4. Performance heatmap - Color-coded matrix
5. Radar chart - Top 5 algorithms
6. Summary table - Comprehensive ranking

**Routing Implementation (4 files + HTML):**
7. Network map - Interactive Jakarta waterways
8. Optimal route - Highlighted path D1→D5→D6→H1
9. Algorithm comparison - Travel time bars
10. Path details - Route comparison table

**Enhanced Analysis (5 files + HTML):**
11. Multi-metric dashboard - 4-panel analysis
12. Efficiency scatter - Computational vs quality
13. Radar complexity - Multi-dimensional profiles
14. Comprehensive ranking - Color-coded scorecard
15. Path complexity - Stops vs time paradox

### Scripts

| Script | Purpose | Output |
|--------|---------|--------|
| `scraper.py` | Generate benchmark data | `csv/data.csv` |
| `analysis.ipynb` | Main analysis & ML | `csv/processed_data.csv`, `*.pkl`, `img/ppt_graph_*.png` |
| `water_ambulance_routing.py` | Routing implementation | `csv/ambulance_routing_results.csv`, `img/network_map.*`, `img/optimal_route.*` |
| `generate_enhanced_viz.py` | Advanced visualizations | `img/multi_metric_analysis.*`, `img/efficiency_scatter.*`, etc. |
| `generate_network.py` | Algorithm similarity network | `csv/nodes.csv`, `csv/edges.csv` |
| `generate_waterways_gephi.py` | Waterways network | `csv/waterways_nodes.csv`, `csv/waterways_edges.csv` |

### Documentation Files

- **README.md**: Panduan utama (file ini)
- **ROUTING_DOCUMENTATION.md**: Dokumentasi sistem routing dengan paragraf deskriptif untuk 4 visualisasi dasar
- **ENHANCED_VISUALIZATION_DOC.md**: Dokumentasi 5 visualisasi enhanced dengan penjelasan insight
- **PROJECT_SUMMARY.md**: Summary komprehensif project, findings, dan recommendations
- **GEPHI_GUIDE.md**: Tutorial lengkap step-by-step Gephi import & analysis
- **GEPHI_QUICKSTART.md**: Quick reference untuk Gephi (1-2 halaman)

## Network Specifications

### Algorithm Similarity Network (Gephi Network 1)
- **Nodes**: 9 algoritma
- **Edges**: 6 koneksi
- **Criteria**: Dua algoritma terhubung jika `|execution_time(A) - execution_time(B)| < 3000 ms`
- **Weight**: `1 / (|difference| + 1)` - Semakin mirip, weight semakin tinggi
- **Density**: 16.67%
- **Connected Components**: 1 (fully connected)
- **Isolated Nodes**: 3 (Floyd-Warshall, Johnson, Bellman-Ford)

**Connections:**
1. A* ↔ Dijkstra (diff: 2576 ms, weight: 0.000388)
2. A* ↔ Multi-Source BFS (diff: 1868 ms, weight: 0.000535)
3. BFS ↔ DFS (diff: 1168 ms, weight: 0.000855) ⭐ Highest weight
4. BFS ↔ Multi-Source BFS (diff: 2318 ms, weight: 0.000431)
5. BFS ↔ Topological Sort (diff: 2856 ms, weight: 0.000350)
6. DFS ↔ Topological Sort (diff: 1688 ms, weight: 0.000592)

### Jakarta Waterways Network (Gephi Network 2)
- **Nodes**: 16 lokasi
  - 8 Dermaga: D1-D8 (Muara Angke, Ancol, Kali Besar, Sunda Kelapa, Muara Karang, Pluit, Marunda, Tanjung Priok)
  - 8 Rumah Sakit: H1-H8 (Siloam Kebon Jeruk, RS Pluit, RSPI Puri Indah, RS Atmajaya, RS Husada, RS PIK, RS Premier Jatinegara, RS Koja)
- **Edges**: 26 jalur air
- **Network Density**: 0.217
- **Average Degree**: 3.25
- **Network Diameter**: 5 hops
- **Is Connected**: Yes

**Hub Locations (Highest Degree):**
1. D6 - Dermaga Pluit: 5 koneksi
2. H2 - RS Pluit: 5 koneksi
3. D3 - Dermaga Kali Besar: 4 koneksi
4. D4 - Dermaga Sunda Kelapa: 4 koneksi
5. D5 - Dermaga Muara Karang: 4 koneksi

**Optimal Route (Dijkstra Result):**
- **Path**: D1 → D5 → D6 → H1
- **Segments**:
  1. D1 (Muara Angke) → D5 (Muara Karang): 8 min
  2. D5 (Muara Karang) → D6 (Pluit): 10 min
  3. D6 (Pluit) → H1 (Siloam): 32 min
- **Total Time**: 50 menit
- **Stops**: 3 pemberhentian
- **Distance**: 7,800 meters

**Suboptimal Route (DFS/BFS/A* Result):**
- **Path**: D1 → H3 → H1
- **Segments**:
  1. D1 (Muara Angke) → H3 (RSPI Puri Indah): 35 min
  2. H3 (RSPI) → H1 (Siloam): 20 min
- **Total Time**: 55 menit
- **Stops**: 2 pemberhentian
- **Distance**: 8,800 meters

**Key Insight**: Rute optimal memerlukan lebih banyak stops (3 vs 2) namun total waktu lebih cepat (50 vs 55 menit) karena memanfaatkan jalur coastal dengan segment time lebih rendah.

## Hasil dan Findings

### Benchmark Performance Results

**Fastest Algorithms (Execution Time):**
1. DFS: 10,178 ms ⭐ Tercepat
2. Topological Sort: 8,490 ms
3. BFS: 11,347 ms
4. Multi-Source BFS: 13,665 ms
5. A*: 15,533 ms

**Slowest Algorithms:**
1. Floyd-Warshall: 61,310 ms ⭐ Terlambat
2. Bellman-Ford: 39,900 ms
3. Johnson: 33,914 ms

**Most Memory Efficient:**
- DFS & BFS: Paling hemat memori (traversal sederhana)

**Least Iterations:**
1. DFS: ~3 iterations
2. A*: ~5 iterations
3. BFS: ~7 iterations

### Routing Implementation Results (D1 → H1)

| Algorithm | Time (min) | Stops | Route | Iterations | Exec Time (ms) | Optimal? |
|-----------|-----------|-------|-------|-----------|----------------|----------|
| **Dijkstra** | **50** | 3 | D1→D5→D6→H1 | 11 | 0.095 | ✅ Yes |
| **Bellman-Ford** | **50** | 3 | D1→D5→D6→H1 | 390 | 0.427 | ✅ Yes |
| **Floyd-Warshall** | **50** | 3 | D1→D5→D6→H1 | 4096 | 1.788 | ✅ Yes |
| **Johnson** | **50** | 3 | D1→D5→D6→H1 | 683 | 0.771 | ✅ Yes |
| **Topological Sort** | **50** | 3 | D1→D5→D6→H1 | 16 | 0.204 | ✅ Yes |
| DFS | 55 | 2 | D1→H3→H1 | 3 | 0.046 | ❌ No |
| BFS | 55 | 2 | D1→H3→H1 | 7 | 0.038 | ❌ No |
| A* | 55 | 2 | D1→H3→H1 | 3 | 0.100 | ❌ No |
| Multi-Source BFS | 55 | 2 | D1→H3→H1 | 7 | 0.114 | ❌ No |

**Best Overall: Dijkstra**
- Optimal solution (50 min)
- Efficient computation (0.095 ms)
- Moderate iterations (11)
- Balance terbaik untuk real-time routing

**Paradox Finding:**
- Optimal route: 3 stops, 50 min ✅
- Suboptimal route: 2 stops, 55 min ❌
- **Kesimpulan**: Fewer stops ≠ faster route (weighted graph optimization)

### Machine Learning Results

**Random Forest Regressor for Execution Time Prediction:**
- Training R²: 0.9847
- Test R²: 0.9423 ⭐ Excellent
- Test RMSE: 4,127 ms
- Test MAE: 2,845 ms

**Top 3 Important Features:**
1. Iterations (importance: 0.42)
2. Nodes (importance: 0.28)
3. Graph Density (importance: 0.15)

**Interpretation**: Model dapat memprediksi execution time dengan akurasi 94.23% berdasarkan karakteristik graph dan algoritma.

## Key Insights & Recommendations

### 1. Algorithm Selection Guidelines

**For Real-Time Emergency Routing (Water Ambulance):**
- ✅ **Primary**: Dijkstra
  - Reason: Optimal solution + fast computation
  - Use case: Single source to single destination
  
- ✅ **Backup**: A* (if good heuristic available)
  - Reason: Faster with proper heuristic
  - Use case: Known geographic coordinates

- ❌ **Avoid**: Floyd-Warshall, Bellman-Ford
  - Reason: Overkill untuk single-pair shortest path
  - Use case: Hanya jika perlu all-pairs distances

**For Multi-Destination Planning:**
- ✅ Floyd-Warshall (compute once, query many times)
- ✅ Johnson (untuk sparse graphs)

**For Quick Approximation (Non-Critical):**
- ✅ BFS/DFS (sangat cepat, acceptable untuk non-emergency)

### 2. Network Design Insights

**Critical Hubs (High Degree Centrality):**
- D6 (Dermaga Pluit): 5 koneksi - **Strategic transit point**
- H2 (RS Pluit): 5 koneksi - **Accessible hospital**

**Recommendation**: Prioritize maintenance dan resource allocation untuk hub locations.

**Betweenness Centrality:**
- D6 Pluit sering dilalui di optimal paths
- **Recommendation**: Enhance capacity di D6 untuk handle high traffic

### 3. Route Optimization Strategy

**Coastal Route Advantage:**
- D1→D5→D6 coastal segments: 8+10 = 18 min
- Direct inland route: Often longer despite fewer stops

**Recommendation**: 
- Develop coastal waterway infrastructure
- Prioritize coastal dermaga maintenance
- Consider tidal/weather impact on coastal routes

### 4. Computational Efficiency

**Dijkstra Sweet Spot:**
- 25x faster than Floyd-Warshall (0.095 ms vs 1.788 ms)
- Same optimal result
- Scalable untuk real-time application

**Trade-off Analysis:**
- Fast algorithms (DFS/BFS): Quick but potentially suboptimal
- Optimal algorithms (Dijkstra): Balance speed + quality
- Comprehensive algorithms (Floyd-Warshall): Slow but complete

## Technical Specifications

### Software & Tools
- **Python**: 3.13.6
- **Jupyter**: For interactive analysis
- **Gephi**: 0.10.1 (network visualization)
- **Key Libraries**:
  - NetworkX 3.x (graph operations)
  - Pandas 2.x (data manipulation)
  - Plotly 5.x (interactive visualization)
  - Scikit-learn 1.x (machine learning)
  - Matplotlib & Seaborn (static plots)

### Performance Requirements
- **Memory**: ~500 MB for full analysis
- **CPU**: Multi-core recommended for ML training
- **Disk**: ~100 MB for data + visualizations
- **Runtime**: 
  - Scraper: ~2-3 minutes
  - Analysis notebook: ~5-8 minutes
  - Routing implementation: <1 second
  - Enhanced viz: ~10-15 seconds

### Scalability
- Tested on graphs: 10-1000 nodes
- Benchmark dataset: 2,152 records
- Waterways network: 16 nodes, 26 edges (realistic Jakarta scale)
- Gephi: Can handle up to 100K nodes (with proper hardware)

## Future Enhancements

### 1. Dynamic Routing
- Real-time traffic conditions
- Weather impact (tidal, wind, rain)
- Vessel availability tracking
- Dynamic weight adjustment

### 2. Multi-Objective Optimization
- Minimize time AND cost
- Maximize patient capacity
- Balance fuel efficiency
- Consider crew availability

### 3. Advanced Features
- Mobile app for crew
- GPS integration
- AIS (Automatic Identification System) tracking
- Machine learning untuk predict congestion
- Multi-ambulance coordination (fleet management)

### 4. Network Expansion
- Add more dermaga (coastal expansion)
- Include klinik/puskesmas as intermediate stops
- Consider river routes (Ciliwung, etc)
- Integration dengan land ambulance handoff points

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## Citation

If you use this project in academic work, please cite:

```bibtex
@software{waterambulance2025,
  author = {Glenferdinza},
  title = {Water Ambulance Routing System - Jakarta Waterways Network},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/Glenferdinza/graphteoryalgorithmscrapper}
}
```

## Troubleshooting

### Common Issues

**Issue: ModuleNotFoundError**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue: Kernel not found in Jupyter**
```bash
# Solution: Install ipykernel in venv
python -m pip install ipykernel
python -m ipykernel install --user --name=tugasakhir
```

**Issue: Gephi can't import CSV**
```bash
# Solution: Check CSV encoding (must be UTF-8)
# Re-run generate scripts if needed
```

**Issue: Plotly figures not showing**
```bash
# Solution: Install kaleido for static image export
pip install kaleido
```

### Getting Help

- 📧 Email: (add your email here)
- 💬 Issues: https://github.com/Glenferdinza/graphteoryalgorithmscrapper/issues
- 📚 Docs: See ROUTING_DOCUMENTATION.md dan GEPHI_GUIDE.md

## Acknowledgments

- Dataset inspiration: Real Jakarta waterways geography
- Algorithms: Classic graph theory textbooks
- Visualization: Plotly, Matplotlib, Seaborn communities
- Network analysis: Gephi consortium

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Project Status

✅ **Completed Components:**
- Benchmark data generation (2,152 records)
- Performance analysis (9 algorithms)
- Real-world routing implementation (Jakarta waterways)
- 14 professional visualizations
- Machine Learning modeling (R² 0.94)
- Gephi network exports
- Comprehensive documentation

🚧 **In Progress:**
- Mobile app development
- Real-time traffic integration
- Extended network coverage

📋 **Planned:**
- Cloud deployment
- API development
- Multi-language support

---

## Created By

**Glenferdinza**  
Graph Theory & Algorithms - Final Project 2025

*For academic purposes - Universitas (add university name)*

---

## Created By

**Glenferdinza**
