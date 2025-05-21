import random
import matplotlib.pyplot as plt
import numpy as np

class Maze:

    def __init__(self, rows, cols, complexity=0.3):
        self.rows = rows
        self.cols = cols
        #/////////////Wall density (0.0 - 1.0)
        self.complexity = complexity 
        #///////////// Initializing grid: 0 = wall, 1 = path
        self.grid = [[0] * cols for _ in range(rows)]  
        self.start = None
        self.end = None

    def generate(self):
        #////////////Creating a valid base maze
        self._carve_path(1, 1)

        #//////////Adding extra paths based on complexity
        extra_path_attempts = int(self.complexity * self.rows * self.cols)
        for _ in range(extra_path_attempts):
            r = random.randint(1, self.rows - 2)
            c = random.randint(1, self.cols - 2)
            if self.grid[r][c] == 0:  
                self.grid[r][c] = 1

        #//////////Adding braiding (optional loops)
        #///////// Break 5% of walls
        braid_attempts = int(0.05 * self.rows * self.cols)  
        for _ in range(braid_attempts):
            r, c = random.randint(1, self.rows - 2), random.randint(1, self.cols - 2)
            #//////Only break walls
            if self.grid[r][c] == 0:  
                self.grid[r][c] = 1

        self.add_start_end_points() 
        return self.grid, self.start, self.end
    

    def _carve_path(self, r, c):
        self.grid[r][c] = 1  
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions) 

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 1 <= nr < self.rows - 1 and 1 <= nc < self.cols - 1 and self.grid[nr][nc] == 0:
                self.grid[r + dr // 2][c + dc // 2] = 1
                #/////////recursively carve the path
                self._carve_path(nr, nc)

    def add_start_end_points(self):
        self.start = (random.randint(1, self.rows - 2), random.randint(1, self.cols - 2))
        self.grid[self.start[0]][self.start[1]] = 2 

        #////// adding random end point
        self.end = (random.randint(1, self.rows - 2), random.randint(1, self.cols - 2))
        #//////////// ensuring start and end are not the same
        while self.end == self.start:  
            self.end = (random.randint(1, self.rows - 2), random.randint(1, self.cols - 2))
        self.grid[self.end[0]][self.end[1]] = 3 
