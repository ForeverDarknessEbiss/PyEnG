# loot/presets/dogbot.py

from loot.item_database import *
from loot.ammo_database import *
from loot.weapons_database import *
from loot.implants_database import *

DOGBOT_LOOT = {
    "items": [
        # --- импланты головы ---
        ("implant", "targeting_computer"),
        ("implant", "neural_processor"),
        
        # --- импланты позвоночника ---
        ("implant", "reinforced_spine"),
        ("implant", "reflex_booster"),
        
        # --- импланты рук (лап) ---
        ("implant", "hydraulic_arm"),
        ("implant", "energy_blades"),
        
        # --- импланты ног ---
        ("implant", "speed_enhancer"),
        ("implant", "stabilizers"),
        
        # --- роботизированные детали (обычные предметы) ---

    ],

    "rare": [
        # --- редкие импланты ---
        ("implant", "targeting_computer"),
        ("implant", "energy_blades"),
        ("implant", "reflex_booster"),
        
        # --- редкие компоненты ---

    ]
}