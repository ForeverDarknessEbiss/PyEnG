# systems/defense_system.py

class DefenseStats:
    """Хранит и рассчитывает все боевые статы игрока"""
    
    def __init__(self, player):
        self.player = player
        
        # Защита
        self.physical = 0
        self.chemical = 0
        self.electric = 0
        self.fire = 0
        
        # Боевые статы
        self.damage_bonus = 0
        self.accuracy_bonus = 0
        
        # Движение
        self.movement_speed = 0
        
        # Энергия
        self.energy_consumption = 0
        self.max_energy = 0
        self.energy_regen = 0
        
        # Ближний бой
        self.melee_damage = 0
        self.melee_speed = 0
        
        # Дальний бой
        self.range_bonus = 0
        self.recoil_reduction = 0
        
        # Разное
        self.carry_weight = 0
        self.jump_height = 0
        self.stealth_bonus = 0
        self.health_regen = 0
    
    def recalculate(self, raw_stats):
        """Применяет процентные модификаторы и сохраняет все статы"""
        
        # 1. Базовая защита
        self.physical = raw_stats.get("physical_defense", 0)
        self.chemical = raw_stats.get("chemical_defense", 0)
        self.electric = raw_stats.get("electric_defense", 0)
        self.fire = raw_stats.get("fire_defense", 0)
        
        # 2. Применяем процентные модификаторы к защите
        physical_percent = raw_stats.get("physical_percent", 0)
        if physical_percent != 0:
            self.physical = int(self.physical * (1 + physical_percent / 100))
        
        chemical_percent = raw_stats.get("chemical_percent", 0)
        if chemical_percent != 0:
            self.chemical = int(self.chemical * (1 + chemical_percent / 100))
        
        electric_percent = raw_stats.get("electric_percent", 0)
        if electric_percent != 0:
            self.electric = int(self.electric * (1 + electric_percent / 100))
        
        fire_percent = raw_stats.get("fire_percent", 0)
        if fire_percent != 0:
            self.fire = int(self.fire * (1 + fire_percent / 100))
        
        # 3. Боевые статы
        self.damage_bonus = raw_stats.get("damage_bonus", 0)
        self.accuracy_bonus = raw_stats.get("accuracy_bonus", 0)
        
        # 4. Движение
        self.movement_speed = raw_stats.get("movement_speed", 0)
        
        # 5. Энергия
        self.energy_consumption = raw_stats.get("energy_consumption", 0)
        self.max_energy = raw_stats.get("max_energy", 0)
        self.energy_regen = raw_stats.get("energy_regen", 0)
        self.constant_energy_drain = raw_stats.get("constant_energy_drain", 0)

        # 6. Ближний бой
        self.melee_damage = raw_stats.get("melee_damage", 0)
        self.melee_speed = raw_stats.get("melee_speed", 0)
        
        # 7. Дальний бой
        self.range_bonus = raw_stats.get("range_bonus", 0)
        self.recoil_reduction = raw_stats.get("recoil_reduction", 0)
        
        # 8. Разное
        self.carry_weight = raw_stats.get("carry_weight", 0)
        self.jump_height = raw_stats.get("jump_height", 0)
        self.stealth_bonus = raw_stats.get("stealth_bonus", 0)
        self.health_regen = raw_stats.get("health_regen", 0)
        
        print(f"[DEFENSE] 📊 Итоговые статы:")
        print(f"  🛡️ Защита: физ={self.physical}, хим={self.chemical}, элек={self.electric}, огонь={self.fire}")
        print(f"  💥 Урон бонус: {self.damage_bonus}%, 🎯 Точность: {self.accuracy_bonus}%")
        print(f"  🏃 Скорость: {self.movement_speed}, 🎒 Грузоподъемность: {self.carry_weight}")
        if self.health_regen > 0:
            print(f"  ❤️ Регенерация: {self.health_regen}/сек")
        if self.energy_consumption != 0:
            print(f"  ⚡ Расход энергии: {self.energy_consumption}%")

        # 🧬 Здоровье
        health_bonus = raw_stats.get("health_bonus", 0)
        if hasattr(self.player, "max_health"):
            old_max = self.player.max_health
            self.player.max_health = health_bonus  # ← убрал 100
            if old_max != self.player.max_health:
                self.player.health = self.player.max_health
        
        # ⚡ Энергия
        energy_bonus = raw_stats.get("energy_bonus", 0)
        if hasattr(self.player, "max_energy"):
            self.player.max_energy = 100 + energy_bonus
    
    def get_all(self):
        """Возвращает все статы для боевой системы"""
        return {
            # Защита
            "physical_defense": self.physical,
            "chemical_defense": self.chemical,
            "electric_defense": self.electric,
            "fire_defense": self.fire,
            
            # Боевые
            "damage_bonus": self.damage_bonus,
            "accuracy_bonus": self.accuracy_bonus,
            
            # Движение
            "movement_speed": self.movement_speed,
            
            # Энергия
            "energy_consumption": self.energy_consumption,
            "max_energy": self.max_energy,
            "energy_regen": self.energy_regen,
            "constant_energy_drain": self.constant_energy_drain,

            # Ближний бой
            "melee_damage": self.melee_damage,
            "melee_speed": self.melee_speed,
            
            # Дальний бой
            "range_bonus": self.range_bonus,
            "recoil_reduction": self.recoil_reduction,
            
            # Разное
            "carry_weight": self.carry_weight,
            "jump_height": self.jump_height,
            "stealth_bonus": self.stealth_bonus,
            "health_regen": self.health_regen,
        }
    
    def __repr__(self):
        return f"Defense(физ={self.physical},хим={self.chemical}, элек={self.electric}, огонь={self.fire}, урон+{self.damage_bonus}%, точн+{self.accuracy_bonus}%)"