class Ammo:
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

# имя_AMMO = Ammo("калибр", от , до , 
#                   stackable= True, is_unique= False,
#                     color=(50, 100, 150),
#                       description="" )

PISTOL_AMMO = Ammo("9mm", 5, 10, 
                   stackable= True, is_unique= False,
                     color=(50, 100, 150),
                       description="патроны 9mm, мелкокалиберный мусор но что поделать" )

RIFLE_AMMO = Ammo("5.56", 5, 15,
    stackable=True, is_unique=False,
    color=(100, 150, 200),
    description="Стандартный винтовочный патрон. Универсальный.")

SHOTGUN_SHELL = Ammo("12g", 2, 6,
    stackable=True, is_unique=False,
    color=(200, 100, 50),
    description="Дробовик. Мощный на ближней дистанции против кожаных тварей.")

ENERGY_CELL = Ammo("energy_cell", 1, 3,
    stackable=True, is_unique=False,
    color=(50, 200, 200),
    description="Ячейка энергии. Используется в энергооружии.")

MAGNUM_AMMO = Ammo(".44", 3, 8,
    stackable=True, is_unique=False,
    color=(200, 150, 50),
    description="Крупнокалиберный патрон. Высокий урон - высокая цена.")

HEAVY_AMMO = Ammo("7.62", 5, 12,
    stackable=True, is_unique=False,
    color=(180, 100, 80),
    description="Тяжёлый винтовочный патрон. В крайнем случа его можно кинуть в кого-то.")