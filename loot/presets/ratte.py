# loot/presets/ratte_preset.py

from loot.item_database import *
from loot.ammo_database import *
from loot.weapons_database import*

RATTE_LOOT = {
    "items": [
        # --- части тела крысы (логично) ---
        LEFT_LEG,
        RIGHT_LEG,
        SPINE,
        
        # --- органические компоненты ---
        LIVING_GEAR,
        NERVE_FIBER,
        BIO_GEL,
        ORGANIC_CIRCUIT,
        
        # --- мелкие детали ---
        GEAR_SMALL,
        BOLTS,
        SPRING,
        WIRE,
        SCRAP_METAL,
        
        # --- электроника ---
        CAPACITOR,
        TRANSISTOR,
        MICROCHIP,
        BROKEN_CPU,
        SSD,
        
        # --- расходники ---
        COMPONENTS,
        ELECTRONICS,
        MECHANICAL_PART,
        
        # --- патроны (редко, но может быть) ---
        PISTOL_AMMO,
    
        # оружие
        ("weapon", "pistol"),
        ("armor", "base_armor"),
        ("artifact","crystal_shield"),
    ],

    "rare": [
        # --- редкие материалы ---
        CARBON_PLATE,
        TITANIUM_ROD,
        NANOTUBE,
        
        # --- крупные детали (не стакаются) ---
        GEAR_LARGE,
        MOTOR_HEAVY,
        HYDRAULIC_CYLINDER,
        
        # --- ценные источники энергии ---
        PORTABLE_REACTOR,
        BATTERY_PACK,
        
        # --- редкие живые компоненты ---
        CORE_EYE,
    ]
}