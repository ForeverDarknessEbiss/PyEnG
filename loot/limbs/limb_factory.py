# loot/limbs/limb_factory.py
import uuid
from .limb import Limb
from loot.limbs_database import LIMBS

def create_limb(limb_id):
    """Создать конечность по ID из базы данных"""
    data = LIMBS.get(limb_id)
    
    if not data:
        raise ValueError(f"Limb '{limb_id}' not found in database")
    
    limb = Limb(**data)
    limb.uid = str(uuid.uuid4())
    print(f"[LOOT] Создаем конечность: {limb_id}")
    return limb