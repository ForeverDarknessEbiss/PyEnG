# loot/limbs/limb.py

class Limb:
    """
    Конечность персонажа/NPC.
    Содержит здоровье и информацию о слотах оружия.
    """
    
    def __init__(self, limb_id: int, name: str, limb_type: str, hp: int, slot_type: str | None = None, slot_count: int = 0):
        self.limb_id = limb_id
        self.name = name
        self.limb_type = limb_type
        self.hp = hp
        self.max_hp = hp
        
        self.slot_type = slot_type
        self.slot_count = slot_count
        
        self.slots = {}
        if slot_type and slot_count > 0:
            for i in range(slot_count):
                slot_id = f"{slot_type}_{i}" if slot_count > 1 else slot_type
                self.slots[slot_id] = None
        
        # Цвет для отображения
        limb_colors = {
            "head": (255, 220, 180),
            "left_arm": (180, 200, 255),
            "right_arm": (180, 200, 255),
            "left_leg": (180, 255, 200),
            "right_leg": (180, 255, 200),
        }
        self.color = limb_colors.get(limb_type, (150, 150, 150))
        self.stackable = False
        self.description = f"{name}\nHP: {hp}\nТип: {limb_type}"
    
    # ===== ЗДОРОВЬЕ =====
    
    def take_damage(self, amount: int) -> int:
        self.hp = max(0, self.hp - amount)
        return self.hp
    
    def heal(self, amount: int) -> int:
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp
    
    def is_destroyed(self) -> bool:
        return self.hp <= 0
    
    # ===== СЛОТЫ =====
    
    def get_slot_info(self) -> tuple[str, int] | None:
        if self.slot_type and self.slot_count > 0:
            return (self.slot_type, self.slot_count)
        return None
    
    def get_slot_ids(self) -> list[str]:
        return list(self.slots.keys())
    
    def equip_to_slot(self, slot_id: str, item) -> bool:
        if slot_id in self.slots:
            self.slots[slot_id] = item
            return True
        return False
    
    def unequip_from_slot(self, slot_id: str):
        if slot_id in self.slots:
            item = self.slots[slot_id]
            self.slots[slot_id] = None
            return item
        return None
    
    def get_equipped_items(self) -> list:
        return [item for item in self.slots.values() if item is not None]
    
    # ===== КОНТЕКСТНОЕ МЕНЮ =====
    
    def get_actions(self, player, slot_data, slot_type):
        """Возвращает список действий для контекстного меню."""
        actions = []
        
        # Действие "Экипировать" — только если конечность в инвентаре
        if slot_type == "inventory":
            # Определяем слот для этой конечности
            target_slot = self._get_equip_slot()
            if target_slot:
                actions.append({
                    "name": f"Экипировать ({self.name})",
                    "action": lambda: self._equip_from_inventory(player)
                })
        
        # Действие "Снять" — только если конечность экипирована
        if slot_type == "equipment":
            actions.append({
                "name": f"Снять ({self.name})",
                "action": lambda: self._unequip_to_inventory(player, slot_data)
            })
        
        # Выбросить — всегда
        actions.append({
            "name": "Выбросить",
            "action": lambda: player.drop_item_by_reference(self)
        })
        
        return actions
    
    def _get_equip_slot(self) -> str | None:
        """Возвращает имя слота экипировки для этой конечности."""
        limb_to_slot = {
            "head": "limbs_head",
            "left_arm": "limbs_hand_left",
            "right_arm": "limbs_hand_right",
            "left_leg": "limbs_leg_left",
            "right_leg": "limbs_leg_right",
        }
        return limb_to_slot.get(self.limb_type)
    
    def _equip_from_inventory(self, player):
        """Экипирует конечность из инвентаря с полной заменой."""
        target_slot = self._get_equip_slot()
        if not target_slot:
            return
        
        # Снимаем старую конечность, если есть
        old_limb = player.equipment.slots.get(target_slot)
        if old_limb and old_limb is not self:
            # Снимаем оружие из всех слотов старой конечности
            for weapon_slot in list(player.equipment.slots.keys()):
                if weapon_slot.startswith("weapon_"):
                    weapon = player.equipment.slots.get(weapon_slot)
                    if weapon:
                        player.inventory.add_item(weapon, 1)
                        player.equipment.slots[weapon_slot] = None
            
            player.equipment.slots[target_slot] = None
            player.limb_health_system.remove_limb(old_limb.limb_id)
            player.inventory.add_item(old_limb, 1)
        
        # Экипируем новую
        player.equipment.slots[target_slot] = self
        player.limb_health_system.add_limb(self)
        
        # Обновляем слоты оружия (могло измениться количество)
        player.equipment.update_slots_from_limbs(player.limb_health_system)
        
        # Удаляем новую из инвентаря
        for i, slot in enumerate(player.inventory.slots):
            if slot and slot.item is self:
                player.inventory.slots[i] = None
                break

    def _unequip_to_inventory(self, player, slot_name):
        """Снимает конечность и кладёт в инвентарь."""
        if player.inventory.has_free_space_for_item(self):
            # Снимаем оружие из слотов конечности
            for weapon_slot in list(player.equipment.slots.keys()):
                if weapon_slot.startswith("weapon_"):
                    weapon = player.equipment.slots.get(weapon_slot)
                    if weapon:
                        player.inventory.add_item(weapon, 1)
                        player.equipment.slots[weapon_slot] = None
            
            player.equipment.slots[slot_name] = None
            player.limb_health_system.remove_limb(self.limb_id)
            player.equipment.update_slots_from_limbs(player.limb_health_system)
            player.inventory.add_item(self, 1)
    
    # ===== СЕРИАЛИЗАЦИЯ =====
    
    def to_dict(self) -> dict:
        return {
            "limb_id": self.limb_id,
            "name": self.name,
            "limb_type": self.limb_type,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "slot_type": self.slot_type,
            "slot_count": self.slot_count
        }