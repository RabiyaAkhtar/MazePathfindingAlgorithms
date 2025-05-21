import csv
import time
from maze import Maze
from pathfinding import bfs, dfs, a_star
from plot_results import plot_results, filter_by_condition
import matplotlib.pyplot as plt

results = []

sizes = [10, 20, 30, 40, 50]
complexities = [0.1, 0.3, 0.5, 0.7]
distance_cases = ["short", "medium", "long"]

#///////////////////// Running Experiments
for size in sizes:
    for complexity in complexities:
        for distance_case in distance_cases:
            maze_obj = Maze(size, size, complexity=complexity)
            grid, _, _ = maze_obj.generate()

            start = (1, 1)
            end = (size - 1, size - 1)

            if distance_case == "short":
                end = (2, 2)
            elif distance_case == "medium":
                end = (size // 2, size // 2)
            elif distance_case == "long":
                end = (size - 1, size - 1)

            grid[start[0]][start[1]] = 2
            grid[end[0]][end[1]] = 3

            print(f"\nTesting Size: {size}x{size}, Complexity: {complexity}, Start: {start}, End: {end}")

            start_t = time.perf_counter()
            path_bfs, visited_bfs = bfs(grid, start, end)
            elapsed_bfs = time.perf_counter() - start_t

            start_t = time.perf_counter()
            path_dfs, visited_dfs = dfs(grid, start, end)
            elapsed_dfs = time.perf_counter() - start_t

            start_t = time.perf_counter()
            path_astar, visited_astar = a_star(grid, start, end)
            elapsed_astar = time.perf_counter() - start_t

            results.append(["BFS", size, complexity, distance_case, len(path_bfs), visited_bfs, elapsed_bfs])
            results.append(["DFS", size, complexity, distance_case, len(path_dfs), visited_dfs, elapsed_dfs])
            results.append(["A*", size, complexity, distance_case, len(path_astar), visited_astar, elapsed_astar])


save_csv = input("\nWould you like to save the experiment results to a CSV file? (y/n): ")
if save_csv.lower() == 'y':
    with open('experiment_results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Algorithm", "Maze_Size", "Complexity", "Distance_Case", "Path_Length", "Visited_Nodes", "Time_Seconds"])
        writer.writerows(results)
    print("\n[OK] Results saved to 'experiment_results.csv'")
else:
    print("\n[INFO] Results were not saved to CSV.")

plt.show(block=False)


def handle_historical_data():
    current_data = None
    dataset_source = 'csv'
    user_choice = input("\nWould you like to filter the results and visualize a specific test case? (y/n): ").strip().lower()
    
    if user_choice == 'y':
        while True:
            try:
                maze_size = int(input("Enter Maze Size (10, 20, 30, 40, 50): "))
                if maze_size in sizes:
                    break
                else:
                    print("[!] Invalid input. Please enter a valid Maze Size from the list.")
            except ValueError:
                print("[!] Invalid input. Please enter a number.")

        while True:
            try:
                complexity = float(input("Enter Complexity (0.1, 0.3, 0.5, 0.7): "))
                if complexity in complexities:
                    break
                else:
                    print("[!] Invalid input. Please enter a valid Complexity from the list.")
            except ValueError:
                print("[!] Invalid input. Please enter a float value like 0.3.")

        while True:
            distance_case = input("Enter Distance Case (short/medium/long): ").strip().lower()
            if distance_case in distance_cases:
                break
            else:
                print("[!] Invalid input. Please enter 'short', 'medium', or 'long'.")

        filter_condition = filter_by_condition(maze_size, complexity, distance_case)
        plot_results(filter_condition=filter_condition, dataset_source=dataset_source, current_data=current_data, chart_type='bar')
    else:
        plot_results(dataset_source=dataset_source, current_data=current_data)

print("\n[1] Plot historical saved data (CSV)")
print("[2] Plot current experiment session data")
data_source_choice = input("Choose option [1/2]: ").strip()

if data_source_choice == '1':
    handle_historical_data()

elif data_source_choice == '2':
    plot_results(dataset_source='live', current_data=results)

else:
    print("[!] Invalid choice, defaulting to historical CSV.")
    handle_historical_data()
