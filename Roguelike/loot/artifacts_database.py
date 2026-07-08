# loot/artifacts_database.py
# База данных артефактов с статичными и процентными бонусами

ARTIFACTS = {
    "crystal_shield": {
        "name": "Crystal Shield",
        "description": "Кристаллический артефакт, усиливает защиту от магии",
        "static_bonuses": {
            "physical": 3,
            "electric": 8,
            "fire": 5
        },
        "percent_modifiers": {
            "physical": -4  # Теряем 4% физической защиты
        },
        "rarity": "uncommon"
    },
    
    "iron_plate": {
        "name": "Iron Plate",
        "description": "Железная пластина - грубо но эффективно",
        "static_bonuses": {
            "physical": 15,
            "chemical": 2
        },
        "percent_modifiers": {
            "electric": -6,  # Уязвимость к электричеству
            "fire": -3
        },
        "rarity": "common"
    },
    
    "chemical_filter": {
        "name": "Chemical Filter",
        "description": "Фильтр от химических веществ",
        "static_bonuses": {
            "chemical": 12,
            "fire": 2
        },
        "percent_modifiers": {
            "physical": -2,
            "electric": -5
        },
        "rarity": "uncommon"
    },
    
    "void_stone": {
        "name": "Void Stone",
        "description": "Редкий камень, поглощает урон всех типов",
        "static_bonuses": {
            "physical": 8,
            "chemical": 8,
            "electric": 8,
            "fire": 8
        },
        "percent_modifiers": {},
        "rarity": "rare"
    },
    
    "paradox_orb": {
        "name": "Paradox Orb",
        "description": "Могущественный артефакт с противоречивыми свойствами",
        "static_bonuses": {
            "physical": 10,
            "electric": 15
        },
        "percent_modifiers": {
            "physical": -10,  # Значительный штраф к физической защите
            "fire": -8
        },
        "rarity": "epic"
    }
}
