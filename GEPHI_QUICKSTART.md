# Quick Start Guide - Gephi Visualization

## File-File yang Tersedia untuk Gephi

### Network 1: Algorithm Similarity Network
```
📁 csv/nodes.csv          → 9 algoritma sebagai nodes
📁 csv/edges.csv          → Koneksi berdasarkan similarity execution time
```
**Visualisasi**: Clustering algoritma berdasarkan performa mirip

### Network 2: Jakarta Waterways Network
```
📁 csv/waterways_nodes.csv         → 16 lokasi (8 dermaga + 8 RS)
📁 csv/waterways_edges.csv         → 26 jalur air
📁 csv/optimal_path_nodes.csv      → Highlight rute optimal
📁 csv/waterways_network_stats.csv → Statistik network
```
**Visualisasi**: Peta geografis routing ambulans air Jakarta

---

## Langkah Cepat Import ke Gephi

### 1. Buka Gephi
- Download: https://gephi.org/
- Install dan jalankan

### 2. Import Network

**Step A: Import Nodes**
1. File → Import Spreadsheet
2. Pilih: `csv/nodes.csv` atau `csv/waterways_nodes.csv`
3. Import as: **Nodes table**
4. Next → Finish

**Step B: Import Edges**
1. File → Import Spreadsheet
2. Pilih: `csv/edges.csv` atau `csv/waterways_edges.csv`
3. Import as: **Edges table**
4. Next → Finish

### 3. Layout Network

**Untuk Algorithm Network:**
- Layout: **ForceAtlas 2**
- Settings: Scaling 2000, Gravity 1.0
- Enable: Dissuade Hubs, Prevent Overlap
- Run → tunggu 30-60 detik → Stop

**Untuk Waterways Network:**
- Layout: **Geo Layout** (install plugin dulu)
- Latitude: Latitude column
- Longitude: Longitude column
- Scale: 1000
- Run

### 4. Styling

**Node Color by Type:**
- Appearance → Nodes → Color → Partition
- Parameter: Type
- Apply

**Node Size by Degree/Performance:**
- Appearance → Nodes → Size → Ranking
- Parameter: AvgExecutionTime atau Degree
- Min: 10, Max: 50
- Apply

**Edge Thickness by Weight:**
- Appearance → Edges → Size → Ranking
- Parameter: Weight
- Min: 0.5, Max: 5
- Apply

### 5. Show Labels
- Klik icon **T** di toolbar bawah
- Labels akan muncul

### 6. Export
- Tab: Preview
- Export: PNG/SVG/PDF
- Resolution: 4096 x 4096

---

## Analisis yang Bisa Dilakukan

### Statistics Panel (Kanan)

1. **Average Degree**
   - Berapa rata-rata koneksi per node
   - Tinggi = network highly connected

2. **Modularity (Community Detection)**
   - Deteksi cluster/komunitas dalam network
   - Hasil: Community classes untuk coloring

3. **Network Diameter**
   - Longest shortest path dalam network
   - Indikator "compactness" network

4. **PageRank**
   - Node mana yang paling "central"
   - Penting dalam network

5. **Betweenness Centrality**
   - Node yang sering jadi "jembatan" antar node lain
   - Critical untuk routing

### Visualisasi Hasil Statistics

**Setelah run Modularity:**
- Color nodes by: Modularity Class
- Setiap community punya warna berbeda

**Setelah run PageRank:**
- Size nodes by: PageRank
- Node penting = lebih besar

---

## Tips Visualisasi Terbaik

### Algorithm Network:
1. **Layout**: ForceAtlas 2
2. **Node Color**: By community (Modularity)
3. **Node Size**: By AvgExecutionTime
4. **Edge Thickness**: By Weight
5. **Background**: White
6. **Export**: PNG 4096x4096

### Waterways Network:
1. **Layout**: Geo Layout (geografis)
2. **Node Color**: By Type (dermaga = biru, RS = merah)
3. **Node Size**: By Degree (hub = besar)
4. **Edge Thickness**: By Time (cepat = tipis, lambat = tebal)
5. **Highlight**: Optimal path dengan warna hijau
6. **Export**: PNG dengan annotation

---

## Troubleshooting

**Problem**: Nodes bertumpukan
- **Fix**: Enable "Prevent Overlap" di ForceAtlas 2

**Problem**: Labels tidak terbaca
- **Fix**: Preview → Font size 14-16

**Problem**: Network terlalu rapat/renggang
- **Fix**: Adjust "Scaling" di layout settings

**Problem**: Export image terpotong
- **Fix**: Preview → Reset Zoom → Export

---

## Hasil yang Diharapkan

### Algorithm Network:
- Cluster algoritma mirip (BFS-DFS, Dijkstra-Bellman-Ford)
- Isolated nodes (Floyd-Warshall, Johnson, Bellman-Ford)
- Clear separation optimal vs suboptimal

### Waterways Network:
- Peta geografis Jakarta
- Hub dermaga terlihat (D6 Pluit = 5 koneksi)
- Rute optimal D1→D5→D6→H1 highlighted
- Dermaga coastal lebih connected

---

## Deliverables untuk Presentasi

1. **Screenshot Gephi**:
   - Algorithm network dengan community colors
   - Waterways network dengan geo-layout
   - Optimal path highlighted

2. **Statistics Export**:
   - Degree distribution table
   - Community detection results
   - Centrality measures

3. **Interpretasi**:
   - Apa arti clusters algoritma?
   - Hub mana yang paling penting?
   - Kenapa rute optimal melewati D5 dan D6?

---

## Next: Baca Panduan Lengkap

Untuk tutorial detail step-by-step dengan screenshots:
👉 **Baca file: GEPHI_GUIDE.md**

Untuk troubleshooting advanced dan tips profesional:
👉 **Gephi Documentation**: https://gephi.org/users/

Semua file CSV sudah siap di folder `csv/` - tinggal import ke Gephi!
