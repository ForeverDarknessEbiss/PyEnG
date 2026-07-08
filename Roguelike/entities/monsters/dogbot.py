from .monster import Monster

class DogbotMonster(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            width=20,
            height=30,
            color=(228, 0, 228),
            speed=200,
            max_hp=50,
            resistances={
                "physical": 10,
                "chemical": 10,
                "electric": -5
            }
        )
        self.loot_preset = "dogbot"
        self.vision_range = 600
        self.stop_distance = 150