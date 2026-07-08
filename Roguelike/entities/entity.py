import pygame

class Entity:
    def __init__(self, x, y, width, height, color):
        """
        Базовый класс сущности.
        :param x: координата X
        :param y: координата Y
        :param width: ширина сущности
        :param height: высота сущности
        :param color: цвет сущности (кортеж RGB)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def update(self):
        """
        Базовый метод обновления сущности.
        Может быть переопределен в подклассах.
        """
        pass

    def draw(self, screen, camera):

        screen_x = self.x - camera.x
        screen_y = self.y - camera.y

        rect = pygame.Rect(
            screen_x,
            screen_y,
            self.width,
            self.height
        )

        pygame.draw.rect(screen, self.color, rect)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
