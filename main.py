#///// Main.py: for generating and visualizing mazes,solving them with different pathfinding 
# algorithms (BFS, DFS, and A*), and comparing their performance.

import time
from datetime import datetime
from maze import Maze
from visualizer import Visualizer, visualize_complexity_comparison
from pathfinding import bfs, dfs, a_star
from plot_results import plot_maze_results
 

#//////////Generates, solves, and visualizes a single maze using the selected theme.

def run_single_maze(theme='modern'):
    """Run pathfinding on a single maze with visualization"""
    visualizer = Visualizer(theme=theme)

    try:
        rows = int(input("Enter maze rows (e.g., 20): "))
        cols = int(input("Enter maze columns (e.g., 20): "))
        complexity = float(input("Enter maze complexity (0.1 - 0.7 recommended): "))
    except ValueError:
        print("Invalid input! Using default values: 20x20, complexity=0.3")
        rows, cols, complexity = 20, 20, 0.3

    maze_obj = Maze(rows=rows, cols=cols, complexity=complexity)
    grid, start, end = maze_obj.generate()

    print(f"\nMaze Size: {rows}x{cols}, Complexity: {complexity}")
    print(f"Start: {start}, End: {end}")
    print(f"Start walkable? {grid[start[0]][start[1]] in (1, 2, 3)}")
    print(f"End walkable? {grid[end[0]][end[1]] in (1, 2, 3)}")

    visualizer.visualize_maze(grid)
    

    #/////////////Run all algorithms
    start_time = time.perf_counter()
    path_bfs, space_bfs = bfs(grid, start, end)
    elapsed_bfs = time.perf_counter() - start_time

    start_time = time.perf_counter()
    path_dfs, space_dfs = dfs(grid, start, end)
    elapsed_dfs = time.perf_counter() - start_time

    start_time = time.perf_counter()
    path_astar, space_astar = a_star(grid, start, end)
    elapsed_astar = time.perf_counter() - start_time

    #////////////Visualize paths
    if path_bfs:
        visualizer.visualize_path_animated(grid, path_bfs, "BFS", elapsed_bfs)
        
    else:
        print("BFS could not find a path.")

    if path_dfs:
        visualizer.visualize_path_animated(grid, path_dfs, "DFS", elapsed_dfs)
        
    else:
        print("DFS could not find a path.")

    if path_astar:
        visualizer.visualize_path_animated(grid, path_astar, "A*", elapsed_astar)
        
    else:
        print("A* could not find a path.")

    #////////////Generate report
    generate_report(maze_obj, start, end, 
                   elapsed_bfs, elapsed_dfs, elapsed_astar,
                   len(path_bfs), len(path_dfs), len(path_astar),
                   space_bfs, space_dfs, space_astar)



def generate_report(maze_obj, start, end, 
                   elapsed_bfs, elapsed_dfs, elapsed_astar,
                   path_len_bfs, path_len_dfs, path_len_astar,
                   space_bfs, space_dfs, space_astar):
    """Generate performance report"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    summary = f"""
--- Pathfinding Summary Report ---

Date & Time: {now}
Maze Generation Algorithm: Prim's Algorithm
Maze Size: {maze_obj.rows} x {maze_obj.cols}
Complexity: {getattr(maze_obj, 'complexity', 0.3)}
Start Point: {start}
End Point: {end}

Algorithm   | Time (sec) | Path Length | Visited Nodes
------------|------------|-------------|--------------
BFS         | {elapsed_bfs:.6f} | {path_len_bfs}          | {space_bfs}
DFS         | {elapsed_dfs:.6f} | {path_len_dfs}          | {space_dfs}
A*          | {elapsed_astar:.6f} | {path_len_astar}          | {space_astar}

Notes:
- BFS guarantees shortest path but explores many nodes
- DFS is fast but path length varies
- A* balances speed and path quality
"""

    with open("report.txt", "w") as file:
        file.write(summary)
    print("\n[✔] Report saved to 'report.txt'")

    #////////Asking the user if they want to get performance plots
    if input("\nGenerate performance plots? (y/n): ").lower() == 'y':
        image_path = plot_maze_results(
            elapsed_bfs, elapsed_dfs, elapsed_astar,
            space_bfs, space_dfs, space_astar,
            path_len_bfs, path_len_dfs, path_len_astar,
            maze_obj.rows, maze_obj.cols
        )
        with open("report.txt", "a") as file:
            file.write(f"\nPerformance plots saved to: {image_path}")
        print("Performance plots generated. Basic summary and plot path saved to 'report.txt'.")
    else:
        print("No plots were generated. Basic summary has been saved to 'report.txt'.")



# /////////Displays the main menu for maze analysis and handles user selection.
def main():
    print("""
=== Maze Pathfinding Analyzer ===
[1] Analyze single maze
[2] Compare algorithms across complexities
[3] Exit
""")
    
    choice = input("Select option (1-3): ").strip()
    
    if choice == '1':
        # Ask for theme selection
        theme = input("Choose theme (lego/vintage): ").strip().lower()
        if theme not in ['lego', 'vintage']:
            print("Invalid theme, using modern")
            theme = 'lego'
        run_single_maze(theme=theme)
        
    elif choice == '2':
        # Complexity comparison
        theme = input("Choose comparison theme (lego/vintage): ").strip().lower()
        if theme not in ['lego', 'vintage']:
            print("Invalid theme, using vintage")
            theme = 'vintage'
        print(f"\nGenerating complexity comparison ({theme} theme)...")
        visualize_complexity_comparison(style=theme)
        
    elif choice == '3':
        print("Exiting...")
        return
        
    else:
        print("Invalid choice. Running default single maze with modern theme.")
        run_single_maze(theme='modern')

if __name__ == "__main__":
    main()