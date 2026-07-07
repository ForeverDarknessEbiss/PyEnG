# systems/equipment_system.py

class EquipmentSystem:
    def __init__(self, player):
        self.player = player
        self.slots = {
            "weapon_primary": None,
            "weapon_secondary": None,
            "weapon_melee": None,
            "armor": None,
            "art_1": None,
            "art_2": None,
            "art_3": None,
            "art_4": None,
            "implant_head_1": None,
            "implant_head_2": None,
            "implant_leg_1": None,
            "implant_leg_2": None,
            "implant_spine_1": None,
            "implant_spine_2": None,
            "implant_spine_3": None,
            "implant_hand_1": None,
            "implant_hand_2": None,
            "limbs_head": None,
            "limbs_leg_right": None,
            "limbs_leg_left": None,
            "limbs_hand_right": None,
            "limbs_hand_left": None

        }
        self.stats = {}  # кэш суммарных бонусов
    
    SLOT_META = {
        "weapon_primary": {"layer": "weapons", "type": "weapon"},
        "weapon_secondary": {"layer": "weapons", "type": "weapon"},
        "weapon_melee": {"layer": "weapons", "type": "weapon"},

        "armor": {"layer": "armor", "type": "armor"},

        "art_1": {"layer": "artifacts", "type": "artifact"},
        "art_2": {"layer": "artifacts", "type": "artifact"},
        "art_3": {"layer": "artifacts", "type": "artifact"},
        "art_4": {"layer": "artifacts", "type": "artifact"},

        "implant_head_1": {"layer": "implants", "type": "implant"},
        "implant_head_2": {"layer": "implants", "type": "implant"},

        "implant_leg_1": {"layer": "implants", "type": "implant"},
        "implant_leg_2": {"layer": "implants", "type": "implant"},

        "implant_spine_1": {"layer": "implants", "type": "implant"},
        "implant_spine_2": {"layer": "implants", "type": "implant"},
        "implant_spine_3": {"layer": "implants", "type": "implant"},

        "implant_hand_1": {"layer": "implants", "type": "implant"},
        "implant_hand_2": {"layer": "implants", "type": "implant"},
        
        "limbs_head":{"layer": "limbs", "body": "limbs"},
        "limbs_leg_right":{"layer": "limbs","body": "limbs"},
        "limbs_leg_left":{"layer": "limbs","body": "limbs"},
        "limbs_hand_right":{"layer": "limbs","body": "limbs"},
        "limbs_hand_left":{"layer": "limbs","body": "limbs"},
    }
    
    def unequip(self, slot):
        """Снять предмет из слота (вернуть в инвентарь)"""
        if slot not in self.slots or not self.slots[slot]:
            return None

        item = self.slots[slot]
        print(f"\n[EQUIP] ❌ Снимаем: {item.name} из слота '{slot}'")
        self.slots[slot] = None

        # 🆕 Деактивация механик импланта
        if item and hasattr(item, "mechanics") and hasattr(self.player, "implant_manager"):
            self.player.implant_manager.on_unequip(item.uid)

        self._recalc_stats()
        return item

    def equip(self, item, slot):
        """Надеть предмет в слот"""
        print(f"\n[EQUIP] ✅ Надеваем: {item.name} в слот '{slot}'")
        
        if slot not in self.slots:
            print(f"[EQUIP] ❌ Неизвестный слот: {slot}")
            return False

        # снимаем текущий предмет (если есть)
        if self.slots[slot]:
            old_item = self.slots[slot]
            print(f"[EQUIP] 🔄 Заменяем: {old_item.name} на {item.name}")
            self.unequip(slot)

        self.slots[slot] = item
        print(f"[EQUIP] 📍 Слот '{slot}' обновлен")

        # 🆕 Активация механик импланта
        if hasattr(item, "mechanics") and hasattr(self.player, "implant_manager"):
            self.player.implant_manager.on_equip(item, item.uid)        
        
        self._recalc_stats()
        return True

    def get_weapon(self):
        
        """Удобный доступ к оружию"""
    
        return self.slots.get("weapon_primary")
    
    def get_slots_by_layer(self, layer):
        from systems.equipment_system import SLOT_METAS
        return {slot: self.slots[slot] for slot in SLOT_METAS[layer]}

    def _recalc_stats(self):
        """Собирает ВСЕ сырые статы со всей экипировки"""
        raw_stats = {}
        
        for slot, item in self.slots.items():
            if not item:
                continue
            
            # Артефакты и импланты (stats)
            if hasattr(item, "stats"):
                for stat, value in item.stats.items():
                    raw_stats[stat] = raw_stats.get(stat, 0) + value
                print(f"  {slot}: {item.name} - stats={getattr(item, 'stats', 'нет')}")
            # Броня (resistances)
            if hasattr(item, "resistances"):
                for resist_type, value in item.resistances.items():
                    stat_name = f"{resist_type}_defense"
                    raw_stats[stat_name] = raw_stats.get(stat_name, 0) + value
            
            # Артефакты (static_bonuses)
            if hasattr(item, "static_bonuses"):
                for resist_type, value in item.static_bonuses.items():
                    stat_name = f"{resist_type}_defense"
                    raw_stats[stat_name] = raw_stats.get(stat_name, 0) + value
            
            # Процентные модификаторы артефактов
            if hasattr(item, "percent_modifiers"):
                for resist_type, percent in item.percent_modifiers.items():
                    key = f"{resist_type}_percent"
                    raw_stats[key] = raw_stats.get(key, 0) + percent
            
            
        
        # Отправляем сырые данные в defense для финального расчета
        if hasattr(self.player, "defense"):
            self.player.defense.recalculate(raw_stats)
