# loot/limbs/limb.py
import uuid

class Limb:
    def __init__(
        self,
        name="Unknown Limb",
        description="Нет описания",
        limb_type="hand",  # head, leg_left, leg_right, hand_left, hand_right
        stats=None,  # {"movement_speed": 10, "carry_weight": 20, ...}
        color=(150, 100, 100),
        stackable=False,
        is_unique=True,
        rarity="common",
        health_bonus= 0
    ):
        self.name = name
        self.description = description
        self.uid = str(uuid.uuid4())
        self.limb_type = limb_type
        self.stats = stats if stats else {}
        self.color = color
        self.stackable = stackable
        self.is_unique = is_unique
        self.rarity = rarity
        self.type = "limb"
        self.health_bonus = health_bonus

        # 🎯 Определяем доступные слоты в зависимости от типа конечности
        self.available_slots = self._get_available_slots()
    
    def _get_available_slots(self):
        """Возвращает список слотов, подходящих для этой конечности"""
        slot_map = {
            "head": ["limbs_head"],
            "hand_left": ["limbs_hand_left"],
            "hand_right": ["limbs_hand_right"],
            "leg_left": ["limbs_leg_left"],
            "leg_right": ["limbs_leg_right"],
        }
        return slot_map.get(self.limb_type, [])
    
    def get_actions(self, player, slot_data=None, slot_type="inventory"):
        actions = []
        
        # Проверяем, надета ли уже эта конечность
        equipped_slot = None
        for slot, item in player.equipment.slots.items():
            if item and hasattr(item, 'uid') and item.uid == self.uid:
                equipped_slot = slot
                break
        
        if slot_type == "inventory":
            if equipped_slot:
                actions.append({
                    "name": "Снять",
                    "action": lambda: player.inventory.unequip_item(self, player)
                })
            else:
                # Показываем только подходящие слоты
                for slot in self.available_slots:
                    current_item = player.equipment.slots.get(slot)
                    if current_item:
                        action_name = f"Заменить {slot} (сейчас {current_item.name})"
                    else:
                        action_name = f"Экипировать в {slot}"
                    
                    actions.append({
                        "name": action_name,
                        "action": lambda s=slot: player.inventory.equip_from_slot(
                            slot_data, player, force_slot=s
                        )
                    })
            
            actions.append({
                "name": "Выбросить",
                "action": lambda: player.drop_item_by_reference(self)
            })
            
        elif slot_type == "equipment":
            actions.append({
                "name": "Снять",
                "action": lambda: player.inventory.unequip_item(self, player)
            })
            actions.append({
                "name": "Выбросить",
                "action": lambda: player.drop_equipped_item(self)
            })
        
        return actions
    
    def __repr__(self):
        return f"Limb({self.name}, type={self.limb_type}, stats={self.stats})"