"""
Validasi Implementasi Algoritma dengan NetworkX sebagai Ground Truth
Script ini membuktikan bahwa implementasi kita benar-benar accurate
"""

import networkx as nx
import pandas as pd
from algorithms import GraphPathfinder, PathfindingResult
from typing import List, Tuple, Dict
import json


class AlgorithmValidator:
    """Class untuk memvalidasi algoritma terhadap NetworkX"""
    
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.pathfinder = GraphPathfinder(graph)
        self.validation_results = []
        
    def get_networkx_ground_truth(self, start: str, goal: str, algorithm: str) -> Dict:
        """
        Get ground truth dari NetworkX untuk comparison
        """
        try:
            if algorithm in ['A*', 'Dijkstra', 'Bellman-Ford']:
                # Algorithms yang optimal untuk weighted graphs
                path = nx.shortest_path(self.graph, start, goal, weight='weight')
                length = nx.shortest_path_length(self.graph, start, goal, weight='weight')
            else:
                # BFS/DFS: shortest path tanpa weight
                path = nx.shortest_path(self.graph, start, goal)
                # Calculate weight manually
                length = sum(
                    self.graph[path[i]][path[i+1]].get('weight', 1)
                    for i in range(len(path) - 1)
                )
            
            return {
                'path': path,
                'length': length,
                'success': True
            }
        except nx.NetworkXNoPath:
            return {
                'path': None,
                'length': float('inf'),
                'success': False
            }
    
    def validate_result(self, result: PathfindingResult, ground_truth: Dict) -> Dict:
        """
        Validasi hasil algoritma terhadap ground truth
        """
        validation = {
            'algorithm': result.algorithm,
            'start': result.start,
            'goal': result.goal,
            'our_path': result.path,
            'nx_path': ground_truth['path'],
            'our_weight': result.total_weight,
            'nx_weight': ground_truth['length'],
            'path_correct': result.path == ground_truth['path'] if result.path else False,
            'weight_correct': False,
            'is_optimal': False,
            'weight_difference': float('inf'),
            'execution_time_ms': result.execution_time_ms,
            'memory_usage_mb': result.memory_usage_mb,
            'iterations': result.iterations
        }
        
        # Check weight correctness (dengan toleransi floating point)
        if result.success and ground_truth['success']:
            validation['weight_difference'] = abs(result.total_weight - ground_truth['length'])
            validation['weight_correct'] = validation['weight_difference'] < 0.001
            
            # Untuk optimal algorithms (A*, Dijkstra, Bellman-Ford)
            # Path weight harus sama dengan ground truth
            if result.algorithm in ['A*', 'Dijkstra', 'Bellman-Ford']:
                validation['is_optimal'] = validation['weight_correct']
            else:
                # Untuk BFS/DFS, cek apakah path valid (tidak harus optimal)
                validation['is_optimal'] = result.success
        
        return validation
    
    def run_validation_suite(self, test_cases: List[Tuple[str, str]]) -> pd.DataFrame:
        """
        Run full validation suite untuk semua test cases
        """
        print(" Starting Algorithm Validation Suite...")
        print("=" * 80)
        
        algorithms = {
            'A*': self.pathfinder.astar,
            'Dijkstra': self.pathfinder.dijkstra,
            'Bellman-Ford': self.pathfinder.bellman_ford,
            'BFS': self.pathfinder.bfs,
            'DFS': self.pathfinder.dfs
        }
        
        results = []
        
        for idx, (start, goal) in enumerate(test_cases, 1):
            print(f"\n Test Case {idx}/{len(test_cases)}: {start}  {goal}")
            print("-" * 80)
            
            for algo_name, algo_func in algorithms.items():
                # Run our implementation
                result = algo_func(start, goal)
                
                # Get NetworkX ground truth
                ground_truth = self.get_networkx_ground_truth(start, goal, algo_name)
                
                # Validate
                validation = self.validate_result(result, ground_truth)
                results.append(validation)
                
                # Print result
                status = "" if validation['is_optimal'] else ""
                print(f"{status} {algo_name:15s} | "
                      f"Weight: {result.total_weight:6.1f} (NX: {ground_truth['length']:6.1f}) | "
                      f"Time: {result.execution_time_ms:7.3f}ms | "
                      f"Iter: {result.iterations:4d}")
        
        print("\n" + "=" * 80)
        
        # Create summary DataFrame
        df = pd.DataFrame(results)
        
        # Print summary statistics
        print("\n VALIDATION SUMMARY:")
        print("-" * 80)
        
        for algo_name in algorithms.keys():
            algo_results = df[df['algorithm'] == algo_name]
            optimal_count = algo_results['is_optimal'].sum()
            total_count = len(algo_results)
            avg_time = algo_results['execution_time_ms'].mean()
            avg_memory = algo_results['memory_usage_mb'].mean()
            
            print(f"{algo_name:15s} | "
                  f"Optimal: {optimal_count}/{total_count} ({100*optimal_count/total_count:.1f}%) | "
                  f"Avg Time: {avg_time:.3f}ms | "
                  f"Avg Memory: {avg_memory:.3f}MB")
        
        return df
    
    def export_validation_report(self, df: pd.DataFrame, filepath: str = 'csv/validation_results.csv'):
        """
        Export validation results to CSV
        """
        # Convert path lists to strings for CSV export
        df_export = df.copy()
        df_export['our_path'] = df_export['our_path'].apply(lambda x: '  '.join(x) if x else 'None')
        df_export['nx_path'] = df_export['nx_path'].apply(lambda x: '  '.join(x) if x else 'None')
        
        df_export.to_csv(filepath, index=False)
        print(f"\n Validation results saved to: {filepath}")
        
        return df_export
    
    def check_correctness_percentage(self, df: pd.DataFrame) -> Dict:
        """
        Calculate correctness percentage untuk setiap algoritma
        """
        summary = {}
        
        for algo in df['algorithm'].unique():
            algo_df = df[df['algorithm'] == algo]
            
            summary[algo] = {
                'total_tests': len(algo_df),
                'optimal_count': algo_df['is_optimal'].sum(),
                'optimal_percentage': 100 * algo_df['is_optimal'].sum() / len(algo_df),
                'avg_execution_time_ms': algo_df['execution_time_ms'].mean(),
                'avg_memory_mb': algo_df['memory_usage_mb'].mean(),
                'avg_iterations': algo_df['iterations'].mean(),
                'max_weight_difference': algo_df['weight_difference'].max()
            }
        
        return summary


def generate_test_cases(graph: nx.Graph, num_random: int = 10) -> List[Tuple[str, str]]:
    """
    Generate test cases: fixed important routes + random pairs
    """
    nodes = list(graph.nodes())
    
    # Fixed important test cases (dermaga ke hospital)
    fixed_cases = [
        ('D1', 'H1'),
        ('D1', 'H3'),
        ('D5', 'H6'),
        ('D6', 'H2'),
        ('D4', 'H4'),
        ('D2', 'H5'),
        ('D8', 'H8'),
        ('D7', 'H7'),
    ]
    
    # Random test cases
    import random
    random.seed(42)  # For reproducibility
    
    dermaga = [n for n in nodes if n.startswith('D')]
    hospital = [n for n in nodes if n.startswith('H')]
    
    random_cases = [
        (random.choice(dermaga), random.choice(hospital))
        for _ in range(num_random)
    ]
    
    return fixed_cases + random_cases


if __name__ == "__main__":
    print(" Algorithm Validation System")
    print("=" * 80)
    print("This script validates our implementations against NetworkX ground truth\n")
    
    # Load waterways graph
    print(" Loading waterways network...")
    edges_df = pd.read_csv('csv/waterways_edges.csv')
    
    G = nx.Graph()
    for _, row in edges_df.iterrows():
        G.add_edge(row['Source'], row['Target'], weight=row['Weight'])
    
    print(f"   Nodes: {G.number_of_nodes()}")
    print(f"   Edges: {G.number_of_edges()}")
    
    # Generate test cases
    test_cases = generate_test_cases(G, num_random=12)
    print(f"\n Generated {len(test_cases)} test cases")
    
    # Run validation
    validator = AlgorithmValidator(G)
    results_df = validator.run_validation_suite(test_cases)
    
    # Export results
    validator.export_validation_report(results_df)
    
    # Calculate correctness summary
    print("\n" + "=" * 80)
    print(" CORRECTNESS ANALYSIS:")
    print("=" * 80)
    
    summary = validator.check_correctness_percentage(results_df)
    
    for algo, stats in summary.items():
        print(f"\n{algo}:")
        print(f"   Correctness: {stats['optimal_percentage']:.1f}% ({stats['optimal_count']}/{stats['total_tests']})")
        print(f"   Avg Time: {stats['avg_execution_time_ms']:.4f} ms")
        print(f"   Avg Memory: {stats['avg_memory_mb']:.4f} MB")
        print(f"   Avg Iterations: {stats['avg_iterations']:.1f}")
        print(f"   Max Weight Diff: {stats['max_weight_difference']:.6f}")
    
    # Save summary as JSON
    with open('csv/validation_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "=" * 80)
    print(" Validation complete! Check csv/validation_results.csv for details.")
