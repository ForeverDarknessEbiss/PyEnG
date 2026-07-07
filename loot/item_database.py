# loot/item_database.py



class LootItem:
    def __init__(
            self,
            name,
            min_count=1,
            max_count=3,
            is_unique=False,
            color=(255, 255, 255),
            description="Нет описания",
            stackable=None
        ):
            self.name = name
            self.min_count = min_count
            self.max_count = max_count
            self.is_unique = is_unique # это автоматoм делает скакаемость Folse
           
            # is_unique=True  → stackable=False
            # is_unique=False → stackable=True
            self.color = color
            self.description = description

            if stackable is None:  # стакаемость 
                self.stackable = not is_unique  # дефолтная логика 
            else:
                self.stackable = stackable  #переопределение

# __ПРИМЕР ЕСЛИ ЗАБУДУ = КЛАСС("ИМЯ", МИН.ВЫПАДЕНИЕ,
#                              МАКС.ВЫПАДЕНИЕ,ЦВЕТ,
#                              ОПИСАНИЕ, СТАКАЕМОСТЬ, УНИКАЛЬНОСТЬ) ОТСУТСТВИЕ ПАРАМЕТРА ЗАДАЕТ ДЭФОЛТНЫЙ ПАРАМЕТР


# --- КОМПОНЕНТЫ ---
COMPONENTS = LootItem("components", 1, 30,
    color=(100, 200, 255),
    description="Используется для крафта") # пример актуального предмета 

ELECTRONICS = LootItem("electronics", 1, 30,
    is_unique=True,
    color=(200, 100, 100),)

MECHANICAL_PART = LootItem("mechanical_part", 1, 20)

# --- ЧАСТИ ТЕЛА ---
LEFT_LEG = LootItem("left_leg", 1, 1,
    is_unique=True,
    color=(200, 100, 100),
    description="Чья-то левая нога...")

RIGHT_LEG = LootItem("right_leg", 1, 1, is_unique=True)

SPINE = LootItem("spine", 1, 1, is_unique=True)

# --- ТЕХНО ---
PROCESSOR = LootItem("processor", 1, 1, 
    is_unique=True,
    color=(150, 255, 150),
    description="Мозг машины...мой мозг")

SSD = LootItem("ssd", 1, 2)

# --- МЕТАЛЛОЛОМ И ДЕТАЛИ ---
SCRAP_METAL = LootItem("scrap_metal", 5, 20,
    stackable=True,
    color=(120, 120, 120),
    description="Обломки металла. Пригодятся для ремонта.")

BOLTS = LootItem("bolts", 3, 12,
    stackable=True,
    color=(150, 130, 100),
    description="Винты и гайки. Всегда нужны.")

SPRING = LootItem("spring", 1, 5,
    stackable=True,
    color=(180, 160, 100),
    description="Пружина. Хранит энергию удара.")

GEAR_SMALL = LootItem("gear_small", 1, 6,
    stackable=True,
    color=(200, 180, 80),
    description="Маленькая шестерёнка.")

GEAR_LARGE = LootItem("gear_large", 1, 3,
    stackable=False,
    color=(210, 190, 70),
    description="Большая шестерёнка. Тяжёлая, не складывается, логично.")

LIVING_GEAR = LootItem("living_gear", 1, 1,
    stackable=False,
    color=(50, 200, 50),
    description="Живая шестерёнка. Пульсирует. Главное не ложить их вместе, ато провернут рюкзак наизнанку.")

# --- ЭЛЕКТРОНИКА ---
WIRE = LootItem("wire", 2, 10,
    stackable=True,
    color=(200, 150, 50),
    description="Медный провод. Для электрики.")

CAPACITOR = LootItem("capacitor", 1, 4,
    stackable=True,
    color=(100, 150, 200),
    description="Конденсатор. Накопляет энергию.")

TRANSISTOR = LootItem("transistor", 1, 3,
    stackable=True,
    color=(80, 120, 180),
    description="Транзистор. Основа микросхем.")

MICROCHIP = LootItem("microchip", 1, 2,
    stackable=True,
    color=(50, 200, 150),
    description="Микрочип. Кусочек моего мозга...конкретно этот - не моего...")

BROKEN_CPU = LootItem("broken_cpu", 1, 1,
    stackable=True,
    color=(200, 100, 100),
    description="Сгоревший процессор. Можно разобрать на детали.")

# --- ЖИВЫЕ КОМПОНЕНТЫ ---
ORGANIC_CIRCUIT = LootItem("organic_circuit", 1, 1,
    stackable=False,
    color=(100, 200, 100),
    description="Органическая плата. Да что здесь происходит ?!.")

NERVE_FIBER = LootItem("nerve_fiber", 2, 5,
    stackable=True,
    color=(180, 100, 200),
    description="Нервные волокна. Чувствительные.")

BIO_GEL = LootItem("bio_gel", 1, 3,
    stackable=True,
    color=(50, 200, 100),
    description="Биогель. Восстанавливает ткани.")

CORE_EYE = LootItem("core_eye", 1, 1,
    stackable=False,
    color=(255, 100, 100),
    description="Глаз-процессор. Он моргнул когда я его взял")

# --- ДВИГАТЕЛИ И ПРИВОДЫ ---
SERVO = LootItem("servo", 1, 3,
    stackable=True,
    color=(150, 100, 50),
    description="Сервопривод. Ловкость серворук и никакого мошенничества.")

MOTOR_SMALL = LootItem("motor_small", 1, 2,
    stackable=True,
    color=(120, 80, 40),
    description="Моторчик. Для лёгких механизмов.")

MOTOR_HEAVY = LootItem("motor_heavy", 1, 1,
    stackable=False,
    color=(80, 60, 30),
    description="Тяжёлый мотор. Для больших машин.")

HYDRAULIC_CYLINDER = LootItem("hydraulic_cylinder", 1, 1,
    stackable=False,
    color=(200, 100, 50),
    description="Гидроцилиндр. Мощный толкатель.")

# --- РЕДКИЕ МАТЕРИАЛЫ ---
CARBON_PLATE = LootItem("carbon_plate", 1, 2,
    stackable=True,
    color=(80, 80, 100),
    description="Карбоновая пластина. Лёгкая и прочная.")

TITANIUM_ROD = LootItem("titanium_rod", 1, 2,
    stackable=True,
    color=(150, 150, 180),
    description="Титановый стержень.")

NANOTUBE = LootItem("nanotube", 1, 1,
    stackable=True,
    color=(100, 200, 200),
    description="Нанотрубка. Сверхпрочная.")

PORTABLE_REACTOR = LootItem("portable_reactor", 1, 1,
    stackable=False,
    color=(255, 100, 255),
    description="Портативный термоядерный реактор. Компактный источник энергии." \
    " В случае исполнения дерективы об самоуничтожении, разблокировать внешний магнитный контур.")

BATTERY_PACK = LootItem("battery_pack", 1, 1,
    stackable=False,
    color=(200, 200, 100),
    description="Блок мощных батарей. Тяжело, примитивно, энергоёмко .")