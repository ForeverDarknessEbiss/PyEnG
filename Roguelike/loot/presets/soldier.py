from loot.item_database import *
from loot.ammo_database import *
from loot.weapons_database import *

SOLDIER_LOOT = {
    "items": [
        # военные детали
        COMPONENTS,
        ELECTRONICS,
        MECHANICAL_PART,
        SCRAP_METAL,
        WIRE,
        SERVO,
        MOTOR_SMALL,
        
        # патроны
        RIFLE_AMMO,
        PISTOL_AMMO,
        
        # оружие
        ("weapon", "rifle"),
        ("weapon", "assault_rifle"),
        ("armor", "base_armor"),
        ("artifact","crystal_shield"),
    ],
    "rare": [
        # редкие компоненты
        CARBON_PLATE,
        NANOTUBE,
        PORTABLE_REACTOR,
        
        # редкие патроны
        HEAVY_AMMO,
        ENERGY_CELL,
        
        # редкое оружие
        ("weapon", "machinegun"),
        ("weapon", "energy_rifle"),
        ("weapon", "sniper_rifle"),
    ]
}