import heapq
from collections import deque

def is_walkable(x, y, grid):
    return grid[x][y] != 1

def get_neighbors(x, y, grid):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  #/////////// up, down, left, right
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and is_walkable(nx, ny, grid):
            neighbors.append((nx, ny))
    return neighbors

def dfs(maze, start, end):
    stack = [(start, [start])]
    visited = set()

    while stack:
        (r, c), path = stack.pop()
        if (r, c) in visited:
            continue
        visited.add((r, c))

        if (r, c) == end:
            return path, len(visited)

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < len(maze) and 0 <= nc < len(maze[0])
                    and maze[nr][nc] != 0):
                stack.append(((nr, nc), path + [(nr, nc)]))

    return [], len(visited)

def bfs(maze, start, end):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        (r, c), path = queue.popleft()
        if (r, c) in visited:
            continue
        visited.add((r, c))

        if (r, c) == end:
            return path, len(visited)

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < len(maze) and 0 <= nc < len(maze[0])
                    and maze[nr][nc] != 0):
                queue.append(((nr, nc), path + [(nr, nc)]))

    return [], len(visited)


def a_star(maze, start, end):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (heuristic(start, end), 0, start, [start]))
    visited = set()

    while open_set:
        f, g, current, path = heapq.heappop(open_set)

        if current in visited:
            continue
        visited.add(current)

        if current == end:
            return path, len(visited)

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = current[0] + dr, current[1] + dc
            if (0 <= nr < len(maze) and 0 <= nc < len(maze[0])
                    and maze[nr][nc] != 0):
                heapq.heappush(open_set, (
                    g + 1 + heuristic((nr, nc), end),
                    g + 1,
                    (nr, nc),
                    path + [(nr, nc)]
                ))

    return [], len(visited)
