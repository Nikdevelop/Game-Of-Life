import pygame
import numba
import numpy as np


def fill_grid(screen: pygame.Surface, grid: np.ndarray, cell_size: tuple, dead_color: tuple, alive_color: tuple):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            pygame.draw.rect(screen, alive_color if grid[y][x] == 1 else dead_color, (x*cell_size, y*cell_size, cell_size, cell_size))


@numba.njit
def calc(grid: np.ndarray, pos: tuple):
    x, y = pos[0], pos[1]

    count = 0
    for i in range(max(0, y-1), min(len(grid), y+2)):
        for j in range(max(0, x-1), min(len(grid[0]), x+2)):
            if i == y and j == x:
                continue
            if grid[i][j] == 1:
                count += 1

    if grid[y][x] == 0 and count == 3:
        return 1

    if grid[y][x] == 1 and count in [2, 3]:
        return 1
    elif grid[y][x] == 1:
        return 0

    return 0


@numba.njit
def update(grid: np.ndarray):
    newgrd = grid.copy()
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            newgrd[y][x] = calc(grid, (x, y))
    return newgrd


def draw_grid(screen: pygame.Surface, x_cnt: int, y_cnt: int, grid_color: tuple, cell_size: int, thickness: int):
    width, height = screen.get_size()
    for c in range(x_cnt):
        pygame.draw.line(screen, grid_color, (c*cell_size, 0),
                        (c*cell_size, height), thickness)

    for c in range(y_cnt):
        pygame.draw.line(screen, grid_color, (0, c*cell_size),
                        (width, c*cell_size), thickness)


def create_life(grid: np.ndarray, cell_size: int):
    cx, cy = pygame.mouse.get_pos()
    grid[cy//cell_size][cx//cell_size] = 1


def is_start_clicked(screen: pygame.Surface, cell_size: int):
    size = screen.get_size()
    cx, cy = pygame.mouse.get_pos()

    if size[0]//cell_size == cx//cell_size+1 and 0 == cy//cell_size:
        return True
    return False