import pygame
from config import TILE_SIZE


class GameMap:
    def __init__(self):

        self.width = 500
        self.height = 500

        # простая карта (0 = пол)
        self.tiles = [
            [0 for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def is_walkable(self, x, y):

        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x] == 0

        return False

    def draw(self, screen, camera):

        # получаем только видимые тайлы
        visible_tiles = camera.get_visible_tiles(self)

        for (x, y) in visible_tiles:

            screen_x, screen_y = camera.world_to_screen(x, y)

            rect = pygame.Rect(
                screen_x,
                screen_y,
                TILE_SIZE,
                TILE_SIZE
            )

            pygame.draw.rect(screen, (80, 80, 80), rect, 1)
