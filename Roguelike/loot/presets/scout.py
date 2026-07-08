from loot.item_database import *
from loot.ammo_database import *
from loot.weapons_database import *

SCOUT_LOOT = {
    "items": [
        # лёгкие детали
        GEAR_SMALL,
        BOLTS,
        SPRING,
        WIRE,
        COMPONENTS,
        
        # патроны
        PISTOL_AMMO,
        ENERGY_CELL,
        
        # оружие
        ("weapon", "pistol"),
        ("weapon", "laser_pistol"),
        ("weapon", "smg"),
        ("armor", "base_armor"),
        ("artifact","crystal_shield"),
    ],
    "rare": [
        # редкие детали
        CARBON_PLATE,
        TITANIUM_ROD,
        NANOTUBE,
        
        # редкое оружие
        ("weapon", "magnum"),
        ("weapon", "crowbar"),
    ]
}