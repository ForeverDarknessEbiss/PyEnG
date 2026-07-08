class BaseInteractiveObject:
    def __init__(self, uid, x, y, config):
        self.uid = uid
        self.x = x
        self.y = y
        self.config = config
        self.hp = config.get("hp", 1)
        self.max_hp = self.hp
        self.is_destroyed = False
    
    def take_damage(self, amount):
        if self.is_destroyed:
            return
        self.hp -= amount
        if self.hp <= 0:
            self._destroy()
    
    def _destroy(self):
        self.is_destroyed = True
        self._on_destroy()
    
    def _on_destroy(self):
        pass
    
    def on_interact(self, player):
        pass
    
    def get_interact_button(self):
        return "F"
    
    def can_enter(self):
        return self.is_destroyed
    
    def update(self, delta_time):
        pass
    
    def draw(self, screen, camera):
        pass

    def is_nearby(self, player, max_distance=60):
        """
        Проверяет, находится ли игрок достаточно близко для взаимодействия.
        max_distance: в пикселях (по умолчанию 60 = ~1.5 тайла)
        """
        # Вычисляем центры объектов
        obj_center_x = self.x + self.config.get("width", 40) // 2
        obj_center_y = self.y + self.config.get("height", 40) // 2
        player_center_x = player.x + player.width // 2
        player_center_y = player.y + player.height // 2
        
        distance = ((obj_center_x - player_center_x) ** 2 + (obj_center_y - player_center_y) ** 2) ** 0.5
        return distance <= max_distance

    def toggle(self, player):
        """
        Переключает состояние объекта (открыть/закрыть).
        Вызывается из InteractiveManager при нажатии F.
        """
        if self.is_destroyed:
            return False
        
        # Проверяем дистанцию
        if not self.is_nearby(player):
            print(f"[{self.uid}] Игрок слишком далеко")
            return False
        
        # Переключаем состояние (будет переопределено в наследниках)
        return self._on_toggle(player)

    def _on_toggle(self, player):
        """
        Конкретная логика переключения.
        Должна быть переопределена в наследниках.
        """
        pass