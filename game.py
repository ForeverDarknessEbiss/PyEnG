import pygame
import sys #
from config import *
from camera import Camera
from entities import Player #
from map import GameMap
from managers.monster_manager import MonsterManager
# --- монстры , решить проблему огромного количества импортов 
from entities.monsters.aggressive import AggressiveMonster
from entities.monsters.ratte import RatteMonster
from entities.monsters.poogalo import PoogaloMonster
from entities.monsters.soldier import SoldierMonster
from entities.monsters.heavy import HeavyMonster
from entities.monsters.scout import ScoutMonster
from entities.monsters.dogbot import DogbotMonster
# --- оружие , та же проблема что с монстрами 
from loot.weapons.weapon_factory import create_weapon
from loot.equipments.armor_factory import create_equipments
from loot.implants.implant_factory import create_implant
#
from systems.loot_system import LootSystem
from systems import CombatSystem, CollisionSystem #
from systems.hitbox_system import HitboxSystem
from systems.damage_system import DamageSystem
from systems.damage_text_system import DamageTextSystem
from systems.inventory_system import Inventory
from systems.ui_inventory_system import draw_inventory, draw_equipment_tabs, draw_equipment,draw_context_menu
from systems.ui_global_system import WeaponCarousel
from systems.radial_menu import RadialMenu
from systems.interactive.manager import InteractiveManager


def main():
    pygame.init()
    monster_manager = MonsterManager()
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    all_monsters = []
    clock = pygame.time.Clock()
    collision_system = CollisionSystem()
    damage_text_system = DamageTextSystem()
    damage_system = DamageSystem()
    hitbox_system = HitboxSystem(damage_system, damage_text_system)
    combat_system = CombatSystem(hitbox_system, camera, collision_system, damage_system, monster_manager, damage_text_system)
    loot_system = LootSystem() 
    inventory = Inventory()
    hovered_slot = None
    hovered_type = None
    ui_layer = "game"
    active_equipment_layer = "equipment"
    equipment_tab_buttons = []  
    interactive_manager = InteractiveManager()



    # Создание основных объектов
    player = Player(x=100, y=100,  loot_system=loot_system, width=40, height=40, color=(0, 255, 0), speed=5, )
    weapon_carousel = WeaponCarousel()
    
    radial_menu = RadialMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
    radial_menu.player = player

    #камеру перенес в самый вверх под init
    game_map = GameMap()  # Предполагается, что у тебя есть класс карты

    
    player.game_map = game_map
    player.monster_manager = monster_manager
    player.loot_system = loot_system
        

    # Пример спавна монстров№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№
    monster_manager.spawn_monster(AggressiveMonster(x=200, y=200))

    
    running = True


    # Тестовые объекты для дебага
    interactive_manager.spawn("chest", "test_chest_01", player.x + 80, player.y, {
        "hp": 50,
        "width": 48,
        "height": 48,
        "inventory": ["medkit", "ammo_9mm", "vodka"]
    })

    interactive_manager.spawn("chest", "test_chest_02", player.x - 80, player.y + 40, {
        "hp": 30,
        "width": 48,
        "height": 48,
        "inventory": ["bandage", "energy_cell"]
    })

        # ------НАЧАЛО ИГРОВОГО ЦИКЛА -------

    while running:

        delta_time = clock.tick(60) / 1000.0  # Время между кадрами в секундах

        if player.inventory.context_menu:
            ui_layer = "context_menu"
        elif player.inventory.is_open:
            ui_layer = "inventory"  

        else:
            ui_layer = "game"
        
        # ОБРАБОТКА СОБЫТИЙ #####################################################################################

        for event in pygame.event.get(): # ВСЕ СОБЫТИЯ ТОЛЬКО ТУТ В ЭТОМ ФОР

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_i:
                    player.inventory.is_open = not player.inventory.is_open
                        # 🔥 закрываем ВСЁ при закрытии
                    if not player.inventory.is_open:
                        player.inventory.context_menu = None
                        player.inventory.context_buttons = []

                    if event.key == pygame.K_f and hovered_slot is not None:
                        player.inventory.open_context_menu(hovered_slot, player)

                elif event.key == pygame.K_x:

                    # Проверяем, открыт ли инвентарь и есть ли ховер
                    if hovered_type == "inventory" and hovered_slot is not None:
                            item = player.drop_item(hovered_slot, loot_system)
                            # if item:
                            #     player.drop_item(item)

                    elif hovered_type == "equipment" and hovered_slot is not None:
                        # Если ховер на экипировке — используем drop_equipped_item
                        item = player.equipment.slots.get(hovered_slot)
                        if item:
                            player.drop_equipped_item(item)
                    else:
                        print("[DEBUG] Нет слота для выброса")

                elif ui_layer == "game":

                    if event.key == pygame.K_r:
                        combat_system.try_reload(player)

                if event.key == pygame.K_f:
                    if ui_layer == "game":
                        interactive_manager.try_interact_nearest(player)

                if event.key == pygame.K_TAB:
                    radial_menu.active = True
                    radial_menu.update_segments(player)
                    radial_menu.selected_segment = None

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_TAB:
                    if radial_menu.active:
                        radial_menu.activate()
                        radial_menu.active = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                    # ----------- ЛКМ НАЖАТИЕ-----------
                if event.button == 1:   
                    # выбор в контекстное меню
                    if ui_layer == "context_menu":
                        clicked = player.inventory.handle_context_click(player, mouse_pos)
                        if not clicked:
                            # клик мимо кнопок — закрываем меню
                            player.inventory.context_menu = None
                            player.inventory.context_buttons = []
                            # ui_layer обновится в начале цикла
                    else:                       
                        # 👇 клик вне меню — закрываем
                        if player.inventory.context_menu:                           
                            player.inventory.context_menu = None
                            player.inventory.context_buttons = []

                    # 🆕 Клик по иконке персонажа (только если инвентарь не открыт)
                    if ui_layer != "inventory":
                        if hasattr(weapon_carousel, 'character_icon_rect'):
                            if weapon_carousel.character_icon_rect.collidepoint(mouse_pos):
                                print("[UI] Клик по иконке персонажа")
                                # TODO: открыть меню управления имплантами
                                pass

                        # 🆕 Проверка клика по слотам имплантов в тултипе
                    if weapon_carousel.handle_implant_slot_click(mouse_pos, player):
                        pass  # клик обработан, дальше не идём

                    for rect, layer_id in equipment_tab_buttons:
                        if rect.collidepoint(mouse_pos):
                            active_equipment_layer = layer_id

                    # ---------- ПКМ НАЖАТИЕ -----------

                                    # окрыть контекстное меню
                elif event.button == 3:
                    if ui_layer == "inventory" and hovered_slot is not None:
                        
                        player.inventory.open_context_menu(hovered_slot, player, slot_type=hovered_type)

                mouse_pos = pygame.mouse.get_pos()
                for rect, tab_id in equipment_tab_buttons:
                    if rect.collidepoint(mouse_pos):
                        active_equipment_layer = tab_id
                       

            # joystick.handle_event(event)

        # =========================
        # 🎮 2. СОСТОЯНИЕ ВВОДА 
        # =========================
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # =========================
        # 🕹 3. ДВИЖЕНИЕ
        # =========================
        player.handle_input(keys)
        player.update(game_map, None, delta_time)
        # =========================
        #  4. пКМ УДЕРЖАНИЕ
        # =========================
        if mouse_buttons[2]:
            if ui_layer == "game":
                combat_system.try_attack(player)

            # 🎮 джойстик
            # joystick.handle_event(event)
                          
        combat_system.update_pc(player)

        # combat_system.update_mobile(right_joystick)
        combat_system.update(delta_time)

        # Обновление камеры
        camera.update(player)

        # Обновление монстров
        monster_manager.update_all(player, game_map, delta_time)
        collision_system.resolve_player_monsters(player, monster_manager.all_monsters)

        # система хитбоксов
        hitbox_system.update(delta_time)
        hitbox_system.check_hits(monster_manager.all_monsters)

        # инвентарь визуалочка 
        draw_inventory(screen, inventory)

        # текст урона
        damage_text_system.update(delta_time)

        # лут с мертвых
        monster_manager.remove_dead(loot_system)

        # обновление системы лута 
        loot_system.update(player, delta_time)

        # обновление состояние интерактивных объектов
        interactive_manager.update(delta_time)
        
        if radial_menu.active:
            radial_menu.update(pygame.mouse.get_pos())

        # Отрисовка
        screen.fill((0, 0, 0))  # Очистка экрана
        game_map.draw(screen, camera)  # Рисуем карту
        monster_manager.draw_all(screen, camera)  # Рисуем монстров
        player.draw(screen, camera)  # Рисуем игрока
        # joystick.draw(screen)  # Рисуем джойстик
        damage_text_system.draw(screen, camera)#  рисуем урон
        hitbox_system.draw(screen, camera) # УДАЛИТЬ ВМЕСТЕ С МЕТОДОМ ПО СООТВЕТСТВУЮЩЕЙ ДЕРИКТОРИИ рисует хитбокс удара
        loot_system.draw(screen, camera, player)#  рисуем лут
        interactive_manager.draw(screen, camera)
        weapon_carousel.draw(screen, player)
        radial_menu.draw(screen)
        # 🆕 Отрисовка миникарты (радар)
        if hasattr(player, 'implant_manager'):
            for uid, data in player.implant_manager.active_mechanics.items():
                if data["key"] == "radar":
                    data["instance"].draw(screen, camera)
        # UI (поверх всего)
        if player.inventory.is_open:

            hovered_slot, hovered_type = draw_inventory(screen, player.inventory, active_equipment_layer)
            equipment_tab_buttons = draw_equipment_tabs(screen, active_equipment_layer)
            draw_equipment(screen, player, active_equipment_layer)
            draw_context_menu(screen, player.inventory)
            # draw_stats(screen, player, active_equipment_layer)
        else:
            hovered_slot = None

        

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()