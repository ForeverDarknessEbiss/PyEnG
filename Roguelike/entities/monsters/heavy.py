from .monster import Monster

class HeavyMonster(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            width=50,
            height=50,
            color=(80, 80, 100),
            speed=80,
            max_hp=150,
            resistances={
                "physical": 20,
                "chemical": 10,
                "electric": -5
            }
        )
        self.loot_preset = "heavy"
        self.vision_range = 600
        self.stop_distance = 90