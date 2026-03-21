from heapq import heappush, heappop
from utils import MOVES
from heuristics import manhattan, euclidean

def astar(maze, start, goals, heuristic="manhattan"):
    
    # Selección de heurística
    if heuristic == "manhattan":
        h_func = manhattan
    else:
        h_func = euclidean

    open_list = []
    heappush(open_list, (0, start, [start]))  # (f, nodo, path)

    visited = set()
    nodes_explored = 0
    g_cost = {start: 0}

    while open_list:
        f, current, path = heappop(open_list)
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
                if maze[nx][ny] != '1':

                    tentative_g = g_cost[current] + 1

                    if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                        g_cost[neighbor] = tentative_g

                        h = min(h_func(neighbor, goal) for goal in goals)

                        f = tentative_g + h

                        heappush(open_list, (f, neighbor, path + [neighbor]))

    return None, nodes_explored