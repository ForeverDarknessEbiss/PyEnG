# camera.py
import pygame
from config import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self, width, height):
        """
        Камера с эффектом резинки (плавно следует за игроком)
        width, height: размер экрана в пикселях
        """
        self.width = width
        self.height = height
        
        # Позиция камеры в мировых координатах (в пикселях)
        self.x = 0
        self.y = 0
        
        # Целевая позиция (куда камера хочет прийти)
        self.target_x = 0
        self.target_y = 0
        
        # Скорость камеры (0.0 - 1.0, чем выше, тем быстрее)
        self.speed = 0.1
        
        # Отступы от края, когда камера начинает двигаться
        self.margin_x = width // 2
        self.margin_y = height // 2
        
    def update(self, player):
        """
        Обновление позиции камеры с эффектом резинки
        player: объект игрока
        """
        # Получаем позицию игрока в пикселях
        player_pixel_x = player.x + player.width // 2
        player_pixel_y = player.y + player.height // 2
        
        # Вычисляем, где должна быть камера, чтобы игрок был в центре
        ideal_x = player_pixel_x - self.width // 2
        ideal_y = player_pixel_y - self.height // 2
        
        # Плавно двигаем камеру к идеальной позиции (резинка)
        self.x += (ideal_x - self.x) * self.speed
        self.y += (ideal_y - self.y) * self.speed
        
        # Сохраняем целевую позицию
        self.target_x = ideal_x
        self.target_y = ideal_y
    
    def world_to_screen(self, world_x, world_y): #тайловая метрика 
        """
        Конвертирует мировые координаты (в тайлах) в экранные (в пикселях)
        """
        screen_x = world_x * TILE_SIZE - self.x
        screen_y = world_y * TILE_SIZE - self.y
        return (screen_x, screen_y)
    
    def screen_to_world(self, screen_x, screen_y):
        """
        Конвертирует экранные координаты в мировые (в тайлах)
        Нужно для определения, по какому тайлу нажали пальцем
        """
        world_x = int((screen_x + self.x) // TILE_SIZE)
        world_y = int((screen_y + self.y) // TILE_SIZE)
        return (world_x, world_y)
    
    def is_visible(self, world_x, world_y):
        """
        Проверяет, виден ли тайл на экране (для ленивого рендера)
        """
        screen_x, screen_y = self.world_to_screen(world_x, world_y)
        
        # Проверяем с запасом в один тайл по краям
        return (-TILE_SIZE <= screen_x <= self.width and 
                -TILE_SIZE <= screen_y <= self.height)
    
    def get_visible_tiles(self, game_map):
        """
        Возвращает список тайлов, которые сейчас видны на экране
        game_map: объект карты
        """
        visible = []
        
        # Определяем диапазон тайлов, которые могут быть видны
        start_x = int(max(0, self.x // TILE_SIZE))
        start_y = int(max(0, self.y // TILE_SIZE))
        end_x = int(min(game_map.width, (self.x + self.width) // TILE_SIZE + 2))
        end_y = int(min(game_map.height, (self.y + self.height) // TILE_SIZE + 2))
        
        # Собираем видимые тайлы
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                visible.append((x, y))
        
        return visible
    
    def shake(self, intensity=5, duration=10):
        """
        Эффект тряски камеры (пригодится для ударов)
        """
        # TODO: реализовать эффект тряски
        pass

    def world_to_screen_pixel(self, pixel_x, pixel_y): #пиксельная метрика 
        """Конвертирует мировые пиксельные координаты в экранные"""
        screen_x = pixel_x - self.x
        screen_y = pixel_y - self.y
        return (screen_x, screen_y)
    
    def screen_to_world_pixel(self, screen_x, screen_y):
        """Конвертирует экранные координаты в мировые пиксельные"""
        world_pixel_x = screen_x + self.x
        world_pixel_y = screen_y + self.y
        return (world_pixel_x, world_pixel_y)