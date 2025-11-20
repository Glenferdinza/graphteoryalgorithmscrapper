"""
Water Ambulance Routing System - Jakarta Waterways Network
===========================================================
Sistem routing ambulans air untuk jalur perairan Jakarta yang mensimulasikan
jaringan dermaga dan rumah sakit dengan implementasi 9 algoritma pencarian jalur.

Studi Kasus: Rute Optimal dari Dermaga Muara Angke ke RS Siloam Kebon Jeruk
"""

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from collections import deque
import heapq
import time
from typing import Dict, List, Tuple, Set
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# JAKARTA WATERWAYS NETWORK - GRAPH DEFINITION
# ============================================================================

class JakartaWaterwaysNetwork:
    """
    Representasi jaringan jalur perairan Jakarta untuk ambulans air.
    Mencakup dermaga, rumah sakit, dan rute air antar lokasi.
    """
    
    def __init__(self):
        self.G = nx.Graph()
        self._build_network()
    
    def _build_network(self):
        """Membangun graf jaringan waterways Jakarta dengan lokasi riil"""
        
        # Nodes: Dermaga dan Rumah Sakit di Jakarta
        # Format: (id, name, type, coordinates)
        locations = [
            # Dermaga
            ('D1', 'Dermaga Muara Angke', 'dermaga', (-6.1075, 106.7547)),
            ('D2', 'Dermaga Ancol', 'dermaga', (-6.1256, 106.8436)),
            ('D3', 'Dermaga Kali Besar', 'dermaga', (-6.1378, 106.8142)),
            ('D4', 'Dermaga Sunda Kelapa', 'dermaga', (-6.1203, 106.8074)),
            ('D5', 'Dermaga Muara Karang', 'dermaga', (-6.1145, 106.7689)),
            ('D6', 'Dermaga Pluit', 'dermaga', (-6.1189, 106.7908)),
            ('D7', 'Dermaga Marunda', 'dermaga', (-6.1089, 106.9456)),
            ('D8', 'Dermaga Tanjung Priok', 'dermaga', (-6.1067, 106.8956)),
            
            # Rumah Sakit
            ('H1', 'RS Siloam Kebon Jeruk', 'hospital', (-6.1893, 106.7842)),
            ('H2', 'RS Pluit', 'hospital', (-6.1256, 106.7923)),
            ('H3', 'RSPI Puri Indah', 'hospital', (-6.1878, 106.7456)),
            ('H4', 'RS Atmajaya', 'hospital', (-6.1356, 106.8145)),
            ('H5', 'RS Husada', 'hospital', (-6.1445, 106.8334)),
            ('H6', 'RS Pantai Indah Kapuk', 'hospital', (-6.1289, 106.7623)),
            ('H7', 'RS Premier Jatinegara', 'hospital', (-6.2156, 106.8645)),
            ('H8', 'RS Koja', 'hospital', (-6.1089, 106.9123)),
        ]
        
        # Add nodes dengan attributes
        for node_id, name, node_type, coords in locations:
            self.G.add_node(node_id, name=name, type=node_type, 
                          lat=coords[0], lon=coords[1])
        
        # Edges: Jalur air dengan jarak (dalam meter) dan waktu tempuh (menit)
        # Format: (source, target, distance_m, time_min)
        waterways = [
            # Jalur utara (coastal routes)
            ('D1', 'D5', 1200, 8),
            ('D5', 'D6', 1500, 10),
            ('D6', 'D4', 2100, 14),
            ('D4', 'D3', 800, 6),
            ('D3', 'D2', 1800, 12),
            ('D2', 'D8', 3500, 22),
            ('D8', 'D7', 4200, 28),
            
            # Jalur ke rumah sakit dari dermaga (removed direct D1->H1)
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
            
            # Jalur antar rumah sakit (backup routes)
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
        
        # Add edges dengan weight (waktu tempuh)
        for source, target, distance, time_min in waterways:
            self.G.add_edge(source, target, 
                          distance=distance, 
                          time=time_min,
                          weight=time_min)  # Weight untuk algoritma
    
    def get_node_info(self, node_id: str) -> Dict:
        """Mendapatkan informasi lengkap node"""
        return self.G.nodes[node_id]
    
    def get_edge_info(self, source: str, target: str) -> Dict:
        """Mendapatkan informasi lengkap edge"""
        return self.G[source][target]
    
    def visualize_network(self, path=None, title="Jakarta Waterways Network"):
        """Visualisasi network dengan Plotly (interactive) - Enhanced dengan annotations"""
        
        # Extract coordinates
        pos = {node: (data['lon'], data['lat']) 
               for node, data in self.G.nodes(data=True)}
        
        # Create edges trace
        edge_x = []
        edge_y = []
        edge_text = []
        
        for edge in self.G.edges(data=True):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_text.append(f"{edge[2]['time']} min ({edge[2]['distance']}m)")
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1.5, color='#A8DADC'),
            hoverinfo='text',
            text=edge_text,
            mode='lines',
            name='Jalur Air'
        )
        
        # Create nodes trace
        node_x = []
        node_y = []
        node_text = []
        node_color = []
        node_size = []
        
        for node, data in self.G.nodes(data=True):
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(f"{data['name']}<br>Type: {data['type']}")
            
            if data['type'] == 'dermaga':
                node_color.append('#4A90E2')
                node_size.append(15)
            else:
                node_color.append('#E63946')
                node_size.append(18)
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=[self.G.nodes[node]['name'] for node in self.G.nodes()],
            textposition="top center",
            textfont=dict(size=9),
            hovertext=node_text,
            marker=dict(
                size=node_size,
                color=node_color,
                line=dict(width=2, color='white')
            ),
            name='Lokasi'
        )
        
        # Highlight path if provided
        data_traces = [edge_trace, node_trace]
        annotations = []
        
        if path:
            # Enhanced path visualization dengan garis tebal dan warna mencolok
            path_x = []
            path_y = []
            for i in range(len(path) - 1):
                x0, y0 = pos[path[i]]
                x1, y1 = pos[path[i+1]]
                path_x.extend([x0, x1, None])
                path_y.extend([y0, y1, None])
            
            path_trace = go.Scatter(
                x=path_x, y=path_y,
                line=dict(width=6, color='#FFD700'),  # Gold color untuk optimal path
                mode='lines',
                name='Rute Optimal',
                showlegend=True
            )
            data_traces.append(path_trace)
            
            # Add numbered arrows and step labels for each segment in the path
            total_time = 0
            for i in range(len(path) - 1):
                start_node = path[i]
                end_node = path[i+1]
                x0, y0 = pos[start_node]
                x1, y1 = pos[end_node]
                
                # Get edge time
                if self.G.has_edge(start_node, end_node):
                    edge_time = self.G[start_node][end_node]['time']
                    total_time += edge_time
                    
                    # Calculate midpoint for annotation
                    mid_x = (x0 + x1) / 2
                    mid_y = (y0 + y1) / 2
                    
                    # Add arrow annotation
                    annotations.append(dict(
                        x=x1, y=y1,
                        ax=x0, ay=y0,
                        xref='x', yref='y',
                        axref='x', ayref='y',
                        showarrow=True,
                        arrowhead=3,
                        arrowsize=1.5,
                        arrowwidth=3,
                        arrowcolor='#FF6B35',
                        opacity=0.8
                    ))
                    
                    # Add step number and time label
                    start_name = self.G.nodes[start_node]['name'].split()[0]  # Short name
                    end_name = self.G.nodes[end_node]['name'].split()[0]
                    
                    annotations.append(dict(
                        x=mid_x, y=mid_y,
                        text=f"<b>Step {i+1}</b><br>{edge_time} min",
                        showarrow=False,
                        font=dict(
                            size=11,
                            color='white',
                            family='Arial Black'
                        ),
                        bgcolor='#FF6B35',
                        borderpad=4,
                        borderwidth=2,
                        bordercolor='white',
                        opacity=0.95
                    ))
            
            # Add START marker
            start_pos = pos[path[0]]
            annotations.append(dict(
                x=start_pos[0], y=start_pos[1],
                text="🚩 START",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor='green',
                ax=0, ay=-40,
                font=dict(size=13, color='green', family='Arial Black'),
                bgcolor='rgba(255,255,255,0.9)',
                borderpad=4
            ))
            
            # Add FINISH marker
            end_pos = pos[path[-1]]
            annotations.append(dict(
                x=end_pos[0], y=end_pos[1],
                text="🏁 FINISH",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor='red',
                ax=0, ay=40,
                font=dict(size=13, color='red', family='Arial Black'),
                bgcolor='rgba(255,255,255,0.9)',
                borderpad=4
            ))
            
            # Add total time info box
            annotations.append(dict(
                x=0.02, y=0.98,
                xref='paper', yref='paper',
                text=f"<b>RUTE OPTIMAL</b><br>" + 
                     f"Path: {' → '.join(path)}<br>" +
                     f"Total Waktu: <b>{total_time} menit</b><br>" +
                     f"Pemberhentian: {len(path)} lokasi",
                showarrow=False,
                font=dict(size=11, color='#1D3557', family='Arial'),
                bgcolor='rgba(42, 157, 143, 0.15)',
                bordercolor='#2A9D8F',
                borderwidth=2,
                borderpad=8,
                align='left',
                xanchor='left',
                yanchor='top'
            ))
        
        # Create figure
        fig = go.Figure(data=data_traces)
        
        # Update layout with annotations
        fig.update_layout(
            title=dict(text=title, font=dict(size=18, family='Arial Black')),
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20, l=20, r=20, t=80),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=800,
            width=1400,
            annotations=annotations,
            legend=dict(
                x=0.02, y=0.02,
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='#457B9D',
                borderwidth=1
            )
        )
        
        return fig

# ============================================================================
# ALGORITHM IMPLEMENTATIONS
# ============================================================================

class RoutingAlgorithms:
    """Implementasi 9 algoritma pencarian jalur untuk ambulans air"""
    
    def __init__(self, graph: nx.Graph):
        self.graph = graph
    
    def dfs(self, start: str, goal: str) -> Tuple[List[str], float, int]:
        """Depth-First Search"""
        visited = set()
        stack = [(start, [start])]
        iterations = 0
        
        while stack:
            iterations += 1
            node, path = stack.pop()
            
            if node == goal:
                total_time = self._calculate_path_time(path)
                return path, total_time, iterations
            
            if node not in visited:
                visited.add(node)
                for neighbor in self.graph.neighbors(node):
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor]))
        
        return [], float('inf'), iterations
    
    def bfs(self, start: str, goal: str) -> Tuple[List[str], float, int]:
        """Breadth-First Search"""
        visited = {start}
        queue = deque([(start, [start])])
        iterations = 0
        
        while queue:
            iterations += 1
            node, path = queue.popleft()
            
            if node == goal:
                total_time = self._calculate_path_time(path)
                return path, total_time, iterations
            
            for neighbor in self.graph.neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return [], float('inf'), iterations
    
    def dijkstra(self, start: str, goal: str) -> Tuple[List[str], float, int]:
        """Dijkstra's Algorithm"""
        distances = {node: float('inf') for node in self.graph.nodes()}
        distances[start] = 0
        previous = {node: None for node in self.graph.nodes()}
        pq = [(0, start)]
        iterations = 0
        
        while pq:
            iterations += 1
            current_dist, current = heapq.heappop(pq)
            
            if current == goal:
                path = self._reconstruct_path(previous, start, goal)
                return path, current_dist, iterations
            
            if current_dist > distances[current]:
                continue
            
            for neighbor in self.graph.neighbors(current):
                weight = self.graph[current][neighbor]['weight']
                distance = current_dist + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))
        
        return [], float('inf'), iterations
    
    def a_star(self, start: str, goal: str) -> Tuple[List[str], float, int]:
        """A* Algorithm with Euclidean heuristic"""
        def heuristic(n1, n2):
            lat1, lon1 = self.graph.nodes[n1]['lat'], self.graph.nodes[n1]['lon']
            lat2, lon2 = self.graph.nodes[n2]['lat'], self.graph.nodes[n2]['lon']
            return np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 100000
        
        open_set = [(0, start)]
        came_from = {}
        g_score = {node: float('inf') for node in self.graph.nodes()}
        g_score[start] = 0
        f_score = {node: float('inf') for node in self.graph.nodes()}
        f_score[start] = heuristic(start, goal)
        iterations = 0
        
        while open_set:
            iterations += 1
            current = heapq.heappop(open_set)[1]
            
            if current == goal:
                path = self._reconstruct_path_astar(came_from, start, goal)
                return path, g_score[goal], iterations
            
            for neighbor in self.graph.neighbors(current):
                tentative_g = g_score[current] + self.graph[current][neighbor]['weight']
                
                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return [], float('inf'), iterations
    
    def bellman_ford(self, start: str, goal: str) -> Tuple[List[str], float, int]:
        """Bellman-Ford Algorithm"""
        distances = {node: float('inf') for node in self.graph.nodes()}
        distances[start] = 0
        previous = {node: None for node in self.graph.nodes()}
        iterations = 0
        
        for _ in range(len(self.graph.nodes()) - 1):
            for u, v, data in self.graph.edges(data=True):
                iterations += 1
                weight = data['weight']
                
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    previous[v] = u
                
                if distances[v] + weight < distances[u]:
                    distances[u] = distances[v] + weight
                    previous[u] = v
        
        path = self._reconstruct_path(previous, start, goal)
        return path, distances[goal], iterations
    
    def floyd_warshall(self, start: str, goal: str) -> Tuple[List[str], float, int]:
        """Floyd-Warshall Algorithm"""
        nodes = list(self.graph.nodes())
        n = len(nodes)
        dist = {(i, j): float('inf') for i in nodes for j in nodes}
        next_node = {(i, j): None for i in nodes for j in nodes}
        iterations = 0
        
        for node in nodes:
            dist[(node, node)] = 0
        
        for u, v, data in self.graph.edges(data=True):
            dist[(u, v)] = data['weight']
            dist[(v, u)] = data['weight']
            next_node[(u, v)] = v
            next_node[(v, u)] = u
        
        for k in nodes:
            for i in nodes:
                for j in nodes:
                    iterations += 1
                    if dist[(i, j)] > dist[(i, k)] + dist[(k, j)]:
                        dist[(i, j)] = dist[(i, k)] + dist[(k, j)]
                        next_node[(i, j)] = next_node[(i, k)]
        
        path = self._reconstruct_path_floyd(next_node, start, goal)
        return path, dist[(start, goal)], iterations
    
    def johnson(self, start: str, goal: str) -> Tuple[List[str], float, int]:
        """Johnson's Algorithm"""
        iterations = 0
        new_node = 'temp_source'
        G_temp = self.graph.copy()
        G_temp.add_node(new_node)
        
        for node in self.graph.nodes():
            G_temp.add_edge(new_node, node, weight=0)
        
        h = {node: 0 for node in G_temp.nodes()}
        for _ in range(len(G_temp.nodes()) - 1):
            for u, v, data in G_temp.edges(data=True):
                iterations += 1
                if h[u] + data['weight'] < h[v]:
                    h[v] = h[u] + data['weight']
        
        distances = {node: float('inf') for node in self.graph.nodes()}
        distances[start] = 0
        previous = {node: None for node in self.graph.nodes()}
        pq = [(0, start)]
        
        while pq:
            iterations += 1
            current_dist, current = heapq.heappop(pq)
            
            if current == goal:
                path = self._reconstruct_path(previous, start, goal)
                return path, current_dist, iterations
            
            for neighbor in self.graph.neighbors(current):
                weight = self.graph[current][neighbor]['weight']
                reweighted = weight + h[current] - h[neighbor]
                distance = current_dist + reweighted
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))
        
        return [], float('inf'), iterations
    
    def topological_sort(self, start: str, goal: str) -> Tuple[List[str], float, int]:
        """Topological Sort based pathfinding"""
        visited = set()
        stack = []
        iterations = 0
        
        def dfs_visit(node):
            nonlocal iterations
            iterations += 1
            visited.add(node)
            for neighbor in self.graph.neighbors(node):
                if neighbor not in visited:
                    dfs_visit(neighbor)
            stack.append(node)
        
        for node in self.graph.nodes():
            if node not in visited:
                dfs_visit(node)
        
        topo_order = stack[::-1]
        
        distances = {node: float('inf') for node in self.graph.nodes()}
        distances[start] = 0
        previous = {node: None for node in self.graph.nodes()}
        
        for node in topo_order:
            if distances[node] != float('inf'):
                for neighbor in self.graph.neighbors(node):
                    weight = self.graph[node][neighbor]['weight']
                    if distances[node] + weight < distances[neighbor]:
                        distances[neighbor] = distances[node] + weight
                        previous[neighbor] = node
        
        path = self._reconstruct_path(previous, start, goal)
        return path, distances[goal], iterations
    
    def multi_source_bfs(self, start: str, goal: str) -> Tuple[List[str], float, int]:
        """Multi-Source BFS"""
        sources = [n for n in self.graph.nodes() 
                  if self.graph.nodes[n]['type'] == 'dermaga']
        
        visited = {s: {s} for s in sources}
        queues = {s: deque([(s, [s])]) for s in sources}
        iterations = 0
        
        while any(queues.values()):
            iterations += 1
            for source in sources:
                if not queues[source]:
                    continue
                    
                node, path = queues[source].popleft()
                
                if node == goal and source == start:
                    total_time = self._calculate_path_time(path)
                    return path, total_time, iterations
                
                for neighbor in self.graph.neighbors(node):
                    if neighbor not in visited[source]:
                        visited[source].add(neighbor)
                        queues[source].append((neighbor, path + [neighbor]))
        
        return self.bfs(start, goal)
    
    def _calculate_path_time(self, path: List[str]) -> float:
        """Menghitung total waktu tempuh untuk path"""
        if len(path) < 2:
            return 0
        
        total = 0
        for i in range(len(path) - 1):
            total += self.graph[path[i]][path[i+1]]['weight']
        return total
    
    def _reconstruct_path(self, previous: Dict, start: str, goal: str) -> List[str]:
        """Rekonstruksi path dari dictionary previous"""
        path = []
        current = goal
        
        while current is not None:
            path.append(current)
            current = previous[current]
        
        path.reverse()
        
        if path[0] != start:
            return []
        
        return path
    
    def _reconstruct_path_astar(self, came_from: Dict, start: str, goal: str) -> List[str]:
        """Rekonstruksi path untuk A*"""
        path = [goal]
        current = goal
        
        while current in came_from:
            current = came_from[current]
            path.append(current)
        
        path.reverse()
        return path
    
    def _reconstruct_path_floyd(self, next_node: Dict, start: str, goal: str) -> List[str]:
        """Rekonstruksi path untuk Floyd-Warshall"""
        if next_node[(start, goal)] is None:
            return []
        
        path = [start]
        current = start
        
        while current != goal:
            current = next_node[(current, goal)]
            path.append(current)
        
        return path

# ============================================================================
# MAIN EXECUTION - BENCHMARK & VISUALIZATION
# ============================================================================

def main():
    print("=" * 80)
    print("WATER AMBULANCE ROUTING SYSTEM - JAKARTA WATERWAYS")
    print("=" * 80)
    
    # Initialize network
    network = JakartaWaterwaysNetwork()
    algorithms = RoutingAlgorithms(network.G)
    
    # Define routing scenario
    START = 'D1'  # Dermaga Muara Angke
    GOAL = 'H1'   # RS Siloam Kebon Jeruk
    
    start_name = network.get_node_info(START)['name']
    goal_name = network.get_node_info(GOAL)['name']
    
    print(f"\nSkenario: Emergency Route Planning")
    print(f"Start: {start_name}")
    print(f"Goal:  {goal_name}")
    print("\n" + "=" * 80)
    
    # Run all algorithms
    algo_list = [
        ('DFS', algorithms.dfs),
        ('BFS', algorithms.bfs),
        ('Dijkstra', algorithms.dijkstra),
        ('A*', algorithms.a_star),
        ('Bellman-Ford', algorithms.bellman_ford),
        ('Floyd-Warshall', algorithms.floyd_warshall),
        ('Johnson', algorithms.johnson),
        ('Topological Sort', algorithms.topological_sort),
        ('Multi-Source BFS', algorithms.multi_source_bfs),
    ]
    
    results = []
    
    for algo_name, algo_func in algo_list:
        print(f"\nRunning {algo_name}...")
        start_time = time.time()
        path, total_time, iterations = algo_func(START, GOAL)
        execution_time = (time.time() - start_time) * 1000
        
        results.append({
            'Algorithm': algo_name,
            'Path': path,
            'Time (minutes)': total_time,
            'Path Length': len(path) - 1 if path else 0,
            'Iterations': iterations,
            'Execution Time (ms)': round(execution_time, 3)
        })
        
        if path:
            print(f"  Path: {' -> '.join(path)}")
            print(f"  Travel Time: {total_time:.1f} minutes")
            print(f"  Stops: {len(path) - 1}")
        else:
            print(f"  No path found!")
    
    # Create results DataFrame
    df_results = pd.DataFrame(results)
    
    print("\n" + "=" * 80)
    print("ALGORITHM COMPARISON RESULTS")
    print("=" * 80)
    print(df_results.to_string(index=False))
    
    # Save results
    df_results.to_csv('csv/ambulance_routing_results.csv', index=False)
    print("\nResults saved to: csv/ambulance_routing_results.csv")
    
    # Visualizations
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80)
    
    # 1. Network visualization
    print("\n1. Visualizing Jakarta Waterways Network...")
    fig1 = network.visualize_network(
        title="Jakarta Waterways Network - Ambulans Air"
    )
    fig1.write_html('img/network_map.html')
    fig1.write_image('img/network_map.png', width=1400, height=700, scale=2)
    print("   Saved: img/network_map.html & img/network_map.png")
    
    # 2. Best path visualization (Dijkstra/A*)
    best_algo = df_results.loc[df_results['Time (minutes)'].idxmin()]
    best_path = best_algo['Path']
    
    print(f"\n2. Visualizing optimal route ({best_algo['Algorithm']})...")
    fig2 = network.visualize_network(
        path=best_path,
        title=f"Rute Optimal: {start_name} ke {goal_name}<br>Algorithm: {best_algo['Algorithm']} - {best_algo['Time (minutes)']:.1f} menit"
    )
    fig2.write_html('img/optimal_route.html')
    fig2.write_image('img/optimal_route.png', width=1400, height=700, scale=2)
    print("   Saved: img/optimal_route.html & img/optimal_route.png")
    
    # 3. Performance comparison chart
    print("\n3. Creating performance comparison chart...")
    fig3 = go.Figure()
    
    fig3.add_trace(go.Bar(
        x=df_results['Algorithm'],
        y=df_results['Time (minutes)'],
        marker_color='#4A90E2',
        text=df_results['Time (minutes)'].round(1),
        textposition='outside',
        name='Travel Time'
    ))
    
    fig3.update_layout(
        title='Perbandingan Waktu Tempuh Antar Algoritma<br>Rute: Dermaga Muara Angke ke RS Siloam Kebon Jeruk',
        xaxis_title='Algoritma',
        yaxis_title='Waktu Tempuh (menit)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=600,
        width=1400,
        font=dict(size=12, family='Arial'),
        xaxis=dict(tickangle=-45)
    )
    
    fig3.write_html('img/algorithm_comparison.html')
    fig3.write_image('img/algorithm_comparison.png', width=1400, height=600, scale=2)
    print("   Saved: img/algorithm_comparison.html & img/algorithm_comparison.png")
    
    # 4. Path comparison table
    print("\n4. Creating detailed path comparison...")
    
    path_details = []
    for _, row in df_results.iterrows():
        if row['Path']:
            path_str = ' -> '.join([network.get_node_info(n)['name'][:20] 
                                   for n in row['Path']])
            path_details.append({
                'Algoritma': row['Algorithm'],
                'Waktu Tempuh': f"{row['Time (minutes)']:.1f} menit",
                'Jumlah Pemberhentian': row['Path Length'],
                'Rute': path_str
            })
    
    df_paths = pd.DataFrame(path_details)
    
    fig4 = go.Figure(data=[go.Table(
        header=dict(
            values=['<b>' + col + '</b>' for col in df_paths.columns],
            fill_color='#457B9D',
            align='left',
            font=dict(color='white', size=12)
        ),
        cells=dict(
            values=[df_paths[col] for col in df_paths.columns],
            fill_color='#F1FAEE',
            align='left',
            font=dict(size=11)
        )
    )])
    
    fig4.update_layout(
        title='Detail Rute Setiap Algoritma',
        height=500,
        width=1400,
        font=dict(family='Arial')
    )
    
    fig4.write_html('img/path_details.html')
    fig4.write_image('img/path_details.png', width=1400, height=500, scale=2)
    print("   Saved: img/path_details.html & img/path_details.png")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\nBest Algorithm: {best_algo['Algorithm']}")
    print(f"Optimal Travel Time: {best_algo['Time (minutes)']:.1f} minutes")
    print(f"Number of Stops: {best_algo['Path Length']}")
    print(f"Route: {' -> '.join([network.get_node_info(n)['name'] for n in best_path])}")
    
    print("\n" + "=" * 80)
    print("ALL VISUALIZATIONS COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    main()
