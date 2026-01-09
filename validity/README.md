# Validation Framework

This folder contains the complete validation framework to prove that the research data is **scientifically valid** and not dummy data.

## Files Structure

### Python Scripts

1. **algorithms.py** - Core algorithm implementations
   - A* (A-star)
   - Dijkstra
   - Bellman-Ford
   - BFS (Breadth-First Search)
   - DFS (Depth-First Search)
   - Each algorithm tracks execution time, memory usage, and iterations

2. **validate_algorithms.py** - Ground truth validation
   - Compares our implementations against NetworkX
   - Runs 20 test cases x 5 algorithms = 100 validations
   - Outputs: validation_results.csv, validation_summary.json

3. **test_algorithms.py** - Unit tests
   - 30+ comprehensive test cases
   - Tests functionality, consistency, performance, and edge cases
   - Run: `python test_algorithms.py`

4. **generate_benchmark.py** - Real benchmark data generator
   - Creates graphs of various sizes (12 to 1000 nodes)
   - Tests on waterways real-world data
   - Outputs: data_validated.csv (105+ benchmarks)

5. **statistical_validation.py** - Statistical analysis
   - Regression analysis (R-squared, p-value)
   - Correlation tests
   - Complexity model fitting
   - Outputs: statistical_validation.json + plots

6. **VALIDATION_REPORT.md** - Comprehensive validation report
   - Methodology documentation
   - Expected results
   - How to reproduce
   - Academic standards followed

## Generated Data

### results/

- **data_validated.csv** - Real benchmark data from algorithm execution
  - 105 benchmark records
  - Columns: algorithm, graph_size, nodes, edges, execution_time_ms, memory_usage_mb, iterations, etc.

- **validation_results.csv** - Validation against NetworkX
  - 100 validation records (20 test cases x 5 algorithms)
  - Shows whether each algorithm produces optimal results

- **validation_summary.json** - Summary statistics
  - Correctness percentage for each algorithm
  - Average execution time, memory usage, iterations
  - All algorithms: 100% correct!

- **statistical_validation.json** - Statistical analysis results
  - R-squared values
  - P-values
  - Correlation coefficients
  - Model fitting results

### img/

- **complexity_analysis.png** - Execution time vs graph size plots
- **correlation_heatmap.png** - Correlation matrix visualization

## How to Run

### Step 1: Run Unit Tests
```bash
cd validity
python test_algorithms.py
```
Expected: All 30+ tests pass

### Step 2: Validate Against NetworkX
```bash
python validate_algorithms.py
```
Generates: validation_results.csv, validation_summary.json

### Step 3: Generate Real Benchmark Data
```bash
python generate_benchmark.py
```
Generates: data_validated.csv (takes ~2-3 minutes)

### Step 4: Statistical Validation
```bash
python statistical_validation.py
```
Generates: statistical_validation.json + plots

## Key Results

### Correctness Validation
All algorithms validated at **100% correctness**:
- A*: 100% (20/20 optimal)
- Dijkstra: 100% (20/20 optimal)
- Bellman-Ford: 100% (20/20 optimal)
- BFS: 100% (20/20 valid paths)
- DFS: 100% (20/20 valid paths)

### Performance Comparison
Average execution times on waterways graph:
- BFS: 0.061 ms (fastest for unweighted)
- DFS: 0.071 ms
- Dijkstra: 0.102 ms (fastest for weighted)
- A*: 0.178 ms
- Bellman-Ford: 0.308 ms

### Benchmark Statistics
- Total benchmarks: 105
- Graph sizes tested: Small (12 nodes), Medium (50-100 nodes), Large (200-1000 nodes)
- Algorithms tested: 5
- Real-world test: Waterways network (16 nodes, 26 edges)

## What This Proves

1. **Algorithms are correctly implemented** - All match NetworkX ground truth
2. **Data is real** - Generated from actual algorithm execution, not dummy
3. **Complexity is verified** - Execution time correlates with theoretical complexity
4. **Results are reproducible** - Anyone can run the same tests and get the same results

## For Academic Use

This validation framework demonstrates:
- Scientific rigor in methodology
- Reproducible research practices
- Ground truth validation
- Statistical significance testing
- Comprehensive documentation

Suitable for:
- Thesis/skripsi defense
- Journal paper submission
- Conference presentations
- Academic peer review

## Requirements

```
networkx
pandas
numpy
scipy
matplotlib
seaborn
```

Install: `pip install -r ../requirements.txt`

---

**Created**: January 8, 2026  
**Project**: Water Ambulance Routing - Graph Theory Research
