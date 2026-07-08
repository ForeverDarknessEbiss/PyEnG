from .monster import Monster

class RatteMonster(Monster):

    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            width=40, 
            height=20,
            color=(100, 100, 100),
            speed=200, # скорость
            max_hp=20, # макс хп
            resistances={
                "physical": 0,
                "chemical": 5,
                "electric": 0
            }
        )

        self.loot_preset = "ratte" 

        self.vision_range = 600 # дальность видимости
        self.stop_distance = 55 # дистанция сближения менее 50 приводит к сдвигу персонажа
        # отрицательные значения в параграфе резистов приведут к повышению полученного урона (уязвимости к урону)