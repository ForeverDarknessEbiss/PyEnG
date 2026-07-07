from entities.entity import Entity
import math
import pygame

class Monster(Entity):
    """
    Базовый класс монстра.
    Все типы монстров наследуются от него.
    """



    def __init__(
        self,
        x,
        y,
        width=40,
        height=40,
        color=(200, 0, 0),
        speed=60,
        max_hp=100,
        resistances=None
    ):
        super().__init__(x, y, width, height, color)

        self.speed = speed
        self.alive = True

        self.dx = 0
        self.dy = 0

        self.stop_distance = 0

        # лут прессета
        self.loot_preset = None

        # здоровье
        self.max_hp = max_hp
        self.hp = max_hp

        # защита
        if resistances is None:
            resistances = {}

        self.resistances = {
            "physical": resistances.get("physical", 0),
            "chemical": resistances.get("chemical", 0),
            "electric": resistances.get("electric", 0),
        }

    def update(self, player, game_map, delta_time):
        """
        Базовое обновление монстра.
        Здесь можно будет писать общую логику.
        """
        pass

    def take_damage(self, damage):
        self.hp -= damage

        if self.hp <= 0:
            self.alive = False

    def get_rect(self):
        return pygame.Rect(self.x , self.y , self.width, self.height)