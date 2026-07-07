# chest.py (полная версия с учетом правок)
import pygame
from ..base import BaseInteractiveObject

OBJECT_TYPE = "chest"

class ObjectClass(BaseInteractiveObject):
    def __init__(self, uid, x, y, config):
        super().__init__(uid, x, y, config)
        self.is_open = False
        self.inventory = config.get("inventory", [])
        
        # Кэшируем игрока, который взаимодействовал
        self._interacting_player = None 
        
        # Максимальная дистанция, на которой сундук закроется сам
        self.interaction_range = config.get("interaction_range", 80)

    def _on_toggle(self, player):
        """Переключение состояния сундука"""
        if not self.is_open:
            self.is_open = True
            self._interacting_player = player # Запоминаем, кто открыл
            print(f"[CHEST] Открыт сундук {self.uid}")
            # TODO: Открыть UI инвентаря
            player.open_container(self)
        else:
            self._close()
        return True

    def _close(self):
        """Закрыть сундук и очистить UI"""
        if self.is_open:
            self.is_open = False
            print(f"[CHEST] Закрыт сундук {self.uid}")
            if self._interacting_player:
                self._interacting_player.close_container()  # <-- ЗАКРЫВАЕМ UI
            # TODO: Закрыть UI инвентаря, если он был открыт именно этим сундуком
            self._interacting_player = None

    def update(self, delta_time):
        """
        Вызывается каждый кадр. 
        Проверяет, не ушел ли игрок слишком далеко.
        """
        super().update(delta_time)
        
        if self.is_open and self._interacting_player:
            # Если игрок отошел дальше радиуса действия — закрываемся
            if not self.is_nearby(self._interacting_player, self.interaction_range):
                self._close()

    def _on_destroy(self):
        """Смерть сундука"""
        # Сначала закрываем (чтобы UI пропал)
        self._close()
        
        # Выбрасываем содержимое на пол
        for item in self.inventory:
            # TODO: Спавн предметов на землю через LootSystem
            pass
        self.inventory = []
        
        print(f"[CHEST] Сундук {self.uid} уничтожен")

    def draw(self, screen, camera):
        if self.is_destroyed:
            return  # сломанные не рисуем
        
        screen_x, screen_y = camera.world_to_screen_pixel(self.x, self.y)
        
        # Цвета только для сундука
        if self.is_open:
            color = (101, 67, 33)   # открыт
        else:
            color = (139, 69, 19)   # закрыт
        
        w = self.config.get("width", 48)
        h = self.config.get("height", 48)
        
        rect = pygame.Rect(screen_x, screen_y, w, h)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)  # рамка
        
        # Дебаг-текст
        if not hasattr(self, '_font'):
            self._font = pygame.font.Font(None, 16)
        
        if not self.is_open:
            text = self._font.render("F", True, (255, 255, 255))
            screen.blit(text, (screen_x + w//2 - 8, screen_y - 20))