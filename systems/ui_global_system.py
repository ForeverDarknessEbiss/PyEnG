import pygame
import camera
class WeaponCarousel:
    def __init__(self):
        # Активный слот (центральный)
        self.active_x = 20
        self.active_y = 740
        self.active_w = 180
        self.active_h = 60
        
        # Размеры неактивных слотов
        self.inactive_w = 140
        self.inactive_h = 40
        
        # Отступ между слотами
        self.gap = 20

        self.tooltip_open = False

        # Настройки HP бара
        self.hp_x = 560
        self.hp_y = 820
        self.hp_width = 200
        self.hp_height = 20
        self.hp_color = (212,97,51)  

        # Настройки Energy бара
        self.energy_x = 765
        self.energy_y = 820
        self.energy_width = 200
        self.energy_height = 20
        self.energy_color = (0, 127, 255)  

        # 🆕 Иконка персонажа
        self.character_icon_x = 480
        self.character_icon_y = 800
        self.character_icon_size = 60

        # 🆕 Индикаторы имплантов
        self.implant_indicators = ImplantIndicators(
            x=985,           # координата X
            y=820,          # координата Y
            width=40,       # ширина
            height=40,      # высота
            padding=10      # отступ между индикаторами
        )

        # Настройки текста
        self.font_size = 18
        self.font_color = (255, 255, 255)
        self.font = pygame.font.Font(None, self.font_size)

        # Порядок слотов по кругу (сверху вниз, циклически)
        self.slot_order = ["weapon_primary", "weapon_secondary", "weapon_melee"]
        
        # Вычисляем позиции неактивных слотов
        self.top_y = self.active_y - self.inactive_h - self.gap
        self.bottom_y = self.active_y + self.active_h + self.gap
    
    def _draw_carousel(self, screen, player):
        active_slot = player.active_weapon_slot
        active_index = self.slot_order.index(active_slot)
        
        # Получаем три слота в порядке циклического вращения
        # Верхний слот = предыдущий по кругу
        # Центральный = активный
        # Нижний слот = следующий по кругу
        top_index = (active_index - 1) % len(self.slot_order)
        bottom_index = (active_index + 1) % len(self.slot_order)
        
        top_slot = self.slot_order[top_index]
        center_slot = self.slot_order[active_index]
        bottom_slot = self.slot_order[bottom_index]
        
        # Рисуем все три слота
        self._draw_slot(screen, player, top_slot, 
                       self.active_x, self.top_y, 
                       self.inactive_w, self.inactive_h, False)
        self._draw_slot(screen, player, center_slot, 
                       self.active_x, self.active_y, 
                       self.active_w, self.active_h, True)
        self._draw_slot(screen, player, bottom_slot, 
                       self.active_x, self.bottom_y, 
                       self.inactive_w, self.inactive_h, False)
    
    def _draw_slot(self, screen, player, slot_name, x, y, w, h, is_active):
        weapon = player.equipment.slots.get(slot_name)
        font = pygame.font.Font(None, 24)
        
        # Рамка
        color = (200, 200, 200) if is_active else (100, 100, 100)
        border_width = 3 if is_active else 2
        pygame.draw.rect(screen, color, (x, y, w, h), border_width)
        
        if weapon:
            # Иконка
            icon_rect = pygame.Rect(x + 4, y + 4, w - 8, h - 8)
            pygame.draw.rect(screen, weapon.color, icon_rect)
            
            # Номер слота
            numbers = {"weapon_primary": 1, "weapon_secondary": 2, "weapon_melee": 3}
            num_surf = font.render(str(numbers.get(slot_name, "?")), True, (255, 255, 255))
            screen.blit(num_surf, (x + 5, y + 5))
            
            # Патроны (только для активного и дальнобойного)
            if is_active and weapon.weapon_type == "ranged":
                # TODO: получить количество патронов из инвентаря
                ammo_text = f"{weapon.current_ammo}/??"
                ammo_surf = font.render(ammo_text, True, (255, 255, 255))
                screen.blit(ammo_surf, (x + w - ammo_surf.get_width() - 5, y + h - 25))
        else:
            empty_text = font.render("EMPTY", True, (100, 100, 100))
            text_rect = empty_text.get_rect(center=(x + w//2, y + h//2))
            screen.blit(empty_text, text_rect)

    def draw_character_icon(self, screen, player):
        """Отрисовка иконки персонажа"""
        x = self.character_icon_x
        y = self.character_icon_y
        size = self.character_icon_size
        
        # Фон
        pygame.draw.rect(screen, (50, 50, 50), (x, y, size, size))
        pygame.draw.rect(screen, (100, 100, 100), (x, y, size, size), 2)
        
        # Силуэт
        center_x = x + size // 2
        center_y = y + size // 2
        pygame.draw.circle(screen, (150, 150, 150), (center_x, center_y), size // 3)
        
        # Ховер для тултипа
        mouse_x, mouse_y = pygame.mouse.get_pos()
        icon_rect = pygame.Rect(x, y, size, size)
        
        if icon_rect.collidepoint(mouse_x, mouse_y):
            self.draw_limb_schema_tooltip(screen, player, mouse_x, mouse_y)

    def draw_limb_schema_tooltip(self, screen, player, icon_rect):
        """Отрисовка схемы слотов имплантов (над иконкой персонажа)"""
        
        # Позиция тултипа (над иконкой персонажа)
        x = icon_rect.x + icon_rect.width // 2
        y = icon_rect.y + 2
        
        width = 180
        height = 180
        
        # Фон
        tooltip_rect = pygame.Rect(x - width//2, y - height, width, height)
        pygame.draw.rect(screen, (30, 30, 30), tooltip_rect)
        pygame.draw.rect(screen, (100, 100, 100), tooltip_rect, 1)
        
        # Центр схемы (относительно тултипа)
        center_x = tooltip_rect.x + width // 2
        base_y = tooltip_rect.y + 20
        
        # Настройки слотов
        slot_size = 24
        gap = 8

        # Ряд 1: Голова (2 слота)
        self._draw_implant_slot(screen, player, center_x - 15, base_y, slot_size, "implant_head_1")
        self._draw_implant_slot(screen, player, center_x + 15, base_y, slot_size, "implant_head_2")
        
        # Ряд 2: Руки + Тело (4 слота)
        self._draw_implant_slot(screen, player, center_x - 55, base_y + 45, slot_size, "implant_hand_1")
        self._draw_implant_slot(screen, player, center_x - 18, base_y + 45, slot_size, "implant_spine_1")
        self._draw_implant_slot(screen, player, center_x + 18, base_y + 45, slot_size, "implant_spine_2")
        self._draw_implant_slot(screen, player, center_x + 55, base_y + 45, slot_size, "implant_hand_2")
        
        # Ряд 3: Тело центральное (1 слот)
        self._draw_implant_slot(screen, player, center_x, base_y + 90, slot_size, "implant_spine_3")
        
        # Ряд 4: Ноги (2 слота)
        self._draw_implant_slot(screen, player, center_x - 25, base_y + 130, slot_size, "implant_leg_1")
        self._draw_implant_slot(screen, player, center_x + 25, base_y + 130, slot_size, "implant_leg_2")

    def _draw_implant_slot(self, screen, player, x, y, size, slot_id):
        """Отрисовка конкретного слота импланта"""
        
        # Получаем имплант из конкретного слота
        implant = player.equipment.slots.get(slot_id)
        has_implant = implant is not None
        
        rect = pygame.Rect(x - size//2, y - size//2, size, size)
        
        if has_implant:
            # Проверяем состояние импланта (ВКЛ/ВЫКЛ)
            is_enabled = True
            if hasattr(implant, 'enabled'):
                is_enabled = implant.enabled
            elif hasattr(implant, 'uid') and player.implant_manager:
                mechanic = player.implant_manager.get_mechanic_by_uid(implant.uid)
                if mechanic:
                    is_enabled = mechanic.enabled
            
            if is_enabled:
                # Включён - полный цвет
                pygame.draw.rect(screen, implant.color, rect)
                pygame.draw.rect(screen, (200, 200, 200), rect, 2)
            else:
                # Выключен - затемнённый цвет (делим RGB на 3)
                dark_color = tuple(c // 3 for c in implant.color)
                pygame.draw.rect(screen, dark_color, rect)
                pygame.draw.rect(screen, (100, 100, 100), rect, 2)
                
                # Текст OFF
                font = pygame.font.Font(None, 12)
                off_text = font.render("OFF", True, (150, 150, 150))
                off_rect = off_text.get_rect(center=(x, y))
                screen.blit(off_text, off_rect)
        else:
            # Свободный слот - пустой контур
            pygame.draw.rect(screen, (80, 80, 80), rect, 2)
    
    def draw_hp_bar(self, screen, player):
        """Отрисовка полоски здоровья"""

        total_hp = player.limb_health_system.get_total_hp()
        max_hp = player.limb_health_system.get_total_max_hp()
        if max_hp <= 0:
            return
        percent = total_hp / max_hp

        current_width = int(self.hp_width * percent)
        
        # Полоска
        pygame.draw.rect(screen, self.hp_color, 
                        (self.hp_x, self.hp_y, current_width, self.hp_height))
        
        # Текст (здоровье)
        text = f"{int(total_hp)}/{int(max_hp)}"
        text_surf = self.font.render(text, True, self.font_color)
        text_rect = text_surf.get_rect(center=(self.hp_x + self.hp_width // 2, 
                                                self.hp_y -10))
        screen.blit(text_surf, text_rect)

    def _draw_hp_tooltip(self, screen, player, mouse_x, mouse_y):
        """Отрисовка тултипа с информацией о здоровье конечностей"""
        hp_rect = pygame.Rect(self.hp_x, self.hp_y, self.hp_width, self.hp_height)
        if not hp_rect.collidepoint(mouse_x, mouse_y):
            return
        
        font = pygame.font.Font(None, 18)
        width = 220
        line_height = 20
        
        # Получаем статус конечностей из limb_health_system
        limbs_status = []
        for limb_id, limb in player.limb_health_system.limbs.items():
            limbs_status.append({
                "name": limb.name,
                "current": limb.hp,
                "max": limb.max_hp,
                "broken": limb.is_destroyed()
            })
        
        # Вычисляем высоту окна (заголовок + конечности)
        height = 30 + len(limbs_status) * line_height
        
        x = mouse_x + 15
        y = mouse_y - height - 10
        
        # Фон
        pygame.draw.rect(screen, (30, 30, 30), (x, y, width, height))
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height), 1)
        
        # Заголовок
        title = font.render(f"❤️ Здоровье конечностей", True, (255, 200, 200))
        screen.blit(title, (x + 8, y + 5))
        
        # Список конечностей
        y_offset = y + 25
        for limb in limbs_status:
            if limb["broken"]:
                color = (255, 100, 100)
                text = font.render(f"{limb['name']}: 💀 Сломана", True, color)
            else:
                color = (200, 200, 200)
                bar_len = int(10 * limb["current"] / limb["max"])
                bar = "█" * bar_len + "░" * (10 - bar_len)
                text = font.render(f"{limb['name']}: {limb['current']}/{limb['max']} [{bar}]", True, color)
            
            screen.blit(text, (x + 12, y_offset))
            y_offset += line_height

    def get_limb_schema_rect(self, icon_rect):
        """Возвращает прямоугольник тултипа для проверки ховера"""
        x = icon_rect.x + icon_rect.width // 2
        y = icon_rect.y + 10  # как в draw_limb_schema_tooltip
        width = 180
        height = 180
        return pygame.Rect(x - width//2, y - height, width, height)

    def draw_character_icon(self, screen, player):
        x = self.character_icon_x
        y = self.character_icon_y
        size = self.character_icon_size
        
        # Сохраняем rect для проверки кликов
        self.character_icon_rect = pygame.Rect(x, y, size, size)
        
        # Фон
        pygame.draw.rect(screen, (50, 50, 50), self.character_icon_rect)
        pygame.draw.rect(screen, (100, 100, 100), self.character_icon_rect, 2)
        
        # Силуэт
        center_x = x + size // 2
        center_y = y + size // 2
        pygame.draw.circle(screen, (150, 150, 150), (center_x, center_y), size // 3)
        
        # 🆕 Флаг состояния тултипа
        if not hasattr(self, 'tooltip_open'):
            self.tooltip_open = False
        
        # Ховер для тултипа
        mouse_x, mouse_y = pygame.mouse.get_pos()
        icon_rect = pygame.Rect(x, y, size, size)
        tooltip_rect = self.get_limb_schema_rect(self.character_icon_rect)
        
        # Проверка ховера на иконке и тултипе
        hover_icon = icon_rect.collidepoint(mouse_x, mouse_y)
        hover_tooltip = tooltip_rect and tooltip_rect.collidepoint(mouse_x, mouse_y)
        
        # Открываем тултип при наведении на иконку
        if hover_icon:
            self.tooltip_open = True
        
        # Закрываем тултип если мышь ушла и с иконки, и с тултипа
        if not hover_icon and not hover_tooltip:
            self.tooltip_open = False
        
        # Рисуем тултип если нужно
        if self.tooltip_open:
            self.draw_limb_schema_tooltip(screen, player, self.character_icon_rect)
    
    def draw(self, screen, player):
        """Главный метод отрисовки всего HUD"""
        # Рисуем карусель оружия
        self._draw_carousel(screen, player)  # переименуй текущий draw в _draw_carousel
        
        # Рисуем полоски
        self.draw_hp_bar(screen, player)

        # 🆕 Рисуем тултип 
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self._draw_hp_tooltip(screen, player, mouse_x, mouse_y)
        self.implant_indicators.draw(screen, player)
        self.draw_character_icon(screen, player)

                # В ui_global_system.py, в draw()
        # if hasattr(player, 'implant_manager'):
        #     for uid, data in player.implant_manager.active_mechanics.items():
        #         if data["key"] == "radar":
        #             # 🆕 Передаём все нужные аргументы
        #             data["instance"].draw(screen, camera, game_map, monster_manager, loot_system)

    def handle_implant_slot_click(self, mouse_pos, player):
        """Проверяет, был ли клик по слоту импланта в тултипе"""
        if not self.tooltip_open:
            return False
        
        # Получаем позицию тултипа
        tooltip_rect = self.get_limb_schema_rect(self.character_icon_rect)
        if not tooltip_rect.collidepoint(mouse_pos):
            return False
        
        # Координаты клика относительно тултипа
        local_x = mouse_pos[0] - tooltip_rect.x
        local_y = mouse_pos[1] - tooltip_rect.y
        
        # Параметры слотов
        slot_size = 24
        center_x = tooltip_rect.width // 2
        base_y = 20
        
        # Список слотов для проверки: (slot_name, x_offset, y_offset)
        slots = [
            # Голова
            ("implant_head_1", center_x - 15, base_y),
            ("implant_head_2", center_x + 15, base_y),
            # Руки + тело (ряд 2)
            ("implant_hand_1", center_x - 55, base_y + 45),
            ("implant_spine_1", center_x - 18, base_y + 45),
            ("implant_spine_2", center_x + 18, base_y + 45),
            ("implant_hand_2", center_x + 55, base_y + 45),
            # Тело центральное
            ("implant_spine_3", center_x, base_y + 90),
            # Ноги
            ("implant_leg_1", center_x - 25, base_y + 130),
            ("implant_leg_2", center_x + 25, base_y + 130),
        ]
        
        # Проверяем каждый слот
        for slot_name, slot_x, slot_y in slots:
            slot_rect = pygame.Rect(
                tooltip_rect.x + slot_x - slot_size//2,
                tooltip_rect.y + slot_y - slot_size//2,
                slot_size, slot_size
            )
            if slot_rect.collidepoint(mouse_pos):
                self.toggle_implant(player, slot_name)
                return True
        
        return False

    def toggle_implant(self, player, slot_name):
        """Включает/выключает имплант в слоте"""
        implant = player.equipment.slots.get(slot_name)
        if not implant:
            return
        
        # Получаем механику импланта
        mechanic = player.implant_manager.get_mechanic_by_uid(implant.uid)
        if mechanic:
            new_state = not mechanic.enabled
            mechanic.set_enabled(new_state)
            print(f"[IMPLANT] {implant.name} -> {'ВКЛ' if new_state else 'ВЫКЛ'}")
        else:
            # Если механики нет, просто переключаем флаг на импланте
            if not hasattr(implant, 'enabled'):
                implant.enabled = True
            implant.enabled = not implant.enabled
            print(f"[IMPLANT] {implant.name} -> {'ВКЛ' if implant.enabled else 'ВЫКЛ'}")


class ImplantIndicators:
    def __init__(self, x, y, width, height, padding):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.padding = padding
        self.font = pygame.font.Font(None, 16)
    
    def draw(self, screen, player):
        """Отрисовка индикаторов активных имплантов"""
        # Собираем импланты с механиками
        implants_with_indicators = []
        
        for slot, item in player.equipment.slots.items():
            if item and hasattr(item, "mechanics") and item.mechanics:
                # Получаем механику из менеджера
                mechanic = player.implant_manager.get_mechanic_by_uid(item.uid)
                if mechanic:
                    implants_with_indicators.append({
                        "name": item.name,
                        "mechanic": mechanic,
                        "color": item.color
                    })
        
        # Отрисовка
        for i, implant in enumerate(implants_with_indicators):
            x = self.x + i * (self.width + self.padding)
            y = self.y
            
            # Фон индикатора
            pygame.draw.rect(screen, (50, 50, 50), (x, y, self.width, self.height))
            pygame.draw.rect(screen, (100, 100, 100), (x, y, self.width, self.height), 1)
            
            # Иконка (цвет предмета)
            icon_rect = pygame.Rect(x + 4, y + 4, self.width - 8, self.height - 8)
            
            # Затемнение если на кулдауне или выключен
            mechanic = implant["mechanic"]
            if mechanic.cooldown_timer > 0:
                # Кулдаун - затемнённый цвет + таймер
                color = tuple(c // 3 for c in implant["color"])
                pygame.draw.rect(screen, color, icon_rect)
                # Текст таймера
                timer_text = f"{mechanic.cooldown_timer:.1f}"
                text_surf = self.font.render(timer_text, True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=(x + self.width//2, y + self.height//2))
                screen.blit(text_surf, text_rect)
            elif not mechanic.enabled:
                # Выключен - серый
                color = (80, 80, 80)
                pygame.draw.rect(screen, color, icon_rect)
                off_text = self.font.render("OFF", True, (150, 150, 150))
                off_rect = off_text.get_rect(center=(x + self.width//2, y + self.height//2))
                screen.blit(off_text, off_rect)
            else:
                # Готов к использованию
                pygame.draw.rect(screen, implant["color"], icon_rect)