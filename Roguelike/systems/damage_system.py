class DamageSystem:

    def calculate_damage(self, attack, defense):

        total_damage = 0

        # физ урон
        if "physical" in attack:
            phys = attack["physical"]
            resist = defense.get("physical", 0)

            total_damage += phys * (1 - resist / 100)

        # хим урон
        if "chemical" in attack:
            chem = attack["chemical"]
            resist = defense.get("chemical", 0)

            total_damage += chem * (1 - resist / 100)

        # электрический
        if "electric" in attack:
            elec = attack["electric"]
            resist = defense.get("electric", 0)

            total_damage += elec * (1 - resist / 100)

        # термальный 
        if "fire" in attack:
            fire = attack["fire"]
            resist = defense.get("fire", 0)

            total_damage += fire * (1 - resist / 100)


        return total_damage