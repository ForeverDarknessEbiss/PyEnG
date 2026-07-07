import pygame
from loot.weapons.weapon import Weapon


class InventoryItem:
    def __init__(self, item, amount):
        self.item = item
        self.amount = amount 


INVENTORY_CONFIG = {
    # инвентарь
        "x": 770,
        "y": 0,
        "cols": 5, #колонки 
        "rows": 8, # строки (560 пикселей на данный момент )
        "slot_size": 60,
        "padding": 10, # отступы 
        "bg_color": (30, 30, 30),
        "slot_color": (100, 100, 100),
        "text_color": (1, 1, 1),

        # окно описания 
        "tooltip_x": 1140,
        "tooltip_y": 0,
        "tooltip_width": 300,
        "tooltip_height": 410,

        # Окно характеристик
        "stats_x": 380, 
        "stats_y": 0,
        "stats_width": 380,
        "stats_height": 120,

        # позиция слотов в слоях
        "slot_positions": {

        "weapon_primary": (380, 120, 100, 220),
        "weapon_secondary": (660, 120, 100, 220),
        "weapon_melee": (500, 280, 140, 60),
        "armor": (500, 120, 140, 140),

        "implant_head_1": (500, 120, 80, 80),
        "implant_head_2": (600, 120, 80, 80),

        "implant_spine_1": (525, 220, 60, 60),
        "implant_spine_2": (595, 220, 60, 60),
        "implant_spine_3": (560, 290, 60, 60),

        "implant_hand_1": (430, 240, 70, 140),
        "implant_hand_2": (680, 240, 70, 140),

        "implant_leg_1": (520, 360, 60, 160),
        "implant_leg_2": (600, 360, 60, 160),

        "art_1":(500, 120, 100, 100),
        "art_2":(640, 240, 100, 100),
        "art_3":(360, 240, 100, 100),
        "art_4":(500, 360, 100, 100),

        "limbs_head":(555, 120, 75, 75), 
        "limbs_leg_right":(455, 300, 130, 130), 
        "limbs_leg_left":(600, 300, 130, 130), 
        "limbs_hand_right":(425, 200, 120, 60 ),
        "limbs_hand_left":(640, 200, 120, 60),

    },

        "equipment_bg_color": (30, 30, 30),
        "equipment_slot_color": (120, 120, 120),
        "equipment_text_color": (255, 255, 255),

        "layers": {
            "equipment": ["weapon_primary", "weapon_secondary", "weapon_melee", "armor"],
            "artifacts": ["art_1", "art_2", "art_3", "art_4"],
            "implants": [
                        "implant_head_1", "implant_head_2",
                        "implant_spine_1", "implant_spine_2", "implant_spine_3",
                        "implant_hand_1", "implant_hand_2",
                        "implant_leg_1", "implant_leg_2"],
            "limbs":["limbs_head", "limbs_leg_right", "limbs_leg_left", "limbs_hand_right", "limbs_hand_left"]
            
        },
        "button_x":120,
        "button_y": 80,
        "button_width": 120,
        "button_height": 40,
        "button_padding": 1,
        "button_bg_color": (20, 20, 20),
        "button_color": (60, 60, 60),
        "button_active_color": (120, 120, 120),
        "text_button_color": (255, 255, 255),
        "tabs": [
                {"id": "equipment", "name": "Билд"},
                {"id": "implants", "name": "Спецмодули"},
                {"id": "artifacts", "name": "Артефакты"},
                {"id": "limbs", "name": "Конечности"},
    ]       
        }


class Inventory:
    def __init__(self, size=20):
        self.size = size
        self.slots = [None] * size
        self.is_open = False
        self.selection_mode = False
        self.selection_item = None
        self.context_menu = None
        self.context_buttons = []
        self.external_container = None
        
    def add_item(self, item, amount=1):
        "Пытается добавить предмет в инвентарь"
        "возвращает True если успешно"

        # player = getattr(self, "player", None)  # нужно передать player в инвентарь
        # if player:
        #     stats = player.get_combat_stats()
        #     carry_weight = stats.get("carry_weight", 0)
        #     current_weight = self.get_total_weight()
            
        #     if current_weight + item.weight > carry_weight:
        #         print("[INVENTORY] ❌ Слишком тяжело!")
        #         return False

        # ___СТАКИНГ___
    # 1. Проверяем, есть ли уже такой uid в инвентаре
        item_uid = getattr(item, 'uid', None)
        if item_uid:
            for slot in self.slots:
                if slot and hasattr(slot.item, 'uid') and slot.item.uid == item_uid:
                    print(f"[DUPLICATE] Предмет {item.name} с uid {item_uid} уже в инвентаре!")
                    return False  # или увеличить amount, если стакается
        
        # 2. Стакинг (только если предмет стакается)
        if item.stackable:
            for slot in self.slots:
                if slot and slot.item.name == item.name:
                    slot.amount += amount
                    print(f"[STACK] {item.name} +{amount}, теперь {slot.amount}")
                    return True
        
        # 3. Пустой слот
        for i in range(len(self.slots)):
            if self.slots[i] is None:
                self.slots[i] = InventoryItem(item, amount)
                print(f"[NEW SLOT] {item.name} x{amount} (uid={item_uid})")
                return True
        
        return False

    def has_free_space_for_item(self, item):
        """Проверяет, есть ли место для предмета"""
        # Если предмет стакается - проверяем наличие стака
        if item.stackable:
            for slot in self.slots:
                if slot and slot.item.name == item.name:
                    return True
        
        # Проверяем пустые слоты
        for slot in self.slots:
            if slot is None:
                return True
        
        return False

    def equip_from_slot(self, slot_index, player, force_slot=None):
        """Экипировать предмет из слота инвентаря"""
        
        if slot_index >= len(self.slots):
            return False

        item_slot = self.slots[slot_index]
        if not item_slot:
            return False

        item = item_slot.item
        
        # Определяем целевой слот
        target_slot = force_slot
        if not target_slot:
            # Если слот не указан, определяем сами
            if isinstance(item, Weapon):
                # Для оружия ищем первый свободный слот
                weapon_slots = ["weapon_primary", "weapon_secondary"]
                for slot in weapon_slots:
                    if player.equipment.slots.get(slot) is None:
                        target_slot = slot
                        break
                if not target_slot:
                    target_slot = weapon_slots[0]  # или force замену
            elif hasattr(item, "slot"):
                target_slot = item.slot
            else:
                return False
        
        # Универсальная логика замены
        # Получаем текущий предмет в слоте
        current_item = player.equipment.slots.get(target_slot)
        
        # Если тот же предмет - ничего не делаем
        if current_item is item:
            return False
        
        # Снимаем старый предмет (если есть)
        old_item = None
        if current_item:
            old_item = player.equipment.unequip(target_slot)
        
        # Надеваем новый предмет
        success = player.equipment.equip(item, target_slot)
        
        if success:
            # Удаляем предмет из инвентаря
            self.slots[slot_index] = None
            
            # Если был старый предмет, добавляем его в инвентарь
            if old_item:
                self.add_item(old_item, 1)
            
            return True
        
        # Если не получилось надеть, возвращаем старый предмет обратно
        if old_item:
            player.equipment.equip(old_item, target_slot)
        
        return False

    def unequip_item(self, item, player):
        """Снять предмет и положить в инвентарь"""
        for slot_name, equipped in player.equipment.slots.items():
            if equipped == item:
                # Снимаем предмет
                player.equipment.unequip(slot_name)
                # Добавляем в инвентарь (проверяем, нет ли уже стака)
                # Для брони стака обычно нет, но на всякий случай
                added = self.add_item(item, 1)
                if not added:
                    # Если не добавилось (нет места), возвращаем обратно
                    player.equipment.equip(item, slot_name)
                    return False
                return True
        return False

    def get_slot_under_mouse(self, mouse_x, mouse_y):
        cfg = INVENTORY_CONFIG

        start_x = cfg["x"]
        start_y = cfg["y"]
        slot_size = cfg["slot_size"]
        padding = cfg["padding"]
        cols = cfg["cols"]

        for i in range(len(self.slots)):
            col = i % cols
            row = i // cols

            x = start_x + col * (slot_size + padding)
            y = start_y + row * (slot_size + padding)

            rect = pygame.Rect(x, y, slot_size, slot_size)

            if rect.collidepoint(mouse_x, mouse_y):
                return i

        return None

    def open_context_menu(self, slot_data, player, slot_type="inventory"):
        
        # Определяем item в зависимости от типа слота
        if slot_type == "inventory":
            if self.slots[slot_data] is None:
                return
            item = self.slots[slot_data].item
            
        elif slot_type == "equipment":
            item = player.equipment.slots.get(slot_data)
            if not item:
                return
        else:
            return

        # Если у предмета есть get_actions - используем его
        if hasattr(item, 'get_actions'):
            actions = item.get_actions(player, slot_data, slot_type)
        else:
            # Fallback только для обычных предметов в инвентаре
            actions = [{
                "name": "Выбросить",
                "action": lambda: player.drop_item_by_reference(item)
            }]
        
        self.context_menu = {
            "item": item,
            "actions": actions,
            "position": pygame.mouse.get_pos(), 
            "slot_data": slot_data,
            "slot_type": slot_type    
        }

    def handle_context_click(self, player, mouse_pos):
        if not hasattr(self, "context_buttons"):
            return

        for rect, action in self.context_buttons:
            if rect.collidepoint(mouse_pos):

                # выполнить действие
                action["action"]()

                self.context_menu = None
                return True
        return False
    
