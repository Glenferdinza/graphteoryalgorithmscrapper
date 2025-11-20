"""
Enhanced Visualization for Water Ambulance Routing
Membuat visualisasi tambahan untuk perbandingan mendalam antar algoritma
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import networkx as nx

# Load results
df = pd.read_csv('csv/ambulance_routing_results.csv')

# Parse path strings back to lists
import ast
df['Path'] = df['Path'].apply(ast.literal_eval)

print("Generating enhanced visualizations...")

# ============================================================================
# VISUALIZATION 1: Multi-Metric Comparison
# ============================================================================

print("\n1. Creating multi-metric comparison chart...")

fig1 = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Waktu Tempuh', 'Jumlah Pemberhentian', 
                   'Iterasi Algoritma', 'Execution Time'),
    vertical_spacing=0.12,
    horizontal_spacing=0.1
)

colors = ['#E63946' if t > 50 else '#2A9D8F' for t in df['Time (minutes)']]

fig1.add_trace(
    go.Bar(x=df['Algorithm'], y=df['Time (minutes)'], 
           marker_color=colors, name='Waktu Tempuh',
           text=df['Time (minutes)'], textposition='outside'),
    row=1, col=1
)

fig1.add_trace(
    go.Bar(x=df['Algorithm'], y=df['Path Length'], 
           marker_color='#4A90E2', name='Pemberhentian',
           text=df['Path Length'], textposition='outside'),
    row=1, col=2
)

fig1.add_trace(
    go.Bar(x=df['Algorithm'], y=df['Iterations'], 
           marker_color='#F4A261', name='Iterasi',
           text=df['Iterations'], textposition='outside'),
    row=2, col=1
)

fig1.add_trace(
    go.Bar(x=df['Algorithm'], y=df['Execution Time (ms)'], 
           marker_color='#A8DADC', name='Exec Time',
           text=df['Execution Time (ms)'].round(3), textposition='outside'),
    row=2, col=2
)

fig1.update_xaxes(tickangle=-45)
fig1.update_layout(
    title_text='Analisis Multi-Metrik Performa 9 Algoritma Routing',
    showlegend=False,
    height=800,
    width=1400,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(size=11, family='Arial')
)

fig1.write_html('img/multi_metric_analysis.html')
fig1.write_image('img/multi_metric_analysis.png', width=1400, height=800, scale=2)
print("   Saved: img/multi_metric_analysis.png")

# ============================================================================
# VISUALIZATION 2: Efficiency Scatter Plot
# ============================================================================

print("\n2. Creating efficiency scatter plot...")

fig2 = go.Figure()

optimal_algos = df[df['Time (minutes)'] == df['Time (minutes)'].min()]['Algorithm'].tolist()
suboptimal_algos = df[df['Time (minutes)'] > df['Time (minutes)'].min()]['Algorithm'].tolist()

for _, row in df.iterrows():
    color = '#2A9D8F' if row['Algorithm'] in optimal_algos else '#E63946'
    symbol = 'circle' if row['Algorithm'] in optimal_algos else 'diamond'
    
    fig2.add_trace(go.Scatter(
        x=[row['Iterations']],
        y=[row['Execution Time (ms)']],
        mode='markers+text',
        marker=dict(size=row['Time (minutes)'] * 2, color=color, 
                   line=dict(width=2, color='white'), symbol=symbol),
        text=[row['Algorithm']],
        textposition='top center',
        name=row['Algorithm'],
        hovertemplate=f"<b>{row['Algorithm']}</b><br>" +
                     f"Iterations: {row['Iterations']}<br>" +
                     f"Exec Time: {row['Execution Time (ms)']:.3f} ms<br>" +
                     f"Travel Time: {row['Time (minutes)']} min<br>" +
                     "<extra></extra>"
    ))

fig2.update_layout(
    title='Efisiensi Komputasi vs Kualitas Solusi<br><sub>Ukuran marker = waktu tempuh | Hijau = optimal, Merah = suboptimal</sub>',
    xaxis_title='Jumlah Iterasi (log scale)',
    yaxis_title='Execution Time (ms)',
    xaxis_type='log',
    plot_bgcolor='white',
    paper_bgcolor='white',
    height=700,
    width=1400,
    showlegend=False,
    font=dict(size=12, family='Arial')
)

fig2.write_html('img/efficiency_scatter.html')
fig2.write_image('img/efficiency_scatter.png', width=1400, height=700, scale=2)
print("   Saved: img/efficiency_scatter.png")

# ============================================================================
# VISUALIZATION 3: Route Complexity Analysis
# ============================================================================

print("\n3. Creating route complexity radar chart...")

df_sorted = df.sort_values('Time (minutes)')

fig3 = go.Figure()

metrics_normalized = df_sorted.copy()
metrics_normalized['Time_norm'] = 100 - (metrics_normalized['Time (minutes)'] - 50) * 10
metrics_normalized['Length_norm'] = 100 - (metrics_normalized['Path Length'] - 1) * 20
metrics_normalized['Iter_norm'] = 100 - (metrics_normalized['Iterations'] / metrics_normalized['Iterations'].max() * 100)
metrics_normalized['Exec_norm'] = 100 - (metrics_normalized['Execution Time (ms)'] / metrics_normalized['Execution Time (ms)'].max() * 100)

categories = ['Kecepatan Rute', 'Kesederhanaan Path', 'Efisiensi Iterasi', 'Kecepatan Komputasi']

colors_radar = {
    'Dijkstra': '#2A9D8F',
    'Bellman-Ford': '#4A90E2',
    'Floyd-Warshall': '#F4A261',
    'Johnson': '#E9C46A',
    'Topological Sort': '#95D5B2',
    'DFS': '#E63946',
    'BFS': '#457B9D',
    'A*': '#F1FAEE',
    'Multi-Source BFS': '#A8DADC'
}

for idx, row in metrics_normalized.iterrows():
    values = [
        row['Time_norm'],
        row['Length_norm'],
        row['Iter_norm'],
        row['Exec_norm']
    ]
    values.append(values[0])
    
    fig3.add_trace(go.Scatterpolar(
        r=values,
        theta=categories + [categories[0]],
        fill='toself',
        name=row['Algorithm'],
        line=dict(color=colors_radar.get(row['Algorithm'], '#CCCCCC'), width=2),
        opacity=0.6
    ))

fig3.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 100], showline=True, 
                       linewidth=2, gridcolor='lightgray')
    ),
    title='Radar Perbandingan Karakteristik Algoritma<br><sub>Skor 0-100 (lebih tinggi = lebih baik)</sub>',
    showlegend=True,
    legend=dict(orientation='v', x=1.1, y=0.5),
    height=700,
    width=1400,
    font=dict(size=12, family='Arial'),
    paper_bgcolor='white'
)

fig3.write_html('img/radar_complexity.html')
fig3.write_image('img/radar_complexity.png', width=1400, height=700, scale=2)
print("   Saved: img/radar_complexity.png")

# ============================================================================
# VISUALIZATION 4: Summary Ranking Table
# ============================================================================

print("\n4. Creating comprehensive ranking table...")

df_rank = df.copy()
df_rank['Time Rank'] = df_rank['Time (minutes)'].rank(method='min').astype(int)
df_rank['Path Rank'] = df_rank['Path Length'].rank(method='min').astype(int)
df_rank['Iteration Rank'] = df_rank['Iterations'].rank(method='min').astype(int)
df_rank['Speed Rank'] = df_rank['Execution Time (ms)'].rank(method='min').astype(int)
df_rank['Overall Score'] = (df_rank['Time Rank'] + df_rank['Speed Rank'] + 
                            df_rank['Iteration Rank'] * 0.5).round(1)
df_rank = df_rank.sort_values('Overall Score')

fig4 = go.Figure(data=[go.Table(
    header=dict(
        values=['<b>Rank</b>', '<b>Algoritma</b>', '<b>Waktu Tempuh</b>', 
                '<b>Pemberhentian</b>', '<b>Iterasi</b>', '<b>Exec Time (ms)</b>',
                '<b>Overall Score</b>'],
        fill_color='#457B9D',
        align='center',
        font=dict(color='white', size=13, family='Arial'),
        height=40
    ),
    cells=dict(
        values=[
            list(range(1, len(df_rank) + 1)),
            df_rank['Algorithm'],
            df_rank['Time (minutes)'].apply(lambda x: f"{x:.1f} min"),
            df_rank['Path Length'],
            df_rank['Iterations'],
            df_rank['Execution Time (ms)'].round(3),
            df_rank['Overall Score']
        ],
        fill_color=[['#D4EDDA' if i < 5 else '#FFF3CD' if i < 7 else '#F8D7DA' 
                    for i in range(len(df_rank))]],
        align=['center', 'left', 'center', 'center', 'center', 'center', 'center'],
        font=dict(color='#1D3557', size=12, family='Arial'),
        height=35
    )
)])

fig4.update_layout(
    title='Ranking Komprehensif Algoritma Routing Ambulans Air<br><sub>Hijau = Excellent | Kuning = Good | Merah = Fair</sub>',
    height=600,
    width=1400,
    margin=dict(l=80, r=80, t=100, b=80),
    font=dict(family='Arial', size=12),
    paper_bgcolor='white'
)

fig4.write_html('img/comprehensive_ranking.html')
fig4.write_image('img/comprehensive_ranking.png', width=1400, height=600, scale=2)
print("   Saved: img/comprehensive_ranking.png")

# ============================================================================
# VISUALIZATION 5: Path Length Distribution
# ============================================================================

print("\n5. Creating path analysis visualization...")

path_analysis = []
for _, row in df.iterrows():
    path_analysis.append({
        'Algorithm': row['Algorithm'],
        'Category': 'Optimal (50 min)' if row['Time (minutes)'] == 50 else 'Suboptimal (55 min)',
        'Stops': row['Path Length'],
        'Time': row['Time (minutes)']
    })

df_path = pd.DataFrame(path_analysis)

fig5 = go.Figure()

for category in df_path['Category'].unique():
    subset = df_path[df_path['Category'] == category]
    color = '#2A9D8F' if 'Optimal' in category else '#E63946'
    
    fig5.add_trace(go.Bar(
        name=category,
        x=subset['Algorithm'],
        y=subset['Stops'],
        marker_color=color,
        text=subset['Time'].apply(lambda x: f"{x:.0f} min"),
        textposition='outside',
        hovertemplate="<b>%{x}</b><br>" +
                     "Pemberhentian: %{y}<br>" +
                     "Waktu: %{text}<br>" +
                     "<extra></extra>"
    ))

fig5.update_layout(
    title='Analisis Kompleksitas Rute: Pemberhentian vs Waktu Tempuh<br><sub>Trade-off antara jumlah hop dan total waktu</sub>',
    xaxis_title='Algoritma',
    yaxis_title='Jumlah Pemberhentian',
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    height=600,
    width=1400,
    font=dict(size=12, family='Arial'),
    legend=dict(x=0.7, y=0.95),
    xaxis=dict(tickangle=-45)
)

fig5.write_html('img/path_complexity.html')
fig5.write_image('img/path_complexity.png', width=1400, height=600, scale=2)
print("   Saved: img/path_complexity.png")

print("\n" + "=" * 80)
print("All enhanced visualizations completed!")
print("=" * 80)
print("\nGenerated files:")
print("  - img/multi_metric_analysis.png")
print("  - img/efficiency_scatter.png")
print("  - img/radar_complexity.png")
print("  - img/comprehensive_ranking.png")
print("  - img/path_complexity.png")
print("\nDokumentasi lengkap tersedia di: ROUTING_DOCUMENTATION.md")
