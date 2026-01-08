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
        ('DFS', pathfinder.dfs)
    ]
    
    for name, algo_func in algorithms:
        result = algo_func(start, goal)
        print(f"\n{name}:")
        print(f"  Path: {'  '.join(result.path) if result.path else 'Not found'}")
        print(f"  Total Weight: {result.total_weight:.1f} min")
        print(f"  Path Length: {result.path_length} nodes")
        print(f"  Execution Time: {result.execution_time_ms:.3f} ms")
        print(f"  Memory Usage: {result.memory_usage_mb:.3f} MB")
        print(f"  Iterations: {result.iterations}")
    
    print("\n" + "=" * 70)
    print("\n Algorithm implementation test complete!")
