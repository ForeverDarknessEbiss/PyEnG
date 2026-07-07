# systems/limb_health_system.py
import random

class LimbHealthSystem:
    def __init__(self, player):
        self.player = player
        
        # Структура конечностей
        self.limbs = {
            "head": {"max_hp": 30, "current_hp": 30, "is_broken": False, "name": "Голова"},
            "left_hand": {"max_hp": 25, "current_hp": 25, "is_broken": False, "name": "Левая рука"},
            "right_hand": {"max_hp": 25, "current_hp": 25, "is_broken": False, "name": "Правая рука"},
            "left_leg": {"max_hp": 35, "current_hp": 35, "is_broken": False, "name": "Левая нога"},
            "right_leg": {"max_hp": 35, "current_hp": 35, "is_broken": False, "name": "Правая нога"}
        }
        
        # Отображение слотов экипировки на конечности
        self.slot_to_limb = {
            "limbs_head": "head",
            "limbs_hand_left": "left_hand",
            "limbs_hand_right": "right_hand",
            "limbs_leg_left": "left_leg",
            "limbs_leg_right": "right_leg"
        }
    
    def take_damage(self, target_limb, damage):
        """Нанести урон по конечности"""
        if target_limb not in self.limbs:
            print(f"[LIMB] Неизвестная конечность: {target_limb}")
            return False
        
        limb = self.limbs[target_limb]
        
        # Если конечность уже сломана
        if limb["is_broken"]:
            print(f"[LIMB] {limb['name']} уже сломана, урон перераспределяется")
            self._redistribute_damage(damage)
            return True
        
        # Наносим урон
        old_hp = limb["current_hp"]
        new_hp = old_hp - damage
        limb["current_hp"] = max(0, new_hp)
        
        print(f"[LIMB] {limb['name']}: {old_hp} -> {limb['current_hp']} / {limb['max_hp']}")
        
        # Проверяем, сломалась ли конечность
        if limb["current_hp"] <= 0:
            limb["is_broken"] = True
            print(f"[LIMB] 💀 {limb['name']} сломана!")
            
            # Снимаем экипировку со сломаной конечности
            self._unequip_from_broken_limb(target_limb)
        
        # Обновляем общее здоровье игрока
        self._update_player_health()
        
        return True
    
    def _redistribute_damage(self, damage):
        """Перераспределяет 50% урона по оставшимся конечностям"""
        # Берем 50% от урона
        redistributed_damage = damage // 2
        
        if redistributed_damage <= 0:
            return
        
        # Собираем здоровые конечности
        healthy_limbs = []
        for limb_id, limb in self.limbs.items():
            if not limb["is_broken"]:
                healthy_limbs.append(limb_id)
        
        if not healthy_limbs:
            print("[LIMB] Все конечности сломаны!")
            return
        
        # Равномерно распределяем урон
        damage_per_limb = redistributed_damage // len(healthy_limbs)
        remainder = redistributed_damage % len(healthy_limbs)
        
        for i, limb_id in enumerate(healthy_limbs):
            damage_to_apply = damage_per_limb + (1 if i < remainder else 0)
            if damage_to_apply > 0:
                self.take_damage(limb_id, damage_to_apply)
    
    def _unequip_from_broken_limb(self, limb_id):
        """Снимает экипировку со сломанной конечности"""
        # Находим слот экипировки, соответствующий конечности
        equipment_slot = None
        for slot, limb in self.slot_to_limb.items():
            if limb == limb_id:
                equipment_slot = slot
                break
        
        if equipment_slot:
            item = self.player.equipment.slots.get(equipment_slot)
            if item:
                print(f"[LIMB] Снимаем {item.name} со сломанной {self.limbs[limb_id]['name']}")
                self.player.equipment.unequip(equipment_slot)
                self.player.inventory.add_item(item, 1)
    
    def _update_player_health(self):
        """Обновляет общее здоровье игрока (сумма HP конечностей)"""
        total_health = 0
        for limb in self.limbs.values():
            total_health += limb["current_hp"]
        
        self.player.max_health = total_health
        self.player.health = min(self.player.health, total_health)
        
        # Если здоровье игрока упало до 0
        if self.player.health <= 0:
            print("[PLAYER] 💀 Игрок погиб!")
    
    def get_limb_by_slot(self, slot_name):
        """Получить ID конечности по слоту экипировки"""
        return self.slot_to_limb.get(slot_name)
    
    def get_limb_status(self):
        """Вернуть статус всех конечностей для отладки"""
        status = {}
        for limb_id, limb in self.limbs.items():
            status[limb_id] = {
                "name": limb["name"],
                "hp": f"{limb['current_hp']}/{limb['max_hp']}",
                "broken": limb["is_broken"]
            }
        return status