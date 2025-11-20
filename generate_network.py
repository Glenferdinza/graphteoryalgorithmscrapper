import pandas as pd
import numpy as np
from itertools import combinations

# CONFIGURATION

INPUT_FILE = 'csv/processed_data.csv'
NODES_OUTPUT = 'csv/nodes.csv'
EDGES_OUTPUT = 'csv/edges.csv'

# Threshold untuk membuat edge (ms)
EXECUTION_TIME_THRESHOLD = 3000  # Jika selisih < 3000ms, maka terhubung

# LOAD DATA

print("=" * 70)
print("NETWORK GENERATOR FOR GEPHI")
print("=" * 70)

print(f"\nLoading data from: {INPUT_FILE}")
df = pd.read_csv(INPUT_FILE)

print(f"Data loaded successfully!")
print(f"   Total records: {len(df):,}")
print(f"   Columns: {', '.join(df.columns)}\n")

# GENERATE NODES

print("=" * 70)
print("GENERATING NODES")
print("=" * 70)

# Ambil algorithm unik sebagai nodes
# Hitung rata-rata execution_time untuk setiap algorithm
nodes_data = df.groupby('algorithm').agg({
    'execution_time_ms': ['mean', 'std', 'count']
}).reset_index()

nodes_data.columns = ['algorithm', 'avg_exec_time', 'std_exec_time', 'count']

# Buat nodes DataFrame untuk Gephi
nodes = pd.DataFrame({
    'Id': nodes_data['algorithm'],
    'Label': nodes_data['algorithm'],
    'AvgExecutionTime': nodes_data['avg_exec_time'].round(2),
    'StdExecutionTime': nodes_data['std_exec_time'].round(2),
    'SampleCount': nodes_data['count']
})

print(f"\nGenerated {len(nodes)} nodes:")
print(nodes.to_string(index=False))

# Save nodes
nodes_gephi = nodes[['Id', 'Label']]  # Gephi minimal requirement
nodes.to_csv(NODES_OUTPUT, index=False)
print(f"\nNodes saved to: {NODES_OUTPUT}")

# GENERATE EDGES

print("\n" + "=" * 70)
print("GENERATING EDGES")
print("=" * 70)

edges_list = []

# Buat dictionary untuk lookup execution time per algorithm
algo_exec_time = dict(zip(nodes['Id'], nodes['AvgExecutionTime']))

print(f"\n\Checking all possible algorithm pairs...")
print(f"   Threshold: |execution_time_diff| < {EXECUTION_TIME_THRESHOLD} ms\n")

# Generate edges dari semua kombinasi algorithm pairs
algorithm_pairs = list(combinations(nodes['Id'], 2))

for algo_a, algo_b in algorithm_pairs:
    exec_time_a = algo_exec_time[algo_a]
    exec_time_b = algo_exec_time[algo_b]
    
    # Hitung selisih execution time
    diff = abs(exec_time_a - exec_time_b)
    
    # Cek apakah memenuhi threshold
    if diff < EXECUTION_TIME_THRESHOLD:
        # Hitung weight: semakin kecil selisih, semakin besar weight
        weight = 1 / (diff + 1)
        
        edges_list.append({
            'Source': algo_a,
            'Target': algo_b,
            'Weight': round(weight, 6),
            'ExecutionTimeDiff': round(diff, 2),
            'Type': 'Undirected'
        })
        
        print(f"   {algo_a:20s} ↔ {algo_b:20s} | Diff: {diff:7.2f} ms | Weight: {weight:.6f}")

# Create edges DataFrame
if edges_list:
    edges = pd.DataFrame(edges_list)
    
    print(f"\nGenerated {len(edges)} edges")
    print(f"   Average weight: {edges['Weight'].mean():.6f}")
    print(f"   Min weight: {edges['Weight'].min():.6f}")
    print(f"   Max weight: {edges['Weight'].max():.6f}")
    
    # Save edges
    edges_gephi = edges[['Source', 'Target', 'Weight', 'Type']]  # Gephi format
    edges.to_csv(EDGES_OUTPUT, index=False)
    print(f"\nEdges saved to: {EDGES_OUTPUT}")
else:
    print("\nNo edges generated! Try increasing EXECUTION_TIME_THRESHOLD")
    edges = pd.DataFrame(columns=['Source', 'Target', 'Weight', 'Type'])
    edges.to_csv(EDGES_OUTPUT, index=False)

# NETWORK STATISTICS

print("\n" + "=" * 70)
print("NETWORK STATISTICS")
print("=" * 70)

print(f"\nNodes: {len(nodes)}")
print(f"Edges: {len(edges)}")
if len(edges) > 0:
    # Hitung degree (jumlah koneksi) per node
    degree_count = pd.concat([
        edges['Source'].value_counts(),
        edges['Target'].value_counts()
    ]).groupby(level=0).sum().sort_values(ascending=False)
    
    print(f"Network Density: {len(edges) / (len(nodes) * (len(nodes) - 1) / 2) * 100:.2f}%")
    print(f"\nNode Connectivity (Top 5):")
    for i, (node, degree) in enumerate(degree_count.head(5).items(), 1):
        print(f"   {i}. {node:20s} : {int(degree)} connections")
    
    print(f"\nIsolated Nodes (no connections):")
    connected_nodes = set(edges['Source']).union(set(edges['Target']))
    isolated_nodes = set(nodes['Id']) - connected_nodes
    if isolated_nodes:
        for node in isolated_nodes:
            print(f"   - {node}")
    else:
        print(f"   No isolated nodes! All algorithms are connected.")
else:
    print(f"\nNetwork is empty - no edges created!")

# GEPHI IMPORT INSTRUCTIONS

print("\n" + "=" * 70)
print("HOW TO IMPORT TO GEPHI")
print("=" * 70)

print("""
1️⃣  Open Gephi
2️⃣  Go to: File → Import Spreadsheet
3️⃣  Import NODES first:
    - Select: csv/nodes.csv
    - Import as: Nodes table
    - Click 'Next' and 'Finish'

4️⃣  Import EDGES:
    - Go to: File → Import Spreadsheet
    - Select: csv/edges.csv
    - Import as: Edges table
    - Click 'Next' and 'Finish'

5️⃣  Visualize:
    - Go to 'Overview' tab
    - Apply layout: ForceAtlas 2 / Fruchterman Reingold
    - Adjust node size based on 'Degree' or 'AvgExecutionTime'
    - Color nodes by 'Modularity' or custom attribute

6️⃣  Analyze:
    - Run Statistics: Average Degree, Network Diameter, Modularity
    - Use filters to highlight specific algorithm clusters

📊 Your network is ready for analysis!
""")

print("=" * 70)
print("NETWORK GENERATION COMPLETED!")
print("=" * 70)

# ADDITIONAL: Export network summary

# Create summary report
summary = {
    'Total Nodes': [len(nodes)],
    'Total Edges': [len(edges)],
    'Avg Execution Time (all algorithms)': [nodes['AvgExecutionTime'].mean().round(2)],
    'Execution Time Threshold': [EXECUTION_TIME_THRESHOLD],
    'Network Density (%)': [round(len(edges) / (len(nodes) * (len(nodes) - 1) / 2) * 100, 2) if len(nodes) > 1 else 0]
}

summary_df = pd.DataFrame(summary)
summary_df.to_csv('csv/network_summary.csv', index=False)
print(f"\n📋 Network summary saved to: csv/network_summary.csv")

print("\n🎉 Done! Ready to visualize in Gephi!")
