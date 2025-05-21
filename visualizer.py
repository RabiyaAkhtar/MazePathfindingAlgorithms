import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.patheffects as pe
import numpy as np
import os
import time
from maze import Maze
from pathfinding import bfs, dfs, a_star
from PIL import Image
import imageio
from datetime import datetime


class Visualizer:
    def __init__(self, theme='modern'):
        self.theme = theme
        self.image_paths = {
            'modern': {
                'flag': 'flag.png',
                'character': 'dwarf.png'
            },
            'vintage': {
                'castle': 'castle_unlit.PNG',
                'castle_lit': 'castle_lit.png',
                'character': 'explorer.png'
            }
        }

    def visualize_maze(self, grid):
        if self.theme == 'vintage':
            self._visualize_maze_vintage(grid)
        else:
            self._visualize_maze_modern(grid)

    def visualize_path_animated(self, grid, path, algorithm_name, elapsed_time):
        if self.theme == 'vintage':
            self._visualize_path_animated_vintage(grid, path, algorithm_name, elapsed_time)
        else:
            self._visualize_path_animated_modern(grid, path, algorithm_name, elapsed_time)

    def _visualize_maze_modern(self, grid, flag_image_path='flag.png'):
        maze_array = np.array(grid)
        cmap = mcolors.ListedColormap(['white', 'green', 'lime', 'red'])
        bounds = [0, 1, 2, 3, 4]
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(maze_array, cmap=cmap, norm=norm, interpolation='none')
        ax.axis('off')

        start = np.argwhere(maze_array == 2)
        end = np.argwhere(maze_array == 3)

        if start.size > 0:
            ax.text(start[0][1], start[0][0], "Start", fontsize=8, color='black',
                    ha='center', va='center', weight='bold',
                    path_effects=[pe.withStroke(linewidth=1, foreground="white")])

        if end.size > 0:
            ax.text(end[0][1], end[0][0], "End", fontsize=8, color='black',
                    ha='center', va='center', weight='bold',
                    path_effects=[pe.withStroke(linewidth=1, foreground="white")])

        plt.title("Maze: Start & End Marked")
        plt.show()
        plt.close()

    def _visualize_maze_vintage(self, grid, castle_image_path='castle_unlit.PNG'):
        maze_array = np.array(grid)
        cmap = mcolors.ListedColormap(['white', 'black', 'gray', 'dimgray'])
        bounds = [0, 1, 2, 3, 4]
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(maze_array, cmap=cmap, norm=norm, interpolation='none')
        ax.set_xticks(np.arange(-0.5, maze_array.shape[1], 1), minor=True)
        ax.set_yticks(np.arange(-0.5, maze_array.shape[0], 1), minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=0.3)
        ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

        start = np.argwhere(maze_array == 2)
        end = np.argwhere(maze_array == 3)

        if start.size > 0:
            ax.text(start[0][1], start[0][0], "Start", fontsize=8, color='black',
                    ha='center', va='center', weight='bold',
                    path_effects=[pe.withStroke(linewidth=1, foreground="white")])

        if end.size > 0:
            ax.text(end[0][1], end[0][0], "End", fontsize=8, color='black',
                    ha='center', va='center', weight='bold',
                    path_effects=[pe.withStroke(linewidth=1, foreground="white")])

        plt.title("Maze Layout")
        plt.show()
        plt.close()

    def _visualize_path_animated_modern(self, grid, path, algorithm_name, elapsed_time, 
                                        dwarf_image_path='images/dwarf.png', flag_image_path='images/flag.png'):
        maze_array = np.array(grid, dtype=float)
        cmap = mcolors.ListedColormap(['white', 'green', 'lime', 'red', 'blue'])
        bounds = [0, 0.5, 1, 2, 3, 4]
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_title(f"{algorithm_name} Path — Time: {elapsed_time:.6f} sec")
        ax.axis('off')

        img = ax.imshow(maze_array, cmap=cmap, norm=norm, interpolation='none')
        start = path[0]
        end = path[-1]

        #/////////placing flag at end
        if os.path.exists(flag_image_path):
            flag_img = mpimg.imread(flag_image_path)
            flag_icon = OffsetImage(flag_img, zoom=0.015)
            flag_artist = AnnotationBbox(flag_icon, (end[1], end[0]), frameon=False)
            ax.add_artist(flag_artist)

        #////////placing Dwarf at start
        if os.path.exists(dwarf_image_path):
            dwarf_img = mpimg.imread(dwarf_image_path)
            dwarf_icon = OffsetImage(dwarf_img, zoom=0.015)
            dwarf_artist = AnnotationBbox(dwarf_icon, (start[1], start[0]), frameon=False)
            ax.add_artist(dwarf_artist)
        else:
            dwarf_artist = ax.scatter(start[1], start[0], c='cyan', s=80)

        plt.draw()
        plt.pause(0.5)

        for idx, (r, c) in enumerate(path):
            if maze_array[r][c] == 1:
                maze_array[r][c] = 0.5
                img.set_data(maze_array)

            if isinstance(dwarf_artist, AnnotationBbox):
                dwarf_artist.xybox = (c, r)
            else:
                dwarf_artist.set_offsets([c, r])

            plt.draw()
            plt.pause(0.05)

        plt.pause(1)
        plt.show()
        plt.close()


    def _visualize_path_animated_vintage(self, grid, path, algorithm_name, elapsed_time, 
                                         explorer_image_path='images/explorer.png',
                                     castle_unlit_path='images/castle_unlit.PNG',
                                     castle_lit_path='images/castle_lit.png'):
        maze_array = np.array(grid, dtype=float)
        cmap = mcolors.ListedColormap(['white', 'black', 'gray', 'dimgray', 'blue'])
        bounds = [0, 0.5, 1, 2, 3, 4]
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_title(f"{algorithm_name} Path — Time: {elapsed_time:.6f} sec")
        ax.imshow(maze_array, cmap=cmap, norm=norm, interpolation='none')

        ax.set_xticks(np.arange(-0.5, maze_array.shape[1], 1), minor=True)
        ax.set_yticks(np.arange(-0.5, maze_array.shape[0], 1), minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=0.3)
        ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

        start = path[0]
        end = path[-1]

        #//////// placing unlit castle at start
        if os.path.exists(castle_unlit_path):
            start_castle_img = mpimg.imread(castle_unlit_path)
            start_castle_icon = OffsetImage(start_castle_img, zoom=0.09)
            start_castle_artist = AnnotationBbox(start_castle_icon, (start[1], start[0]), frameon=False)
            ax.add_artist(start_castle_artist)

        # //////////placing unlit castle ateEnd
        if os.path.exists(castle_unlit_path):
            end_castle_img = mpimg.imread(castle_unlit_path)
            end_castle_icon = OffsetImage(end_castle_img, zoom=0.09)
            end_castle_artist = AnnotationBbox(end_castle_icon, (end[1], end[0]), frameon=False)
            ax.add_artist(end_castle_artist)

        #/////////placing explorer at start
        if os.path.exists(explorer_image_path):
            explorer_img = mpimg.imread(explorer_image_path)
            explorer_icon = OffsetImage(explorer_img, zoom=0.025)
            explorer_artist = AnnotationBbox(explorer_icon, (start[1], start[0]), frameon=False)
            ax.add_artist(explorer_artist)
        else:
            explorer_artist = ax.scatter(start[1], start[0], c='cyan', s=80)

        plt.draw()
        plt.pause(0.5)

        for idx, (r, c) in enumerate(path):
            if maze_array[r][c] == 1:
                maze_array[r][c] = 0.5
                ax.imshow(maze_array, cmap=cmap, norm=norm, interpolation='none')

            if isinstance(explorer_artist, AnnotationBbox):
                explorer_artist.xybox = (c, r)
            else:
                explorer_artist.set_offsets([c, r])

            plt.draw()
            plt.pause(0.05)

        #////////////after reaching end, replace unlit castle with lit one
        if os.path.exists(castle_lit_path):
            lit_castle_img = mpimg.imread(castle_lit_path)
            lit_castle_icon = OffsetImage(lit_castle_img, zoom=0.07)
            lit_castle_artist = AnnotationBbox(lit_castle_icon, (end[1], end[0]), frameon=False)
            #///////////// Hide unlit castle
            end_castle_artist.set_visible(False)  
            ax.add_artist(lit_castle_artist)
            plt.draw()
            plt.pause(1)

    
        plt.show()
        plt.close()


# ////////////////Generates a 4x4 grid: Original maze + solved versions for BFS/DFS/A.
def visualize_complexity_comparison(style='vintage'):

    complexities = [0.1, 0.3, 0.5, 0.7]
    algorithms = ['BFS', 'DFS', 'A*']

    fig, axs = plt.subplots(4, 4, figsize=(20, 20))
    fig.suptitle("Maze Pathfinding Comparison Across Complexities\nOriginal vs BFS, DFS, A*", 
                fontsize=10, fontweight='bold', y=1.02)

    column_titles = ['Original Maze', 'BFS', 'DFS', 'A*']
    for col, title in enumerate(column_titles):
        axs[0, col].set_title(title, fontsize=13, fontweight='bold')

    if style == 'vintage':
        cmap_original = mcolors.ListedColormap(['white', 'black', 'gray', 'dimgray'])
        cmap_solved = 'viridis'
    else:
        cmap_original = mcolors.ListedColormap(['white', 'green', 'lime', 'red'])
        cmap_solved = 'plasma'

    for row, comp in enumerate(complexities):
        maze_obj = Maze(20, 20, complexity=comp)
        grid, start, end = maze_obj.generate()
        original_grid = np.array(grid)

        axs[row, 0].imshow(original_grid, cmap=cmap_original)
        axs[row, 0].axis('off')
        axs[row, 0].text(-0.05, 0.5, f"Complexity:\n{comp}", ha='right', va='center',
                        transform=axs[row, 0].transAxes,
                        fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='black'))

        for col, algo in enumerate(algorithms, start=1):
            t0 = time.perf_counter()
            if algo == 'BFS':
                path, _ = bfs(grid, start, end)
            elif algo == 'DFS':
                path, _ = dfs(grid, start, end)
            else:
                path, _ = a_star(grid, start, end)
            elapsed = time.perf_counter() - t0

            solved_grid = original_grid.copy()
            for (r, c) in path:
                if solved_grid[r][c] == 1:
                    solved_grid[r][c] = 0.5

            axs[row, col].imshow(solved_grid, cmap=cmap_solved)
            axs[row, col].axis('off')
            axs[row, col].text(-0.05, 0.5,
                             f"Path: {len(path)}nodes\nTime: {elapsed:.4f}s",
                             ha='right', va='center',
                             transform=axs[row, col].transAxes,
                             fontsize=10,
                             bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='black'))

    plt.tight_layout()
    plt.show()
    print("Complexity comparison complete: Mazes with complexities 0.1, 0.3, 0.5, and 0.7 along with their BFS, DFS, and A* pathfinding results (time and nodes visited) are now displayed.")
    