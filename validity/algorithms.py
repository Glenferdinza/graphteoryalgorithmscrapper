"""
Implementasi Algoritma Pathfinding dengan Tracking Detail
Setiap algoritma di-trace untuk membuktikan validitas data benchmark
"""

import heapq
import time
import tracemalloc
from collections import deque
from typing import Dict, List, Tuple, Optional, Set
import networkx as nx
import math


class PathfindingResult:
    """Container untuk hasil eksekusi algoritma"""
    def __init__(self, algorithm: str, start: str, goal: str):
        self.algorithm = algorithm
        self.start = start
        self.goal = goal
        self.path: Optional[List[str]] = None
        self.path_length: int = 0
        self.total_weight: float = 0
        self.execution_time_ms: float = 0
        self.memory_usage_mb: float = 0
        self.iterations: int = 0
        self.nodes_explored: List[str] = []
        self.success: bool = False
        
    def __repr__(self):
        return (f"PathfindingResult(algorithm={self.algorithm}, "
                f"path={self.path}, weight={self.total_weight:.2f}, "
                f"time={self.execution_time_ms:.3f}ms, "
                f"memory={self.memory_usage_mb:.3f}MB)")


class GraphPathfinder:
    """Class untuk menjalankan berbagai algoritma pathfinding"""
    
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        
    def heuristic(self, node1: str, node2: str) -> float:
        """
        Heuristic function untuk A* - menggunakan straight-line distance
        Jika tidak ada koordinat, return 0 (jadi seperti Dijkstra)
        """
        if 'x' in self.graph.nodes[node1] and 'y' in self.graph.nodes[node1]:
            x1, y1 = self.graph.nodes[node1]['x'], self.graph.nodes[node1]['y']
            x2, y2 = self.graph.nodes[node2]['x'], self.graph.nodes[node2]['y']
            return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return 0
    
    def reconstruct_path(self, came_from: Dict, current: str) -> List[str]:
        """Rekonstruksi path dari dictionary came_from"""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    def astar(self, start: str, goal: str) -> PathfindingResult:
        """
        Implementasi A* Algorithm dengan tracking detail
        Time Complexity: O(E log V)
        Space Complexity: O(V)
        """
        result = PathfindingResult("A*", start, goal)
        
        # Start tracking
        tracemalloc.start()
        start_time = time.perf_counter()
        
        # A* Algorithm
        open_set = {start}
        came_from = {}
        g_score = {node: float('inf') for node in self.graph.nodes()}
        g_score[start] = 0
        f_score = {node: float('inf') for node in self.graph.nodes()}
        f_score[start] = self.heuristic(start, goal)
        
        # Priority queue: (f_score, node)
        heap = [(f_score[start], start)]
        
        while open_set:
            result.iterations += 1
            
            # Get node with lowest f_score
            current = min(open_set, key=lambda x: f_score[x])
            result.nodes_explored.append(current)
            
            # Goal reached
            if current == goal:
                result.path = self.reconstruct_path(came_from, current)
                result.path_length = len(result.path)
                result.total_weight = g_score[goal]
                result.success = True
                break
            
            open_set.remove(current)
            
            # Explore neighbors
            for neighbor in self.graph.neighbors(current):
                tentative_g_score = g_score[current] + self.graph[current][neighbor].get('weight', 1)
                
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    
                    if neighbor not in open_set:
                        open_set.add(neighbor)
        
        # Stop tracking
        end_time = time.perf_counter()
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        result.execution_time_ms = (end_time - start_time) * 1000
        result.memory_usage_mb = peak_memory / 1024 / 1024
        
        return result
    
    def dijkstra(self, start: str, goal: str) -> PathfindingResult:
        """
        Implementasi Dijkstra Algorithm dengan tracking detail
        Time Complexity: O(E log V)
        Space Complexity: O(V)
        """
        result = PathfindingResult("Dijkstra", start, goal)
        
        # Start tracking
        tracemalloc.start()
        start_time = time.perf_counter()
        
        # Dijkstra Algorithm
        distances = {node: float('inf') for node in self.graph.nodes()}
        distances[start] = 0
        came_from = {}
        visited = set()
        
        # Priority queue: (distance, node)
        heap = [(0, start)]
        
        while heap:
            result.iterations += 1
            
            current_dist, current = heapq.heappop(heap)
            
            if current in visited:
                continue
                
            visited.add(current)
            result.nodes_explored.append(current)
            
            # Goal reached
            if current == goal:
                result.path = self.reconstruct_path(came_from, current)
                result.path_length = len(result.path)
                result.total_weight = distances[goal]
                result.success = True
                break
            
            # Explore neighbors
            for neighbor in self.graph.neighbors(current):
                if neighbor in visited:
                    continue
                    
                weight = self.graph[current][neighbor].get('weight', 1)
                distance = current_dist + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    came_from[neighbor] = current
                    heapq.heappush(heap, (distance, neighbor))
        
        # Stop tracking
        end_time = time.perf_counter()
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        result.execution_time_ms = (end_time - start_time) * 1000
        result.memory_usage_mb = peak_memory / 1024 / 1024
        
        return result
    
    def bellman_ford(self, start: str, goal: str) -> PathfindingResult:
        """
        Implementasi Bellman-Ford Algorithm dengan tracking detail
        Time Complexity: O(V * E)
        Space Complexity: O(V)
        """
        result = PathfindingResult("Bellman-Ford", start, goal)
        
        # Start tracking
        tracemalloc.start()
        start_time = time.perf_counter()
        
        # Bellman-Ford Algorithm
        distances = {node: float('inf') for node in self.graph.nodes()}
        distances[start] = 0
        came_from = {}
        
        nodes = list(self.graph.nodes())
        edges = list(self.graph.edges(data=True))
        
        # Relax edges V-1 times
        for i in range(len(nodes) - 1):
            result.iterations += 1
            updated = False
            
            for u, v, data in edges:
                weight = data.get('weight', 1)
                
                # Check both directions (undirected graph)
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    came_from[v] = u
                    updated = True
                    
                if distances[v] + weight < distances[u]:
                    distances[u] = distances[v] + weight
                    came_from[u] = v
                    updated = True
            
            if not updated:
                break
        
        # Reconstruct path
        if goal in came_from or start == goal:
            result.path = self.reconstruct_path(came_from, goal)
            result.path_length = len(result.path)
            result.total_weight = distances[goal]
            result.success = True
            result.nodes_explored = [n for n in nodes if distances[n] != float('inf')]
        
        # Stop tracking
        end_time = time.perf_counter()
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        result.execution_time_ms = (end_time - start_time) * 1000
        result.memory_usage_mb = peak_memory / 1024 / 1024
        
        return result
    
    def bfs(self, start: str, goal: str) -> PathfindingResult:
        """
        Implementasi BFS (Breadth-First Search) dengan tracking detail
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        Note: BFS tidak mempertimbangkan weight, hanya hop count
        """
        result = PathfindingResult("BFS", start, goal)
        
        # Start tracking
        tracemalloc.start()
        start_time = time.perf_counter()
        
        # BFS Algorithm
        queue = deque([start])
        visited = {start}
        came_from = {}
        
        while queue:
            result.iterations += 1
            current = queue.popleft()
            result.nodes_explored.append(current)
            
            # Goal reached
            if current == goal:
                result.path = self.reconstruct_path(came_from, current)
                result.path_length = len(result.path)
                # Calculate total weight for comparison
                result.total_weight = sum(
                    self.graph[result.path[i]][result.path[i+1]].get('weight', 1)
                    for i in range(len(result.path) - 1)
                )
                result.success = True
                break
            
            # Explore neighbors
            for neighbor in self.graph.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)
        
        # Stop tracking
        end_time = time.perf_counter()
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        result.execution_time_ms = (end_time - start_time) * 1000
        result.memory_usage_mb = peak_memory / 1024 / 1024
        
        return result
    
    def dfs(self, start: str, goal: str) -> PathfindingResult:
        """
        Implementasi DFS (Depth-First Search) dengan tracking detail
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        Note: DFS tidak menjamin shortest path
        """
        result = PathfindingResult("DFS", start, goal)
        
        # Start tracking
        tracemalloc.start()
        start_time = time.perf_counter()
        
        # DFS Algorithm
        stack = [start]
        visited = set()
        came_from = {}
        
        while stack:
            result.iterations += 1
            current = stack.pop()
            
            if current in visited:
                continue
                
            visited.add(current)
            result.nodes_explored.append(current)
            
            # Goal reached
            if current == goal:
                result.path = self.reconstruct_path(came_from, current)
                result.path_length = len(result.path)
                # Calculate total weight
                result.total_weight = sum(
                    self.graph[result.path[i]][result.path[i+1]].get('weight', 1)
                    for i in range(len(result.path) - 1)
                )
                result.success = True
                break
            
            # Explore neighbors
            for neighbor in self.graph.neighbors(current):
                if neighbor not in visited:
                    came_from[neighbor] = current
                    stack.append(neighbor)
        
        # Stop tracking
        end_time = time.perf_counter()
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        result.execution_time_ms = (end_time - start_time) * 1000
        result.memory_usage_mb = peak_memory / 1024 / 1024
        
        return result
    
    def topological_sort(self) -> PathfindingResult:
        """
        Implementasi Topological Sort untuk DAG (Directed Acyclic Graph)
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        Note: Hanya untuk directed graph tanpa cycle
        """
        result = PathfindingResult("Topological-Sort", "START", "END")
        
        # Start tracking
        tracemalloc.start()
        start_time = time.perf_counter()
        
        # Calculate in-degree untuk setiap node
        in_degree = {node: 0 for node in self.graph.nodes()}
        for u, v in self.graph.edges():
            in_degree[v] += 1
        
        # Queue untuk nodes dengan in-degree 0
        queue = deque([node for node in in_degree if in_degree[node] == 0])
        topo_order = []
        
        while queue:
            result.iterations += 1
            node = queue.popleft()
            topo_order.append(node)
            result.nodes_explored.append(node)
            
            for neighbor in self.graph.neighbors(node):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Check if graph is DAG (no cycle)
        if len(topo_order) == len(self.graph.nodes()):
            result.path = topo_order
            result.path_length = len(topo_order)
            result.total_weight = len(topo_order)
            result.success = True
        else:
            result.success = False  # Graph has cycle
        
        # Stop tracking
        end_time = time.perf_counter()
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        result.execution_time_ms = (end_time - start_time) * 1000
        result.memory_usage_mb = peak_memory / 1024 / 1024
        
        return result
    
    def multi_source_bfs(self, sources: List[str], goal: str) -> PathfindingResult:
        """
        Implementasi Multi-Source BFS
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        Berguna untuk routing dari multiple sources ke single destination
        """
        result = PathfindingResult("Multi-Source-BFS", str(sources), goal)
        
        # Start tracking
        tracemalloc.start()
        start_time = time.perf_counter()
        
        # BFS dari multiple sources
        queue = deque(sources)
        visited = set(sources)
        came_from = {source: None for source in sources}
        found_from = None
        
        while queue:
            result.iterations += 1
            current = queue.popleft()
            result.nodes_explored.append(current)
            
            # Goal reached
            if current == goal:
                found_from = current
                break
            
            # Explore neighbors
            for neighbor in self.graph.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)
        
        # Reconstruct path from closest source
        if found_from:
            path = []
            current = goal
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            
            result.path = path
            result.path_length = len(path)
            # Calculate total weight
            result.total_weight = sum(
                self.graph[result.path[i]][result.path[i+1]].get('weight', 1)
                for i in range(len(result.path) - 1)
            )
            result.success = True
        
        # Stop tracking
        end_time = time.perf_counter()
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        result.execution_time_ms = (end_time - start_time) * 1000
        result.memory_usage_mb = peak_memory / 1024 / 1024
        
        return result
    
    def floyd_warshall(self) -> Tuple[Dict, Dict]:
        """
        Implementasi Floyd-Warshall Algorithm
        Time Complexity: O(V^3)
        Space Complexity: O(V^2)
        Menghitung shortest path antara ALL pairs of nodes
        """
        # Start tracking
        tracemalloc.start()
        start_time = time.perf_counter()
        
        nodes = list(self.graph.nodes())
        n = len(nodes)
        node_index = {node: i for i, node in enumerate(nodes)}
        
        # Initialize distance matrix
        INF = float('inf')
        dist = [[INF] * n for _ in range(n)]
        next_node = [[None] * n for _ in range(n)]
        
        # Set diagonal to 0
        for i in range(n):
            dist[i][i] = 0
        
        # Set edges
        for u, v, data in self.graph.edges(data=True):
            i, j = node_index[u], node_index[v]
            weight = data.get('weight', 1)
            dist[i][j] = weight
            dist[j][i] = weight  # Undirected graph
            next_node[i][j] = j
            next_node[j][i] = i
        
        # Floyd-Warshall algorithm
        iterations = 0
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    iterations += 1
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_node[i][j] = next_node[i][k]
        
        # Stop tracking
        end_time = time.perf_counter()
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        execution_time_ms = (end_time - start_time) * 1000
        memory_usage_mb = peak_memory / 1024 / 1024
        
        # Convert to dict format
        dist_dict = {}
        next_dict = {}
        for i, u in enumerate(nodes):
            for j, v in enumerate(nodes):
                dist_dict[(u, v)] = dist[i][j]
                next_dict[(u, v)] = nodes[next_node[i][j]] if next_node[i][j] is not None else None
        
        return {
            'dist': dist_dict,
            'next': next_dict,
            'execution_time_ms': execution_time_ms,
            'memory_usage_mb': memory_usage_mb,
            'iterations': iterations,
            'nodes': nodes
        }
    
    def floyd_warshall_path(self, start: str, goal: str, fw_result: Dict) -> PathfindingResult:
        """
        Extract path dari Floyd-Warshall result
        """
        result = PathfindingResult("Floyd-Warshall", start, goal)
        
        result.execution_time_ms = fw_result['execution_time_ms']
        result.memory_usage_mb = fw_result['memory_usage_mb']
        result.iterations = fw_result['iterations']
        
        # Reconstruct path
        if fw_result['dist'][(start, goal)] == float('inf'):
            result.success = False
            return result
        
        path = [start]
        current = start
        while current != goal:
            current = fw_result['next'][(current, goal)]
            if current is None:
                result.success = False
                return result
            path.append(current)
        
        result.path = path
        result.path_length = len(path)
        result.total_weight = fw_result['dist'][(start, goal)]
        result.success = True
        
        return result
    
    def johnsons_algorithm(self) -> Dict:
        """
        Implementasi Johnson's Algorithm untuk All-Pairs Shortest Path
        Time Complexity: O(V^2 log V + VE)
        Space Complexity: O(V^2)
        Lebih efisien dari Floyd-Warshall untuk sparse graph
        """
        # Start tracking
        tracemalloc.start()
        start_time = time.perf_counter()
        
        # Step 1: Add new node q connected to all nodes with weight 0
        G_temp = self.graph.copy()
        q = 'TEMP_Q_NODE'
        for node in list(self.graph.nodes()):
            G_temp.add_edge(q, node, weight=0)
        
        # Step 2: Run Bellman-Ford dari q untuk detect negative cycle
        temp_pathfinder = GraphPathfinder(G_temp)
        distances_from_q = {}
        iterations = 0
        
        # Simplified Bellman-Ford
        dist = {node: float('inf') for node in G_temp.nodes()}
        dist[q] = 0
        
        for _ in range(len(G_temp.nodes()) - 1):
            for u, v, data in G_temp.edges(data=True):
                iterations += 1
                weight = data.get('weight', 1)
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
        
        # Check for negative cycle
        has_negative_cycle = False
        for u, v, data in G_temp.edges(data=True):
            weight = data.get('weight', 1)
            if dist[u] + weight < dist[v]:
                has_negative_cycle = True
                break
        
        if has_negative_cycle:
            tracemalloc.stop()
            return {'error': 'Graph contains negative cycle'}
        
        distances_from_q = {node: dist[node] for node in self.graph.nodes()}
        
        # Step 3: Reweight edges: w'(u,v) = w(u,v) + h(u) - h(v)
        G_reweighted = self.graph.copy()
        for u, v, data in G_reweighted.edges(data=True):
            old_weight = data.get('weight', 1)
            new_weight = old_weight + distances_from_q[u] - distances_from_q[v]
            G_reweighted[u][v]['weight'] = new_weight
        
        # Step 4: Run Dijkstra dari setiap node
        all_pairs_dist = {}
        reweighted_pathfinder = GraphPathfinder(G_reweighted)
        
        for source in self.graph.nodes():
            dijkstra_result = reweighted_pathfinder.dijkstra(source, list(self.graph.nodes())[0])
            # Get distances to all nodes (simplified)
            for target in self.graph.nodes():
                if source == target:
                    all_pairs_dist[(source, target)] = 0
                else:
                    # Try to get distance
                    temp_result = reweighted_pathfinder.dijkstra(source, target)
                    if temp_result.success:
                        # Correct weight: d(u,v) = d'(u,v) - h(u) + h(v)
                        corrected_weight = (temp_result.total_weight - 
                                          distances_from_q[source] + 
                                          distances_from_q[target])
                        all_pairs_dist[(source, target)] = corrected_weight
                        iterations += temp_result.iterations
                    else:
                        all_pairs_dist[(source, target)] = float('inf')
        
        # Stop tracking
        end_time = time.perf_counter()
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        return {
            'dist': all_pairs_dist,
            'execution_time_ms': (end_time - start_time) * 1000,
            'memory_usage_mb': peak_memory / 1024 / 1024,
            'iterations': iterations,
            'reweighting': distances_from_q
        }
    
    def johnsons_path(self, start: str, goal: str, johnsons_result: Dict) -> PathfindingResult:
        """
        Extract path dari Johnson's Algorithm result
        """
        result = PathfindingResult("Johnsons-Algorithm", start, goal)
        
        result.execution_time_ms = johnsons_result['execution_time_ms']
        result.memory_usage_mb = johnsons_result['memory_usage_mb']
        result.iterations = johnsons_result['iterations']
        
        # Get distance
        dist = johnsons_result['dist'].get((start, goal), float('inf'))
        
        if dist == float('inf'):
            result.success = False
            return result
        
        # Reconstruct path using reweighted graph + Dijkstra
        h = johnsons_result['reweighting']
        G_reweighted = self.graph.copy()
        for u, v, data in G_reweighted.edges(data=True):
            old_weight = data.get('weight', 1)
            new_weight = old_weight + h[u] - h[v]
            G_reweighted[u][v]['weight'] = new_weight
        
        pathfinder = GraphPathfinder(G_reweighted)
        temp_result = pathfinder.dijkstra(start, goal)
        
        if temp_result.success:
            result.path = temp_result.path
            result.path_length = temp_result.path_length
            result.total_weight = dist
            result.success = True
        else:
            result.success = False
        
        return result


if __name__ == "__main__":
    # Quick test dengan waterways graph
    import pandas as pd
    
    print(" Testing Algorithms Implementation...\n")
    
    # Load waterways graph
    edges_df = pd.read_csv('csv/waterways_edges.csv')
    G = nx.Graph()
    
    for _, row in edges_df.iterrows():
        G.add_edge(row['Source'], row['Target'], weight=row['Weight'])
    
    # Initialize pathfinder
    pathfinder = GraphPathfinder(G)
    
    # Test case: D1 to H1
    start, goal = 'D1', 'H1'
    print(f"Test Route: {start}  {goal}\n")
    print("=" * 70)
    
    # Run all algorithms
    algorithms = [
        ('A*', pathfinder.astar),
        ('Dijkstra', pathfinder.dijkstra),
        ('Bellman-Ford', pathfinder.bellman_ford),
        ('BFS', pathfinder.bfs),
        ('DFS', pathfinder.dfs),
        ('Topological-Sort', lambda s, g: pathfinder.topological_sort()),
        ('Multi-Source-BFS', lambda s, g: pathfinder.multi_source_bfs(['D1', 'D2'], g))
    ]
    
    for name, algo_func in algorithms:
        if name in ['Topological-Sort']:
            result = algo_func(start, goal)
            print(f"\n{name}:")
            print(f"  Path: {'  '.join(result.path) if result.path else 'Not found'}")
            print(f"  Total Weight: {result.total_weight:.1f}")
            print(f"  Path Length: {result.path_length} nodes")
            print(f"  Execution Time: {result.execution_time_ms:.3f} ms")
            print(f"  Memory Usage: {result.memory_usage_mb:.3f} MB")
            print(f"  Iterations: {result.iterations}")
        else:
            result = algo_func(start, goal)
            print(f"\n{name}:")
            print(f"  Path: {'  '.join(result.path) if result.path else 'Not found'}")
            print(f"  Total Weight: {result.total_weight:.1f} min")
            print(f"  Path Length: {result.path_length} nodes")
            print(f"  Execution Time: {result.execution_time_ms:.3f} ms")
            print(f"  Memory Usage: {result.memory_usage_mb:.3f} MB")
            print(f"  Iterations: {result.iterations}")
    
    # Test Floyd-Warshall
    print("\n\nFloyd-Warshall (All-Pairs Shortest Path):")
    fw_result = pathfinder.floyd_warshall()
    print(f"  Execution Time: {fw_result['execution_time_ms']:.3f} ms")
    print(f"  Memory Usage: {fw_result['memory_usage_mb']:.3f} MB")
    print(f"  Iterations: {fw_result['iterations']}")
    fw_path = pathfinder.floyd_warshall_path(start, goal, fw_result)
    print(f"  Path {start}  {goal}: {'  '.join(fw_path.path) if fw_path.path else 'Not found'}")
    print(f"  Total Weight: {fw_path.total_weight:.1f} min")
    
    # Test Johnson's Algorithm
    print("\n\nJohnsons-Algorithm (All-Pairs Shortest Path):")
    johnsons_result = pathfinder.johnsons_algorithm()
    if 'error' not in johnsons_result:
        print(f"  Execution Time: {johnsons_result['execution_time_ms']:.3f} ms")
        print(f"  Memory Usage: {johnsons_result['memory_usage_mb']:.3f} MB")
        print(f"  Iterations: {johnsons_result['iterations']}")
        johnsons_path = pathfinder.johnsons_path(start, goal, johnsons_result)
        print(f"  Path {start}  {goal}: {'  '.join(johnsons_path.path) if johnsons_path.path else 'Not found'}")
        print(f"  Total Weight: {johnsons_path.total_weight:.1f} min")
    else:
        print(f"  Error: {johnsons_result['error']}")
    
    print("\n" + "=" * 70)
    print("\n Algorithm implementation test complete!")
