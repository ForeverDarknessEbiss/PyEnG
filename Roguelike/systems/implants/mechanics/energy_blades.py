# systems/implants/mechanics/energy_blades.py
import math
import pygame
from ..base import BaseMechanic
from systems.damage_text_system import DamageTextSystem 

class Mechanic(BaseMechanic):
    def __init__(self, player, config=None):
        super().__init__(player, config)
        self.dash_damage = config.get("dash_damage", 25)
        self.dash_distance = config.get("dash_distance", 120)
        self.bleed_damage = config.get("bleed_damage", 5)
        self.bleed_duration = config.get("bleed_duration", 3.0)
    
    def _on_use(self, attack_vector=None, damage_text_system=None):
        """Рывок с уроном (вызывается из try_attack)"""
        if attack_vector is None:
            # fallback: последнее направление движения
            dx = self.player.last_dx if self.player.last_dx != 0 else 1
            dy = self.player.last_dy if self.player.last_dy != 0 else 0
        else:
            dx, dy = attack_vector
        
        # Нормализация
        length = math.hypot(dx, dy)
        if length > 0:
            dx /= length
            dy /= length
        else:
            dx, dy = 1, 0
        
        # Центр игрока
        start_x = self.player.x + self.player.width // 2
        start_y = self.player.y + self.player.height // 2
        # Точка конца рывка
        end_x = start_x + dx * self.dash_distance
        end_y = start_y + dy * self.dash_distance
        
        # Перемещаем игрока
        self.player.x = end_x - self.player.width // 2
        self.player.y = end_y - self.player.height // 2
        # Наносим урон врагам на линии
        self._damage_enemies_in_line(start_x, start_y, end_x, end_y, damage_text_system)

    def _damage_enemies_in_line(self, start_x, start_y, end_x, end_y, damage_text_system=None):
        """Наносит урон всем врагам на линии рывка"""
        
        for monster in self.player.monster_manager.all_monsters:
            if not monster.alive:
                continue

            # Центр монстра
            monster_x = monster.x + monster.width // 2
            monster_y = monster.y + monster.height // 2
            
            # Проверяем попадание в линию
            if self._point_to_line_distance(monster_x, monster_y, start_x, start_y, end_x, end_y) < 30:
                monster.take_damage(self.dash_damage)
                
                # 🆕 Текст урона
                if damage_text_system:
                    damage_text_system.add(monster_x, monster_y, self.dash_damage)

                if hasattr(monster, 'apply_bleed'):
                    monster.apply_bleed(self.bleed_damage, self.bleed_duration)

    def _point_to_line_distance(self, px, py, x1, y1, x2, y2):
        """Расстояние от точки до отрезка"""
        line_len = math.hypot(x2 - x1, y2 - y1)
        if line_len == 0:
            return math.hypot(px - x1, py - y1)
        
        # Проекция точки на линию
        t = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / (line_len ** 2)
        t = max(0, min(1, t))
        
        # Ближайшая точка на отрезке
        proj_x = x1 + t * (x2 - x1)
        proj_y = y1 + t * (y2 - y1)
        
        return math.hypot(px - proj_x, py - proj_y)