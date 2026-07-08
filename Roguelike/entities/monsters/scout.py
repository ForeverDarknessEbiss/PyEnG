from .monster import Monster

class ScoutMonster(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            width=30,
            height=30,
            color=(150, 150, 50),
            speed=300,
            max_hp=30,
            resistances={
                "physical": 5,
                "chemical": 5,
                "electric": 10
            }
        )
        self.loot_preset = "scout"
        self.vision_range = 800
        self.stop_distance = 60