

import math


class AISystem:
    """
    Система искусственного интеллекта.
    Решает куда должны двигаться монстры.
    """

    def update(self, monsters, player):

        

        for monster in monsters:

            if not monster.alive:
                continue

            # направление к игроку
            dx = player.x - monster.x
            dy = player.y - monster.y

            distance = math.sqrt(dx * dx + dy * dy)
            # проверка дальности агрессии
            if distance > monster.vision_range:
                monster.dx = 0
                monster.dy = 0 
            # проверка дальности атаки где монстр подходит на свою дальность атаки 
            elif distance > monster.stop_distance:
                monster.dx = dx / distance
                monster.dy = dy / distance
            else:
                monster.dx = 0
                monster.dy = 0
