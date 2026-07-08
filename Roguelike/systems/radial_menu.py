import pygame
import math

class RadialMenu:
    def __init__(self, screen_width, screen_height):
        self.center_x = screen_width // 2
        self.center_y = screen_height // 2
        self.radius_outer = 200
        self.radius_inner = 120
        self.icon_size = 48
        self.active = False
        self.segments = []
        self.selected_segment = None
        self.activated_this_frame = False
        
        # Цвета
        self.bg_color = (20, 20, 20, 200)
        self.highlight_color = (100, 150, 200, 200)
        self.segment_color = (40, 40, 40, 200)
        
        # Шрифт
        self.font = pygame.font.Font(None, 14)
    
    def update_segments(self, player):
        """Обновляет список сегментов на основе активных имплантов"""
        self.segments = []
        
        # Собираем импланты с активными механиками (скилами)
        for slot, implant in player.equipment.slots.items():
            if not implant:
                continue
            
            # Проверяем, есть ли у импланта механика
            if not hasattr(implant, 'mechanics') or not implant.mechanics:
                continue
            
            # Проверяем, включён ли имплант
            is_enabled = True
            if hasattr(implant, 'enabled'):
                is_enabled = implant.enabled
            elif implant.uid and hasattr(player, 'implant_manager'):
                mechanic = player.implant_manager.get_mechanic_by_uid(implant.uid)
                if mechanic:
                    is_enabled = mechanic.enabled
            
            if not is_enabled:
                continue
            
            # Проверяем, есть ли у механики активная способность
            # (пока пропускаем, позже добавим флаг)
            
            self.segments.append({
                "name": implant.name,
                "color": implant.color,
                "implant": implant,
                "uid": implant.uid,
                "cooldown": 0  # TODO: получить из механики
            })
        
        # Добавляем сегмент отмены
        self.segments.append({
            "name": "Cancel",
            "color": (150, 50, 50),
            "implant": None,
            "uid": None,
            "cooldown": 0
        })
        
        # Рассчитываем углы для сегментов
        if self.segments:
            angle_step = 360 / len(self.segments)
            for i, seg in enumerate(self.segments):
                seg["start_angle"] = i * angle_step
                seg["end_angle"] = (i + 1) * angle_step
    
    def update(self, mouse_pos):
        """Обновляет выбранный сегмент на основе позиции мыши"""
        if not self.active:
            return
        
        mouse_x, mouse_y = mouse_pos
        
        print(f"[RADIAL] update: mouse=({mouse_x},{mouse_y})")
        
        for seg in self.segments:
            in_segment = self._point_in_segment(mouse_x, mouse_y, seg["start_angle"], seg["end_angle"])
            print(f"  {seg['name']}: start={seg['start_angle']:.1f}, end={seg['end_angle']:.1f}, hit={in_segment}")
            if in_segment:
                self.selected_segment = seg
                print(f"[RADIAL] >>> ВЫБРАН: {seg['name']}")
                return
    
        # Если мышь не в сегменте, НЕ сбрасываем
        print("[RADIAL] Мышь вне сегментов, оставляем предыдущий выбор")    
    
    def _point_in_segment(self, px, py, start_angle, end_angle):
        """Проверяет, находится ли точка в сегменте"""
        dx = px - self.center_x
        dy = py - self.center_y
        dist = math.hypot(dx, dy)
        
        # Проверка расстояния
        if not (self.radius_inner <= dist <= self.radius_outer):
            print(f"    dist={dist:.1f}, не в радиусе ({self.radius_inner}-{self.radius_outer})")
            return False
        
        # Проверка угла
        angle = math.degrees(math.atan2(dy, dx))
        if angle < 0:
            angle += 360
        
        # Нормализация угла в диапазон сегмента
        if start_angle <= end_angle:
            result = start_angle <= angle <= end_angle
            print(f"    angle={angle:.1f}, range={start_angle:.1f}-{end_angle:.1f}, hit={result}")
            return result
        else:
            result = angle >= start_angle or angle <= end_angle
            print(f"    angle={angle:.1f}, пересекает 0°, range={start_angle:.1f}-{end_angle:.1f}, hit={result}")
            return result
        
    def activate(self):
        """Активирует выбранный сегмент"""
        print(f"[RADIAL] activate() START, selected_segment={self.selected_segment}")
        
        if not self.selected_segment:
            print("[RADIAL] Нет выбранного сегмента")
            return False
        
        seg = self.selected_segment
        print(f"[RADIAL] Активируем: {seg['name']}")
        
        if seg["name"] == "Cancel":
            print("[RADIAL] Отмена")
            self.selected_segment = None
            return True
        
        if seg["implant"] and hasattr(seg["implant"], 'uid'):
            if hasattr(self, 'player') and self.player:
                mechanic = self.player.implant_manager.get_mechanic_by_uid(seg["uid"])
                if mechanic:
                    print(f"[RADIAL] Вызываем mechanic.use()")
                    result = mechanic.use()
                    print(f"[RADIAL] Результат: {result}")
                    self.selected_segment = None
                    return result
                else:
                    print(f"[RADIAL] Механика не найдена для uid {seg['uid']}")
        
        print("[RADIAL] Не удалось активировать")
        return False
    
    def draw(self, screen):
        """Отрисовка радиального меню"""
        if not self.active:
            return
        
        # Полупрозрачный фон
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Рисуем сегменты
        for i, seg in enumerate(self.segments):
            is_selected = (seg == self.selected_segment)
            self._draw_segment(screen, seg["start_angle"], seg["end_angle"], 
                              seg["color"], is_selected, seg["name"], seg.get("cooldown", 0))
    
    def _draw_segment(self, screen, start_angle, end_angle, color, is_selected, name, cooldown):
        """Рисует один сегмент"""
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # Рисуем сектор (заливка)
        points = [(self.center_x, self.center_y)]
        
        # Внешняя дуга
        for angle in range(int(start_angle), int(end_angle) + 1):
            rad = math.radians(angle)
            x = self.center_x + self.radius_outer * math.cos(rad)
            y = self.center_y + self.radius_outer * math.sin(rad)
            points.append((x, y))
        
        # Внутренняя дуга (обратно)
        for angle in range(int(end_angle), int(start_angle) - 1, -1):
            rad = math.radians(angle)
            x = self.center_x + self.radius_inner * math.cos(rad)
            y = self.center_y + self.radius_inner * math.sin(rad)
            points.append((x, y))
        
        # Цвет сегмента
        if is_selected:
            seg_color = self.highlight_color
        else:
            seg_color = self.segment_color
        
        pygame.draw.polygon(screen, seg_color, points)
        
        # 🆕 Рисуем ТОЛЬКО внешнюю и внутреннюю границы (без радиальных линий)
        # Внешняя граница
        outer_points = []
        for angle in range(int(start_angle), int(end_angle) + 1):
            rad = math.radians(angle)
            x = self.center_x + self.radius_outer * math.cos(rad)
            y = self.center_y + self.radius_outer * math.sin(rad)
            outer_points.append((x, y))
        if len(outer_points) > 1:
            pygame.draw.lines(screen, (100, 100, 100), False, outer_points, 2)
        
        # Внутренняя граница
        inner_points = []
        for angle in range(int(start_angle), int(end_angle) + 1):
            rad = math.radians(angle)
            x = self.center_x + self.radius_inner * math.cos(rad)
            y = self.center_y + self.radius_inner * math.sin(rad)
            inner_points.append((x, y))
        if len(inner_points) > 1:
            pygame.draw.lines(screen, (100, 100, 100), False, inner_points, 2)
        
        # Иконка
        mid_angle = (start_angle + end_angle) / 2
        mid_rad = math.radians(mid_angle)
        icon_x = self.center_x + (self.radius_inner + self.radius_outer) // 2 * math.cos(mid_rad)
        icon_y = self.center_y + (self.radius_inner + self.radius_outer) // 2 * math.sin(mid_rad)
        
        icon_rect = pygame.Rect(icon_x - self.icon_size//2, icon_y - self.icon_size//2, 
                                self.icon_size, self.icon_size)
        
        if cooldown > 0:
            dark_color = tuple(c // 3 for c in color)
            pygame.draw.rect(screen, dark_color, icon_rect)
            timer_text = self.font.render(f"{cooldown:.1f}", True, (255, 255, 255))
            timer_rect = timer_text.get_rect(center=(icon_x, icon_y))
            screen.blit(timer_text, timer_rect)
        else:
            pygame.draw.rect(screen, color, icon_rect)
            pygame.draw.rect(screen, (200, 200, 200), icon_rect, 2)
        
        # Название (только если выбран)
        if is_selected and name != "Cancel":
            text = self.font.render(name, True, (255, 255, 255))
            text_rect = text.get_rect(center=(icon_x, icon_y + self.icon_size//2 + 10))
            screen.blit(text, text_rect)