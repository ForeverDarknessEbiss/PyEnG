# loot/implants/implant_factory.py
from .implant import Implant
from loot.implants_database import IMPLANTS
import uuid

def create_implant(implant_id):
    """Создать имплант по ID из базы данных"""
    data = IMPLANTS.get(implant_id)
    
    if not data:
        raise ValueError(f"Implant '{implant_id}' not found in database")
    
    # Создаём имплант один раз
    implant = Implant(**data)
    implant.uid = str(uuid.uuid4())
    print(f"[LOOT] Создаем имплант: {implant_id}")
    
    # Конфиг для механики (будет использован в manager.py)
    implant.mechanic_config = {
        "cooldown": implant.cooldown,
        "energy_cost": implant.energy_cost,
        "charge_time": implant.charge_time,
        "charge_drain": implant.charge_drain,
        "min_energy": implant.min_energy,
        "active_time": implant.active_time,
    }
    
    return implant