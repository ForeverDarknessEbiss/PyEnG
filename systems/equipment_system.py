# systems/equipment_system.py
from systems.limb_health_system import LimbHealthSystem
class EquipmentSystem:
    """
    Управляет слотами экипировки.
    Слоты создаются динамически на основе данных из LimbHealthSystem.
    """
    
    def __init__(self):
        # slot_id -> equipped_item
        self.slots: dict[str, object | None] = {}
    
    # ===== СОЗДАНИЕ СЛОТОВ ИЗ LIMB SYSTEM =====
    
    def update_slots_from_limbs(self, limb_health_system: "LimbHealthSystem"):
        """
        Обновляет ТОЛЬКО слоты оружия на основе конечностей.
        Не трогает слоты limbs_*, implant_*, art_* и т.д.
        """
        slots_info = limb_health_system.get_all_slots_info()
        
        # Удаляем только старые слоты оружия
        weapon_slots_to_remove = [sid for sid in self.slots if sid.startswith("weapon_")]
        for sid in weapon_slots_to_remove:
            del self.slots[sid]
        
        # Создаём новые слоты оружия
        for slot_type, slot_count in slots_info.items():
            for i in range(slot_count):
                if slot_count > 1:
                    slot_id = f"{slot_type}_{i}"
                else:
                    slot_id = slot_type
                self.slots[slot_id] = None
    
    # ===== РАБОТА СО СЛОТАМИ =====
    
    def equip(self, slot_id: str, item) -> bool:
        print(f"[EQUIP] trying slot={repr(slot_id)}, in slots={slot_id in self.slots}")
        print(f"[EQUIP] all slots: {list(self.slots.keys())}")
        if slot_id in self.slots:
            self.slots[slot_id] = item
            return True
        return False
    
    def unequip(self, slot_id: str):
        """
        Убирает предмет из слота.
        Возвращает предмет или None.
        """
        if slot_id in self.slots:
            item = self.slots[slot_id]
            self.slots[slot_id] = None
            return item
        return None
    
    def get_equipped(self, slot_id: str):
        """Возвращает предмет в слоте или None."""
        return self.slots.get(slot_id)
    
    def get_all_equipped(self) -> dict[str, object]:
        """Возвращает все непустые слоты."""
        return {slot_id: item for slot_id, item in self.slots.items() if item is not None}
    
    # ===== ИНФОРМАЦИЯ О СЛОТАХ =====
    
    def get_slot_ids(self) -> list[str]:
        """Возвращает список всех ID слотов."""
        return list(self.slots.keys())
    
    def get_slots_by_type(self, slot_type: str) -> list[str]:
        """Возвращает ID слотов определённого типа."""
        return [sid for sid in self.slots if sid.startswith(slot_type)]
    
    def slot_count(self) -> int:
        return len(self.slots)
    
    # ===== СОХРАНЕНИЕ =====
    
    def to_dict(self) -> dict:
        return {
            slot_id: item.item_id if item else None
            for slot_id, item in self.slots.items()
        }