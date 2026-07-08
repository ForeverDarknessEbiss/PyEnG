# loot/implants_database.py

IMPLANTS = {
    # ========== ИМПЛАНТЫ ГОЛОВЫ ==========
    "targeting_computer": {
        "name": "Targeting Computer",
        "description": "Нейросеть для обработки баллистических данных",
        "implant_type": "head",
        "stats": {
            "accuracy_bonus": 15,
            "range_bonus": 10,
            "constant_energy_drain": 5
        },
        "mechanics": [],
        "cooldown": 0,
        "energy_cost": 0,
        "charge_time": 0,
        "charge_drain": 0,
        "min_energy": 20,
        "active_time": 0,
        "color": (100, 150, 255),
        "rarity": "uncommon"
    },
    
    "neural_processor": {
        "name": "Neural Processor",
        "description": "Ускоряет обработку визуальной информации",
        "implant_type": "head",
        "stats": {
            "accuracy_bonus": 20,
            "range_bonus": 5,
            "energy_consumption": -5
        },
        "mechanics": [],
        "cooldown": 0,
        "energy_cost": 0,
        "charge_time": 0,
        "charge_drain": 0,
        "min_energy": 20,
        "active_time": 0,
        "color": (150, 100, 255),
        "rarity": "rare"
    },
    
    "optic_camouflage": {
        "name": "Optic Camouflage",
        "description": "Искажает свет вокруг головы",
        "implant_type": "head",
        "stats": {
            "stealth_bonus": 25,
            "accuracy_bonus": -5
        },
        "mechanics": [],
        "cooldown": 0,
        "energy_cost": 0,
        "charge_time": 0,
        "charge_drain": 0,
        "min_energy": 20,
        "active_time": 0,
        "color": (100, 200, 200),
        "rarity": "rare"
    },
    "radar_implant": {
        "name": "Лидар",
        "description": "Показывает миникарту в углу экрана",
        "implant_type": "head",
        "stats": {"constant_energy_drain": 1},
        "mechanics": ["radar"],
        "minimap_size": 200,
        "minimap_x": None,  # будет вычислен в коде
        "minimap_y": None,  # будет вычислен в коде
        "radar_radius": 300,
        "color": (100, 200, 200),
        "rarity": "uncommon"
    },
    
    # ========== ИМПЛАНТЫ РУК ==========
    "hydraulic_arm": {
        "name": "Hydraulic Arm",
        "description": "Увеличивает физическую силу",
        "implant_type": "hand",
        "stats": {
            "melee_damage": 20,
            "melee_speed": 10,
            "carry_weight": 30,
            "accuracy_bonus": -5
        },
        "mechanics": [],
        "cooldown": 0,
        "energy_cost": 0,
        "charge_time": 0,
        "charge_drain": 0,
        "min_energy": 20,
        "active_time": 0,
        "color": (150, 100, 100),
        "rarity": "common"
    },
    
    "precision_servos": {
        "name": "Precision Servos",
        "description": "Микро-сервоприводы для точных движений",
        "implant_type": "hand",
        "stats": {
            "accuracy_bonus": 25,
            "melee_speed": 5,
            "melee_damage": -5
        },
        "mechanics": [],
        "cooldown": 0,
        "energy_cost": 0,
        "charge_time": 0,
        "charge_drain": 0,
        "min_energy": 20,
        "active_time": 0,
        "color": (100, 200, 150),
        "rarity": "uncommon"
    },
    
    "energy_blades": {
        "name": "Энергетические клинки",
        "description": "Рывок наносит урон и кровотечение",
        "implant_type": "hand",
        "stats": {
            "melee_damage": 15,
            "energy_consumption": 10
        },
        "mechanics": ["energy_blades"],
        "cooldown": 0.5,
        "energy_cost": 2,
        "color": (100, 200, 255),
        "rarity": "rare"
    },
        
    "recoil_dampeners": {
        "name": "Recoil Dampeners",
        "description": "Гасит отдачу стрелкового оружия",
        "implant_type": "hand",
        "stats": {
            "accuracy_bonus": 15,
            "recoil_reduction": 30,
            "melee_speed": -5
        },
        "mechanics": [],
        "cooldown": 0,
        "energy_cost": 0,
        "charge_time": 0,
        "charge_drain": 0,
        "min_energy": 20,
        "active_time": 0,
        "color": (200, 150, 100),
        "rarity": "uncommon"
    },
    
    # ========== ИМПЛАНТЫ НОГ ==========
    "speed_enhancer": {
        "name": "Speed Enhancer",
        "description": "Усиливает мышцы ног для быстрого бега",
        "implant_type": "leg",
        "stats": {
            "movement_speed": 25,
            "energy_consumption": 10,
            "carry_weight": -10
        },
        "mechanics": [],
        "cooldown": 0,
        "energy_cost": 0,
        "charge_time": 0,
        "charge_drain": 0,
        "min_energy": 20,
        "active_time": 0,
        "color": (100, 255, 100),
        "rarity": "uncommon"
    },
    
    "dash_implant": {
        "name": "Реактивный ускоритель",
        "description": "Мгновенный рывок в направлении движения",
        "implant_type": "leg",
        "stats": {
            "energy_consumption": 10,
            "movement_speed": 5
        },
        "mechanics": ["dash"],
        "cooldown": 3.0,
        "energy_cost": 20,
        "charge_time": 0,
        "charge_drain": 0,
        "min_energy": 20,
        "active_time": 0,
        "color": (100, 200, 100),
        "rarity": "rare"
    },
    
    "stabilizers": {
        "name": "Stabilizers",
        "description": "Гироскопы для устойчивости",
        "implant_type": "leg",
        "stats": {
            "accuracy_bonus": 10,
            "movement_speed": -5,
            "energy_consumption": -5
        },
        "mechanics": [],
        "cooldown": 0,
        "energy_cost": 0,
        "charge_time": 0,
        "charge_drain": 0,
        "min_energy": 20,
        "active_time": 0,
        "color": (100, 200, 150),
        "rarity": "common"
    },
    
    "spring_legs": {
        "name": "Spring Legs",
        "description": "Пружинные механизмы для прыжков",
        "implant_type": "leg",
        "stats": {
            "jump_height": 40,
            "movement_speed": 10,
            "carry_weight": -15,
            "energy_consumption": 5
        },
        "mechanics": [],
        "cooldown": 0,
        "energy_cost": 0,
        "charge_time": 0,
        "charge_drain": 0,
        "min_energy": 20,
        "active_time": 0,
        "color": (200, 200, 100),
        "rarity": "uncommon"
    },
    
    "power_treads": {
        "name": "Power Treads",
        "description": "Мощные приводы для переноски грузов",
        "implant_type": "leg",
        "stats": {
            "carry_weight": 50,
            "movement_speed": -10,
            "energy_consumption": 15
        },
        "mechanics": [],
        "cooldown": 0,
        "energy_cost": 0,
        "charge_time": 0,
        "charge_drain": 0,
        "min_energy": 20,
        "active_time": 0,
        "color": (150, 150, 100),
        "rarity": "rare"
    },
    
    # ========== ИМПЛАНТЫ ТЕЛА (ПОЗВОНОЧНИК) ==========
    "reinforced_spine": {
        "name": "Reinforced Spine",
        "description": "Укрепленный позвоночник",
        "implant_type": "spine",
        "stats": {
            "physical_defense": 15,
            "carry_weight": 20,
            "energy_consumption": -5
        },
        "mechanics": [],
        "cooldown": 0,
        "energy_cost": 0,
        "charge_time": 0,
        "charge_drain": 0,
        "min_energy": 20,
        "active_time": 0,
        "color": (200, 150, 100),
        "rarity": "common"
    },
    
    "emp_implant": {
        "name": "ЭМИ-импульс",
        "description": "Электромагнитный импульс, отключающий механических врагов",
        "implant_type": "spine",
        "stats": {},
        "mechanics": ["emp"],
        "cooldown": 10.0,
        "energy_cost": 0,
        "charge_time": 5.0,
        "charge_drain": 10,
        "min_energy": 20,
        "active_time": 1.0,
        "color": (100, 200, 255),
        "rarity": "rare"
    },
    
    "reflex_booster": {
        "name": "Reflex Booster",
        "description": "Ускоряет нервные импульсы",
        "implant_type": "spine",
        "stats": {
            "attack_speed": 15,
            "movement_speed": 5,
            "energy_consumption": 10
        },
        "mechanics": [],
        "cooldown": 0,
        "energy_cost": 0,
        "charge_time": 0,
        "charge_drain": 0,
        "min_energy": 20,
        "active_time": 0,
        "color": (100, 200, 200),
        "rarity": "uncommon"
    },
    
    "energy_core": {
        "name": "Energy Core",
        "description": "Мини-реактор в позвоночнике",
        "implant_type": "spine",
        "stats": {
            "max_energy": 50,
            "energy_regen": 5,
            "physical_defense": -5,
            "fire_defense": 10
        },
        "mechanics": [],
        "cooldown": 0,
        "energy_cost": 0,
        "charge_time": 0,
        "charge_drain": 0,
        "min_energy": 20,
        "active_time": 0,
        "color": (255, 150, 50),
        "rarity": "rare"
    },
    
    "cooling_system": {
        "name": "Cooling System",
        "description": "Система охлаждения имплантов",
        "implant_type": "spine",
        "stats": {
            "energy_consumption": -15,
            "fire_defense": 15,
            "movement_speed": -5
        },
        "mechanics": [],
        "cooldown": 0,
        "energy_cost": 0,
        "charge_time": 0,
        "charge_drain": 0,
        "min_energy": 20,
        "active_time": 0,
        "color": (100, 200, 255),
        "rarity": "uncommon"
    },
    
    "adrenal_booster": {
        "name": "Adrenal Booster",
        "description": "Стимулирует выработку адреналина",
        "implant_type": "spine",
        "stats": {
            "damage_bonus": 15,
            "attack_speed": 10,
            "energy_consumption": 20,
            "physical_defense": -8
        },
        "mechanics": [],
        "cooldown": 0,
        "energy_cost": 0,
        "charge_time": 0,
        "charge_drain": 0,
        "min_energy": 20,
        "active_time": 0,
        "color": (255, 100, 150),
        "rarity": "rare"
    },
    
    "regenerator": {
        "name": "Regenerator",
        "description": "Медицинский нано-комплекс",
        "implant_type": "spine",
        "stats": {
            "health_regen": 2,
            "chemical_defense": 10,
            "energy_consumption": 10
        },
        "mechanics": [],
        "cooldown": 0,
        "energy_cost": 0,
        "charge_time": 0,
        "charge_drain": 0,
        "min_energy": 20,
        "active_time": 0,
        "color": (100, 255, 150),
        "rarity": "epic"
    }
}