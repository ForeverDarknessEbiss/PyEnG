from .weapon import Weapon
from loot.weapons_database import WEAPONS


def create_weapon(weapon_id):
    data = WEAPONS.get(weapon_id)
    
    if not data:
        raise ValueError(f"weapon '{weapon_id}'not found ")
    
    return Weapon(**data)