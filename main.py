import pygame
from random import choices
import utils
import time
import numpy as np

# Colors
WHITE = (255, 255, 255)
BACKGROUND = (24, 24, 33)
CELL_ALIVE = (255, 108, 63)
CELL_DEAD = (0, 0, 0)
GRID = (50, 50, 50)
# GRID = (24, 24, 33)

# Parameters
WIDTH, HEIGHT = 1520, 800
CELL_SIZE = 16
GRID_THICKNESS = 1
FPS = 3
RANDOMIZE = True
EDITOR_MODE = False


class GameOfLife:
    def __init__(
        self,
        screen: pygame.Surface,
        w: int,
        h: int,
        cell_size: int,
        fps: int,
        randomize: bool = True,
    ) -> None:
        self.fps = fps
        self.screen = screen
        self.cell_x_cnt, self.cell_y_cnt = round(w / cell_size), round(h / cell_size)
        self.grid = np.array(
            [
                (
                    choices([0, 1], k=self.cell_x_cnt)
                    if randomize
                    else [0] * self.cell_x_cnt
                )
                for _ in range(self.cell_y_cnt)
            ]
        )
        self.is_editor_mode = False
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.frame = 0

    def run(self):
        while self.is_running:
            self.update()
            self.clock.tick(60)

            self.screen.fill(BACKGROUND)
            self.draw_grid()

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif (
                    event.type == pygame.MOUSEMOTION
                    and pygame.mouse.get_pressed()[0]
                    or pygame.mouse.get_pressed()[0]
                ):
                    utils.create_life(self.grid, CELL_SIZE)
                elif pygame.mouse.get_pressed()[2]:
                    self.is_editor_mode = not self.is_editor_mode

    def update(self):
        cur = time.time()
        if self.frame / (cur - self.start_time) > self.fps:
            return

        if cur - self.start_time >= 1:
            pygame.display.set_caption(
                f"Game Of Life. FPS: {(self.frame / (cur-self.start_time)): .2f}"
            )
            self.start_time = time.time()
            self.frame = 0

        self.frame += 1

        if not self.is_editor_mode:
            self.grid = utils.update(self.grid)

    def draw_grid(self):
        utils.fill_grid(self.screen, self.grid, CELL_SIZE, CELL_DEAD, CELL_ALIVE)
        utils.draw_grid(
            self.screen,
            self.cell_x_cnt,
            self.cell_y_cnt,
            GRID,
            CELL_SIZE,
            GRID_THICKNESS,
        )


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Of Life")

    game = GameOfLife(screen, WIDTH, HEIGHT, CELL_SIZE, FPS)
    game.run()

    pygame.quit()
