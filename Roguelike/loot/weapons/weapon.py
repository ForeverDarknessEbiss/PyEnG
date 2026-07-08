import uuid
class Weapon:
    def __init__(
        self,
        name="Unknown",
        damage=None,              # dict: {"physical": 10, "fire": 5}
        attack_speed=1.0,
        range=50,
        area=None,               # для мили (ширина/высота)
        weapon_type="melee",     # melee / ranged
        spread=0,                # для стрельбы
        magazine_size=0,
        ammo_type=None,
        description="Нет описания",
        stackable=False,
        is_unique=False,
        color=(150, 150, 150) 
    ):
        self.name = name
        self.uid = str(uuid.uuid4())
        # 💥 ВАЖНО: если не передали — создаём пустой словарь
        self.damage = damage if damage else {}

        self.attack_speed = attack_speed
        self.range = range
        self.area = area

        self.weapon_type = weapon_type
        self.spread = spread

        self.magazine_size = magazine_size
        self.current_ammo = magazine_size
        self.ammo_type = ammo_type

        self.area = area
        self.description = description
        self.stackable = stackable  # ← для инвентаря
        self.is_unique = is_unique 
        self.color = color
    def attack(self, player, combat_system):
        combat_system.handle_attack(player, self)

    def get_actions(self, player, slot_data=None, slot_type="inventory"):
            actions = []

            # 🎯 Доступные слоты
            if self.weapon_type == "melee":
                self.available_slots = ["weapon_melee"]
            elif self.weapon_type == "ranged":
                self.available_slots = ["weapon_primary", "weapon_secondary"]
            else:
                self.available_slots = []
                
            # Проверяем, надет ли предмет (по uid)
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