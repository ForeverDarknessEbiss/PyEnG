# loot/presets/aggressive_preset.py
from loot.item_database import *
from loot.limbs_database import *

AGGRESSIVE_LOOT ={"items": [
        # ... существующие импланты ...
        
        # конечности
        ("limb", "basic_hand_left"),
        ("limb", "basic_hand_right"),
        ("limb", "basic_leg_left"),
        ("limb", "basic_leg_right"),
    ],
    "rare": [
        # ... существующие редкие ...
        
        # редкие конечности
        ("limb", "hydraulic_hand_left"),
        ("limb", "combat_hand_right"),
        ("limb", "speed_leg_left"),
        ("limb", "stabilizer_leg_right"),

        # оружие
        ("weapon", "pistol"),
        ("weapon", "magnum"),
        ("weapon", "sniper_rifle"),
        ("weapon", "machinegun"),
    ]
}