import pygame
from systems.inventory_config import INVENTORY_CONFIG



        # МЕТОД ОТРИСОВКИ ИНВЕНТАРЯ 
def draw_inventory(screen, inventory, active_equipment_layer=None):
    
    config = INVENTORY_CONFIG
    font = pygame.font.SysFont(None, 24)

    if inventory.external_container:
        draw_container_panel(screen, inventory.external_container, config)

    x0 = config["x"]
    y0 = config["y"]
    slot_size = config["slot_size"]
    padding = config["padding"]
    cols = config["cols"]
    rows = config["rows"]

    # 📦 фон
    width = cols * (slot_size + padding) + padding
    height = rows * (slot_size + padding) + padding
    pygame.draw.rect(screen, config["bg_color"], (x0, y0, width, height))

    # 🖱️ мышка
    mouse_x, mouse_y = pygame.mouse.get_pos()
    grid_x = mouse_x - x0
    grid_y = mouse_y - y0

    col = grid_x // (slot_size + padding)
    row = grid_y // (slot_size + padding)

    hovered_slot = None
    hovered_item = None

    # if hovered_slot is not None:
    #     slot = inventory.slots[hovered_slot]
    #     if slot:
    #         draw_tooltip(screen, slot, config)

    # 👉 определяем слот
    if 0 <= col < cols and 0 <= row < rows:
        hovered_slot = int(row * cols + col)

        if hovered_slot < len(inventory.slots):
            hovered_item = inventory.slots[hovered_slot]

    x = x0 + padding
    y = y0 + padding

    # 🎯 рисуем слоты
    for i in range(rows * cols):

        slot = inventory.slots[i] if i < len(inventory.slots) else None

        # ✨ анимация
        offset_y = -6 if i == hovered_slot else 0

        rect = pygame.Rect(x, y + offset_y, slot_size, slot_size)
        pygame.draw.rect(screen, config["slot_color"], rect, 2)

        # 🎨 предмет
        if slot:
            item_rect = pygame.Rect(
                x + 4,
                y + 4 + offset_y,
                slot_size - 8,
                slot_size - 8
            )

            pygame.draw.rect(screen, slot.item.color, item_rect)

            if slot.amount > 1:
                text = str(slot.amount)
                surf = font.render(text, True, config["text_color"])
                screen.blit(surf, (x + 2, y + slot_size - 18 + offset_y))

        # ➡️ движение по сетке
        x += slot_size + padding

        if (i + 1) % cols == 0:
            x = x0 + padding
            y += slot_size + padding

    # 📌 tooltip (ВАЖНО — вне цикла!)
    if hovered_item:
        draw_tooltip(screen, hovered_item, config)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    hovered_equipment = check_equipment_hover(mouse_x, mouse_y, active_equipment_layer) if active_equipment_layer else None
    
    # приоритет: если есть ховер на экипировке — возвращаем его
    if hovered_equipment:
        return hovered_equipment, "equipment"
    return hovered_slot, "inventory"

def draw_equipment(screen, player, active_equipment_layer):

    config = INVENTORY_CONFIG
    
    font = pygame.font.SysFont(None, 24)
    hovered_item = None
    slots = config["layers"][active_equipment_layer]
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for slot_name in slots:
        data = config["slot_positions"].get(slot_name)
        if not data:
            continue

        # 👇 распаковываем (x, y, width, height)
        x, y, w, h = data

        item = player.equipment.slots.get(slot_name)

        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, config["equipment_slot_color"], rect, 2)

        if item:
            item_rect = pygame.Rect(
                x + 4,
                y + 4,
                w - 8,
                h - 8
            )
            pygame.draw.rect(screen, item.color, item_rect)

            # Проверяем ховер
            if rect.collidepoint(mouse_x, mouse_y):
                hovered_item = item

        # подпись слота (чуть ниже)
        text = font.render(slot_name, True, config["equipment_text_color"])
        screen.blit(text, (x, y + h + 2))

    if hovered_item:
        draw_tooltip(screen, hovered_item, config)

def check_equipment_hover(mouse_x, mouse_y, active_layer):

    config = INVENTORY_CONFIG
    slots = config["layers"][active_layer]
    positions = config["slot_positions"]

    for slot_name in slots:
        if slot_name not in positions:
            continue
        x, y, w, h = positions[slot_name]
        rect = pygame.Rect(x, y, w, h)
        if rect.collidepoint(mouse_x, mouse_y):
            return slot_name
    return None

def draw_equipment_tabs(screen, active_layer):

    
    config = INVENTORY_CONFIG
    font = pygame.font.SysFont(None, 24)
    buttons = []

    x = config["button_x"]
    y = config["button_y"]

    for tab in config["tabs"]:
        rect = pygame.Rect(
            x,
            y,
            config["button_width"],
            config["button_height"])
        
        buttons.append((rect, tab["id"]))


        color = (
            config["button_active_color"]
            if tab["id"] == active_layer
            else config["button_color"]
        )

        pygame.draw.rect(screen, color, rect)

        text = font.render(tab["name"], True, config["text_button_color"])
        text_rect = text.get_rect(center=(x + config["button_width"] // 2, y + config["button_height"] // 2))
        screen.blit(text, text_rect)

        buttons.append((rect, tab["id"]))

        y += config["button_height"] + config["button_padding"]

    return buttons

        # draw text

def draw_tooltip(screen, data, config):
    font_title = pygame.font.SysFont(None, 28)
    font_text = pygame.font.SysFont(None, 22)

    config = INVENTORY_CONFIG
    # mouse_x, mouse_y = pygame.mouse.get_pos() 

    # 📦 размеры панели
    x = config["tooltip_x"]
    y = config["tooltip_y"]
    width = config["tooltip_width"]
    height = config["tooltip_height"]

    # 📦 фон
    pygame.draw.rect(screen, (25, 25, 25), (x, y, width, height))
    pygame.draw.rect(screen, (120, 120, 120), (x, y, width, height), 2)

    # =========================
    # 🖼️ ИКОНКА (по центру)
    # =========================
    icon_size = 40
    icon_x = x + width // 2 - icon_size // 2
    icon_y = y + 10

    if hasattr(data, 'item'):  # InventoryItem
        item_obj = data.item
        amount = data.amount
    else:  # Сам предмет
        item_obj = data
        amount = 1
        
    pygame.draw.rect(screen, item_obj.color, (icon_x, icon_y, icon_size, icon_size))

    # =========================
    # 📝 НАЗВАНИЕ
    # =========================
    name = item_obj.name
    name_lines = wrap_text(name, font_title, width - 20)

    name_y = icon_y + icon_size + 10

    for line in name_lines:
        surf = font_title.render(line, True, (255, 255, 255))
        line_x = x + width // 2 - surf.get_width() // 2
        screen.blit(surf, (line_x, name_y))
        name_y += 28

    # =========================
    # 📜 ОПИСАНИЕ (с переносами)
    # =========================
    description = getattr(item_obj, "description", "Нет описания")

    lines = wrap_text(description, font_text, width - 20)

    text_y = name_y + 30

    for line in lines:
        surf = font_text.render(line, True, (200, 200, 200))
        screen.blit(surf, (x + 10, text_y))
        text_y += 20

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + ("" if current_line =="" else " ") + word 
        width, _ = font.size(test_line)

        if width <= max_width:
            current_line = test_line
        else:
            if current_line:

                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)        

    
    return lines

def draw_context_menu(screen, inventory):

    menu = getattr(inventory, "context_menu", None)
    if not menu:
        return

    font = pygame.font.Font(None, 28)

    x, y = menu["position"]

    width = 220
    height = 40 * len(menu["actions"])

    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, (20, 20, 20), rect)
    pygame.draw.rect(screen, (200, 200, 200), rect, 2)

    buttons = []

    for i, action in enumerate(menu["actions"]):
        btn_rect = pygame.Rect(x, y + i * 40, width, 40)

        pygame.draw.rect(screen, (60, 60, 60), btn_rect)

        text = font.render(action["name"], True, (255, 255, 255))
        screen.blit(text, (btn_rect.x + 10, btn_rect.y + 10))

        buttons.append((btn_rect, action))

    inventory.context_buttons = buttons



# def draw_stats(screen, player, active_equipment_layer):
    # cfg = INVENTORY_CONFIG
    #stats_x = cfg["stats_x"]
    # stats_y = cfg["stats_y"] 
    # cell_width = cfg["stats_width"]
    # cell_height = cfg["stats_height"]


def _draw_defense_bar(screen, x, y, width, total_stats, layer_stats, stat_key, name, color):
    """Отрисовка полоски защиты"""
    font = pygame.font.Font(None, 18)
    
    total = total_stats.get(f"{stat_key}_defense", 0)
    layer = layer_stats.get(f"{stat_key}_defense", 0)
    
    # Название
    name_surf = font.render(name, True, color)
    screen.blit(name_surf, (x + 10, y))
    
    # Значение
    value_text = f"{total}"
    value_surf = font.render(value_text, True, (255, 255, 255))
    screen.blit(value_surf, (x + width - 50, y))
    
    # Полоска
    bar_width = width - 120
    bar_height = 12
    bar_x = x + 10
    bar_y = y + 18
    
    # Фон полоски
    pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
    
    # Заполнение (максимум 100)
    fill_width = int(bar_width * min(total / 100, 1))
    pygame.draw.rect(screen, color, (bar_x, bar_y, fill_width, bar_height))
    
    # Бонус от слоя
    if layer != 0:
        bonus_x = bar_x + fill_width
        bonus_width = int(bar_width * min(layer / 100, 1))
        pygame.draw.rect(screen, (100, 100, 100), (bonus_x, bar_y, bonus_width, bar_height))
        
        # Текст бонуса
        bonus_text = f"+{layer}" if layer > 0 else f"{layer}"
        bonus_surf = font.render(bonus_text, True, (200, 200, 200))
        screen.blit(bonus_surf, (bonus_x + 5, bar_y - 2))

def _draw_bonus_bar(screen, x, y, width, name, total, layer, color):
    """Отрисовка полоски бонуса"""
    font = pygame.font.Font(None, 18)
    
    # Название
    name_surf = font.render(name, True, color)
    screen.blit(name_surf, (x + 10, y))
    
    # Значение
    value_text = f"{total}%"
    value_surf = font.render(value_text, True, (255, 255, 255))
    screen.blit(value_surf, (x + width - 50, y))
    
    # Полоска
    bar_width = width - 120
    bar_height = 12
    bar_x = x + 10
    bar_y = y + 18
    
    # Фон
    pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
    
    # Заполнение (от -50 до +50, центр 0)
    if total > 0:
        fill_width = int(bar_width * min(total / 50, 1))
        pygame.draw.rect(screen, color, (bar_x + bar_width//2, bar_y, fill_width, bar_height))
    elif total < 0:
        fill_width = int(bar_width * min(abs(total) / 50, 1))
        pygame.draw.rect(screen, (150, 50, 50), (bar_x + bar_width//2 - fill_width, bar_y, fill_width, bar_height))
    
    # Бонус от слоя
    if layer != 0:
        bonus_text = f"+{layer}%" if layer > 0 else f"{layer}%"
        bonus_surf = font.render(bonus_text, True, (200, 200, 200))
        screen.blit(bonus_surf, (bar_x + bar_width - 30, bar_y - 2))

def _get_layer_stats(player, active_equipment_layer):
    """Получить статы от текущего слоя (вкладки)"""
    from systems.inventory_system import INVENTORY_CONFIG

    layer_stats = {}
    
    # Получаем список слотов для текущей вкладки
    layers = INVENTORY_CONFIG["layers"]
    if active_equipment_layer not in layers:
        return layer_stats
    
    slots = layers[active_equipment_layer]
    
    # Суммируем статы из слотов
    for slot in slots:
        item = player.equipment.slots.get(slot)
        if item and hasattr(item, "stats"):
            for stat, value in item.stats.items():
                layer_stats[stat] = layer_stats.get(stat, 0) + value
        
        # Для брони (resistances)
        if item and hasattr(item, "resistances"):
            for resist_type, value in item.resistances.items():
                stat_name = f"{resist_type}_defense"
                layer_stats[stat_name] = layer_stats.get(stat_name, 0) + value
        
        # Для артефактов
        if item and hasattr(item, "static_bonuses"):
            for resist_type, value in item.static_bonuses.items():
                stat_name = f"{resist_type}_defense"
                layer_stats[stat_name] = layer_stats.get(stat_name, 0) + value
    
    return layer_stats

# ui_inventory_system.py (добавить в конец файла)

def draw_container_panel(screen, container, config):
    """Рисует панель контейнера (сундука) справа от инвентаря"""
    font = pygame.font.SysFont(None, 24)
    
    # Позиция: слева от инвентаря или справа — на твой вкус
    panel_x = config["x"] - 220  # слева от инвентаря
    panel_y = config["y"]
    panel_width = 200
    panel_height = config["rows"] * (config["slot_size"] + config["padding"]) + config["padding"]
    
    # Фон
    pygame.draw.rect(screen, (30, 30, 30), (panel_x, panel_y, panel_width, panel_height))
    pygame.draw.rect(screen, (120, 120, 120), (panel_x, panel_y, panel_width, panel_height), 2)
    
    # Заголовок
    title = font.render(f"Сундук ({container.hp}/{container.max_hp})", True, (255, 255, 255))
    screen.blit(title, (panel_x + 10, panel_y + 10))
    
    # Содержимое
    y_offset = panel_y + 40
    for item in container.inventory:
        text = font.render(f"• {item}", True, (200, 200, 200))
        screen.blit(text, (panel_x + 10, y_offset))
        y_offset += 25