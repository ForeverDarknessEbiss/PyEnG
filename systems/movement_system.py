# systems/movement_system.py
import math

class MovementSystem:
    """
    Система движения для игрока и монстров
    """
    
    def __init__(self, entity=None):
        self.entity = entity
        self.dx = 0
        self.dy = 0
        self.last_dx = 1
        self.last_dy = 0
    
    def set_direction(self, dx, dy):
        """Установить направление движения"""
        self.dx = dx
        self.dy = dy
        if dx != 0 or dy != 0:
            self.last_dx = dx
            self.last_dy = dy
    
    def get_normalized_direction(self):
        """Вернуть нормализованное направление"""
        dx = self.dx
        dy = self.dy
        length = math.hypot(dx, dy)
        if length > 0:
            dx /= length
            dy /= length
        return dx, dy
    
    def update_player(self, game_map, base_speed, delta_time, speed_bonus=0):
        """Обновление позиции игрока с проверкой карты"""
        dx, dy = self.get_normalized_direction()
        
        final_speed = base_speed * (1 + speed_bonus / 100)
        
        new_x = self.entity.x + dx * final_speed 
        new_y = self.entity.y + dy * final_speed 
        
        # Проверка коллизий с картой
        grid_x = int(new_x // 40)
        grid_y = int(new_y // 40)
        
        if game_map.is_walkable(grid_x, grid_y):
            self.entity.x = new_x
            self.entity.y = new_y
        
        return dx, dy
    
    def update_monster(self, monster, delta_time):
        """Обновление позиции монстра"""
        if not monster.alive:
            return
        monster.x += monster.dx * monster.speed * delta_time
        monster.y += monster.dy * monster.speed * delta_time
    
    def update_monsters(self, monsters, delta_time):
        """Обновление позиции всех монстров"""
        for monster in monsters:
            self.update_monster(monster, delta_time)
    