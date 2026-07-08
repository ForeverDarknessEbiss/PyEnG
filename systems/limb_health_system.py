# systems/limb_health_system.py
from loot.limbs.limb import Limb
class LimbHealthSystem:
    """
    Управляет конечностями существа.
    Хранит объекты Limb, управляет здоровьем, предоставляет данные смежным системам.
    """
    
    def __init__(self):
        # limb_id -> Limb
        self.limbs: dict[int, "Limb"] = {}
    
    # ===== УПРАВЛЕНИЕ =====
    
    def add_limb(self, limb: "Limb"):
        """Добавляет конечность."""
        self.limbs[limb.limb_id] = limb
    
    def remove_limb(self, limb_id: int):
        """Удаляет конечность по ID."""
        self.limbs.pop(limb_id, None)
    
    def has_limb(self, limb_id: int) -> bool:
        """Проверяет наличие конечности."""
        return limb_id in self.limbs
    
    # ===== ЗДОРОВЬЕ =====
    
    def damage_limb(self, limb_id: int, amount: int) -> int:
        """Наносит урон. Возвращает остаток HP."""
        limb = self.limbs.get(limb_id)
        if limb:
            return limb.take_damage(amount)
        return 0
    
    def heal_limb(self, limb_id: int, amount: int) -> int:
        """Лечит. Возвращает остаток HP."""
        limb = self.limbs.get(limb_id)
        if limb:
            return limb.heal(amount)
        return 0
    
    def is_destroyed(self, limb_id: int) -> bool:
        """Уничтожена ли конечность."""
        limb = self.limbs.get(limb_id)
        return limb.is_destroyed() if limb else True
    
    # ===== ДОСТУП =====
    
    def get_limb(self, limb_id: int) -> "Limb | None":
        """Возвращает конечность по ID."""
        return self.limbs.get(limb_id)
    
    def get_limb_by_type(self, limb_type: str) -> "Limb | None":
        """Возвращает первую конечность указанного типа (обратная совместимость)."""
        for limb in self.limbs.values():
            if limb.limb_type == limb_type:
                return limb
        return None
    
    def get_all_limbs(self) -> list["Limb"]:
        """Возвращает все конечности."""
        return list(self.limbs.values())
    
    # ===== ДАННЫЕ ДЛЯ EQUIPMENT SYSTEM =====
    
    def get_all_slots_info(self) -> dict[str, int]:
        """
        Собирает информацию о слотах со всех конечностей.
        Возвращает: {"weapon_left": 3, "weapon_right": 1}
        """
        slots = {}
        for limb in self.limbs.values():
            info = limb.get_slot_info()
            if info:
                slot_type, slot_count = info
                slots[slot_type] = slot_count
        return slots
    
    # ===== ОБЩЕЕ HP =====
    
    def get_total_hp(self) -> int:
        return sum(limb.hp for limb in self.limbs.values())
    
    def get_total_max_hp(self) -> int:
        return sum(limb.max_hp for limb in self.limbs.values())
    
    # ===== СОХРАНЕНИЕ =====
    
    def to_dict(self) -> dict:
        return {str(limb_id): limb.to_dict() for limb_id, limb in self.limbs.items()}