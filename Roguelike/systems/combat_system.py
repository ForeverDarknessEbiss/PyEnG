import pygame
import math
import random

class CombatSystem:

    def __init__(self, hitbox_system, camera, collision_system, damage_system, monster_manager, damage_text_system):
        self.hitbox_system = hitbox_system
        self.attack_timer = 0
        self.camera = camera
        self.attack_vector = (0, 0)
        self.collision_system = collision_system
        self.damage_system = damage_system
        self.monster_manager = monster_manager
        # self.monster_manager.all_monsters 
        self.damage_text_system = damage_text_system
        self.debug_shot = None ############################                    УДАЛИТЬ ПОТОМ            №№№№№№№№№№№№№№№№№№№№№№№№№№№№

    def update_pc(self, player):

        # направление атаки — от игрока к мыши
        mx, my = pygame.mouse.get_pos()

        # переводим мышь в мировые координаты(без этого говна мыш и игрок находятся в разных координатных метриках)
        world_x = mx + self.camera.x
        world_y = my + self.camera.y
        #тем кто залезет сюда после меня: world_ локальная координата, не используйте ее нигде
        px = player.x + player.width // 2
        py = player.y + player.height // 2

        dx = world_x - px
        dy = world_y - py

        dist = math.hypot(dx, dy)
        #нормализация 
        if dist > 0:
            dx /= dist
            dy /= dist
        else:
            dx, dy = 0, 0

        self.attack_vector = (dx, dy)

    def update_mobile(self, right_joystick):

        # направление атаки — правый джойстик
        self.attack_vector = right_joystick.get_direction()

        self.attack_timer = self.attack_cooldown

    def handle_attack(self, player, weapon):

        # ⛔ нет патронов
        if weapon.weapon_type == "ranged":
            if weapon.current_ammo <= 0:
                return
            
            weapon.current_ammo -= 1

        if weapon.weapon_type == "melee":
            self._melee_attack(player, weapon)

        elif weapon.weapon_type == "ranged":
            self._ranged_attack(player, weapon)

    def try_reload(self, player):
        """Попытка перезарядки оружия"""
        weapon = getattr(player, "weapon", None)
        if not weapon:
            
            return False

        # только для дальнобойного
        if weapon.weapon_type != "ranged":
            
            return False

        # если обойма полная
        if weapon.current_ammo >= weapon.magazine_size:
           
            return False

        # сколько нужно до полной
        needed = weapon.magazine_size - weapon.current_ammo

        # ищем патроны в инвентаре
        ammo_taken = self._take_ammo_from_inventory(player, weapon.ammo_type, needed)

        if ammo_taken > 0:
            weapon.current_ammo += ammo_taken
            
            return True

        
        return False
    
    def _take_ammo_from_inventory(self, player, ammo_type, needed):
        """
        Забирает патроны из инвентаря.
        Возвращает количество изъятых.
        """
        inventory = getattr(player, "inventory", None)
        if not inventory:
            
            return 0

        taken = 0
        for i, slot in enumerate(inventory.slots):
            if slot is None:
                continue

            item = slot.item
            # проверяем, что это патроны нужного типа
            if hasattr(item, "name") and item.name == ammo_type:
                # сколько можем взять из этой стопки
                can_take = min(slot.amount, needed - taken)

                if can_take > 0:
                    slot.amount -= can_take
                    taken += can_take

                    # если стопка опустела — удаляем слот
                    if slot.amount <= 0:
                        inventory.slots[i] = None

                    if taken >= needed:
                        break

        return taken    

    def _melee_attack(self, player, weapon):
        combat_stats = player.get_combat_stats()
        damage_bonus = combat_stats.get("damage_bonus", 0)
        melee_damage_bonus = combat_stats.get("melee_damage", 0)
        melee_speed_bonus = combat_stats.get("melee_speed", 0)
        
        # 1. Получаем направление на мышь
        import pygame
        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_mouse_x = mouse_x + self.camera.x
        world_mouse_y = mouse_y + self.camera.y
        
        # Центр игрока
        center_x = player.x + player.width // 2
        center_y = player.y + player.height // 2
        
        # Направление атаки (нормализованный вектор)
        dx = world_mouse_x - center_x
        dy = world_mouse_y - center_y
        
        length = math.hypot(dx, dy)
        if length > 0:
            dx /= length
            dy /= length
        else:
            dx, dy = 1, 0
        
        # 2. Позиция хитбокса (центр + смещение по направлению)
        hitbox_x = center_x + dx * weapon.range
        hitbox_y = center_y + dy * weapon.range
        
        # Смещаем хитбокс, чтобы он был центрирован относительно направления
        hitbox_x -= weapon.area[0] // 2
        hitbox_y -= weapon.area[1] // 2
        
        # 3. Модифицируем урон
        modified_damage = weapon.damage.copy()
        
        # Общий бонус урона
        if damage_bonus != 0:
            for dmg_type, dmg_value in modified_damage.items():
                modified_damage[dmg_type] = max(1, int(dmg_value * (1 + damage_bonus / 100)))
        
        # Специальный бонус ближнего боя
        if melee_damage_bonus != 0:
            for dmg_type, dmg_value in modified_damage.items():
                modified_damage[dmg_type] = max(1, dmg_value + melee_damage_bonus)
        
        # 4. Создаем хитбокс
        self.hitbox_system.create_hitbox(
            hitbox_x,
            hitbox_y,
            weapon.area[0],
            weapon.area[1],
            owner=player,
            damage=modified_damage,
            lifetime=0.1
        )     

        if hasattr(player, 'implant_manager'):
            for uid, data in player.implant_manager.active_mechanics.items():
                if data["key"] == "energy_blades":
                    mechanic = data["instance"]
                    # Добавляем кровотечение к цели
                    # (нужно модифицировать хитбокс или добавить эффект)
                    pass
        
                # Возвращаем бонус скорости
        return melee_speed_bonus
    
    def _ranged_attack(self, player, weapon):
        combat_stats = player.get_combat_stats()
        import pygame
        import random
        import math

        accuracy_bonus = combat_stats.get("accuracy_bonus", 0)
        damage_bonus = combat_stats.get("damage_bonus", 0)
        range_bonus = combat_stats.get("range_bonus", 0)
        recoil_reduction = combat_stats.get("recoil_reduction", 0)

        # применяем бонусы
        final_range = weapon.range * (1 + range_bonus / 100)
        final_spread = weapon.spread * (100 - accuracy_bonus) / 100
        final_spread = final_spread * (100 - recoil_reduction) / 100
        final_spread = max(1, final_spread)

        # 1. старт (центр игрока)
        start_x = player.x + player.width // 2
        start_y = player.y + player.height // 2

        # 2. мышка (экран → мир пиксели)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_mouse_x = mouse_x + self.camera.x
        world_mouse_y = mouse_y + self.camera.y

        # 3. направление (НОРМАЛЬНОЕ, не last_dx)
        dx = world_mouse_x - start_x
        dy = world_mouse_y - start_y

        length = (dx**2 + dy**2) ** 0.5
        if length != 0:
            dx /= length
            dy /= length

        # 4. перпендикулярное направление
        perp_x = -dy
        perp_y = dx

        # 5. радиус круга разброса на максимальной дистанции
        spread_rad = math.radians(final_spread)
        max_radius = final_range * math.tan(spread_rad)

        # 6. случайная точка в круге
        angle = random.uniform(0, 2 * math.pi)
        r = max_radius * math.sqrt(random.uniform(0, 1))  # равномерно по площади
        offset_x = r * math.cos(angle)
        offset_y = r * math.sin(angle)

        # 7. точка в основании конуса (в мировых координатах)
        base_x = start_x + dx * weapon.range + perp_x * offset_x
        base_y = start_y + dy * weapon.range + perp_y * offset_y

        # 8. направление выстрела
        shot_dx = base_x - start_x
        shot_dy = base_y - start_y
        shot_length = math.hypot(shot_dx, shot_dy)

        if shot_length > 0:
            shot_dx /= shot_length
            shot_dy /= shot_length

        # 9. конец луча (по дальности до выбранной точки)
        end_x = start_x + shot_dx * shot_length
        end_y = start_y + shot_dy * shot_length

        # дебаг вызов метода трассировки дров в хитбокс систем 
        self.hitbox_system.set_debug_line((start_x, start_y), (end_x, end_y))

        # 10. РЕЙКАСТ
        hit = self.collision_system.raycast(
            start_x,
            start_y,
            end_x,
            end_y,
            self.monster_manager.all_monsters
        )

        # 11. урон
        if hit:
            target = hit["object"]
            point = hit["point"]

            # Модифицируем урон оружия бонусами
            modified_damage = weapon.damage.copy()
            if damage_bonus != 0:
                for dmg_type, dmg_value in modified_damage.items():
                    modified_damage[dmg_type] = max(1, int(dmg_value * (1 + damage_bonus / 100)))

            # Рассчитываем итоговый урон через damage_system
            damage = self.damage_system.calculate_damage(
                modified_damage,
                getattr(target, "defense", {})
            )

            # 🩸 РАСПРЕДЕЛЕНИЕ УРОНА ПО КОНЕЧНОСТЯМ (только для игрока)
            if target == player:
                # Список конечностей для случайного выбора
                limbs_list = ["head", "left_hand", "right_hand", "left_leg", "right_leg"]
                target_limb = random.choice(limbs_list)
                
                # Наносим урон по конкретной конечности
                player.limb_health.take_damage(target_limb, damage)
            else:
                # Старая логика для монстров
                if hasattr(target, "take_damage"):
                    target.take_damage(damage)

            # Отображаем текст урона
            self.damage_text_system.add(point[0], point[1], damage)

            # эффект попадания
            self._spawn_impact_effect(point)

    def update(self, delta_time):
        if self.attack_timer > 0:
            self.attack_timer -= delta_time

    def try_attack(self, player):
        if self.attack_timer > 0:
            return

        weapon = player.weapon
        has_weapon = weapon is not None

        if not has_weapon and hasattr(player, 'implant_manager'):
            for uid, data in player.implant_manager.active_mechanics.items():
                if data["key"] == "energy_blades"and data["instance"].enabled:
                    data["instance"].use(attack_vector=self.attack_vector,damage_text_system=self.damage_text_system)
                    self.attack_timer = 0.5
                    return


        # ========== ОСТАЛЬНОЙ КОД БЕЗ ИЗМЕНЕНИЙ ==========
        weapon = player.weapon

        # если оружия нет — бьём дефолтной атакой
        if weapon is None:
            from loot.weapons.weapon import Weapon

            fists = Weapon(
                name="fists",
                damage={"physical": 5},
                attack_speed=1.5,
                range=30,
                area=(30, 30),
                weapon_type="melee"
            )

            self._melee_attack(player, fists)
            self.attack_timer = 1 / fists.attack_speed
            return

        # Получаем бонус скорости атаки
        combat_stats = player.get_combat_stats()
        attack_speed_bonus = 0
        
        if weapon.weapon_type == "melee":
            attack_speed_bonus = combat_stats.get("melee_speed", 0)
        elif weapon.weapon_type == "ranged":
            # Для дальнего боя можно добавить свой бонус
            pass        

        # Применяем бонус к скорости атаки
        final_attack_speed = weapon.attack_speed * (1 + attack_speed_bonus / 100)

        weapon.attack(player, self)

        self.attack_timer = 1 / final_attack_speed


    def _spawn_impact_effect(self, point):
        """
        🔥 Здесь позже подключается система частиц:
        - искры
        - дым
        - осколки
        """
        pass