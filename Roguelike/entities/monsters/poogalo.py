from .monster import Monster

class PoogaloMonster(Monster):

    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            width=40, #
            height=40,
            color=(0, 0, 155),
            speed=0, # скорость
            max_hp=12000, # макс хп
            resistances={
                "physical": 0,
                "chemical": 5,
                "electric": 0
            }
        )

        self.vision_range = 400 # дальность видимости
        self.stop_distance = 60 # дистанция сближения 
        # отрицательные значения в параграфе резистов приведут к повышению полученного урона (уязвимости к урону)