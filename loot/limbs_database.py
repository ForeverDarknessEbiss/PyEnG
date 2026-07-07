# loot/limbs_database.py
# "energy_regen": 1  # +1 к регенерации энергии
LIMBS = {
# ========== ГОЛОВА ==========

    "basic_head": {
        "name": "Basic Head",
        "description": "Стандартная голова. Ничего особенного.",
        "limb_type": "head",
        "stats": {
            "health_bonus": 15,
            "energy_regen": 1
        },
        "color": (200, 180, 150),
        "rarity": "common"
    },

    "enhanced_sensors": {
        "name": "Enhanced Sensors",
        "description": "Улучшенные сенсоры для лучшего обзора",
        "limb_type": "head",
        "stats": {
            "accuracy_bonus": 10,
            "range_bonus": 5,
            "health_bonus": 18,
            "energy_regen": 2
        },
        "color": (100, 150, 200),
        "rarity": "uncommon"
    },

    "combat_visor": {
        "name": "Combat Visor",
        "description": "Тактический визор с системой наведения",
        "limb_type": "head",
        "stats": {
            "accuracy_bonus": 20,
            "range_bonus": 10,
            "energy_consumption": 5,
            "health_bonus": 22,
            "energy_regen": 3
        },
        "color": (50, 100, 200),
        "rarity": "rare"
    },

    "reinforced_cranium": {
        "name": "Reinforced Cranium",
        "description": "Укрепленный череп для защиты мозга",
        "limb_type": "head",
        "stats": {
            "health_bonus": 35,
            "energy_regen": 1,
            "movement_speed": -3
        },
        "color": (150, 150, 180),
        "rarity": "uncommon"
    },

    "neural_interface": {
        "name": "Neural Interface",
        "description": "Прямое подключение к нейросети",
        "limb_type": "head",
        "stats": {
            "accuracy_bonus": 15,
            "energy_regen": 4,
            "health_bonus": 12,
            "energy_consumption": 5
        },
        "color": (150, 100, 200),
        "rarity": "rare"
    },

    "optic_camouflage": {
        "name": "Optic Camouflage",
        "description": "Искажает свет вокруг головы, делая невидимым",
        "limb_type": "head",
        "stats": {
            "stealth_bonus": 25,
            "accuracy_bonus": -5,
            "health_bonus": 14,
            "energy_consumption": 8
        },
        "color": (100, 200, 200),
        "rarity": "rare"
    },

    "targeting_computer_head": {
        "name": "Targeting Computer Head",
        "description": "Встроенный баллистический вычислитель",
        "limb_type": "head",
        "stats": {
            "accuracy_bonus": 25,
            "range_bonus": 15,
            "energy_consumption": 10,
            "health_bonus": 10,
            "energy_regen": 1
        },
        "color": (100, 150, 255),
        "rarity": "epic"
    },

    "radioactive_scanner": {
        "name": "Radioactive Scanner",
        "description": "Сканирует местность на наличие радиации",
        "limb_type": "head",
        "stats": {
            "accuracy_bonus": 5,
            "health_bonus": 13,
            "energy_regen": 2,
            "constant_energy_drain": 3
        },
        "color": (100, 255, 100),
        "rarity": "uncommon"
    },
    
    # ========== ЛЕВАЯ РУКА ==========

    "basic_hand_left": {
        "name": "Basic Left Hand",
        "description": "Стандартная левая рука.",
        "limb_type": "hand_left",
        "stats": {
            "carry_weight": 5,
            "melee_damage": 2,
            "accuracy_bonus": -1,
            "health_bonus": 20,
            "energy_regen": 1
        },
        "color": (200, 180, 150),
        "rarity": "common"
    },

    "hydraulic_hand_left": {
        "name": "Hydraulic Left Hand",
        "description": "Гидравлическая рука для тяжелой работы",
        "limb_type": "hand_left",
        "stats": {
            "carry_weight": 35,
            "melee_damage": 15,
            "accuracy_bonus": -8,
            "health_bonus": 28,
            "energy_regen": 2,
            "energy_consumption": 5
        },
        "color": (150, 100, 100),
        "rarity": "uncommon"
    },

    "precision_hand_left": {
        "name": "Precision Left Hand",
        "description": "Рука с микросервоприводами для точной работы",
        "limb_type": "hand_left",
        "stats": {
            "accuracy_bonus": 20,
            "reload_speed": 15,
            "melee_damage": -8,
            "health_bonus": 18,
            "energy_regen": 3,
            "energy_consumption": 3
        },
        "color": (100, 200, 150),
        "rarity": "rare"
    },

    "shield_arm_left": {
        "name": "Shield Arm Left",
        "description": "Встроенный энергетический щит в левой руке",
        "limb_type": "hand_left",
        "stats": {
            "physical_defense": 15,
            "fire_defense": 10,
            "carry_weight": -10,
            "health_bonus": 25,
            "energy_regen": 1,
            "energy_consumption": 8
        },
        "color": (100, 150, 200),
        "rarity": "rare"
    },

    "grappling_hand_left": {
        "name": "Grappling Left Hand",
        "description": "Встроенный крюк-кошка для быстрого перемещения",
        "limb_type": "hand_left",
        "stats": {
            "movement_speed": 5,
            "jump_height": 15,
            "carry_weight": -5,
            "health_bonus": 16,
            "energy_regen": 2,
            "constant_energy_drain": 2
        },
        "color": (150, 200, 150),
        "rarity": "uncommon"
    },

    "claw_hand_left": {
        "name": "Claw Left Hand",
        "description": "Острые когти вместо пальцев",
        "limb_type": "hand_left",
        "stats": {
            "melee_damage": 25,
            "melee_speed": 10,
            "accuracy_bonus": -5,
            "health_bonus": 22,
            "energy_regen": 1,
            "energy_consumption": 4
        },
        "color": (180, 100, 100),
        "rarity": "rare"
    },

    "medical_scanner_left": {
        "name": "Medical Scanner Left",
        "description": "Сканирует здоровье и выявляет повреждения",
        "limb_type": "hand_left",
        "stats": {
            "health_regen": 1,
            "accuracy_bonus": 5,
            "health_bonus": 15,
            "energy_regen": 2,
            "constant_energy_drain": 3
        },
        "color": (100, 200, 200),
        "rarity": "uncommon"
    },

    "full_cyber_arm_left": {
        "name": "Full Cyber Arm Left",
        "description": "Полностью кибернетическая рука высшего класса",
        "limb_type": "hand_left",
        "stats": {
            "carry_weight": 50,
            "melee_damage": 20,
            "accuracy_bonus": 15,
            "health_bonus": 35,
            "energy_regen": 4,
            "energy_consumption": 10
        },
        "color": (50, 150, 200),
        "rarity": "epic"
    },
    
# ========== ПРАВАЯ РУКА ==========

"basic_hand_right": {
    "name": "Basic Right Hand",
    "description": "Стандартная правая рука.",
    "limb_type": "hand_right",
    "stats": {
        "damage_bonus": 2,
        "recoil_reduction": 5,
        "health_bonus": 20,
        "energy_regen": 1
    },
    "color": (200, 180, 150),
    "rarity": "common"
},

"combat_hand_right": {
    "name": "Combat Right Hand",
    "description": "Боевая рука с усиленной конструкцией",
    "limb_type": "hand_right",
    "stats": {
        "damage_bonus": 12,
        "recoil_reduction": 20,
        "accuracy_bonus": 5,
        "health_bonus": 26,
        "energy_regen": 2,
        "energy_consumption": 6
    },
    "color": (180, 100, 100),
    "rarity": "uncommon"
},

"energy_hand_right": {
    "name": "Energy Hand Right",
    "description": "Рука с энергетическим каналом",
    "limb_type": "hand_right",
    "stats": {
        "flat_electric_damage": 8,
        "electric_damage_bonus": 20,
        "physical_damage_bonus": -12,
        "health_bonus": 22,
        "energy_regen": 3,
        "energy_consumption": 8
    },
    "color": (100, 150, 255),
    "rarity": "rare"
},

"sniper_hand_right": {
    "name": "Sniper Hand Right",
    "description": "Стабилизирует руку для снайперской стрельбы",
    "limb_type": "hand_right",
    "stats": {
        "accuracy_bonus": 25,
        "range_bonus": 20,
        "recoil_reduction": 30,
        "melee_speed": -15,
        "health_bonus": 18,
        "energy_regen": 2,
        "energy_consumption": 5
    },
    "color": (100, 200, 100),
    "rarity": "rare"
},

"rocket_hand_right": {
    "name": "Rocket Hand Right",
    "description": "Встроенный реактивный ускоритель для удара",
    "limb_type": "hand_right",
    "stats": {
        "melee_damage": 30,
        "damage_bonus": -5,
        "recoil_reduction": -10,
        "health_bonus": 24,
        "energy_regen": 1,
        "energy_consumption": 12,
        "constant_energy_drain": 2
    },
    "color": (200, 100, 50),
    "rarity": "rare"
},

"drone_controller_right": {
    "name": "Drone Controller Right",
    "description": "Управляет привязанным дроном",
    "limb_type": "hand_right",
    "stats": {
        "accuracy_bonus": 10,
        "range_bonus": 15,
        "health_bonus": 15,
        "energy_regen": 2,
        "constant_energy_drain": 4
    },
    "color": (100, 200, 200),
    "rarity": "uncommon"
},

"shield_generator_right": {
    "name": "Shield Generator Right",
    "description": "Генерирует защитное поле",
    "limb_type": "hand_right",
    "stats": {
        "physical_defense": 20,
        "electric_defense": 15,
        "fire_defense": 10,
        "health_bonus": 20,
        "energy_regen": 1,
        "energy_consumption": 10,
        "constant_energy_drain": 3
    },
    "color": (100, 150, 200),
    "rarity": "rare"
},

"full_cyber_arm_right": {
    "name": "Full Cyber Arm Right",
    "description": "Полностью кибернетическая рука высшего класса",
    "limb_type": "hand_right",
    "stats": {
        "damage_bonus": 25,
        "recoil_reduction": 30,
        "reload_speed": 25,
        "accuracy_bonus": 15,
        "health_bonus": 38,
        "energy_regen": 4,
        "energy_consumption": 12
    },
    "color": (50, 150, 200),
    "rarity": "epic"
},
    
# ========== ЛЕВАЯ НОГА ==========

"basic_leg_left": {
    "name": "Basic Left Leg",
    "description": "Стандартная левая нога.",
    "limb_type": "leg_left",
    "stats": {
        "movement_speed": 5,
        "health_bonus": 25,
        "energy_regen": 1
    },
    "color": (200, 180, 150),
    "rarity": "common"
},

"speed_leg_left": {
    "name": "Speed Leg Left",
    "description": "Облегченная нога для скорости",
    "limb_type": "leg_left",
    "stats": {
        "movement_speed": 20,
        "carry_weight": -15,
        "health_bonus": 22,
        "energy_regen": 2,
        "energy_consumption": 3
    },
    "color": (100, 200, 100),
    "rarity": "uncommon"
},

"spring_leg_left": {
    "name": "Spring Leg Left",
    "description": "Пружинный механизм для высоких прыжков",
    "limb_type": "leg_left",
    "stats": {
        "jump_height": 35,
        "movement_speed": 8,
        "carry_weight": -10,
        "health_bonus": 24,
        "energy_regen": 2,
        "energy_consumption": 5
    },
    "color": (200, 200, 100),
    "rarity": "uncommon"
},

"sturdy_leg_left": {
    "name": "Sturdy Leg Left",
    "description": "Укрепленная нога для переноски грузов",
    "limb_type": "leg_left",
    "stats": {
        "carry_weight": 30,
        "movement_speed": -5,
        "health_bonus": 35,
        "energy_regen": 1,
        "energy_consumption": 4
    },
    "color": (150, 150, 100),
    "rarity": "uncommon"
},

"stealth_leg_left": {
    "name": "Stealth Leg Left",
    "description": "Бесшумное передвижение",
    "limb_type": "leg_left",
    "stats": {
        "stealth_bonus": 20,
        "movement_speed": 3,
        "health_bonus": 20,
        "energy_regen": 2,
        "energy_consumption": 3
    },
    "color": (100, 100, 150),
    "rarity": "rare"
},

"shock_leg_left": {
    "name": "Shock Leg Left",
    "description": "Генерирует электрический заряд при ударе ногой",
    "limb_type": "leg_left",
    "stats": {
        "melee_damage": 15,
        "flat_electric_damage": 5,
        "movement_speed": -3,
        "health_bonus": 26,
        "energy_regen": 1,
        "energy_consumption": 6,
        "constant_energy_drain": 2
    },
    "color": (100, 200, 255),
    "rarity": "rare"
},

"hover_leg_left": {
    "name": "Hover Leg Left",
    "description": "Парит над землей, игнорируя препятствия",
    "limb_type": "leg_left",
    "stats": {
        "movement_speed": 15,
        "carry_weight": -20,
        "health_bonus": 18,
        "energy_regen": 2,
        "energy_consumption": 8,
        "constant_energy_drain": 3
    },
    "color": (150, 200, 200),
    "rarity": "rare"
},

"full_cyber_leg_left": {
    "name": "Full Cyber Leg Left",
    "description": "Полностью кибернетическая нога высшего класса",
    "limb_type": "leg_left",
    "stats": {
        "movement_speed": 30,
        "jump_height": 25,
        "carry_weight": 25,
        "health_bonus": 40,
        "energy_regen": 4,
        "energy_consumption": 10
    },
    "color": (50, 150, 200),
    "rarity": "epic"
},

    # ========== ПРАВАЯ НОГА ==========

"basic_leg_right": {
    "name": "Basic Right Leg",
    "description": "Стандартная правая нога.",
    "limb_type": "leg_right",
    "stats": {
        "movement_speed": 5,
        "health_bonus": 25,
        "energy_regen": 1
    },
    "color": (200, 180, 150),
    "rarity": "common"
},

"stabilizer_leg_right": {
    "name": "Stabilizer Leg Right",
    "description": "Нога с гироскопами для устойчивости",
    "limb_type": "leg_right",
    "stats": {
        "accuracy_bonus": 12,
        "recoil_reduction": 20,
        "movement_speed": -3,
        "health_bonus": 28,
        "energy_regen": 2,
        "energy_consumption": 4
    },
    "color": (150, 150, 100),
    "rarity": "uncommon"
},

"power_tread_right": {
    "name": "Power Tread Right",
    "description": "Мощный привод для увеличения грузоподъемности",
    "limb_type": "leg_right",
    "stats": {
        "carry_weight": 45,
        "movement_speed": -8,
        "health_bonus": 32,
        "energy_regen": 1,
        "energy_consumption": 8,
        "constant_energy_drain": 2
    },
    "color": (150, 100, 80),
    "rarity": "rare"
},

"kick_leg_right": {
    "name": "Kick Leg Right",
    "description": "Усиленная нога для мощных пинков",
    "limb_type": "leg_right",
    "stats": {
        "melee_damage": 25,
        "movement_speed": -2,
        "health_bonus": 30,
        "energy_regen": 1,
        "energy_consumption": 6
    },
    "color": (180, 120, 80),
    "rarity": "uncommon"
},

"dash_leg_right": {
    "name": "Dash Leg Right",
    "description": "Реактивный ускоритель для рывка",
    "limb_type": "leg_right",
    "stats": {
        "movement_speed": 15,
        "carry_weight": -15,
        "health_bonus": 22,
        "energy_regen": 2,
        "energy_consumption": 10,
        "constant_energy_drain": 3
    },
    "color": (200, 150, 100),
    "rarity": "rare"
},

"silent_leg_right": {
    "name": "Silent Leg Right",
    "description": "Полностью бесшумное передвижение",
    "limb_type": "leg_right",
    "stats": {
        "stealth_bonus": 25,
        "movement_speed": 2,
        "health_bonus": 20,
        "energy_regen": 2,
        "energy_consumption": 3
    },
    "color": (120, 120, 150),
    "rarity": "rare"
},

"regen_leg_right": {
    "name": "Regen Leg Right",
    "description": "Восстанавливает здоровье ноги со временем",
    "limb_type": "leg_right",
    "stats": {
        "health_regen": 1,
        "movement_speed": 3,
        "health_bonus": 24,
        "energy_regen": 3,
        "energy_consumption": 4
    },
    "color": (100, 200, 150),
    "rarity": "uncommon"
},

"full_cyber_leg_right": {
    "name": "Full Cyber Leg Right",
    "description": "Полностью кибернетическая нога высшего класса",
    "limb_type": "leg_right",
    "stats": {
        "movement_speed": 35,
        "jump_height": 20,
        "carry_weight": 30,
        "accuracy_bonus": 10,
        "health_bonus": 42,
        "energy_regen": 4,
        "energy_consumption": 12
    },
    "color": (50, 150, 200),
    "rarity": "epic"
}

}