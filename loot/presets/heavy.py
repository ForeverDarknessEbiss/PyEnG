from loot.item_database import *
from loot.ammo_database import *
from loot.weapons_database import *

HEAVY_LOOT = {
    "items": [
        # тяжёлые детали
        GEAR_LARGE,
        MOTOR_HEAVY,
        HYDRAULIC_CYLINDER,
        SCRAP_METAL,
        COMPONENTS,
        
        # патроны
        HEAVY_AMMO,
        SHOTGUN_SHELL,
        
        # оружие
        ("weapon", "shotgun"),
        ("weapon", "machinegun"),
        ("armor", "base_armor"),
        ("artifact","crystal_shield"),
    ],
    "rare": [
        # редкие материалы
        CARBON_PLATE,
        TITANIUM_ROD,
        NANOTUBE,
        PORTABLE_REACTOR,
        
        # редкие патроны
        MAGNUM_AMMO,
        ENERGY_CELL,
        
        # редкое оружие
        ("weapon", "magnum"),
        ("weapon", "sniper_rifle"),
    ]
}