# loot/limbs_database.py

# База данных конечностей (Python-словарь)
# Единственный источник истины для характеристик конечностей

LIMBS_DATA = {
    # ===== ГОЛОВА =====
    1: {
        "id": 1,
        "name": "Голова (базовая)",
        "limb_type": "head",
        "hp": 20,
        "slot_type": None,
        "slot_count": 0
    },
    
    # ===== ЛЕВАЯ РУКА =====
    2: {
        "id": 2,
        "name": "Левая рука (базовая)",
        "limb_type": "left_arm",
        "hp": 15,
        "slot_type": "weapon_left",
        "slot_count": 1
    },
    3: {
        "id": 3,
        "name": "Левая рука (продвинутая)",
        "limb_type": "left_arm",
        "hp": 25,
        "slot_type": "weapon_left",
        "slot_count": 2
    },
    4: {
        "id": 4,
        "name": "Левая рука (элитная)",
        "limb_type": "left_arm",
        "hp": 35,
        "slot_type": "weapon_left",
        "slot_count": 3
    },
    
    # ===== ПРАВАЯ РУКА =====
    5: {
        "id": 5,
        "name": "Правая рука (базовая)",
        "limb_type": "right_arm",
        "hp": 15,
        "slot_type": "weapon_right",
        "slot_count": 1
    },
    6: {
        "id": 6,
        "name": "Правая рука (продвинутая)",
        "limb_type": "right_arm",
        "hp": 25,
        "slot_type": "weapon_right",
        "slot_count": 2
    },
    7: {
        "id": 7,
        "name": "Правая рука (элитная)",
        "limb_type": "right_arm",
        "hp": 35,
        "slot_type": "weapon_right",
        "slot_count": 3
    },
    
    # ===== ЛЕВАЯ НОГА =====
    8: {
        "id": 8,
        "name": "Левая нога (базовая)",
        "limb_type": "left_leg",
        "hp": 20,
        "slot_type": None,
        "slot_count": 0
    },
    
    # ===== ПРАВАЯ НОГА =====
    9: {
        "id": 9,
        "name": "Правая нога (базовая)",
        "limb_type": "right_leg",
        "hp": 20,
        "slot_type": None,
        "slot_count": 0
    },

    # ===== РЕДКИЕ КОНЕЧНОСТИ (заглушки) =====
    10: {
        "id": 10,
        "name": "Левая рука (гидравлическая)",
        "limb_type": "left_arm",
        "hp": 30,
        "slot_type": "weapon_left",
        "slot_count": 2
    },
    11: {
        "id": 11,
        "name": "Правая рука (боевая)",
        "limb_type": "right_arm",
        "hp": 30,
        "slot_type": "weapon_right",
        "slot_count": 2
    },
    12: {
        "id": 12,
        "name": "Левая нога (скоростная)",
        "limb_type": "left_leg",
        "hp": 25,
        "slot_type": None,
        "slot_count": 2
    },
    13: {
        "id": 13,
        "name": "Правая нога (стабилизатор)",
        "limb_type": "right_leg",
        "hp": 25,
        "slot_type": None,
        "slot_count": 2
        }

    }

# Словарь для поиска по строковому ключу
LIMBS_BY_NAME = {
    "basic_head": 1,
    "basic_hand_left": 2,
    "advanced_hand_left": 3,
    "elite_hand_left": 4,
    "basic_hand_right": 5,
    "advanced_hand_right": 6,
    "elite_hand_right": 7,
    "basic_leg_left": 8,
    "basic_leg_right": 9,
    "hydraulic_hand_left": 10,
    "combat_hand_right": 11,
    "speed_leg_left": 12,
    "stabilizer_leg_right": 13,
}


class LimbsDatabase:
    """Обёртка над словарём конечностей (замена SQLite)"""

    def fetch_by_name(self, name: str):
        """Поиск конечности по строковому имени. Возвращает кортеж или None."""
        limb_id = LIMBS_BY_NAME.get(name)
        if limb_id:
            return self.fetch_by_id(limb_id)
        return None

    def __init__(self):
        self.data = LIMBS_DATA
    
    def fetch_by_id(self, limb_id: int):
        """Возвращает кортеж (id, name, limb_type, hp, slot_type, slot_count) или None"""
        limb = self.data.get(limb_id)
        if limb:
            return (
                limb["id"],
                limb["name"],
                limb["limb_type"],
                limb["hp"],
                limb["slot_type"],
                limb["slot_count"],
            )
        return None
    
    def fetch_all(self):
        """Возвращает список всех конечностей"""
        return [
            (limb["id"], limb["name"], limb["limb_type"], limb["hp"], limb["slot_type"], limb["slot_count"])
            for limb in self.data.values()
        ]
    
    def fetch_by_type(self, limb_type: str):
        """Возвращает конечности по типу"""
        return [
            (limb["id"], limb["name"], limb["limb_type"], limb["hp"], limb["slot_type"], limb["slot_count"])
            for limb in self.data.values()
            if limb["limb_type"] == limb_type
        ]
    
    def close(self):
        pass  # Для совместимости