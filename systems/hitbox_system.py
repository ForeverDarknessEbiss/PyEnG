# systems/hitbox_system.py

import pygame
import math


class Hitbox:
    """
    Универсальный хитбокс.

    Может использоваться для:
    - удара мечом
    - лучей
    - подбора XP
    - подбора лута
    """

    def __init__(
        self,
        x,
        y,
        width,
        height,
        owner,
        damage= None,
        lifetime=0.1,
        hit_type="attack", 
    ):

        # геометрия
        self.rect = pygame.Rect(x, y, width, height)

        # владелец
        self.owner = owner

        # урон
        self.damage = damage or {}

        # тип хитбокса
        self.hit_type = hit_type

        # время жизни
        self.lifetime = lifetime

        # скорость (используется для орбов)
        self.vx = 0
        self.vy = 0

        # цель магнита
        self.magnet_target = None

        # предотвращает многократные попадания
        self.hit_once = True
        self.already_hit = set()

        self.debug_line = None

class HitboxSystem:

    def __init__(self, damage_system, damage_text_system):

        self.damage_system = damage_system
        self.damage_text_system = damage_text_system
        self.hitboxes = []
        self.debug_line = None  # (start, end) в мировых координатах


    def create_hitbox(
        self,
        x,
        y,
        width,
        height,
        owner,
        damage= None,
        lifetime=0.1,
        hit_type="attack",
    ):

        hitbox = Hitbox(
            x,
            y,
            width,
            height,
            owner,
            damage,
            lifetime,
            hit_type,
        )

        self.hitboxes.append(hitbox)

        return hitbox

    def update(self, delta_time, player=None):

        for hitbox in self.hitboxes[:]:

            # уменьшаем время жизни
            hitbox.lifetime -= delta_time

            if hitbox.lifetime <= 0:
                self.hitboxes.remove(hitbox)
                continue

            # движение (используется орбами)
            hitbox.rect.x += hitbox.vx * delta_time
            hitbox.rect.y += hitbox.vy * delta_time

            # магнит
            if hitbox.hit_type == "xp_orb" and player:

                px, py = player.get_pixel_position()

                dx = px - hitbox.rect.centerx
                dy = py - hitbox.rect.centery

                dist = math.hypot(dx, dy)

                magnet_range = 120

                if dist < magnet_range and dist > 0:

                    speed = 250

                    hitbox.vx = dx / dist * speed
                    hitbox.vy = dy / dist * speed

    def check_hits(self, targets):

        for hitbox in self.hitboxes:

            for target in targets:

                if target == hitbox.owner:
                    continue

                if target in hitbox.already_hit:
                    continue

                if hitbox.rect.colliderect(target.get_rect()):

                    if hasattr(target, "hp"):

                        if isinstance(hitbox.damage, (int, float)):
                            attack_data = {"physical": hitbox.damage}
                        else:
                            attack_data = hitbox.damage

                        damage = self.damage_system.calculate_damage(
                            attack_data,
                            target.resistances
                        )

                        cx = target.x + target.width // 2
                        cy = target.y

                        self.damage_text_system.add(cx, cy, damage)

                        target.take_damage(damage)

                    hitbox.already_hit.add(target)



    def ray_attack(self, player, target, damage):

        if not target:
            return

        self.damage_system.apply_damage(target, damage)

    def draw(self, screen, camera): # ВИЗУАЛИЗАЦИЯ ХИТБОКСА УДАЛИТЬ ПОТОМ 

        for hitbox in self.hitboxes:

            # перевод в экранные координаты (ВАЖНО)
            rect = hitbox.rect.copy()
            rect.x -= camera.x
            rect.y -= camera.y

            pygame.draw.rect(screen, (200, 200, 200), rect, 2)
    
        # отладочная линия
        if self.debug_line:
            start, end = self.debug_line
            start_screen = camera.world_to_screen_pixel(start[0], start[1])
            end_screen = camera.world_to_screen_pixel(end[0], end[1])
            pygame.draw.line(screen, (255, 255, 0), start_screen, end_screen, 2)
            self.debug_line = None  # рисуем один раз

    def set_debug_line(self, start, end):
            """Устанавливает линию для отладки (например, при выстреле)"""
            self.debug_line = (start, end)

    def create_dash_hitbox(self, points, owner, damage, lifetime=0.1, bleed_damage=0, bleed_duration=0):
        """Создаёт хитбокс для рывка (полигон)"""
        hitbox = {
            "points": points,
            "owner": owner,
            "damage": damage,
            "lifetime": lifetime,
            "bleed_damage": bleed_damage,
            "bleed_duration": bleed_duration,
            "type": "dash"
        }
        self.hitboxes.append(hitbox)