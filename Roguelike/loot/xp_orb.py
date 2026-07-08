import pygame
import random
import math


class XPOrb:

    def __init__(self, x, y, value=1):

        self.x = x
        self.y = y

        self.value = value

        self.radius = 6

        # --- СЛУЧАЙНАЯ СКОРОСТЬ РАЗЛЁТА ---
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(80, 160)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)