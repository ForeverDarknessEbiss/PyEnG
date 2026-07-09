# loot/limbs/limb_factory.py

from loot.limbs.limb import Limb
from loot.limbs_database import LimbsDatabase


class LimbFactory:
    """
    Фабрика конечностей.
    Читает сырые данные из LimbsDatabase, создаёт объекты Limb.
    """
    
    def __init__(self, db: LimbsDatabase):
        self.db = db
    
    def create(self, limb_id: int) -> Limb | None:
        """
        Создаёт объект Limb по ID из БД.
        Единственный метод создания — источник данных только БД.
        """
        row = self.db.fetch_by_id(limb_id)
        if row is None:
            return None
        
        # row = (id, name, limb_type, hp, slot_type, slot_count)
        _, name, limb_type, hp, slot_type, slot_count = row
        
        return Limb(
            limb_id=limb_id,
            name=name,
            limb_type=limb_type,
            hp=hp,
            slot_type=slot_type,
            slot_count=slot_count
        )
    