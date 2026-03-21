import numpy as np

def maze_to_colors(maze, path=None, start=None, goals=None, scale=20):
    rows, cols = maze.shape
    img = np.zeros((rows, cols, 3), dtype=np.uint8)

    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == '1':
                img[i, j] = [0, 0, 0]       # pared
            else:
                img[i, j] = [255, 255, 255] # camino

    if path:
        for (i, j) in path:
            img[i, j] = [255, 0, 0]  # rojo

    if start:
        img[start[0], start[1]] = [0, 255, 0]  # verde

    if goals:
        for g in goals:
            img[g[0], g[1]] = [0, 0, 255]  # azul

    img = np.kron(img, np.ones((scale, scale, 1)))

    return img.astype(np.uint8)