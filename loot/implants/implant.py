
# loot/implants/implant.py
import uuid

class Implant:
    def __init__(
        self,
        name="Unknown Implant",
        description="Нет описания",
        implant_type="head",  # head, spine, hand, leg
        stats=None,  # {"damage_bonus": 5, "health": 20, ...}
        color=(100, 200, 100),
        stackable=False,
        is_unique=True,
        rarity="common",
        mechanics=None,      
        cooldown=0,          
        energy_cost=0,
        charge_time=0,
        charge_drain=0,
        min_energy=20,
        active_time=0,
        minimap_size=200,
        minimap_x=None,
        minimap_y=None,
        radar_radius=300
    ):
        self.name = name
        self.description = description
        self.uid = str(uuid.uuid4())
        self.implant_type = implant_type
        self.stats = stats if stats else {}
        self.color = color
        self.stackable = stackable
        self.is_unique = is_unique
        self.rarity = rarity
        self.type = "implant"
        # 🆕 Параметры для активных механик
        self.mechanics = mechanics if mechanics else []
        self.cooldown = cooldown
        self.energy_cost = energy_cost
        # 🆕 Параметры для заряжаемых имплантов
        self.charge_time = charge_time
        self.charge_drain = charge_drain
        self.min_energy = min_energy
        self.active_time = active_time
        # 🆕 Параметры для радара
        self.minimap_size = minimap_size
        self.minimap_x = minimap_x
        self.minimap_y = minimap_y
        self.radar_radius = radar_radius
                
        # 🎯 Определяем доступные слоты в зависимости от типа
        self.available_slots = self._get_available_slots()
    
    def _get_available_slots(self):
        """Возвращает список слотов, подходящих для этого импланта"""
        if self.implant_type == "head":
            return ["implant_head_1", "implant_head_2"]
        elif self.implant_type == "spine":
            return ["implant_spine_1", "implant_spine_2", "implant_spine_3"]
        elif self.implant_type == "hand":
            return ["implant_hand_1", "implant_hand_2"]
        elif self.implant_type == "leg":
            return ["implant_leg_1", "implant_leg_2"]
        else:
            return []
    
    def get_actions(self, player, slot_data=None, slot_type="inventory"):
        actions = []
        
        # Проверяем, надет ли уже этот имплант
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
                # Показываем только подходящие слоты для этого импланта
                for slot in self.available_slots:
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
    
    def __repr__(self):
        return f"Implant({self.name}, type={self.implant_type}, stats={self.stats})"