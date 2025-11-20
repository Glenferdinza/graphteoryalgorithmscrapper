"""
Generate Waterways Network CSV for Gephi
Membuat nodes dan edges dari Jakarta waterways untuk visualisasi di Gephi
"""

import pandas as pd
import networkx as nx

# Import network dari implementasi ambulans
import sys
sys.path.append('.')

# Recreate network structure
locations = [
    # Dermaga (id, name, type, lat, lon)
    ('D1', 'Dermaga Muara Angke', 'dermaga', -6.1075, 106.7547),
    ('D2', 'Dermaga Ancol', 'dermaga', -6.1256, 106.8436),
    ('D3', 'Dermaga Kali Besar', 'dermaga', -6.1378, 106.8142),
    ('D4', 'Dermaga Sunda Kelapa', 'dermaga', -6.1203, 106.8074),
    ('D5', 'Dermaga Muara Karang', 'dermaga', -6.1145, 106.7689),
    ('D6', 'Dermaga Pluit', 'dermaga', -6.1189, 106.7908),
    ('D7', 'Dermaga Marunda', 'dermaga', -6.1089, 106.9456),
    ('D8', 'Dermaga Tanjung Priok', 'dermaga', -6.1067, 106.8956),
    
    # Rumah Sakit (id, name, type, lat, lon)
    ('H1', 'RS Siloam Kebon Jeruk', 'hospital', -6.1893, 106.7842),
    ('H2', 'RS Pluit', 'hospital', -6.1256, 106.7923),
    ('H3', 'RSPI Puri Indah', 'hospital', -6.1878, 106.7456),
    ('H4', 'RS Atmajaya', 'hospital', -6.1356, 106.8145),
    ('H5', 'RS Husada', 'hospital', -6.1445, 106.8334),
    ('H6', 'RS Pantai Indah Kapuk', 'hospital', -6.1289, 106.7623),
    ('H7', 'RS Premier Jatinegara', 'hospital', -6.2156, 106.8645),
    ('H8', 'RS Koja', 'hospital', -6.1089, 106.9123),
]

waterways = [
    # (source, target, distance_m, time_min)
    # Jalur utara (coastal routes)
    ('D1', 'D5', 1200, 8),
    ('D5', 'D6', 1500, 10),
    ('D6', 'D4', 2100, 14),
    ('D4', 'D3', 800, 6),
    ('D3', 'D2', 1800, 12),
    ('D2', 'D8', 3500, 22),
    ('D8', 'D7', 4200, 28),
    
    # Jalur ke rumah sakit (removed D1->H1 for complexity)
    ('D1', 'H3', 5600, 35),
    ('D5', 'H6', 2800, 18),
    ('D6', 'H2', 1100, 8),
    ('D6', 'H1', 5100, 32),
    ('D4', 'H4', 1200, 9),
    ('D3', 'H4', 900, 7),
    ('D3', 'H5', 2100, 14),
    ('D2', 'H5', 2800, 18),
    ('D8', 'H8', 1500, 11),
    ('D7', 'H7', 8500, 52),
    
    # Jalur antar rumah sakit
    ('H1', 'H3', 3200, 20),
    ('H1', 'H2', 4800, 30),
    ('H2', 'H6', 2400, 16),
    ('H4', 'H5', 1800, 12),
    ('H5', 'H7', 7200, 45),
    ('H8', 'H7', 9100, 56),
    
    # Jalur alternatif
    ('D5', 'H2', 2600, 17),
    ('D4', 'H2', 2900, 19),
    ('D6', 'H6', 3100, 20),
]

print("=" * 70)
print("GENERATING WATERWAYS NETWORK FOR GEPHI")
print("=" * 70)

# ============================================================================
# CREATE NODES CSV
# ============================================================================

print("\nCreating nodes CSV...")

nodes_data = []
for loc_id, name, loc_type, lat, lon in locations:
    nodes_data.append({
        'Id': loc_id,
        'Label': name,
        'Type': loc_type,
        'Latitude': lat,
        'Longitude': lon
    })

df_nodes = pd.DataFrame(nodes_data)

# Add additional attributes for Gephi visualization
df_nodes['NodeSize'] = df_nodes['Type'].map({'dermaga': 30, 'hospital': 40})
df_nodes['Color'] = df_nodes['Type'].map({'dermaga': '#4A90E2', 'hospital': '#E63946'})

print(f"Created {len(df_nodes)} nodes")
print(df_nodes.to_string(index=False))

# Save
df_nodes.to_csv('csv/waterways_nodes.csv', index=False)
print("\nSaved: csv/waterways_nodes.csv")

# ============================================================================
# CREATE EDGES CSV
# ============================================================================

print("\nCreating edges CSV...")

edges_data = []
for source, target, distance, time in waterways:
    edges_data.append({
        'Source': source,
        'Target': target,
        'Type': 'Undirected',
        'Distance': distance,
        'Time': time,
        'Weight': time,  # Use time as weight for shortest path
        'Label': f"{time} min"
    })

df_edges = pd.DataFrame(edges_data)

print(f"Created {len(df_edges)} edges")
print(df_edges.head(10).to_string(index=False))
print("...")

# Save
df_edges.to_csv('csv/waterways_edges.csv', index=False)
print("\nSaved: csv/waterways_edges.csv")

# ============================================================================
# CREATE OPTIMAL PATH HIGHLIGHT
# ============================================================================

print("\nCreating optimal path highlight...")

optimal_path = ['D1', 'D5', 'D6', 'H1']
optimal_path_info = []

for i in range(len(optimal_path)):
    node_id = optimal_path[i]
    node_info = df_nodes[df_nodes['Id'] == node_id].iloc[0]
    optimal_path_info.append({
        'NodeId': node_id,
        'NodeName': node_info['Label'],
        'Position': i + 1,
        'IsOptimalPath': True
    })

df_optimal = pd.DataFrame(optimal_path_info)
df_optimal.to_csv('csv/optimal_path_nodes.csv', index=False)
print("Saved: csv/optimal_path_nodes.csv")

print("\nOptimal Path: " + " → ".join([info['NodeName'] for info in optimal_path_info]))

# ============================================================================
# NETWORK STATISTICS
# ============================================================================

print("\n" + "=" * 70)
print("NETWORK STATISTICS FOR GEPHI ANALYSIS")
print("=" * 70)

# Build NetworkX graph for quick stats
G = nx.Graph()
for _, row in df_nodes.iterrows():
    G.add_node(row['Id'], **row.to_dict())
for _, row in df_edges.iterrows():
    G.add_edge(row['Source'], row['Target'], weight=row['Weight'])

print(f"\nNodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")
print(f"Density: {nx.density(G):.3f}")
print(f"Is Connected: {nx.is_connected(G)}")

# Degree statistics
degrees = dict(G.degree())
print(f"\nDegree Statistics:")
print(f"  Average: {sum(degrees.values()) / len(degrees):.2f}")
print(f"  Min: {min(degrees.values())}")
print(f"  Max: {max(degrees.values())}")

print("\nTop 5 Nodes by Degree (Most Connected):")
sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
for i, (node, degree) in enumerate(sorted_degrees[:5], 1):
    node_name = df_nodes[df_nodes['Id'] == node]['Label'].values[0]
    print(f"  {i}. {node_name} ({node}): {degree} connections")

# Save network statistics
stats = {
    'Metric': ['Total Nodes', 'Total Edges', 'Network Density', 'Average Degree', 
               'Diameter', 'Is Connected'],
    'Value': [
        G.number_of_nodes(),
        G.number_of_edges(),
        round(nx.density(G), 3),
        round(sum(degrees.values()) / len(degrees), 2),
        nx.diameter(G) if nx.is_connected(G) else 'N/A',
        'Yes' if nx.is_connected(G) else 'No'
    ]
}
pd.DataFrame(stats).to_csv('csv/waterways_network_stats.csv', index=False)
print("\nSaved: csv/waterways_network_stats.csv")

print("\n" + "=" * 70)
print("ALL FILES GENERATED FOR GEPHI")
print("=" * 70)
print("\nGenerated files:")
print("  1. csv/waterways_nodes.csv - 16 locations (dermaga + RS)")
print("  2. csv/waterways_edges.csv - 29 waterway routes")
print("  3. csv/optimal_path_nodes.csv - Optimal route highlight")
print("  4. csv/waterways_network_stats.csv - Network metrics")
print("\nNext: Import to Gephi following GEPHI_GUIDE.md instructions!")
