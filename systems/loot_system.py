import math
import random
import os
import importlib
from loot.item_entity import ItemEntity


class LootSystem:

    def __init__(self):

        
        self.items = []
        self.orbs = []

        # --- АВТОПОДГРУЗКА ПРЕСЕТОВ ---
        self.presets = {}

        preset_path = "loot.presets"
        folder_path = "loot/presets"

        for file in os.listdir(folder_path):

            if file.endswith(".py") and file != "__init__.py":

                module_name = file[:-3]  # ratte.py → ratte

                module = importlib.import_module(f"{preset_path}.{module_name}")

                # ожидаем имя типа RATTE_LOOT
                attr_name = module_name.upper() + "_LOOT"

                if hasattr(module, attr_name):
                    self.presets[module_name] = getattr(module, attr_name)
                else:
                    print(f"[LootSystem] Нет {attr_name} в {file}")

        print("LOADED PRESETS:", self.presets.keys()) # проверка подгрузки прессетов 
            
    def spawn_xp(self, x, y, value=1):

        from loot.xp_orb import XPOrb

        orb = XPOrb(x, y, value)

        self.orbs.append(orb)

    def update(self, player, delta_time):

        px, py = player.get_pixel_position()

        # --- XP СФЕРЫ ---
        for orb in self.orbs[:]:

            dx = px - orb.x
            dy = py - orb.y

            dist = math.hypot(dx, dy)

            magnet_range = 140
            pickup_range = 18

            # --- МАГНИТ ---
            if dist < magnet_range and dist > 0:
                magnet_speed = 420
                orb.vx = dx / dist * magnet_speed
                orb.vy = dy / dist * magnet_speed

            # --- ДВИЖЕНИЕ ---
            orb.x += orb.vx * delta_time
            orb.y += orb.vy * delta_time

            # --- ЗАМЕДЛЕНИЕ (трение) ---
            orb.vx *= 0.92
            orb.vy *= 0.92

            # --- ПОДБОР ---
            if dist < pickup_range:
                player.add_exp(orb.value)
                self.orbs.remove(orb)

        # --- ПРЕДМЕТЫ ---
        for item in self.items[:]:

            dx = px - item.x
            dy = py - item.y

            dist = math.hypot(dx, dy)

            self.pickup_delay = 0.5 
            # 🆕 уменьшаем задержку
            if item.pickup_delay > 0:
                item.pickup_delay -= delta_time

            has_space = player.inventory.has_free_space_for_item(item.item)
            
            magnet_item_range = 60
            pickup_range = 18

            if  has_space and dist < magnet_item_range and dist > 0 and item.pickup_delay <= 0:
                magnet_speed = 370
                item.vx = dx / dist * magnet_speed
                item.vy = dy / dist * magnet_speed
            else:
                # Если места нет - замедляем и останавливаем
                item.vx *= 0.95
                item.vy *= 0.95
    
            # --- ДВИЖЕНИЕ ---
            item.x += item.vx * delta_time
            item.y += item.vy * delta_time

            # --- ЗАМЕДЛЕНИЕ (трение) ---
            item.vx *= 0.92
            item.vy *= 0.92

            # --- ПОДБОР ---
            if dist < pickup_range and item.pickup_delay <= 0:
                success = player.inventory.add_item(item.item, item.amount)
                if success:
                    # player.add_item(item)  # если add_item возвращает True
                    self.items.remove(item)
                else:
                    # Не удалось добавить - отключаем магнит
                    item.vx = 0
                    item.vy = 0


    def generate_loot(self, monster):
        import random
        rng = random.Random()
        rng.seed()
        
        preset_name = getattr(monster, "loot_preset", None)
        preset = self.presets.get(preset_name)

        if not preset:
            print(f"[LootSystem] Нет пресета: {preset_name}")
            return []

        items = preset["items"]
        rare = preset["rare"]

        drop = []

        num_types = rng.randint(1, 10)
        pool = items + rare
        chosen = rng.sample(pool, min(num_types, len(pool)))

        for item_data in chosen:
            if isinstance(item_data, tuple):
                item_type = item_data[0]
                item_id = item_data[1]
                
                if item_type == "weapon":
                    from loot.weapons.weapon_factory import create_weapon
                    item = create_weapon(item_id)
                elif item_type == "armor":
                    from loot.equipments.armor_factory import create_equipments
                    item = create_equipments(item_id)
                elif item_type == "artifact":
                    from loot.artifacts.artifact_factory import create_artifact
                    item = create_artifact(item_id)
                elif item_type == "implant":
                    from loot.implants.implant_factory import create_implant
                    item = create_implant(item_id)
                elif item_type == "limb":
                    from loot.limbs_database import LimbsDatabase
                    from loot.limbs.limb_factory import LimbFactory
                    db = LimbsDatabase()
                    factory = LimbFactory(db)
                    # Пробуем числовой ID, если не вышло — ищем по имени
                    if isinstance(item_id, int):
                        item = factory.create(item_id)
                    else:
                        row = db.fetch_by_name(item_id)
                        if row:
                            item = factory.create(row[0])
                        else:
                            item = None
                else:
                    continue
                    
                drop.append((item, 1))
                continue

            if getattr(item_data, "is_unique", False):
                amount = 1
            else:
                min_c = getattr(item_data, "min_count", 1)
                max_c = getattr(item_data, "max_count", 3)
                amount = rng.randint(min_c, max_c)

            drop.append((item_data, amount))

        return drop


    def spawn_item(self, item, amount, x, y):
        import random
        import uuid
        
        if isinstance(item, tuple):
            item_type = item[0]
            item_data = item[1]
            
            if item_type == "weapon":
                from loot.weapons.weapon_factory import create_weapon
                base_item = create_weapon(item_data)
            elif item_type == "armor":
                from loot.equipments.armor_factory import create_equipments
                base_item = create_equipments(item_data)
            elif item_type == "implant":
                from loot.implants.implant_factory import create_implant
                base_item = create_implant(item_data)
            elif item_type == "limb":
                from loot.limbs_database import LimbsDatabase
                from loot.limbs.limb_factory import LimbFactory
                db = LimbsDatabase()
                factory = LimbFactory(db)
                if isinstance(item_data, int):
                    base_item = factory.create(item_data)
                else:
                    row = db.fetch_by_name(item_data)
                    if row:
                        base_item = factory.create(row[0])
                    else:
                        base_item = None
            else:
                base_item = item_data
        else:
            base_item = item

        # Если не удалось создать предмет — выходим
        if base_item is None:
            print(f"[LootSystem] ❌ Не удалось создать предмет: {item}")
            return

        for _ in range(amount):
            import copy
            new_item = copy.deepcopy(base_item)
            new_item.uid = str(uuid.uuid4())
            
            entity = ItemEntity(x, y, new_item, 1)
            self.items.append(entity)

    def draw(self, screen, camera, player):

            import pygame

            # --- XP ORBS ---
            for orb in self.orbs:
                screen_x, screen_y = camera.world_to_screen_pixel(orb.x, orb.y)

                pygame.draw.rect(
                    screen,
                    (255, 230, 0),
                    (screen_x, screen_y, 30, 30),
                )

            # --- LOOT ITEMS ---
            for item in self.items:

                screen_x, screen_y = camera.world_to_screen_pixel(item.x, item.y)

                pygame.draw.rect(screen, item.color, (screen_x, screen_y, 30, 30))
                # --- координаты игрока ---
                player_screen_x, player_screen_y = camera.world_to_screen_pixel(player.x, player.y)

                # # --- ЛАЗЕР ---
                # pygame.draw.line(
                #     screen,
                #     (255, 0, 0),  # красный
                #     (player_screen_x, player_screen_y),
                #     (screen_x, screen_y),
                #     2
                # )


        #РАБОТА ВЫБРОСА ПРЕДМЕТА (ВЫЗОВ В ПЛЕЕР ПАЙ)
    def spawn_dropped_item(self, item, x, y, dx, dy, item_uid=None):
        from loot.item_entity import ItemEntity
        import random
        import math
        import copy
        import uuid


        # 🎯 нормализация направления
        length = math.hypot(dx, dy)
        if length == 0:
            dx, dy = 1, 0
        else:
            dx /= length
            dy /= length

        # 🚀 базовая дальность броска
        speed = random.uniform(650, 850)

        # 🎲 разброс (овал)
        spread_x = random.uniform(80, 120)
        spread_y = random.uniform(-20, 20)

        if item_uid:
            item.uid = item_uid

        new_item = copy.deepcopy(item)
        new_item.uid = str(uuid.uuid4())


        entity = ItemEntity(
            x,
            y,
            new_item,
            1
        )

        entity.pickup_delay = 0.8  # 0.5 секунды нельзя подобрать

        # 💨 задаём импульс
        entity.vx = dx * speed + spread_x
        entity.vy = dy * speed + spread_y



        self.items.append(entity)