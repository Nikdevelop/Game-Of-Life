import pygame
from random import choices
import utils
import time
import numpy as np
import keyboard

# Colors
WHITE = (255, 255, 255)
BACKGROUND = (24, 24, 33)
CELL_ALIVE = (255, 108, 63)
CELL_DEAD = (0, 0, 0)
# GRID = (50, 50, 50)
GRID = (24, 24, 33)

# Parameters
WIDTH, HEIGHT = 1500, 1000
CELL_SIZE = 8
GRID_THICKNESS = 2
FPS = 10
RANDOMIZE = True
EDITOR_MODE = True

cell_x_cnt, cell_y_cnt = round(WIDTH / CELL_SIZE), round(HEIGHT / CELL_SIZE)
grid = np.array([choices([0, 1], k=cell_x_cnt) if RANDOMIZE else [
                0] * cell_x_cnt for _ in range(cell_y_cnt)])

_editor_mode = [EDITOR_MODE]
keyboard.add_hotkey('space', utils.change_edit_mode, (_editor_mode, ))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Game Of Life")
clock = pygame.time.Clock()

running = True
start = time.time()
frame = 0
while running:
    cur = time.time()
    if cur-start >= 1:
        pygame.display.set_caption(
            f"Game Of Life. FPS: {(frame / (cur-start)): .2f}")
        start = time.time()
        frame = 0

    frame += 1
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[0]:
            utils.create_life(grid, CELL_SIZE)

    screen.fill(BACKGROUND)
    utils.fill_grid(screen, grid, CELL_SIZE, CELL_DEAD, CELL_ALIVE)
    utils.draw_grid(screen, cell_x_cnt, cell_y_cnt,
                    GRID, CELL_SIZE, GRID_THICKNESS)
    
    if not _editor_mode[0]:
        grid = utils.update(grid)

    pygame.display.update()

pygame.quit()
