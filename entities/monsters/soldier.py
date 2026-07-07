from .monster import Monster

class SoldierMonster(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            width=40,
            height=40,
            color=(50, 100, 150),
            speed=150,
            max_hp=60,
            resistances={
                "physical": 10,
                "chemical": 0,
                "electric": 5
            }
        )
        self.loot_preset = "soldier"
        self.vision_range = 700
        self.stop_distance = 70