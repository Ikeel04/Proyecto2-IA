from collections import deque
from utils import MOVES  

def bfs(maze, start, goals):
    queue = deque([(start, [start])])
    visited = set()
    nodes_explored = 0
    explored_order = []

    while queue:
        current, path = queue.popleft()
        nodes_explored += 1
        explored_order.append(current)

        if current in goals:
            return path, nodes_explored, explored_order

        if current in visited:
            continue

        visited.add(current)

        for move in MOVES:
            nx = current[0] + move[0]
            ny = current[1] + move[1]

            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]):
                if maze[nx][ny] != '1' and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(nx, ny)]))

    return None, path