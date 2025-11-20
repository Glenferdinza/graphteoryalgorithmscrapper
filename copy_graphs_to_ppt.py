"""
Script untuk copy semua grafik ke folder ppt_graphs dengan nama yang jelas
"""

import shutil
import os
from pathlib import Path

# Define source and destination
source_dir = Path("img")
dest_dir = Path("ppt_graphs")

# Create destination directory if not exists
dest_dir.mkdir(exist_ok=True)

# Mapping: source_file -> destination_file
file_mapping = {
    "multi_metric_analysis.png": "1_multi_metric_comparison.png",
    "efficiency_scatter.png": "2_efficiency_scatter.png",
    "radar_complexity.png": "3_radar_characteristics.png",
    "comprehensive_ranking.png": "4_ranking_table.png",
    "path_complexity.png": "5_path_complexity.png",
    "network_map.png": "6_optimal_route_map.png",
    "optimal_route.png": "6_optimal_route_map.png",  # Alternative name
    "path_details.png": "7_path_details.png",
    "algorithm_comparison.png": "8_algorithm_comparison.png",
}

print("=" * 80)
print("COPYING GRAPHS TO PPT_GRAPHS FOLDER")
print("=" * 80)

copied_count = 0
missing_count = 0

for source_name, dest_name in file_mapping.items():
    source_path = source_dir / source_name
    dest_path = dest_dir / dest_name
    
    if source_path.exists():
        shutil.copy2(source_path, dest_path)
        print(f"✅ Copied: {source_name} -> {dest_name}")
        copied_count += 1
    else:
        print(f"⚠️  Missing: {source_name} (skipped)")
        missing_count += 1

# Also copy HTML versions for interactive viewing
html_mapping = {
    "multi_metric_analysis.html": "1_multi_metric_comparison.html",
    "efficiency_scatter.html": "2_efficiency_scatter.html",
    "radar_complexity.html": "3_radar_characteristics.html",
    "comprehensive_ranking.html": "4_ranking_table.html",
    "path_complexity.html": "5_path_complexity.html",
    "network_map.html": "6_optimal_route_map.html",
    "optimal_route.html": "6_optimal_route_map_alt.html",
    "path_details.html": "7_path_details.html",
}

print("\n" + "-" * 80)
print("COPYING HTML INTERACTIVE VERSIONS")
print("-" * 80)

html_copied = 0
for source_name, dest_name in html_mapping.items():
    source_path = source_dir / source_name
    dest_path = dest_dir / dest_name
    
    if source_path.exists():
        shutil.copy2(source_path, dest_path)
        print(f"✅ Copied: {source_name} -> {dest_name}")
        html_copied += 1
    else:
        print(f"⚠️  Missing: {source_name} (skipped)")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"PNG files copied: {copied_count}")
print(f"PNG files missing: {missing_count}")
print(f"HTML files copied: {html_copied}")
print(f"\nDestination: {dest_dir.absolute()}")
print("=" * 80)

# List all files in ppt_graphs
print("\n📁 Files in ppt_graphs folder:")
print("-" * 80)
if dest_dir.exists():
    files = sorted(dest_dir.iterdir())
    for i, file in enumerate(files, 1):
        size_kb = file.stat().st_size / 1024 if file.is_file() else 0
        if file.is_file():
            print(f"{i:2d}. {file.name:40s} ({size_kb:>8.1f} KB)")
else:
    print("⚠️  Folder not found!")

print("\n✅ Done! Check folder: ppt_graphs/")
print("📖 Read README.md in ppt_graphs/ for usage guide")
