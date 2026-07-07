import pygame
from .entity import Entity
import math
from loot.weapons.weapon_factory import create_weapon
from systems.inventory_system import Inventory
from systems.inventory_system import INVENTORY_CONFIG
from systems.equipment_system import EquipmentSystem
from systems.defense_system import DefenseStats
from systems.limb_health_system import LimbHealthSystem
from systems.implants.manager import ImplantMechanicsManager
from systems.movement_system import MovementSystem

class Player(Entity):
    def __init__(self, x, y, width, height, color, speed, loot_system=None):
        super().__init__(x, y, width, height, color)
        self.movement = MovementSystem(self)
        self.speed = speed
        self.joystick_center = (x, y)  # Центр джойстика
        self.joystick_radius = 50      # Радиус зоны джойстика
        self.dx = 0
        self.dy = 0
        self.exp = 0
        self.level = 1
        self.exp_to_next = 100 
        size = INVENTORY_CONFIG["cols"] * INVENTORY_CONFIG["rows"]
        self.inventory = Inventory(size)
        self.inventory_open = False
        self.defense = DefenseStats(self)  # 🛡️ Система защиты - ДО equipment!
        self.equipment = EquipmentSystem(self)
        self.active_weapon_slot = "weapon_primary"
        self.equipment.equip(create_weapon("rifle"), "weapon_primary")
        self.last_dx = 1
        self.last_dy = 0
        self.implant_manager = ImplantMechanicsManager(self)
        self.loot_system = loot_system
        self.base_stats = {
            "damage_bonus": 0,
            "accuracy_bonus": 0,
            "resistance": 0,
            "physical_defense": 0,
            "chemical_defense": 0,
            "electric_defense": 0,
            "fire_defense": 0,
        }
        
        self.health = 0
        self.max_health = 0
        self.radial_menu = None
        # ⚡ Энергия
        self.energy = 100
        self.max_energy = 100
        
        
        # ☢️ Радиация
        self.radiation = 0
        self.max_radiation = 100
        self.radiation_damage_tick = 0
        
        # 🦿 Дефолтные конечности
        self._equip_default_limbs()
        self.limb_health = LimbHealthSystem(self)
    
    def _equip_default_limbs(self):
        """Экипирует стандартные конечности"""
        from loot.limbs.limb_factory import create_limb
        
        default_limbs = {
            "limbs_head": "basic_head",
            "limbs_hand_left": "basic_hand_left",
            "limbs_hand_right": "basic_hand_right",
            "limbs_leg_left": "basic_leg_left",
            "limbs_leg_right": "basic_leg_right"
        }
        
        for slot, limb_id in default_limbs.items():
            limb = create_limb(limb_id)
            self.equipment.equip(limb, slot)

    def update_energy(self, delta_time):
        stats = self.get_combat_stats()
        regen_bonus = stats.get("energy_regen", 0)
        consumption = stats.get("energy_consumption", 0)
        constant_drain = stats.get("constant_energy_drain", 0)
        
        # Базовая регенерация + бонус от конечностей
        regen = regen_bonus
        
        # 🆕 Бонус за стояние (до вычитания drain)
        if self.dx == 0 and self.dy == 0:
            regen *= 1.2
        
        # Вычитаем постоянный расход от имплантов
        regen -= constant_drain
        
        # Применяем эффект энергоэффективности
        regen = regen * (100 - consumption) / 100
        
        self.energy += regen * delta_time
        self.energy = max(0, min(self.max_energy, self.energy))


    def use_energy(self, amount):
        """Потратить энергию (возвращает True если хватило)"""
        if self.energy >= amount:
            self.energy -= amount
            return True
        return False

    @property
    def weapon(self):
        return self.equipment.slots.get(self.active_weapon_slot)

    def get_combat_stats(self):
        """Вернуть все боевые статы игрока"""
        return self.defense.get_all()

    def print_combat_stats(self):
        """Отладочный вывод боевых статов"""
        stats = self.get_combat_stats()
        print("\n" + "="*60)
        print("[PLAYER] 👤 ПОЛНЫЕ БОЕВЫЕ СТАТЫ")
        print("="*60)
        print(f"  Уровень: {self.level} | Опыт: {self.exp}/{self.exp_to_next}")
        print("\n[УРОН И ТОЧНОСТЬ]")
        print(f"  💥 Урон бонус:          {stats.get('damage_bonus', 0)}")
        print(f"  🎯 Точность бонус:      {stats.get('accuracy_bonus', 0)}")
        print(f"  🔰 Сопротивление:       {stats.get('resistance', 0)}")
        print("\n[ЗАЩИТА]")
        print(f"  🔴 Физическая защита:   {stats.get('physical_defense', 0)}")
        print(f"  🟢 Химическая защита:   {stats.get('chemical_defense', 0)}")
        print(f"  🟡 Электрическая защита: {stats.get('electric_defense', 0)}")
        print(f"  🔶 Огненная защита:     {stats.get('fire_defense', 0)}")
        print("="*60 + "\n")


    def get_equipped_item(self, slot_name):
        return self.equipment.slots.get(slot_name)

    def get_pixel_position(self):
        """
        Возвращает позицию игрока в пикселях.
        Камера использует это для центрирования.
        """
        return self.x, self.y


    def update(self, game_map, joystick, delta_time):
        """
        Обновление игрока
        """
        # 1. Получаем направление от джойстика (если есть)
        if joystick:
            jx, jy = joystick.get_direction()
        else:
            jx, jy = 0, 0
        
        # 2. 🆕 Обновляем направление в movement system из текущих self.dx, self.dy
        self.movement.set_direction(self.dx + jx, self.dy + jy)
        
        # 3. Получаем бонус скорости
        stats = self.get_combat_stats()
        speed_bonus = stats.get("movement_speed", 0)
        
        # 4. Обновляем позицию через movement system
        dx, dy = self.movement.update_player(game_map, self.speed, delta_time, speed_bonus)
        
        # 5. Расход энергии при движении
        if dx != 0 or dy != 0:
            movement_cost = 1
            self.energy -= movement_cost * delta_time
            self.energy = max(0, self.energy)
        
        # 6. Обновление энергии
        self.update_energy(delta_time)
        
        # 7. Обновление имплантов
        self.implant_manager.update(delta_time)

    def add_exp(self, amount):  # Система опыта и уровней 

        self.exp += amount

        if self.exp >= self.exp_to_next:
            self.exp -= self.exp_to_next
            self.level += 1

            # пока просто увеличим порог
            self.exp_to_next += 50

            print(f"LEVEL UP! {self.level}")

    def add_item(self, item_entity):
        item = item_entity.item
        amount = item_entity.amount

        if hasattr(item_entity, 'uid') and item_entity.uid:
            item.uid = item_entity.uid

        success = self.inventory.add_item(item, amount)

        if success:
            print(f"🎁 В инвентарь: {item.name} x{amount}")
        else:
            print("❌ Нет места в инвентаре")

    def handle_input(self,  keys):
        """
        Обработка ввода с клавиатуры и мыши.
        """  
        self.dx = 0
        self.dy = 0
        
        # Если есть клавиатура, обрабатываем клавиатуру
        if keys[pygame.K_a]:
            self.dx = -1
        if keys[pygame.K_d]:
            self.dx = 1
        if keys[pygame.K_w]:
            self.dy = -1
        if keys[pygame.K_s]:
            self.dy = 1
        

        if self.dx != 0 or self.dy != 0:  # не трогать, оперделяет последнийвектор движения 
            self.last_dx = self.dx
            self.last_dy = self.dy
                            # переключение слотов снаряжения 
        if keys[pygame.K_1]:
            self.active_weapon_slot = "weapon_primary"
            
        if keys[pygame.K_2]:
            self.active_weapon_slot = "weapon_secondary"

        if keys[pygame.K_3]:
            self.active_weapon_slot = "weapon_melee"

        if keys[pygame.K_SPACE]:
            print("[INPUT] Пробел нажат")
            self.implant_manager.use_mechanic_by_key("dash")

         # СОЗДАЕМ ВЫБРАСЫВАНИЕ ПРЕДМЕТА 
    def drop_item(self, slot_index, loot_system):
        print(f"[DEBUG] drop_item вызван: slot_index={slot_index}, loot_system={loot_system}")
        if slot_index is None:
            print("[DEBUG] slot_index is None")
            return

        if slot_index >= len(self.inventory.slots):
            return

        slot = self.inventory.slots[slot_index]

        if slot is None:
            return

        # 📦 данные
        item = slot.item
        amount = slot.amount
        item_uid = getattr(item, 'uid', None)

        # ❌ удаляем из инвентаря
        self.inventory.slots[slot_index] = None

        # 📍 позиция игрока
        x, y = self.get_pixel_position()

        # ➡️ направление
        dx = self.last_dx
        dy = self.last_dy

        if dx == 0 and dy == 0:
            dx = 1  # дефолт вправо

        # 🎲 создаём выброс
        for _ in range(amount):
            loot_system.spawn_dropped_item(item, x, y, dx, dy, item_uid)

    def drop_equipped_item(self, item):
        """Выбросить экипированный предмет"""
        # ищем в каком слоте экипирован предмет
        for slot_name, equipped in self.equipment.slots.items():
            if equipped == item:
                # снимаем
                self.equipment.unequip(slot_name)
                # выбрасываем в мир
                x, y = self.get_pixel_position()
                dx = self.last_dx if self.last_dx != 0 else 1
                dy = self.last_dy if self.last_dy != 0 else 0
                self.loot_system.spawn_dropped_item(item, x, y, dx, dy)
                return True
        return False            

    def drop_item_by_reference(self, item):
        """Выбросить предмет по ссылке (используется из контекстного меню)"""
        # ищем слот с этим предметом
        for i, slot in enumerate(self.inventory.slots):
            if slot and slot.item == item:
                self.drop_item(i, self.loot_system)
                return True
        return False
    
    def open_container(self, container):
        """Открыть контейнер (сундук, верстак, труп)"""
        self.inventory.is_open = True
        self.inventory.external_container = container
        print(f"[PLAYER] Открыт контейнер {container.uid}")

    def close_container(self):
        """Закрыть контейнер"""
        if self.inventory.external_container:
            print(f"[PLAYER] Контейнер {self.inventory.external_container.uid} закрыт")
        self.inventory.is_open = False
        self.inventory.external_container = None
            