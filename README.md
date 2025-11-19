# Graph Theory Algorithms 

Comparative Study for Water Ambulance Routing

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

Studi komparatif terhadap 9 algoritma pencarian jalur terpendek (shortest path) untuk optimasi routing ambulans air. Project ini menganalisis performa algoritma graf dalam konteks navigasi waterway menggunakan dataset benchmark yang komprehensif.

## Deskripsi

Project ini merupakan analisis mendalam terhadap 9 algoritma graf yang diaplikasikan untuk sistem routing ambulans air:

- **DFS (Depth-First Search)** - Traversal dengan eksplorasi mendalam
- **BFS (Breadth-First Search)** - Traversal level-by-level
- **Dijkstra** - Single-source shortest path untuk weighted graph
- **Bellman-Ford** - Shortest path dengan support negative weights
- **A*** - Heuristic-based optimal pathfinding
- **Topological Sort** - Linearization untuk directed acyclic graphs
- **Multi-Source BFS** - Multiple starting points untuk multi-ambulance
- **Floyd-Warshall** - All-pairs shortest path
- **Johnson's Algorithm** - Efficient all-pairs untuk sparse graphs

Analisis mencakup:
- Perbandingan waktu eksekusi
- Penggunaan memori
- Jumlah iterasi
- Kualitas jalur (path length)
- Skalabilitas pada berbagai ukuran graf (small, medium, large)
- Machine Learning modeling dengan Random Forest (R² ~0.94)
- 6 visualisasi profesional untuk presentasi

## Instalasi dan Cara Menjalankan

### Prerequisites
- Python 3.13 atau lebih tinggi
- pip (Python package manager)

### Langkah Instalasi

1. Clone repository
```bash
git clone https://github.com/Glenferdinza/graphteoryalgorithmscrapper.git
cd graphteoryalgorithmscrapper
```

2. Buat virtual environment (opsional tapi disarankan)
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

### Cara Menjalankan

1. **Generate Data Benchmark**
```bash
python scraper.py
```
File `csv/data.csv` akan dibuat dengan 2,152 records benchmark data.

2. **Jalankan Analysis Notebook**

Buka Jupyter Notebook:
```bash
jupyter notebook analysis.ipynb
```

Atau gunakan VS Code dengan Jupyter extension, lalu:
- Pilih kernel: **Python (Tugas Akhir Graf)**
- Run all cells atau run cell by cell

3. **Output**

Hasil analisis akan menghasilkan:
- `csv/processed_data.csv` - Data yang telah diproses
- `csv/algorithm_performance_summary.csv` - Ringkasan performa
- `execution_time_predictor.pkl` - Machine Learning model
- `img/ppt_graph_*.png` - 6 grafik untuk presentasi (1200x600px @ 2x scale)

## Struktur Folder

```
.
├── csv/
│   ├── data.csv                              # Raw benchmark data
│   ├── processed_data.csv                    # Processed data
│   └── algorithm_performance_summary.csv     # Performance summary
├── img/
│   ├── ppt_graph_1_execution_time.png
│   ├── ppt_graph_2_multi_metric.png
│   ├── ppt_graph_3_scalability.png
│   ├── ppt_graph_4_heatmap.png
│   ├── ppt_graph_5_radar_top5.png
│   └── ppt_graph_6_summary_table.png
├── scraper.py                                # Data generator
├── analysis.ipynb                            # Main analysis notebook
├── execution_time_predictor.pkl              # Trained ML model
├── requirements.txt                          # Python dependencies
└── README.md
```

## Pembuat

**Glenferdinza**

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
