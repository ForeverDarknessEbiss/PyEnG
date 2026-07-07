from systems.ai_system import AISystem
from systems.movement_system import MovementSystem
from systems.collision_system import CollisionSystem

class MonsterManager:
    def __init__(self):
        """
        Инициализация менеджера монстров.
        Здесь мы создаём список для хранения всех монстров.
        """
        self.all_monsters = []
        self.ai_system = AISystem()
        self.movement_system = MovementSystem()
        self.collision_system = CollisionSystem()


    def spawn_monster(self, monster):
        """
        Добавление нового монстра в список.
        :param monster: экземпляр монстра (например, AggressiveMonster)
        """
        self.all_monsters.append(monster)

    def update_all(self, player, game_map, delta_time):
        monsters = self.all_monsters

        self.collision_system.resolve_monster_monster(monsters)
        self.ai_system.update(monsters, player)        
        # 🆕 Правильно: передаём каждого монстра отдельно
        for monster in monsters:
            self.movement_system.update_monster(monster, delta_time)        
        self.collision_system.resolve_player_monsters(player, monsters)

    def draw_all(self, screen, camera):
        """
        Отрисовка всех монстров.
        :param screen: поверхность, на которой рисуем
        :param camera: камера, чтобы отрисовать относительно видимой области
        """
        for monster in self.all_monsters:
            monster.draw(screen, camera)

    def remove_dead(self, loot_system):

        import random

        for monster in self.all_monsters[:]:

            if not monster.alive:


                # --- ДРОП ЛУТА ---
                loot = loot_system.generate_loot(monster)

                for item, amount in loot:
                    loot_system.spawn_item(item, amount, monster.x, monster.y)

                # --- ДРОП ОПЫТА ---
                for i in range(3):
                    loot_system.spawn_xp(
                        monster.x + random.randint(-10, 10),
                        monster.y + random.randint(-10, 10),
                        value=1
                    )

                # --- УДАЛЕНИЕ ---
                self.all_monsters.remove(monster)
                print(f"[DEAD] {monster.__class__.__name__} умер, генерируем лут")