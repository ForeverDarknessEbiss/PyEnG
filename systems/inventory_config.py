# systems/inventory_config.py

INVENTORY_CONFIG = {
    "x": 770,
    "y": 0,
    "cols": 5,
    "rows": 8,
    "slot_size": 60,
    "padding": 10,
    "bg_color": (30, 30, 30),
    "slot_color": (100, 100, 100),
    "text_color": (1, 1, 1),

    "tooltip_x": 1140,
    "tooltip_y": 0,
    "tooltip_width": 300,
    "tooltip_height": 410,

    "stats_x": 380,
    "stats_y": 0,
    "stats_width": 380,
    "stats_height": 120,

    # ===== СТАТИЧЕСКИЕ СЛОТЫ (всё кроме оружия) =====
    "slot_positions": {
        "armor": (500, 120, 140, 140),

        "implant_head_1": (500, 120, 80, 80),
        "implant_head_2": (600, 120, 80, 80),

        "implant_spine_1": (525, 220, 60, 60),
        "implant_spine_2": (595, 220, 60, 60),
        "implant_spine_3": (560, 290, 60, 60),

        "implant_hand_1": (430, 240, 70, 140),
        "implant_hand_2": (680, 240, 70, 140),

        "implant_leg_1": (520, 360, 60, 160),
        "implant_leg_2": (600, 360, 60, 160),

        "art_1": (500, 120, 100, 100),
        "art_2": (640, 240, 100, 100),
        "art_3": (360, 240, 100, 100),
        "art_4": (500, 360, 100, 100),

        "limbs_head": (555, 120, 75, 75),
        "limbs_leg_right": (455, 300, 130, 130),
        "limbs_leg_left": (600, 300, 130, 130),
        "limbs_hand_right": (425, 200, 120, 60),
        "limbs_hand_left": (640, 200, 120, 60),
    },

    # ===== ДИНАМИЧЕСКИЕ ЗОНЫ ОРУЖИЯ =====
    "weapon_slot_zones": {
        "weapon_left": {
            "x": 420,
            "y_top": 60,
            "y_bottom": 640,     # 120 + 220 (старая высота primary)
            "slot_width": 60,
            "slot_height": 60,
        },
        "weapon_right": {
            "x": 660,
            "y_top": 60,
            "y_bottom": 640,
            "slot_width": 60,
            "slot_height": 60,
        },
        "weapon_melee": {
            "x": 500,
            "y_top": 280,
            "y_bottom": 340,
            "slot_width": 140,
            "slot_height": 60,
        },
    },

    "equipment_bg_color": (30, 30, 30),
    "equipment_slot_color": (120, 120, 120),
    "equipment_text_color": (255, 255, 255),

    "layers": {
        "equipment": ["weapon_melee", "armor"],  # weapon_left/right добавляются динамически
        "artifacts": ["art_1", "art_2", "art_3", "art_4"],
        "implants": [
            "implant_head_1", "implant_head_2",
            "implant_spine_1", "implant_spine_2", "implant_spine_3",
            "implant_hand_1", "implant_hand_2",
            "implant_leg_1", "implant_leg_2"
        ],
        "limbs": ["limbs_head", "limbs_leg_right", "limbs_leg_left", "limbs_hand_right", "limbs_hand_left"]
    },
    "button_x": 120,
    "button_y": 80,
    "button_width": 120,
    "button_height": 40,
    "button_padding": 1,
    "button_bg_color": (20, 20, 20),
    "button_color": (60, 60, 60),
    "button_active_color": (120, 120, 120),
    "text_button_color": (255, 255, 255),
    "tabs": [
        {"id": "equipment", "name": "Билд"},
        {"id": "implants", "name": "Спецмодули"},
        {"id": "artifacts", "name": "Артефакты"},
        {"id": "limbs", "name": "Конечности"},
    ]
}