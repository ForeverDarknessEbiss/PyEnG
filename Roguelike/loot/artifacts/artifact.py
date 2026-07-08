# loot/artifacts/artifact.py
import uuid

class Artifact:
    """Базовый класс артефакта с статичными и процентными бонусами защиты"""
    
    def __init__(
        self,
        name="Unknown Artifact",
        description="Нет описания",
        static_bonuses=None,           # {"physical": 5, "fire": -2, ...}
        percent_modifiers=None,        # {"physical": -4, "electric": +8, ...} в процентах
        color=(128, 0, 128),
        stackable=False,
        is_unique=False,
        rarity="common",         # common, uncommon, rare, epic, legendary
        slot=None               
    ):
        self.name = name
        self.description = description
        self.uid = str(uuid.uuid4())  # Уникальный ID для отслеживания конкретного экземпляра артефакта
        # Статичные бонусы/штрафы к защите
        self.static_bonuses = static_bonuses if static_bonuses else {}
        
        # Процентные модификаторы защиты (в процентах, например +8 или -4)
        self.percent_modifiers = percent_modifiers if percent_modifiers else {}
        
        self.color = color
        self.stackable = stackable
        self.is_unique = is_unique
        self.rarity = rarity
        self.artifact_type = "artifact"
        self.type = "artifact"
                # 🎯 Задаем слот
        if slot:
            self.slot = slot
        else:
            # По умолчанию ищем первый свободный слот артефакта
            self.slot = "art_1"  


    def get_actions(self, player, slot_data=None, slot_type="inventory"):
        actions = []

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
                # Показываем ВСЕ слоты артефактов
                artifact_slots = ["art_1", "art_2", "art_3", "art_4"]
                
                for slot in artifact_slots:
                    current_item = player.equipment.slots.get(slot)
                    if current_item:
                        action_name = f"Заменить в {slot} (сейчас {current_item.name})"
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
    
    def get_all_bonuses(self):
        """Вернуть все бонусы и модификаторы"""
        return {
            "static_bonuses": self.static_bonuses.copy(),
            "percent_modifiers": self.percent_modifiers.copy()
        }
    
    def __repr__(self):
        return f"Artifact({self.name}, статич={self.static_bonuses}, проц={self.percent_modifiers})"
