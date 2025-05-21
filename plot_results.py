import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from datetime import datetime


def filter_by_condition(maze_size, complexity, distance_case):
    def condition(row):
        return (
            row['Maze_Size'] == maze_size and
            row['Complexity'] == complexity and
            row['Distance_Case'].lower() == distance_case.lower()
        )
    return condition

def plot_results(filter_condition=None, dataset_source='csv', current_data=None, chart_type='auto'):
    if dataset_source == 'csv':
        try:
            df = pd.read_csv('experiment_results.csv')
        except FileNotFoundError:
            print("[!] No historical CSV file found. Please run experiments first.")
            return
    elif dataset_source == 'live' and current_data is not None:
        df = pd.DataFrame(current_data, columns=[
            "Algorithm", "Maze_Size", "Complexity", "Distance_Case",
            "Path_Length", "Visited_Nodes", "Time_Seconds"
        ])
    else:
        print("[!] Invalid data source or missing current data.")
        return

    if filter_condition:
        filtered_df = df[df.apply(filter_condition, axis=1)]
        if filtered_df.empty:
            print("[!] No data matched your filter. Showing complete dataset instead.")
            filtered_df = df
    else:
        filtered_df = df

    
    if chart_type == 'auto':
        use_bar = dataset_source == 'csv' and filter_condition is not None
    else:
        use_bar = chart_type == 'bar'


    metrics = [
        ("Time Taken (seconds)", "Time_Seconds"),
        ("Visited Nodes (Space Usage)", "Visited_Nodes"), 
        ("Path Length (Optimality)", "Path_Length")
    ]

    for title, column in metrics:
        plt.figure(figsize=(10, 6))
        
        
        algo_data = {}
        for algo in ['BFS', 'DFS', 'A*']:
            subset = filtered_df[filtered_df['Algorithm'] == algo]
            if subset.empty:
                continue
                
            if use_bar:
                plt.bar(
                    subset['Maze_Size'].astype(str) + f" ({algo})",
                    subset[column],
                    label=algo
                )
            else:
                plt.plot(
                    subset['Maze_Size'],
                    subset[column],
                    marker='o',
                    label=algo
                )
            
            algo_data[algo] = subset[column].values
            
        if column == "Visited_Nodes" and not use_bar and len(algo_data) > 1:
            sizes = filtered_df['Maze_Size'].unique()
            if len(sizes) >= 3:  #//////// You need multiple points for trend analysis
                last_size = max(sizes)
                mid_size = np.median(sizes)
                
            
                bfs_growth = algo_data['BFS'][-1] / algo_data['BFS'][0]
                astar_growth = algo_data['A*'][-1] / algo_data['A*'][0]
                
            
                plt.annotate(f'BFS: O(n²)\n{bfs_growth:.1f}x growth', 
                            xy=(last_size, algo_data['BFS'][-1]),
                            xytext=(last_size*0.7, algo_data['BFS'][-1]*0.8),
                            arrowprops=dict(arrowstyle='->'))
                
                plt.annotate(f'A*: ~O(n)\n{astar_growth:.1f}x growth',
                            xy=(last_size, algo_data['A*'][-1]), 
                            xytext=(last_size*0.7, algo_data['A*'][-1]*1.2),
                            arrowprops=dict(arrowstyle='->'))
        
        plt.xlabel("Maze Size")
        plt.ylabel(title)
        plt.title(f"{title} vs Maze Size")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    generate_interpretation(filtered_df, dataset_source)

def generate_interpretation(df, data_source):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report_lines = [
        f"==============================",
        f"Experiment Summary Report",
        f"Date: {timestamp}",
        f"Data Source: {data_source.upper()}",
        f"==============================\n"
    ]

    metrics = {
        "Time": "Time_Seconds",
        "Space": "Visited_Nodes", 
        "Path": "Path_Length"
    }

    for name, col in metrics.items():
        report_lines.append(f"[{name}] Averages:")
        for algo in ['BFS', 'DFS', 'A*']:
            avg = df[df['Algorithm'] == algo][col].mean()
            if name == "Time":
                report_lines.append(f"- {algo}: {avg:.4f}")
            else:
                report_lines.append(f"- {algo}: {avg:.4f}" if name == "Space" else f"- {algo}: {avg:.4f}")
        report_lines.append("")


    bfs_path = df[df['Algorithm'] == 'BFS']['Path_Length'].mean()
    dfs_path = df[df['Algorithm'] == 'DFS']['Path_Length'].mean()
    astar_path = df[df['Algorithm'] == 'A*']['Path_Length'].mean()

    bfs_time = df[df['Algorithm'] == 'BFS']['Time_Seconds'].mean()
    dfs_time = df[df['Algorithm'] == 'DFS']['Time_Seconds'].mean()
    astar_time = df[df['Algorithm'] == 'A*']['Time_Seconds'].mean()

    bfs_space = df[df['Algorithm'] == 'BFS']['Visited_Nodes'].mean()
    dfs_space = df[df['Algorithm'] == 'DFS']['Visited_Nodes'].mean()
    astar_space = df[df['Algorithm'] == 'A*']['Visited_Nodes'].mean()

    report_lines.append("==============================\n")
    report_lines.append("Interpretation:")

    #///////////////Shortest path
    if bfs_path <= astar_path and bfs_path <= dfs_path:
        report_lines.append("Shortest average path: BFS")
    elif astar_path < bfs_path and astar_path < dfs_path:
        report_lines.append("Shortest average path: A*")
    else:
        report_lines.append("Shortest average path: DFS")

    #//////////////Fastest algorithm
    fastest = min(bfs_time, dfs_time, astar_time)
    if fastest == bfs_time:
        report_lines.append("Fastest algorithm: BFS")
    elif fastest == astar_time:
        report_lines.append("Fastest algorithm: A*")
    else:
        report_lines.append("Fastest algorithm: DFS")

    #////////////// Space-efficient
    lowest_space = min(bfs_space, dfs_space, astar_space)
    if lowest_space == bfs_space:
        report_lines.append("Most space-efficient: BFS")
    elif lowest_space == astar_space:
        report_lines.append("Most space-efficient: A*")
    else:
        report_lines.append("Most space-efficient: DFS")

    report_lines.append("\n Trade-offs observed: consider maze size, available memory, and required path quality.\n")
    report_lines.append("==============================")

    with open('experiment_interpretation.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))

    print("Report generated and saved in experiment_interpretation.txt")


def plot_maze_results(bfs_time, dfs_time, astar_time,
                     bfs_space, dfs_space, astar_space,
                     bfs_path_len, dfs_path_len, astar_path_len,
                     rows, cols, timestamp=None):
    
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(f"Algorithm Comparison ({rows}x{cols} Maze)", fontsize=16)


    config = [
        ("Time (s)", [bfs_time, dfs_time, astar_time], 'skyblue'),
        ("Visited Nodes", [bfs_space, dfs_space, astar_space], 'lightgreen'),
        ("Path Length", [bfs_path_len, dfs_path_len, astar_path_len], 'salmon')
    ]

    for idx, (title, values, color) in enumerate(config):
        bars = axs[idx].bar(['BFS', 'DFS', 'A*'], values, color=color)
        axs[idx].set_title(title)
        axs[idx].grid(True, linestyle='--', alpha=0.6)
        
        for bar in bars:
            height = bar.get_height()
            axs[idx].text(bar.get_x() + bar.get_width()/2., height,
                         f'{height:.2f}', ha='center', va='bottom')

    if bfs_space > astar_space * 1.5:
        axs[1].annotate(f'A* uses {bfs_space/astar_space:.1f}x\nfewer nodes than BFS',
                       xy=(2, astar_space), xytext=(1, astar_space*1.5),
                       arrowprops=dict(facecolor='black', shrink=0.05))

    plt.tight_layout()
    
    #////// saving plot with timestamp handling
    os.makedirs('plots', exist_ok=True)
    if timestamp:
        image_path = f'plots/maze_results_{timestamp}.png'
    else:
        image_path = f"plots/maze_run_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
    
    plt.savefig(image_path)
    plt.show()
    print(f"[✔] Plot saved to {image_path}")
    
    return image_path
