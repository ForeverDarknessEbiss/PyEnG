from .equipment import Equipment
from loot.equipment_database import ARMORS


def create_equipments(armor_id):
    data = ARMORS.get(armor_id)
    
    if not data:
        raise ValueError(f"armor '{armor_id}'not found ")
    
    return Equipment(**data)