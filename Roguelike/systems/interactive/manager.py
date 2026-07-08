import importlib
import os
import pygame

class InteractiveManager:
    def __init__(self):
        self.objects = []           # все объекты на карте
        self.object_classes = {}    # {type_key: class}
        self._load_all_objects()
    
    def _load_all_objects(self):
        folder_path = "systems/interactive/objects"
        for file in os.listdir(folder_path):
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]
                module = importlib.import_module(f"systems.interactive.objects.{module_name}")
                if hasattr(module, "OBJECT_TYPE"):
                    self.object_classes[module.OBJECT_TYPE] = module.ObjectClass
    
    def spawn(self, object_type, uid, x, y, config=None):
        if object_type not in self.object_classes:
            print(f"[InteractiveManager] Неизвестный тип: {object_type}")
            return None
        obj = self.object_classes[object_type](uid, x, y, config or {})
        self.objects.append(obj)
        return obj
    
    def get_object_at(self, x, y):
        for obj in self.objects:
            # проверка попадания (в пикселях)
            obj_rect = pygame.Rect(obj.x, obj.y, 40, 40)
            if obj_rect.collidepoint(x, y):
                return obj
        return None
    
    def interact(self, obj, player):
        if not obj.is_destroyed:
            obj.on_interact(player)
    
    def update(self, delta_time):
        for obj in self.objects:
            obj.update(delta_time)
    
    def draw(self, screen, camera):
        for obj in self.objects:
            obj.draw(screen, camera)

    def try_interact_nearest(self, player, max_distance=60):
        """
        Ищет ближайший объект в радиусе и взаимодействует с ним.
        Возвращает True если взаимодействие произошло.
        """
        # Собираем все доступные объекты в радиусе
        nearby = []
        for obj in self.objects:
            if obj.is_destroyed:
                continue
            if obj.is_nearby(player, max_distance):
                nearby.append(obj)
        
        if not nearby:
            print("[InteractiveManager] Нет объектов рядом")
            return False
        
        # Находим ближайший
        player_cx = player.x + player.width // 2
        player_cy = player.y + player.height // 2
        
        def distance_to(obj):
            obj_cx = obj.x + obj.config.get("width", 40) // 2
            obj_cy = obj.y + obj.config.get("height", 40) // 2
            return ((obj_cx - player_cx) ** 2 + (obj_cy - player_cy) ** 2) ** 0.5
        
        nearest = min(nearby, key=distance_to)

        # 🔥 ВАЖНО: Проверяем, не уничтожен ли объект
        if nearest.is_destroyed:
            print(f"[InteractiveManager] {nearest.uid} уничтожен, взаимодействие невозможно")
            return False

        # Взаимодействуем
        return self.interact(nearest, player)

    def interact(self, obj, player):
        """Взаимодействие с конкретным объектом"""
        if obj.is_destroyed:
            return False
        
        # Проверяем дистанцию (на всякий случай)
        if not obj.is_nearby(player):
            print(f"[InteractiveManager] {obj.uid} слишком далеко")
            return False
        
        # Вызываем toggle вместо прямого on_interact
        return obj.toggle(player)
    
    def remove_destroyed(self):
        """Удаляет все уничтоженные объекты из списка"""
        self.objects = [obj for obj in self.objects if not obj.is_destroyed]

    def update(self, delta_time):
        # Сначала обновляем все объекты
        for obj in self.objects:
            obj.update(delta_time)
        
        # Потом чистим мусор (уничтоженные)
        self.remove_destroyed()