"""
Generate Benchmark Data yang RIIL dari Eksekusi Algoritma
Script ini menggantikan data dummy dengan data hasil eksekusi sebenarnya
"""

import pandas as pd
import networkx as nx
import numpy as np
from algorithms import GraphPathfinder
from typing import List, Dict
import random


def create_graph_with_size(num_nodes: int, density: float = 0.3, seed: int = 42) -> nx.Graph:
    """
    Create random graph dengan ukuran tertentu
    
    Args:
        num_nodes: Jumlah nodes
        density: Kepadatan edges (0-1)
        seed: Random seed untuk reproducibility
    """
    random.seed(seed)
    np.random.seed(seed)
    
    G = nx.Graph()
    
    # Add nodes
    for i in range(num_nodes):
        G.add_node(f"N{i}")
    
    # Add edges based on density
    nodes = list(G.nodes())
    max_edges = num_nodes * (num_nodes - 1) // 2
    num_edges = int(max_edges * density)
    
    edges_added = 0
    attempts = 0
    max_attempts = num_edges * 10
    
    while edges_added < num_edges and attempts < max_attempts:
        u = random.choice(nodes)
        v = random.choice(nodes)
        
        if u != v and not G.has_edge(u, v):
            weight = random.randint(1, 100)
            G.add_edge(u, v, weight=weight)
            edges_added += 1
        
        attempts += 1
    
    # Ensure graph is connected
    if not nx.is_connected(G):
        # Connect components
        components = list(nx.connected_components(G))
        for i in range(len(components) - 1):
            u = random.choice(list(components[i]))
            v = random.choice(list(components[i + 1]))
            weight = random.randint(1, 100)
            G.add_edge(u, v, weight=weight)
    
    return G


def benchmark_algorithm_on_graph(pathfinder: GraphPathfinder, 
                                  algorithm_name: str,
                                  start: str, 
                                  goal: str,
                                  graph_size: str,
                                  num_nodes: int,
                                  num_edges: int) -> Dict:
    """
    Benchmark satu algoritma pada satu graph
    """
    algorithms = {
        'A*': pathfinder.astar,
        'Dijkstra': pathfinder.dijkstra,
        'Bellman-Ford': pathfinder.bellman_ford,
        'BFS': pathfinder.bfs,
        'DFS': pathfinder.dfs
    }
    
    algo_func = algorithms[algorithm_name]
    result = algo_func(start, goal)
    
    # Complexity mapping
    complexity_map = {
        'A*': 'O(E log V)',
        'Dijkstra': 'O(E log V)',
        'Bellman-Ford': 'O(V * E)',
        'BFS': 'O(V + E)',
        'DFS': 'O(V + E)'
    }
    
    return {
        'algorithm': algorithm_name,
        'graph_size': graph_size,
        'nodes': num_nodes,
        'edges': num_edges,
        'execution_time_ms': result.execution_time_ms,
        'memory_usage_mb': result.memory_usage_mb,
        'path_length': result.path_length if result.success else 0,
        'total_weight': result.total_weight if result.success else float('inf'),
        'iterations': result.iterations,
        'nodes_explored': len(result.nodes_explored),
        'success': result.success,
        'complexity': complexity_map[algorithm_name]
    }


def generate_comprehensive_benchmark() -> pd.DataFrame:
    """
    Generate comprehensive benchmark untuk berbagai ukuran graph
    """
    print("Generating REAL Benchmark Data...")
    print("=" * 80)
    
    # Define graph sizes
    graph_configs = [
        {'size': 'small', 'nodes': 12, 'density': 0.4, 'runs': 5},
        {'size': 'medium', 'nodes': 50, 'density': 0.2, 'runs': 3},
        {'size': 'medium', 'nodes': 100, 'density': 0.15, 'runs': 3},
        {'size': 'large', 'nodes': 200, 'density': 0.1, 'runs': 2},
        {'size': 'large', 'nodes': 500, 'density': 0.05, 'runs': 2},
        {'size': 'large', 'nodes': 1000, 'density': 0.03, 'runs': 1},
    ]
    
    algorithms = ['A*', 'Dijkstra', 'Bellman-Ford', 'BFS', 'DFS']
    
    all_results = []
    
    for config in graph_configs:
        print(f"\nBenchmarking {config['size'].upper()} graphs ({config['nodes']} nodes)...")
        print("-" * 80)
        
        for run in range(config['runs']):
            # Create graph
            G = create_graph_with_size(
                config['nodes'], 
                config['density'], 
                seed=42 + run
            )
            
            num_nodes = G.number_of_nodes()
            num_edges = G.number_of_edges()
            
            print(f"  Run {run+1}/{config['runs']}: {num_nodes} nodes, {num_edges} edges")
            
            # Select random start and goal
            nodes = list(G.nodes())
            start = random.choice(nodes)
            goal = random.choice([n for n in nodes if n != start])
            
            # Benchmark each algorithm
            pathfinder = GraphPathfinder(G)
            
            for algo in algorithms:
                try:
                    result = benchmark_algorithm_on_graph(
                        pathfinder, algo, start, goal,
                        config['size'], num_nodes, num_edges
                    )
                    all_results.append(result)
                    
                    status = "" if result['success'] else ""
                    print(f"    {status} {algo:15s} | "
                          f"Time: {result['execution_time_ms']:8.3f}ms | "
                          f"Mem: {result['memory_usage_mb']:6.3f}MB | "
                          f"Iter: {result['iterations']:5d}")
                    
                except Exception as e:
                    print(f"     {algo:15s} | ERROR: {str(e)}")
    
    # Add waterways benchmark (real-world data)
    print(f"\nBenchmarking WATERWAYS graph (real data)...")
    print("-" * 80)
    
    edges_df = pd.read_csv('csv/waterways_edges.csv')
    G_waterways = nx.Graph()
    for _, row in edges_df.iterrows():
        G_waterways.add_edge(row['Source'], row['Target'], weight=row['Weight'])
    
    pathfinder_waterways = GraphPathfinder(G_waterways)
    
    # Test multiple routes
    test_routes = [
        ('D1', 'H1'),
        ('D1', 'H3'),
        ('D5', 'H6'),
        ('D6', 'H2'),
        ('D4', 'H4'),
    ]
    
    for start, goal in test_routes:
        print(f"  Route: {start}  {goal}")
        
        for algo in algorithms:
            try:
                result = benchmark_algorithm_on_graph(
                    pathfinder_waterways, algo, start, goal,
                    'waterways', 
                    G_waterways.number_of_nodes(), 
                    G_waterways.number_of_edges()
                )
                all_results.append(result)
                
                status = "" if result['success'] else ""
                print(f"    {status} {algo:15s} | "
                      f"Time: {result['execution_time_ms']:8.3f}ms | "
                      f"Path: {result['path_length']:2d} nodes | "
                      f"Weight: {result['total_weight']:6.1f}")
                
            except Exception as e:
                print(f"     {algo:15s} | ERROR: {str(e)}")
    
    print("\n" + "=" * 80)
    
    return pd.DataFrame(all_results)


def add_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived metrics untuk analisis lebih lanjut
    """
    df = df.copy()
    
    # Efficiency score: lower is better (combined time and memory)
    df['efficiency_score'] = (
        df['execution_time_ms'] / df['execution_time_ms'].max() * 0.6 +
        df['memory_usage_mb'] / df['memory_usage_mb'].max() * 0.4
    )
    
    # Throughput: nodes processed per ms
    df['throughput'] = df['nodes_explored'] / (df['execution_time_ms'] + 0.001)
    
    # Memory efficiency: nodes per MB
    df['memory_efficiency'] = df['nodes_explored'] / (df['memory_usage_mb'] + 0.001)
    
    return df


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print(" REAL BENCHMARK DATA GENERATOR")
    print("=" * 80)
    print("This script generates ACTUAL benchmark data from algorithm execution\n")
    
    # Generate benchmark
    df = generate_comprehensive_benchmark()
    
    # Add derived metrics
    df = add_derived_metrics(df)
    
    # Save results
    output_file = 'csv/data_validated.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n Results saved to: {output_file}")
    print(f"   Total benchmarks: {len(df)}")
    print(f"   Algorithms tested: {df['algorithm'].nunique()}")
    print(f"   Graph sizes: {df['graph_size'].nunique()}")
    
    # Print summary statistics
    print("\n SUMMARY STATISTICS:")
    print("=" * 80)
    
    summary = df.groupby('algorithm').agg({
        'execution_time_ms': ['mean', 'std', 'min', 'max'],
        'memory_usage_mb': ['mean', 'std'],
        'iterations': ['mean'],
        'success': ['sum', 'count']
    }).round(3)
    
    print(summary)
    
    print("\n" + "=" * 80)
    print(" Benchmark generation complete!")
    print("\nNext steps:")
    print("  1. Run: python validate_algorithms.py (to validate against NetworkX)")
    print("  2. Run: python statistical_validation.py (to prove complexity)")
    print("  3. Compare data.csv (old dummy) vs data_validated.csv (new real)")
