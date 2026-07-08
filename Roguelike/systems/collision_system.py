# systems/collision_system.py

import pygame
import math


class CollisionSystem:
    """
    Система коллизий между игроком, монстрами и картой.
    Исправляет залипание объектов.
    """

    def resolve_player_monsters(self, player, monsters):

        

        for monster in monsters:

            if not monster.alive:
                continue

            player_rect = player.get_rect()
            monster_rect = monster.get_rect()

            if player_rect.colliderect(monster_rect):

                # центр объектов
                player_cx = player.x + player.width / 2
                player_cy = player.y + player.height / 2

                monster_cx = monster.x + monster.width / 2
                monster_cy = monster.y + monster.height / 2

                dx = player_cx - monster_cx
                dy = player_cy - monster_cy

                distance = math.sqrt(dx * dx + dy * dy)

                if distance == 0:
                    distance = 0.1

                # сила раздвигания
                push = 4

                nx = dx / distance
                ny = dy / distance

                # раздвигаем
                player.x += nx * push
                player.y += ny * push

                monster.x -= nx * push
                monster.y -= ny * push

    def resolve_monster_monster(self, monsters):

        for i in range(len(monsters)):
            for j in range(i + 1, len(monsters)):

                m1 = monsters[i]
                m2 = monsters[j]

                if not m1.alive or not m2.alive:
                    continue

                if m1.get_rect().colliderect(m2.get_rect()):

                    dx = (m1.x - m2.x)
                    dy = (m1.y - m2.y)

                    dist = math.hypot(dx, dy)
                    if dist == 0:
                        dist = 0.1

                    push = 2

                    nx = dx / dist
                    ny = dy / dist

                    m1.x += nx * push
                    m1.y += ny * push

                    m2.x -= nx * push
                    m2.y -= ny * push


    def raycast(self, start_x, start_y, end_x, end_y, monsters, walls=None):
        """
        🔫 Проверка линии (выстрела)

        Возвращает:
        {
            "object": объект,
            "point": (x, y)
        }
        """

        line = (start_x, start_y, end_x, end_y)

        closest_hit = None
        closest_dist = float("inf")

        # 👾 проверка монстров
        for monster in monsters:

            if not monster.alive:
                continue

            rect = monster.get_rect()

            if rect.clipline(line):
                mx, my = rect.center

                dx = mx - start_x
                dy = my - start_y
                dist = dx * dx + dy * dy

                if dist < closest_dist:
                    closest_dist = dist
                    closest_hit = {
                        "object": monster,
                        "point": (mx, my)
                    }

        # 🧱 проверка стен (если есть)
        if walls:
            for wall in walls:
                if wall.clipline(line):
                    wx, wy = wall.center

                    dx = wx - start_x
                    dy = wy - start_y
                    dist = dx * dx + dy * dy

                    if dist < closest_dist:
                        closest_dist = dist
                        closest_hit = {
                            "object": wall,
                            "point": (wx, wy)
                        }

        return closest_hit