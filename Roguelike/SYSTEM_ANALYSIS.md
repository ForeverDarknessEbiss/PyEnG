# 🎮 Полный анализ системы экипировки, лута и контекстного меню

## 📋 Оглавление
1. [Архитектура системы](#архитектура-системы)
2. [Данные и определения](#данные-и-определения)
3. [Как работает экипировка](#как-работает-экипировка)
4. [Как работает лут](#как-работает-лут)
5. [Как работает контекстное меню](#как-работает-контекстное-меню)
6. **[⚠️ НАЙДЕННЫЕ ПРОБЛЕМЫ](#найденные-проблемы)**

---

## Архитектура системы

### Компоненты системы:

```
┌─ systems/equipment_system.py
│  └─ EquipmentSystem (инициализируется в Player)
│     └─ slots = {weapon_primary, weapon_secondary, armor, implants, artifacts, limbs...}
│
├─ systems/inventory_system.py
│  ├─ Inventory (инициализируется в Player)
│  │  └─ slots[20] — слоты для предметов
│  └─ InventoryItem (обертка: item + amount)
│
├─ systems/loot_system.py
│  ├─ LootSystem (инициализируется в game.py)
│  └─ spawn_item(), spawn_dropped_item(), generate_loot()
│
├─ systems/ui_inventory_system.py
│  ├─ draw_inventory() — рисует слоты инвентаря
│  ├─ draw_equipment() — рисует слоты экипировки
│  ├─ draw_context_menu() — рисует контекстное меню
│  └─ draw_equipment_tabs() — рисует вкладки
│
├─ loot/item_entity.py
│  └─ ItemEntity (предмет в мире с физикой)
│
├─ loot/equipments/equipment.py
│  └─ Equipment (базовый класс для экипировки)
│     └─ get_actions() — возвращает действия для контекстного меню
│
├─ loot/equipment_database.py
│  └─ ARMORS = {...} — таблица доспехов
│
└─ entities/player.py
   └─ Player
      ├─ equipment = EquipmentSystem()
      ├─ inventory = Inventory()
      ├─ equip_weapon()
      ├─ equip_to_slot()
      ├─ replace_weapon()
      ├─ add_item()
      ├─ drop_item()
      ├─ drop_equipped_item()
      └─ drop_item_by_reference()
```

---

## Данные и определения

### 1. Определение слотов экипировки (Equipment System)

**Файл**: `systems/equipment_system.py` (строки 1-22)

```python
class EquipmentSystem:
    def __init__(self, player):
        self.slots = {
            "weapon_primary": None,      # Основное оружие
            "weapon_secondary": None,    # Вспомогательное оружие
            "weapon_melee": None,        # Ближнее оружие
            "armor": None,               # 🔥 БРОНЯ ЗДЕСЬ
            "art_1": None,               # Артефакты
            "art_2": None,
            "art_3": None,
            "art_4": None,
            "implant_head_1": None,      # Имплантаты головы
            "implant_head_2": None,
            # ... и т.д.
        }
```

**Метаинформация слотов** (SLOT_META):
```python
SLOT_META = {
    "armor": {"layer": "armor", "type": "armor"},  # Это ключевой параметр!
    "weapon_primary": {"layer": "weapons", "type": "weapon"},
    # ...
}
```

### 2. Как определяется, является ли объект экипировкой

**Файл**: `loot/equipments/equipment.py`

```python
class Equipment:
    def __init__(self, name, resistances, equipment_type="armor", ...):
        self.name = name
        self.resistances = resistances
        self.equipment_type = equipment_type  # ← Тип: "armor", "artifact", "implant"
        self.color = color
        # ...
```

**База данных предметов**:
```python
# loot/equipment_database.py
ARMORS = {
    "base_armor": {
        "name": "base armor",
        "resistances": {"physical": 10, "fire": 2, ...},
        "equipment_type": "armor",
        "description": "дешманская броня"
    }
}
```

**Фабрика создания**:
```python
# loot/equipments/armor_factory.py
def create_equipments(armor_id):
    data = ARMORS.get(armor_id)
    if not data:
        raise ValueError(f"armor '{armor_id}' not found")
    return Equipment(**data)  # ← Создает объект Equipment
```

---

## Как работает экипировка

### Основные методы экипировки

**1. `EquipmentSystem.equip(item, slot)` — надеть предмет**
```python
# systems/equipment_system.py:78-87
def equip(self, item, slot):
    if slot not in self.slots:
        return False
    
    if self.slots[slot]:  # Если уже что-то надето
        self.unequip(slot)  # Снимаем
    
    self.slots[slot] = item  # Надеваем новое
    self._recalc_stats()
    return True
```

**2. `Player.equip_to_slot(item, slot_name)` — проверка типа и экипировка**
```python
# entities/player.py:65-82
def equip_to_slot(self, item, slot_name):
    slot_meta = self.equipment.SLOT_META.get(slot_name)
    
    if not slot_meta:
        return False
    
    # 🔥 Проверка типа предмета
    if "type" in slot_meta:
        if getattr(item, "type", None) != slot_meta["type"]:
            print(f"❌ нельзя вставить {item} в {slot_name}")
            return False
    
    # Если старый предмет есть — вернуть в инвентарь
    old_item = self.equipment.slots.get(slot_name)
    if old_item:
        self.inventory.add_item(old_item)
    
    self.equipment.equip(item, slot_name)
    return True
```

**3. `Player.replace_weapon(new_weapon, slot)` — специально для оружия**
```python
# entities/player.py:96-102
def replace_weapon(self, new_weapon, slot):
    old_weapon = self.equipment.slots.get(slot)
    
    if old_weapon:
        self.inventory.add_item(old_weapon)
    
    self.equipment.equip(new_weapon, slot)
```

### Проблема: Отсутствие `equip_to_equipment_slot()`

Для брони нужен метод, подобный `equip_to_slot()`, но **он использует проверку типа**.
Однако в Equipment классе НЕ задан атрибут `type`!

---

## Как работает лут

### Система спавна предметов

**1. Спавн предмета в мире** (`loot_system.py:121-140`):
```python
def spawn_item(self, item, amount, x, y):
    # Если это кортеж ("weapon", weapon_id) или ("armor", armor_id)
    if isinstance(item, tuple):
        item_type = item[0]
        item_data = item[1]
        
        if item_type == "weapon":
            from weapons.weapon_factory import create_weapon
            item = create_weapon(item_data)
        elif item_type == "armor":
            from loot.equipments.armor_factory import create_equipments
            item = create_equipments(item_data)  # ← Создается Equipment
    
    for _ in range(amount):
        entity = ItemEntity(x, y, item, 1)  # ← Создается ItemEntity с physics
        self.items.append(entity)
```

**2. Физика и подбор** (`loot_system.py:65-89`):
```python
def update(self, player, delta_time):
    for item in self.items[:]:
        dx = px - item.x
        dy = py - item.y
        dist = math.hypot(dx, dy)
        
        # Магнит (притяжение) на расстояние 60 пикселей
        if dist < 60 and item.pickup_delay <= 0:
            item.vx = (dx / dist) * 320
            item.vy = (dy / dist) * 320
        
        # Подбор предмета (если ближайностью < 18 пикселей)
        if dist < 18 and item.pickup_delay <= 0:
            player.add_item(item)  # ← ItemEntity передается сюда
            self.items.remove(item)
```

**3. Добавление в инвентарь** (`entities/player.py:156-162`):
```python
def add_item(self, item_entity):
    item = item_entity.item        # ← Вытаскиваем Equipment объект
    amount = item_entity.amount
    
    success = self.inventory.add_item(item, amount)  # ← Добавляем Equipment
    
    if success:
        print(f"🎁 В инвентарь: {item.name} x{amount}")
```

**4. Бросание предмета** (`entities/player.py:194-217`):
```python
def drop_item_by_reference(self, item):
    """Выбросить предмет по ссылке (используется из контекстного меню)"""
    for i, slot in enumerate(self.inventory.slots):
        if slot and slot.item == item:
            self.drop_item(i, self.loot_system)
            return True
    return False
```

---

## Как работает контекстное меню

### Открытие контекстного меню (ПКМ)

**В game.py** (строка 177):
```python
elif event.button == 3:  # ПКМ
    print("[DEBUG] ПКМ")
    if ui_layer == "inventory" and hovered_slot is not None:
        # Вызвать открытие меню
        player.inventory.open_context_menu(
            hovered_slot,
            player,
            slot_type=hovered_type  # "inventory" или "equipment"
        )
```

### Метод `Inventory.open_context_menu()` 

**Файл**: `systems/inventory_system.py:214-267`

```python
def open_context_menu(self, slot_data, player, slot_type="inventory"):
    
    # Получаем предмет
    if slot_type == "inventory":
        item = self.slots[slot_data].item
    elif slot_type == "equipment":
        item = player.equipment.slots.get(slot_data)
    
    # Формируем действия
    if slot_type == "inventory":
        actions = [{"name": "Выбросить", ...}]
        
        # Добавляем кнопки экипировки для всех доступных слотов
        if isinstance(item, Weapon):
            equip_slots = ["weapon_primary", "weapon_secondary"]
        elif hasattr(item, "slot"):
            equip_slots = [item.slot]
        
        for slot_name in equip_slots:
            actions.append({
                "name": f"Экипировать ({slot_name})",
                "action": lambda s=slot_name: self.equip_from_slot(slot_data, player, force_slot=s)
            })
    
    elif slot_type == "equipment":
        # 🔥 ДЛЯ ЭКИПИРОВАННОГО ПРЕДМЕТА НУЖЕН МЕТОД get_actions()
        if not hasattr(item, 'get_actions'):
            print(f"[ERROR] {item} (тип: {type(item)}) не имеет get_actions")
            return
        actions = item.get_actions(player)
    
    self.context_menu = {
        "item": item,
        "actions": actions,
        "position": pygame.mouse.get_pos(),
        "slot_data": slot_data,
        "slot_type": slot_type
    }
```

### Отрисовка контекстного меню

**Файл**: `systems/ui_inventory_system.py:360-389`

```python
def draw_context_menu(screen, inventory):
    menu = getattr(inventory, "context_menu", None)
    if not menu:
        return
    
    font = pygame.font.Font(None, 28)
    x, y = menu["position"]
    
    width = 220
    height = 40 * len(menu["actions"])
    
    # Рисуем прямоугольник
    pygame.draw.rect(screen, (20, 20, 20), (x, y, width, height))
    
    # Рисуем кнопки действий
    buttons = []
    for i, action in enumerate(menu["actions"]):
        btn_rect = pygame.Rect(x, y + i * 40, width, 40)
        pygame.draw.rect(screen, (60, 60, 60), btn_rect)
        
        text = font.render(action["name"], True, (255, 255, 255))
        screen.blit(text, (btn_rect.x + 10, btn_rect.y + 10))
        
        buttons.append((btn_rect, action))
    
    inventory.context_buttons = buttons
```

### Клик по контекстному меню

**В game.py** (строка 151):
```python
if ui_layer == "context_menu":
    clicked = player.inventory.handle_context_click(player, mouse_pos)
    if not clicked:
        player.inventory.context_menu = None
```

**Метод** (`inventory_system.py:273-299`):
```python
def handle_context_click(self, player, mouse_pos):
    if not hasattr(self, "context_buttons"):
        return
    
    for rect, action in self.context_buttons:
        if rect.collidepoint(mouse_pos):
            # Выполнить действие
            action["action"]()
            
            # Удалить предмет из слота (если нужно)
            if self.context_menu:
                slot_data = self.context_menu["slot_data"]
                slot_type = self.context_menu["slot_type"]
                
                if slot_type == "inventory":
                    self.slots[slot_data] = None
                elif slot_type == "equipment":
                    player.equipment.unequip(slot_data)
            
            # Закрыть меню
            self.context_menu = None
            return True
    return False
```

---

## ⚠️ НАЙДЕННЫЕ ПРОБЛЕМЫ

### 🔴 КРИТИЧЕСКАЯ ПРОБЛЕМА 1: Ошибка в `Equipment.get_actions()`

**Файл**: `loot/equipments/equipment.py:36-60`

**Проблемный код**:
```python
def get_actions(self, player):
    actions = []
    
    # проверяем, надет ли предмет
    equipped_slot = None
    for slot, item in player.equipment.slots.items():
        if item == self:
            equipped_slot = slot
            break
    
    if equipped_slot:
        # если уже надето — кнопка "Снять"
        actions.append({
            "name": "Снять",
            "action": lambda: player.inventory.unequip_item(self, player)
        })
    else:
        # если не надето — выбор слота
        slots = ["armor"]
        for slot in slots:
            actions.append({
                "name": f"Экипировать ({slot})",
                "action": lambda s=slot: player.replace_weapon(self, s)  # ❌ ОШИБКА!
            })
    
    actions.append({
        "name": "Выбросить",
        "action": lambda: player.drop_equipped_item(self)
    })
    
    return actions
```

**Проблема**: Вызывается `player.replace_weapon()`, но этот метод предназначен ТОЛЬКО для оружия!

**Почему это проблема**:
- `replace_weapon()` работает только с оружейными слотами
- Для брони нужно вызвать `player.equipment.equip(self, slot)` напрямую
- Или создать метод `player.equip_to_slot()` для не-оружейных предметов

**Решение**:
```python
def get_actions(self, player):
    actions = []
    
    equipped_slot = None
    for slot, item in player.equipment.slots.items():
        if item == self:
            equipped_slot = slot
            break
    
    if equipped_slot:
        actions.append({
            "name": "Снять",
            "action": lambda: player.inventory.unequip_item(self, player)
        })
    else:
        # ✅ Правильно: использовать equip() напрямую
        slots = ["armor"]
        for slot in slots:
            actions.append({
                "name": f"Экипировать ({slot})",
                "action": lambda s=slot: player.equipment.equip(self, s)  # ✅ ИСПРАВЛЕНО
            })
    
    actions.append({
        "name": "Выбросить",
        "action": lambda: player.drop_equipped_item(self)
    })
    
    return actions
```

### 🔴 ПРОБЛЕМА 2: Отсутствие атрибута `slot` в Equipment

**Файл**: `loot/equipments/equipment.py`

В классе Equipment нет атрибута `slot`, который используется в `inventory_system.py:240`:
```python
elif hasattr(item, "slot"):
    equip_slots = [item.slot]
```

**Решение**: Добавить атрибут в Equipment:
```python
def __init__(self, ..., slot=None):
    self.slot = slot  # "armor" для брони
```

Или в `equipment_database.py`:
```python
ARMORS = {
    "base_armor": {
        "name": "base armor",
        "slot": "armor",  # ← Добавить это
        "resistances": {"physical": 10, ...},
        ...
    }
}
```

### 🟡 ПРОБЛЕМА 3: Проверка типа в `equip_to_slot()`

**Файл**: `entities/player.py:65-82`

```python
def equip_to_slot(self, item, slot_name):
    slot_meta = self.equipment.SLOT_META.get(slot_name)
    
    # 🔥 Проверка типа
    if "type" in slot_meta:
        if getattr(item, "type", None) != slot_meta["type"]:
            print(f"❌ нельзя вставить {item} в {slot_name}")
            return False
```

**Проблема**: Equipment объект не имеет атрибута `type`!

**Решение**: Добавить в Equipment:
```python
def __init__(self, ..., equipment_type="armor"):
    self.type = equipment_type  # Используется в проверке типа
```

Или просто добавить `item.equipment_type` вместо `item.type`:
```python
if getattr(item, "equipment_type", None) != slot_meta["type"]:
```

---

## 📊 Диаграмма потока экипировки брони

### Текущий (НЕРАБОТАЮЩИЙ) поток:

```
1. ПКМ на броню в инвентаре
   ↓
2. inventory.open_context_menu("inventory", player, hovered_slot)
   ↓
3. Получаем item = self.slots[hovered_slot].item
   ↓
4. Проверяем: isinstance(item, Weapon)? НЕТ
5. Проверяем: hasattr(item, "slot")? 
   ├─ Если НЕТ → кнопка "Экипировать" не добавляется ❌
   └─ Если ДА → добавляем кнопку
   ↓
6. Пользователь нажимает "Экипировать (armor)"
   ↓
7. inventory.equip_from_slot(slot_index, player, force_slot="armor")
   ↓
8. ✅ Вызывается player.equipment.equip(item, "armor")
   ✅ РАБОТАЕТ ДЛЯ ИНВЕНТАРЯ
```

### Поток для ЭКИПИРОВАННОЙ брони:

```
1. ПКМ на экипированную броню в слоте equipment
   ↓
2. inventory.open_context_menu("equipment", player, slot_name="armor")
   ↓
3. Получаем item = player.equipment.slots.get("armor")
   ↓
4. Вызываем item.get_actions(player)
   ↓
5. В Equipment.get_actions():
   ├─ Проверяем equipped_slot: ДА, наделась
   ├─ Добавляем кнопку "Снять"
   ├─ Проверяем else: НЕТ (уже наделась)
   └─ Добавляем кнопку "Выбросить"
   ↓
6. Контекстное меню показывает "Снять" и "Выбросить"
   ↓
7. Пользователь нажимает "Выбросить"
   ├─ Вызывается player.drop_equipped_item(item) ✓
   └─ Предмет выбрасывается в мир ✓
```

---

## 🎯 Итоговая сводка

### ✅ ЧТО РАБОТАЕТ:
1. **Система слотов экипировки** — определена корректно
2. **Добавление предметов в инвентарь** — работает (`add_item()`)
3. **Подбор предметов** — физика и магнит работают
4. **Бросание предметов** — `drop_equipped_item()` работает
5. **Снятие брони** — работает через `unequip_item()`
6. **Отрисовка контекстного меню** — работает
7. **Экипировка оружия** — работает через `replace_weapon()`

### ❌ ЧТО НЕ РАБОТАЕТ:
1. **Экипировка брони через контекстное меню** — `replace_weapon()` вызывается вместо `equip()`
2. **Распознание типа экипировки** — нет атрибута `type` в Equipment
3. **Атрибут `slot` в Equipment** — не задаётся при создании

### 🔧 НУЖНО ИСПРАВИТЬ:
1. В `loot/equipments/equipment.py`: заменить `replace_weapon()` на `equipment.equip()`
2. В `loot/equipments/equipment.py`: добавить атрибуты `type` и `slot`
3. В `loot/equipment_database.py`: добавить `slot` при определении брони
