"""
Unit Tests untuk Algoritma Pathfinding
Memastikan setiap algoritma bekerja sesuai spesifikasi
"""

import unittest
import networkx as nx
from algorithms import GraphPathfinder, PathfindingResult


class TestPathfindingAlgorithms(unittest.TestCase):
    """Test suite untuk semua algoritma pathfinding"""
    
    def setUp(self):
        """Setup test graph sebelum setiap test"""
        # Create simple test graph
        self.simple_graph = nx.Graph()
        self.simple_graph.add_edge('A', 'B', weight=1)
        self.simple_graph.add_edge('B', 'C', weight=2)
        self.simple_graph.add_edge('A', 'C', weight=5)
        self.simple_graph.add_edge('C', 'D', weight=1)
        
        # Create waterways graph dari CSV
        import pandas as pd
        edges_df = pd.read_csv('csv/waterways_edges.csv')
        self.waterways_graph = nx.Graph()
        for _, row in edges_df.iterrows():
            self.waterways_graph.add_edge(row['Source'], row['Target'], weight=row['Weight'])
        
        self.pathfinder_simple = GraphPathfinder(self.simple_graph)
        self.pathfinder_waterways = GraphPathfinder(self.waterways_graph)
    
    # ========== A* Tests ==========
    
    def test_astar_simple_path(self):
        """Test A* menemukan path pada simple graph"""
        result = self.pathfinder_simple.astar('A', 'D')
        self.assertTrue(result.success)
        self.assertIsNotNone(result.path)
        self.assertEqual(result.path[0], 'A')
        self.assertEqual(result.path[-1], 'D')
    
    def test_astar_optimal_path(self):
        """Test A* menemukan optimal path"""
        result = self.pathfinder_simple.astar('A', 'C')
        self.assertTrue(result.success)
        # Optimal path: A -> B -> C (weight = 3), bukan A -> C (weight = 5)
        self.assertEqual(result.total_weight, 3.0)
    
    def test_astar_waterways(self):
        """Test A* pada waterways graph"""
        result = self.pathfinder_waterways.astar('D1', 'H1')
        self.assertTrue(result.success)
        self.assertGreater(len(result.path), 1)
        self.assertGreater(result.iterations, 0)
    
    def test_astar_no_path(self):
        """Test A* ketika tidak ada path"""
        G = nx.Graph()
        G.add_edge('A', 'B', weight=1)
        G.add_node('C')  # Isolated node
        pathfinder = GraphPathfinder(G)
        result = pathfinder.astar('A', 'C')
        self.assertFalse(result.success)
    
    # ========== Dijkstra Tests ==========
    
    def test_dijkstra_simple_path(self):
        """Test Dijkstra menemukan path pada simple graph"""
        result = self.pathfinder_simple.dijkstra('A', 'D')
        self.assertTrue(result.success)
        self.assertIsNotNone(result.path)
    
    def test_dijkstra_optimal_path(self):
        """Test Dijkstra menemukan optimal path"""
        result = self.pathfinder_simple.dijkstra('A', 'C')
        self.assertTrue(result.success)
        self.assertEqual(result.total_weight, 3.0)
    
    def test_dijkstra_same_as_astar(self):
        """Test Dijkstra menghasilkan hasil sama dengan A* (tanpa heuristic)"""
        astar_result = self.pathfinder_waterways.astar('D1', 'H4')
        dijkstra_result = self.pathfinder_waterways.dijkstra('D1', 'H4')
        
        self.assertEqual(astar_result.total_weight, dijkstra_result.total_weight)
    
    # ========== Bellman-Ford Tests ==========
    
    def test_bellman_ford_simple_path(self):
        """Test Bellman-Ford menemukan path"""
        result = self.pathfinder_simple.bellman_ford('A', 'D')
        self.assertTrue(result.success)
        self.assertIsNotNone(result.path)
    
    def test_bellman_ford_optimal_path(self):
        """Test Bellman-Ford menemukan optimal path"""
        result = self.pathfinder_simple.bellman_ford('A', 'C')
        self.assertTrue(result.success)
        self.assertEqual(result.total_weight, 3.0)
    
    def test_bellman_ford_waterways(self):
        """Test Bellman-Ford pada waterways graph"""
        result = self.pathfinder_waterways.bellman_ford('D5', 'H6')
        self.assertTrue(result.success)
        self.assertGreater(len(result.path), 0)
    
    # ========== BFS Tests ==========
    
    def test_bfs_finds_path(self):
        """Test BFS menemukan path (tidak harus optimal)"""
        result = self.pathfinder_simple.bfs('A', 'D')
        self.assertTrue(result.success)
        self.assertIsNotNone(result.path)
    
    def test_bfs_shortest_hops(self):
        """Test BFS menemukan path dengan minimum hops (bukan minimum weight)"""
        result = self.pathfinder_simple.bfs('A', 'C')
        self.assertTrue(result.success)
        # BFS mungkin pilih A -> C (1 hop, weight=5) bukan A -> B -> C (2 hops, weight=3)
        self.assertEqual(result.path_length, 2)  # 2 nodes: A, C
    
    def test_bfs_waterways(self):
        """Test BFS pada waterways graph"""
        result = self.pathfinder_waterways.bfs('D1', 'H1')
        self.assertTrue(result.success)
    
    # ========== DFS Tests ==========
    
    def test_dfs_finds_path(self):
        """Test DFS menemukan path (tidak harus optimal)"""
        result = self.pathfinder_simple.dfs('A', 'D')
        self.assertTrue(result.success)
        self.assertIsNotNone(result.path)
    
    def test_dfs_waterways(self):
        """Test DFS pada waterways graph"""
        result = self.pathfinder_waterways.dfs('D2', 'H5')
        self.assertTrue(result.success)
    
    # ========== Performance Tests ==========
    
    def test_execution_time_tracked(self):
        """Test bahwa execution time di-track"""
        result = self.pathfinder_waterways.astar('D1', 'H8')
        self.assertGreater(result.execution_time_ms, 0)
    
    def test_memory_usage_tracked(self):
        """Test bahwa memory usage di-track"""
        result = self.pathfinder_waterways.dijkstra('D1', 'H8')
        self.assertGreater(result.memory_usage_mb, 0)
    
    def test_iterations_tracked(self):
        """Test bahwa iterations di-track"""
        result = self.pathfinder_waterways.bellman_ford('D6', 'H2')
        self.assertGreater(result.iterations, 0)
    
    # ========== Consistency Tests ==========
    
    def test_optimal_algorithms_same_weight(self):
        """Test bahwa A*, Dijkstra, Bellman-Ford menghasilkan weight yang sama"""
        start, goal = 'D3', 'H4'
        
        astar = self.pathfinder_waterways.astar(start, goal)
        dijkstra = self.pathfinder_waterways.dijkstra(start, goal)
        bellman = self.pathfinder_waterways.bellman_ford(start, goal)
        
        self.assertAlmostEqual(astar.total_weight, dijkstra.total_weight, places=2)
        self.assertAlmostEqual(dijkstra.total_weight, bellman.total_weight, places=2)
    
    def test_path_validity(self):
        """Test bahwa path yang ditemukan valid (semua edges exist)"""
        result = self.pathfinder_waterways.astar('D4', 'H4')
        
        if result.success and result.path:
            for i in range(len(result.path) - 1):
                current = result.path[i]
                next_node = result.path[i + 1]
                self.assertTrue(
                    self.waterways_graph.has_edge(current, next_node),
                    f"Edge {current} -> {next_node} doesn't exist"
                )
    
    def test_weight_calculation_correct(self):
        """Test bahwa total weight calculation correct"""
        result = self.pathfinder_waterways.astar('D6', 'H2')
        
        if result.success and result.path:
            # Manual calculation
            manual_weight = 0
            for i in range(len(result.path) - 1):
                edge_weight = self.waterways_graph[result.path[i]][result.path[i+1]]['weight']
                manual_weight += edge_weight
            
            self.assertAlmostEqual(result.total_weight, manual_weight, places=2)
    
    # ========== Edge Cases ==========
    
    def test_same_start_and_goal(self):
        """Test ketika start == goal"""
        result = self.pathfinder_simple.astar('A', 'A')
        # Bisa success dengan path = ['A'] atau fail, depends on implementation
        if result.success:
            self.assertEqual(len(result.path), 1)
            self.assertEqual(result.total_weight, 0)
    
    def test_multiple_runs_consistent(self):
        """Test bahwa multiple runs menghasilkan hasil konsisten"""
        start, goal = 'D1', 'H3'
        
        result1 = self.pathfinder_waterways.astar(start, goal)
        result2 = self.pathfinder_waterways.astar(start, goal)
        
        self.assertEqual(result1.path, result2.path)
        self.assertEqual(result1.total_weight, result2.total_weight)


class TestPathfindingResult(unittest.TestCase):
    """Test PathfindingResult class"""
    
    def test_result_initialization(self):
        """Test PathfindingResult initialization"""
        result = PathfindingResult("A*", "start", "goal")
        self.assertEqual(result.algorithm, "A*")
        self.assertEqual(result.start, "start")
        self.assertEqual(result.goal, "goal")
        self.assertIsNone(result.path)
        self.assertFalse(result.success)
    
    def test_result_repr(self):
        """Test PathfindingResult string representation"""
        result = PathfindingResult("Dijkstra", "A", "B")
        result.path = ["A", "B"]
        result.total_weight = 10.5
        result.execution_time_ms = 1.234
        result.memory_usage_mb = 0.5
        
        repr_str = repr(result)
        self.assertIn("Dijkstra", repr_str)
        self.assertIn("10.50", repr_str)


def run_tests_with_coverage():
    """Run tests dan print coverage report"""
    import sys
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print(" TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n All tests passed!")
        return 0
    else:
        print("\n Some tests failed!")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(run_tests_with_coverage())
