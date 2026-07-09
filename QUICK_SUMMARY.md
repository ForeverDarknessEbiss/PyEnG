# 🎯 БЫСТРОЕ РЕЗЮМЕ: СИСТЕМА ЭКИПИРОВКИ

## 📍 ПРЯМЫЕ ОТВЕТЫ НА ВАШИ ВОПРОСЫ

### 1️⃣ Где находится equipment_system и как там определяются слоты (armor slot)?

**📁 Файл**: `systems/equipment_system.py`

```
Класс EquipmentSystem:
├── __init__(player)
│   └── self.slots = {
│       'weapon_primary': None,
│       'weapon_secondary': None,
│       'weapon_melee': None,
│       'armor': None,            ← БРОНЯ СЛОТ
│       'art_1-4': None,          ← АРТЕФАКТЫ
│       'implant_*': None,        ← ИМПЛАНТАТЫ
│       'limbs_*': None           ← КОНЕЧНОСТИ
│   }
├── SLOT_META = {...} — метаинформация о типах слотов
├── equip(item, slot) — надеть предмет
├── unequip(slot) — снять предмет
└── _recalc_stats() — пересчитать бонусы
```

**Слот для брони**: `"armor"` с типом `"armor"`

---

### 2️⃣ Как определяется, является ли объект экипировкой?

**📁 Файл**: `loot/equipments/equipment.py`

```python
class Equipment:
    def __init__(self, ..., equipment_type="armor", ...):
        self.equipment_type = equipment_type  # ← "armor", "artifact", "implant"
        self.name = name
        self.resistances = resistances
```

**Определяется по**:
- Классу: наследует `Equipment` (или проверка `isinstance(item, Equipment)`)
- Атрибуту: `item.equipment_type = "armor"`
- Атрибуту: `item.type = "armor"` (для проверки типа слота)
- Атрибуту: `item.slot = "armor"` (целевой слот)

**База данных**: `loot/equipment_database.py` → `ARMORS` словарь

---

### 3️⃣ Где находится лот-система и как там добавляются предметы в инвентарь?

**📁 Файл**: `systems/loot_system.py`

```
Класс LootSystem:
├── __init__()
│   └── self.items = [] — предметы в мире
├── spawn_item(item, amount, x, y)
│   └── Создает ItemEntity и добавляет в self.items
├── spawn_dropped_item(item, x, y, dx, dy)
│   └── Создает предмет с импульсом (для выброса)
├── generate_loot(monster)
│   └── Генерирует лут от монстра по пресету
└── update(player, delta_time)
    ├── Обновляет физику предметов
    ├── Применяет магнит (притяжение) на 60 пикселей
    └── При dist < 18: player.add_item(item_entity)
```

**Поток добавления в инвентарь**:
```
1. Предмет падает: spawn_item() или generate_loot()
2. Физика обновляется: update()
3. Игрок рядом: вызывается player.add_item(ItemEntity)
4. В Player: self.inventory.add_item(item, amount)
5. В Inventory: добавляется в self.slots[] или происходит стакинг
```

**Файл**: `systems/inventory_system.py` → class `Inventory`

---

### 4️⃣ Где и как работает контекстное меню для предметов?

**📁 Файлы**: 
- Логика: `systems/inventory_system.py`
- Отрисовка: `systems/ui_inventory_system.py`
- Обработка событий: `game.py`

```
ПКМ на предмет (game.py:177)
    ↓
inventory.open_context_menu(slot, player, slot_type)
    ↓
Откуда берутся действия:
├─ Если slot_type == "inventory"
│  └─ Стандартные действия (выброс + экипировка)
└─ Если slot_type == "equipment"
   └─ item.get_actions(player) ← из Equipment класса
    ↓
Отрисовка (draw_context_menu)
    ↓
Клик по кнопке (handle_context_click)
    ↓
Выполнить action["action"]()
```

**Действия для экипировки**:
```python
{
    "name": "Экипировать (armor)",
    "action": lambda: inventory.equip_from_slot(slot_index, player, force_slot="armor")
}
```

---

### 5️⃣ Есть ли функция для надевания брони?

**ДА**, есть несколько способов:

**1️⃣ Прямой вызов EquipmentSystem**:
```python
player.equipment.equip(armor_item, "armor")
```

**2️⃣ Через инвентарь**:
```python
player.inventory.equip_from_slot(slot_index, player, force_slot="armor")
```

**3️⃣ Через Player (для оружия)**:
```python
player.equip_weapon(weapon)  # ← ТОЛЬКО ДЛЯ ОРУЖИЯ
player.replace_weapon(weapon, slot)  # ← ТОЛЬКО ДЛЯ ОРУЖИЯ
```

**❌ ПРОБЛЕМА**: Для брони НЕТ аналога, используется `player.replace_weapon()` 
**По ошибке в Equipment.get_actions()!**

---

## 🔴 ОСНОВНАЯ ПРОБЛЕМА: Почему кнопка "Экипировать" отсутствует?

### ❌ ОШИБКА В ФАЙЛЕ: `loot/equipments/equipment.py` (строка 57)

```python
def get_actions(self, player):
    # ...
    else:
        slots = ["armor"]
        for slot in slots:
            actions.append({
                "name": f"Экипировать ({slot})",
                "action": lambda s=slot: player.replace_weapon(self, s)  # ❌ НЕПРАВИЛЬНО!
            })
```

**Проблема**: `replace_weapon()` — это метод для ОРУЖИЯ, не для брони!

```python
# Текущий метод player.replace_weapon()
def replace_weapon(self, new_weapon, slot):
    """Предназначен только для оружия!"""
    old_weapon = self.equipment.slots.get(slot)
    # ...
    self.equipment.equip(new_weapon, slot)
```

**Почему значения может работать или не работать**:
- Метод СУЩЕСТВУЕТ, поэтому ошибка не выбрасывается
- Но он может не применять правильную проверку типа
- Результат: либо предмет не надевается, либо происходит что-то неожиданное

---

## 🔧 ПРОСТОЕ ИСПРАВЛЕНИЕ (1 СТРОКА)

**Файл**: `loot/equipments/equipment.py` (строка 57)

**ИЗ**:
```python
"action": lambda s=slot: player.replace_weapon(self, s)
```

**В**:
```python
"action": lambda s=slot: player.equipment.equip(self, s)
```

**ВСЕ!** Кнопка начнет работать.

---

## 📊 АРХИТЕКТУРНАЯ ДИАГРАММА

```
┌─────────────────────────────────────────────────────┐
│                   PLAYER                            │
├─────────────────────────────────────────────────────┤
│ inventory: Inventory[20 слотов]                     │
│ equipment: EquipmentSystem                          │
│   └─ slots: {"armor": item, ...}                    │
└─────────────────────────────────────────────────────┘
            ↑                           ↑
            │                           │
   add_item()│                    │equip()
   drop_item()│                    │unequip()
            │                           │
┌───────────┴──────────┐  ┌────────────┴───────────┐
│      INVENTORY       │  │  EQUIPMENT SYSTEM      │
├────────────────────────────────────────────────┤
│                                                 │
│ add_item(item, amount)                         │
│ equip_from_slot(slot_idx, player, force_slot) │
│ unequip_item(item, player)                     │
│ open_context_menu(slot, player, type)         │  
│ handle_context_click(player, mouse_pos)       │
│                                                 │
└────────────────────────────────────────────────┘
            ↑
            │
    ПКМ на предмет (игрок)
    
    ↓ open_context_menu()
    ↓ item.get_actions()
    ↓ draw_context_menu()
    ↓ handle_context_click()
    ↓ action["action"]()
```

---

## 📈 СТАТУС СИСТЕМ

| Система | Статус | Проблема |
|---------|--------|----------|
| Equipment System | ✅ Работает | Нет |
| Loot System | ✅ Работает | Нет |
| Inventory System | ✅ Работает | Нет |
| Context Menu (логика) | ✅ Работает | Нет |
| Context Menu (экипировка брони) | ❌ НЕ работает | `replace_weapon()` вместо `equip()` |
| UI отрисовка | ✅ Работает | Нет |
| Подбор предметов | ✅ Работает | Нет |
| Бросание предметов | ✅ Работает | Нет |

---

## 🎯 КРАТКАЯ ИНСТРУКЦИЯ ПО ИСПРАВЛЕНИЮ

```
1. Откройте: loot/equipments/equipment.py
2. Найдите: строка 57
3. Замените: player.replace_weapon(self, s)
4. На: player.equipment.equip(self, s)
5. Сохраните
6. Перезагрузите игру
7. Тест: ПКМ на броню → должна появиться кнопка "Экипировать"
```

---

## 📚 ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ

см. полные анализы:
- `SYSTEM_ANALYSIS.md` — полный технический анализ
- `FIX_GUIDE.md` — пошаговые инструкции по исправлению
