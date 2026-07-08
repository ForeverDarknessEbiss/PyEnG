# systems/implants/mechanics/radar.py
import pygame
from ..base import BaseMechanic

class Mechanic(BaseMechanic):
    def __init__(self, player, config=None):
        super().__init__(player, config)
        # Настройки миникарты
        self.minimap_size = config.get("minimap_size", 200)      # размер окна в пикселях
        self.minimap_x = config.get("minimap_x",  1330)  # позиция X (справа)
        self.minimap_y = config.get("minimap_y",  650) # позиция Y (снизу)
        self.radar_radius = config.get("radar_radius", 1300)      # радиус обзора в мировых единицах
        self.tile_size = config.get("tile_size", 40)             # размер тайла в пикселях
        self.scale = self.minimap_size / (self.radar_radius * 2 / self.tile_size)  # масштаб
        
        # Цвета
        self.wall_color = (50, 50, 50)
        self.floor_color = (30, 30, 30)
        self.player_color = (0, 255, 0)
        self.enemy_color = (255, 0, 0)
        self.loot_color = (255, 255, 0)
        
        self.font = pygame.font.Font(None, 14)
    
    def draw(self, screen, camera):
        """Отрисовка миникарты"""
        if not self.enabled or not self.active:
            return

        game_map = self.player.game_map
        monster_manager = self.player.monster_manager
        loot_system = self.player.loot_system

        if not game_map or not monster_manager or not loot_system:
            return

        # Создаём surface для миникарты
        minimap_surface = pygame.Surface((self.minimap_size, self.minimap_size))
        minimap_surface.fill((0, 0, 0))
        
        # Координаты игрока
        px = self.player.x
        py = self.player.y
        
        # Границы области видимости
        left = px - self.radar_radius
        right = px + self.radar_radius
        top = py - self.radar_radius
        bottom = py + self.radar_radius
        
        # Шаг отрисовки (масштаб)
        step = self.radar_radius * 2 / self.minimap_size
        
        # Рисуем карту (тайлы)
        for world_x in range(int(left), int(right), self.tile_size):
            for world_y in range(int(top), int(bottom), self.tile_size):
                grid_x = int(world_x // self.tile_size)
                grid_y = int(world_y // self.tile_size)
                
                # Проверяем, есть ли стена
                if not game_map.is_walkable(grid_x, grid_y):
                    # Координаты на миникарте
                    map_x = (world_x - left) / (right - left) * self.minimap_size
                    map_y = (world_y - top) / (bottom - top) * self.minimap_size
                    
                    if 0 <= map_x < self.minimap_size and 0 <= map_y < self.minimap_size:
                        pygame.draw.rect(minimap_surface, self.wall_color, 
                                        (map_x, map_y, step, step))
        
        # Рисуем врагов
        for monster in monster_manager.all_monsters:
            if not monster.alive:
                continue
            
            mx, my = monster.x, monster.y
            if left <= mx <= right and top <= my <= bottom:
                map_x = (mx - left) / (right - left) * self.minimap_size
                map_y = (my - top) / (bottom - top) * self.minimap_size
                pygame.draw.rect(minimap_surface, self.enemy_color,
                                (map_x - 2, map_y - 2, 4, 4))
        
        # Рисуем лут
        for item in loot_system.items:
            ix, iy = item.x, item.y
            if left <= ix <= right and top <= iy <= bottom:
                map_x = (ix - left) / (right - left) * self.minimap_size
                map_y = (iy - top) / (bottom - top) * self.minimap_size
                pygame.draw.rect(minimap_surface, self.loot_color,
                                (map_x - 1, map_y - 1, 2, 2))
        
        # Рисуем игрока (в центре)
        center_x = self.minimap_size // 2
        center_y = self.minimap_size // 2
        pygame.draw.rect(minimap_surface, self.player_color,
                        (center_x - 3, center_y - 3, 6, 6))
        
        # Рамка миникарты
        pygame.draw.rect(screen, (100, 100, 100), 
                        (self.minimap_x, self.minimap_y, self.minimap_size, self.minimap_size), 2)
        
        # Накладываем на экран
        screen.blit(minimap_surface, (self.minimap_x, self.minimap_y))
        
        # Текст масштаба
        scale_text = self.font.render(f"Радиус: {self.radar_radius}", True, (200, 200, 200))
        screen.blit(scale_text, (self.minimap_x + 5, self.minimap_y + self.minimap_size + 2))
    
    def set_radar_radius(self, radius):
        """Изменение радиуса обзора (для настройки)"""
        self.radar_radius = max(100, min(1000, radius))
        self.scale = self.minimap_size / (self.radar_radius * 2 / self.tile_size)