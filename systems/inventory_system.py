# systems/inventory_system.py

import pygame
from loot.weapons.weapon import Weapon
from systems.inventory_config import INVENTORY_CONFIG


class InventoryItem:
    def __init__(self, item, amount):
        self.item = item
        self.amount = amount


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
        """Пытается добавить предмет в инвентарь. Возвращает True если успешно."""
        item_uid = getattr(item, 'uid', None)
        if item_uid:
            for slot in self.slots:
                if slot and hasattr(slot.item, 'uid') and slot.item.uid == item_uid:
                    print(f"[DUPLICATE] Предмет {item.name} с uid {item_uid} уже в инвентаре!")
                    return False

        if item.stackable:
            for slot in self.slots:
                if slot and slot.item.name == item.name:
                    slot.amount += amount
                    print(f"[STACK] {item.name} +{amount}, теперь {slot.amount}")
                    return True

        for i in range(len(self.slots)):
            if self.slots[i] is None:
                self.slots[i] = InventoryItem(item, amount)
                print(f"[NEW SLOT] {item.name} x{amount} (uid={item_uid})")
                return True

        return False

    def has_free_space_for_item(self, item):
        if item.stackable:
            for slot in self.slots:
                if slot and slot.item.name == item.name:
                    return True
        for slot in self.slots:
            if slot is None:
                return True
        return False

    def equip_from_slot(self, slot_index, player, force_slot=None):
        if slot_index >= len(self.slots):
            return False
        item_slot = self.slots[slot_index]
        if not item_slot:
            return False
        item = item_slot.item
        target_slot = force_slot
        if not target_slot:
            if isinstance(item, Weapon):
                weapon_slots = ["weapon_primary", "weapon_secondary"]
                for slot in weapon_slots:
                    if player.equipment.slots.get(slot) is None:
                        target_slot = slot
                        break
                if not target_slot:
                    target_slot = weapon_slots[0]
            elif hasattr(item, "slot"):
                target_slot = item.slot
            else:
                return False
        current_item = player.equipment.slots.get(target_slot)
        if current_item is item:
            return False
        old_item = None
        if current_item:
            old_item = player.equipment.unequip(target_slot)
        success = player.equipment.equip(item, target_slot)
        if success:
            self.slots[slot_index] = None
            if old_item:
                self.add_item(old_item, 1)
            return True
        if old_item:
            player.equipment.equip(old_item, target_slot)
        return False

    def unequip_item(self, item, player):
        for slot_name, equipped in player.equipment.slots.items():
            if equipped == item:
                player.equipment.unequip(slot_name)
                added = self.add_item(item, 1)
                if not added:
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
        if hasattr(item, 'get_actions'):
            actions = item.get_actions(player, slot_data, slot_type)
        else:
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
                action["action"]()
                self.context_menu = None
                return True
        return False

    def refresh_limb_slots(self, player):
        """Обновляет слоты экипировки на основе конечностей."""
        if not hasattr(player, 'limb_health_system'):
            return
        if hasattr(player, 'equipment'):
            player.equipment.update_slots_from_limbs(player.limb_health_system)