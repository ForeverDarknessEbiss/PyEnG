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

    def get_actions(self, player, slot_data, slot_type):
        """Возвращает список действий для контекстного меню (ПКМ)"""
        actions = []
        
        if slot_type == "inventory":
            # Собираем все реальные оружейные слоты
            weapon_slots = [sid for sid in player.equipment.slots if sid.startswith("weapon_")]
            
            if self.weapon_type == "melee":
                # melee — только melee-слоты
                melee_slots = [s for s in weapon_slots if "melee" in s]
                for slot_id in melee_slots:
                    actions.append({
                        "name": f"Экипировать ({slot_id})",
                        "action": lambda sid=slot_id: player.inventory.equip_from_slot(
                            player.inventory.slots.index(
                                next(s for s in player.inventory.slots if s and s.item == self)
                            ),
                            player,
                            sid
                        )
                    })
            else:
                # ВСЕ оружейные слоты (кроме melee)
                ranged_slots = [s for s in weapon_slots if "melee" not in s]
                for slot_id in ranged_slots:
                    actions.append({
                        "name": f"Экипировать ({slot_id})",
                        "action": lambda sid=slot_id: player.inventory.equip_from_slot(
                            player.inventory.slots.index(
                                next(s for s in player.inventory.slots if s and s.item == self)
                            ),
                            player,
                            sid
                        )
                    })
        
        elif slot_type == "equipment":
            actions.append({
                "name": "Снять",
                "action": lambda: player.inventory.unequip_item(self, player)
            })
        
        # Выбросить можно всегда
        actions.append({
            "name": "Выбросить",
            "action": lambda: player.drop_item_by_reference(self)
        })
        
        return actions