# systems/implants/mechanics/dash.py
from ..base import BaseMechanic

class Mechanic(BaseMechanic):
    def _on_use(self):
        # Определяем направление рывка
        dx = self.player.last_dx
        dy = self.player.last_dy
        
        # Если нет направления движения - рывок вперёд (по последнему оружию или вправо)
        if dx == 0 and dy == 0:
            dx = 1
            dy = 0
        
        # Нормализуем вектор (диагональ тоже даст длину 1)
        length = (dx**2 + dy**2) ** 0.5
        if length > 0:
            dx /= length
            dy /= length
        
        # Дальность рывка
        dash_distance = 150
        
        # Новая позиция
        new_x = self.player.x + dx * dash_distance
        new_y = self.player.y + dy * dash_distance
        
        # TODO: проверка коллизий с картой и стенами
        # Пока просто применяем
        self.player.x = new_x
        self.player.y = new_y
        
        print(f"[DASH] Рывок: ({dx:.2f}, {dy:.2f}) -> distance={dash_distance}")