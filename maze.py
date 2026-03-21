import numpy as np

def load_maze(path):
    with open(path, 'r') as f:
        maze = [list(line.strip()) for line in f.readlines()]
    return np.array(maze)

def find_positions(maze, value):
    positions = []
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == value:
                positions.append((i, j))
    return positions