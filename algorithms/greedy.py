from heapq import heappush, heappop
from utils import MOVES
from heuristics import manhattan, euclidean

def greedy(maze, start, goals, heuristic="manhattan"):
    
    # Selección de heurística
    if heuristic == "manhattan":
        h_func = manhattan
    else:
        h_func = euclidean

    open_list = []
    heappush(open_list, (0, start, [start]))  # (h, nodo, path)

    visited = set()
    nodes_explored = 0

    while open_list:
        h, current, path = heappop(open_list)
        nodes_explored += 1

        if current in goals:
            return path, nodes_explored

        if current in visited:
            continue

        visited.add(current)

        for move in MOVES:
            nx = current[0] + move[0]
            ny = current[1] + move[1]
            neighbor = (nx, ny)

            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]):
                if maze[nx][ny] != '1' and neighbor not in visited:

                    # Solo usa heurística (NO usa g(n))
                    h = min(h_func(neighbor, goal) for goal in goals)

                    heappush(open_list, (h, neighbor, path + [neighbor]))

    return None, nodes_explored