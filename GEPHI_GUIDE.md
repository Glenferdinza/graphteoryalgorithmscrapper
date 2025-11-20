# Panduan Lengkap Gephi untuk Water Ambulance Routing Project

## Persiapan File untuk Gephi

Project ini menyediakan 2 network berbeda untuk divisualisasikan di Gephi:

### Network 1: Algorithm Similarity Network
- **File**: `csv/nodes.csv` dan `csv/edges.csv`
- **Tujuan**: Memvisualisasikan kemiripan performa antar 9 algoritma
- **Nodes**: 9 algoritma
- **Edges**: Koneksi berdasarkan similarity execution time

### Network 2: Jakarta Waterways Network  
- **File**: `csv/waterways_nodes.csv` dan `csv/waterways_edges.csv`
- **Tujuan**: Memvisualisasikan jaringan dermaga-RS untuk routing ambulans
- **Nodes**: 16 lokasi (8 dermaga + 8 RS)
- **Edges**: Jalur air dengan waktu tempuh

---

## Cara Import ke Gephi - Network 1 (Algorithm Similarity)

### Step 1: Import Nodes

1. Buka Gephi
2. Klik **File → Import Spreadsheet**
3. Pilih file: `csv/nodes.csv`
4. Pada dialog Import:
   - **Separator**: Comma
   - **Import as**: Nodes table
   - **Charset**: UTF-8
5. Klik **Next**
6. Pastikan kolom mapping benar:
   - **Id** → Id
   - **Label** → Label
   - **AvgExecutionTime** → Attribute (Double)
   - **StdExecutionTime** → Attribute (Double)
   - **SampleCount** → Attribute (Integer)
7. Klik **Finish**
8. Pilih **New workspace** atau **Append to existing workspace**

### Step 2: Import Edges

1. Klik **File → Import Spreadsheet** lagi
2. Pilih file: `csv/edges.csv`
3. Pada dialog Import:
   - **Separator**: Comma
   - **Import as**: Edges table
   - **Charset**: UTF-8
4. Klik **Next**
5. Pastikan kolom mapping:
   - **Source** → Source
   - **Target** → Target
   - **Weight** → Weight (Double)
   - **ExecutionTimeDiff** → Attribute (Double)
   - **Type** → Edge Type
6. Klik **Finish**

### Step 3: Layout Network

1. Pergi ke tab **Overview**
2. Di panel **Layout** (kiri bawah), pilih layout algorithm:
   
   **Pilihan 1: ForceAtlas 2** (Recommended)
   - Klik **ForceAtlas 2**
   - Settings:
     - Scaling: 2000
     - Gravity: 1.0
     - Dissuade Hubs: ✓ (checked)
     - Prevent Overlap: ✓ (checked)
   - Klik **Run**
   - Tunggu hingga network stabil (30-60 detik)
   - Klik **Stop**

   **Pilihan 2: Fruchterman Reingold**
   - Settings:
     - Area: 10000
     - Gravity: 100
     - Speed: 1.0
   - Klik **Run** → tunggu → **Stop**

   **Pilihan 3: Yifan Hu**
   - Optimal distance: 200
   - Klik **Run** → tunggu → **Stop**

### Step 4: Styling Nodes

1. Di panel **Appearance** (kiri atas), pilih tab **Nodes**

2. **Node Size** (berdasarkan AvgExecutionTime):
   - Klik icon **Size** (lingkaran berbagai ukuran)
   - Pilih **Ranking**
   - Parameter: **AvgExecutionTime**
   - Min size: 10
   - Max size: 50
   - Klik **Apply**
   - Algoritma dengan execution time tinggi = node besar

3. **Node Color** (berdasarkan cluster atau attribute):
   
   **Option A - Manual Color by Algorithm Type**:
   - Klik icon **Color** (palet warna)
   - Pilih **Partition**
   - Parameter: **Id** (nama algoritma)
   - Assign colors:
     - BFS, DFS: Biru (#4A90E2) - Simple traversal
     - Dijkstra, A*, Bellman-Ford: Hijau (#2A9D8F) - Optimal algorithms
     - Floyd-Warshall, Johnson: Orange (#F4A261) - All-pairs
     - Topological Sort, Multi-Source BFS: Purple (#A8DADC) - Specialized
   - Klik **Apply**

   **Option B - Color by Performance (AvgExecutionTime)**:
   - Pilih **Ranking**
   - Parameter: **AvgExecutionTime**
   - Palette: Choose gradient (Red to Green)
   - Merah = lambat, Hijau = cepat
   - Klik **Apply**

4. **Node Label**:
   - Di toolbar bawah, klik icon **T** (Show Node Labels)
   - Labels akan muncul dengan nama algoritma

### Step 5: Styling Edges

1. Di panel **Appearance**, pilih tab **Edges**

2. **Edge Weight** (thickness):
   - Klik icon **Size**
   - Pilih **Ranking**
   - Parameter: **Weight**
   - Min size: 0.5
   - Max size: 5.0
   - Klik **Apply**
   - Edge dengan weight tinggi = garis tebal (algoritma mirip)

3. **Edge Color**:
   - Klik icon **Color**
   - Pilih **Unique** atau **Ranking by Weight**
   - Color: Abu-abu (#CCCCCC) atau gradient
   - Klik **Apply**

### Step 6: Network Analysis & Statistics

1. Di panel **Statistics** (kanan):

   **A. Average Degree**:
   - Klik **Run** pada Average Degree
   - Result menunjukkan rata-rata koneksi per algoritma
   - Node dengan degree tinggi = algoritma yang mirip banyak algoritma lain

   **B. Network Diameter**:
   - Klik **Run**
   - Shows longest shortest path dalam network
   - Menunjukkan seberapa "dekat" algoritma satu sama lain

   **C. Modularity (Community Detection)**:
   - Klik **Run**
   - Settings: Resolution 1.0
   - Akan detect clusters/communities
   - Hasil: Algoritma ter-cluster berdasarkan similarity

   **D. PageRank**:
   - Klik **Run**
   - Epsilon: 0.001
   - Shows algoritma paling "central" dalam network

2. **Visualize Communities** (setelah run Modularity):
   - Pergi ke **Appearance → Nodes → Color → Partition**
   - Parameter: **Modularity Class**
   - Klik **Apply**
   - Setiap community akan punya warna berbeda

### Step 7: Final Touches & Export

1. **Preview Mode**:
   - Klik tab **Preview** (atas)
   - Settings:
     - Preset: **Default**
     - Node Labels: ✓ Show Labels
     - Font: Arial, Size 12
     - Edge thickness: Proportional
   - Klik **Refresh** untuk lihat preview

2. **Adjust Preview**:
   - Node border width: 2
   - Edge opacity: 70%
   - Background color: White
   - Klik **Refresh**

3. **Export Image**:
   - Klik **Export: SVG/PDF/PNG**
   - Pilih format: PNG
   - Resolution: 4096 x 4096 (high quality)
   - Save as: `gephi_algorithm_network.png`

4. **Export to Web (Sigma.js)**:
   - Go to **File → Export → Sigma.js template**
   - Will create interactive web version
   - Open `network/index.html` di browser

---

## Cara Import ke Gephi - Network 2 (Jakarta Waterways)

### Step 1 & 2: Import Files

Sama seperti Network 1, tapi gunakan:
- `csv/waterways_nodes.csv`
- `csv/waterways_edges.csv`

### Step 3: Geo-Layout (PENTING!)

Karena nodes punya koordinat geografis (lat, lon):

1. Install plugin **GeoLayout**:
   - Go to **Tools → Plugins**
   - Tab **Available Plugins**
   - Search: "GeoLayout"
   - Klik **Install** → Restart Gephi

2. Setelah restart:
   - Go to **Layout** panel
   - Pilih **Geo Layout**
   - Settings:
     - Latitude: **Latitude** (kolom dari CSV)
     - Longitude: **Longitude** (kolom dari CSV)
     - Scale: 1000
   - Klik **Run**
   - Network akan tertata sesuai posisi geografis Jakarta!

### Step 4: Styling untuk Waterways Network

**Node Color by Type**:
- Partition by **Type**
- Dermaga: Biru (#4A90E2)
- Hospital: Merah (#E63946)

**Node Size by Degree**:
- Ranking by **Degree**
- Node dengan banyak koneksi = hub penting

**Edge Color/Width by Time**:
- Ranking by **Time**
- Edge tipis & hijau = jalur cepat
- Edge tebal & merah = jalur lambat

**Highlight Optimal Path**:
- Select nodes: D1, D5, D6, H1
- Right-click → **Filter → Select**
- Change color to green for selected
- Change size to larger

---

## Tips & Tricks Gephi

### 1. Filter Nodes/Edges
- Panel **Filters** (kanan)
- Drag filter ke **Queries**
- Example: Filter edges dengan Weight > 0.0005
- Hanya show algoritma yang sangat mirip

### 2. Ranking Visualization
- Use **Appearance → Ranking** untuk create heatmap effect
- Contoh: Color by AvgExecutionTime
  - Red = slow algorithms
  - Green = fast algorithms

### 3. Time Series (jika ada data temporal)
- Use **Timeline** (bawah)
- Dapat show evolution network over time

### 4. Labels Adjustment
- Klik **T** icon → Label Size adjustment
- Font: Arial Black untuk bold
- Size: Based on node size untuk hierarchy

### 5. Zoom & Navigation
- Mouse wheel: Zoom in/out
- Right-click drag: Rotate
- Middle-click drag: Pan
- Reset view: Klik icon **Reset Zoom** (kiri bawah)

---

## Metrics Interpretation untuk Paper

### Algorithm Network Metrics:

**Average Degree**: 
- Tinggi = banyak algoritma mirip satu sama lain
- Rendah = algoritma sangat distinct

**Modularity**:
- Tinggi (>0.4) = ada clusters jelas
- Clusters menunjukkan "families" algoritma dengan karakteristik mirip

**Network Diameter**:
- Berapa "hop" maksimal antar algoritma paling berbeda
- Indikator diversity algoritma

**Betweenness Centrality**:
- Algoritma yang jadi "bridge" antar groups
- Penting untuk understand transition performa

### Waterways Network Metrics:

**Degree Centrality**:
- Dermaga/RS dengan koneksi terbanyak
- Hub transportation penting

**Betweenness Centrality**:
- Lokasi yang sering dilalui di optimal paths
- Critical nodes untuk emergency response

**Closeness Centrality**:
- Lokasi yang "dekat" ke semua lokasi lain
- Best location untuk ambulance station

---

## Troubleshooting Common Issues

### Issue 1: Nodes overlap
**Solution**: 
- Enable **Prevent Overlap** di ForceAtlas 2
- Atau gunakan **Expansion** layout setelah main layout

### Issue 2: Labels tidak terbaca
**Solution**:
- Adjust Label Size di Appearance
- Atau di Preview mode, increase font size

### Issue 3: Network terlalu sparse/dense
**Solution**:
- Adjust **Scaling** parameter di layout
- Atau filter edges berdasarkan weight threshold

### Issue 4: Export image terpotong
**Solution**:
- Di Preview, klik **Reset Zoom**
- Atau adjust **Margin** di export settings

---

## Deliverables untuk Presentasi

Dari Gephi, generate:

1. **Static Image (PNG)**:
   - Algorithm network dengan community colors
   - Waterways network dengan geo-layout
   - Filename: `gephi_[networkname]_final.png`

2. **Interactive Web (Sigma.js)**:
   - Export to web format
   - Host di GitHub Pages atau local server
   - URL: `index.html`

3. **Statistics Report**:
   - Copy metrics dari Statistics panel
   - Include dalam appendix paper
   - Tables: Degree, Betweenness, Closeness per node

4. **Filtered Views**:
   - View 1: Only optimal algorithms
   - View 2: Only fast algorithms (exec time < 1 ms)
   - View 3: Weighted view (edge weight > threshold)

---

## Next Steps

1. Import kedua network ke Gephi
2. Apply layouts dan styling
3. Run statistics dan analyze
4. Export visualizations
5. Write interpretation dalam paper
6. Compare dengan visualizations dari Python

Gephi memberikan interactive exploration yang powerful untuk network analysis yang complement dengan static visualizations dari Python!
