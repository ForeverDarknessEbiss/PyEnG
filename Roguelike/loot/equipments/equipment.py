import uuid

class Equipment:
    def __init__(
        self,
        name="Unknown",
        resistances = None,
        equipment_type = "armor",                    
        description="Нет описания",
        stackable=False,
        is_unique=False,
        color=(164, 125, 65),
        physical = None,
        chemical = None,
        electric = None,
        fire = None
    ):
        self.name = name
        self.uid = str(uuid.uuid4())
        # 💥 ВАЖНО: если не передали — создаём пустой словарь
        self.resistances = resistances if resistances else {}

        self.physical = physical
        self.chemical = chemical
        self.electric = electric
        self.fire = fire

        self.equipment_type = equipment_type
        self.description = description
        self.stackable = stackable  # ← для инвентаря
        self.is_unique = is_unique 
        self.color = color
        self.slot = "armor"  # 🎯 Слот для экипировки (по умолчанию armor)

    @property
    def type(self):
        """Свойство для совместимости с проверкой типа в SLOT_META"""
        return self.equipment_type

    def get_actions(self, player, slot_data=None, slot_type="inventory"):
        actions = []

        # Проверяем, надет ли предмет
        equipped_slot = None
        for slot, item in player.equipment.slots.items():
            if item and hasattr(item, 'uid') and item.uid == self.uid:
                equipped_slot = slot
                break

        if slot_type == "inventory":
            # Предмет в инвентаре
            if equipped_slot:
                # Если уже надет (редкий случай)
                actions.append({
                    "name": "Снять",
                    "action": lambda: player.inventory.unequip_item(self, player)
                })
            else:
                # 🎯 САМ ПРЕДМЕТ ЗНАЕТ, В КАКОЙ СЛОТ ОН МОЖЕТ БЫТЬ ЭКИПИРОВАН
                target_slot = self.slot if hasattr(self, 'slot') else None
                
                # Если нет слота, определяем по типу
                if not target_slot:
                    if self.equipment_type == "armor":
                        target_slot = "armor"
                    elif self.equipment_type == "implant":
                        # Можно добавить логику для имплантов
                        target_slot = None
                        print(f"[WARNING] Не определен слот для {self.name}")
                
                if target_slot:
                    actions.append({
                        "name": f"Экипировать",
                        "action": lambda s=target_slot: player.inventory.equip_from_slot(slot_data, player, force_slot=s)
                    })
            
            actions.append({
                "name": "Выбросить",
                "action": lambda: player.drop_item_by_reference(self)
            })
            
        elif slot_type == "equipment":
            # Предмет уже надет
            actions.append({
                "name": "Снять",
                "action": lambda: player.inventory.unequip_item(self, player)
            })
            actions.append({
                "name": "Выбросить",
                "action": lambda: player.drop_equipped_item(self)
            })

        return actions

    def _equip_from_inventory(self, player, slot_name):
        """Вспомогательный метод для экипировки из инвентаря"""
        # Ищем предмет в инвентаре
        for i, inv_slot in enumerate(player.inventory.slots):
            if inv_slot and inv_slot.item == self:
                # Используем equip_from_slot
                player.inventory.equip_from_slot(i, player, force_slot=slot_name)
                break