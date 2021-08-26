"""
The aim of this is to be able to take a np array, start and end coords, then output a series of coordinates/instructions
Might wanna toggle expansion of map off
"""

import mapping
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
#import queue
#import tcod
# from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

def showonce(current):
    """
    Takes a 2D np array as input and plots it
    """
    fig, ax = plt.subplots(1, 1)
    cmap = colors.ListedColormap(["black", "white"])
    plt.imshow(current, cmap=cmap)
    plt.show() 

def pfind(current, start, end):
    """
    current = np array with 0 indicating obstacle and > 0 indicating cost
    start/end = start and end coordinates in the form [row, col] as norm in numpy
    """
    grid = Grid(matrix=current)

    start = grid.node(*start[::-1])
    end = grid.node(*end[::-1])

    finder = AStarFinder()
    path, runs = finder.find_path(start, end, grid)

    print('operations:', runs, 'path length:', len(path))
    print(grid.grid_str(path=path, start=start, end=end))
    swappedpath = []
    for coord in path:
        swappedpath.append(coord[::-1])
    print(swappedpath)
    return swappedpath

def thicc(test, size):
    dup_test = test.copy()
    coords = np.asarray(np.where(dup_test == 0)).T
    print(coords)

    for coord in coords:
        row, col = coord
        for r in range(row-size, row+size+1):
            for c in range(col-size, col+size+1):
                try:
                    dup_test[r, c] = 0
                except:
                    pass
    return dup_test

if __name__ == "__main__":
    current = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0],
        [0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    current = np.array(current) # Convert to a NumPy array
    showonce(current)
    pfind(current, [1, 1], [5, 18])