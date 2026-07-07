from .monster import Monster

class AggressiveMonster(Monster):

    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            width=40, #
            height=40,
            color=(200, 0, 0),
            speed=80, # скорость
            max_hp=120, # макс хп
            resistances={
                "physical": 10,
                "chemical": 5,
                "electric": 0
            }
        )

        self.loot_preset = "aggressive"
        self.vision_range = 400 # дальность видимости
        self.stop_distance = 60 # дистанция сближения 
        # отрицательные значения в параграфе резистов приведут к повышению полученного урона (уязвимости к урону)