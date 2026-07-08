# systems/implants/manager.py
import importlib

class ImplantMechanicsManager:
    def __init__(self, player):
        self.player = player
        self.active_mechanics = {}      # {implant_uid: mechanic_instance}
        self.mechanic_classes = {}      # {key: class}

    def get_mechanic_by_uid(self, uid):
        """Получить механику по uid импланта"""
        if uid in self.active_mechanics:
            return self.active_mechanics[uid]["instance"]
        return None

    def get_mechanic_by_slot(self, slot_name):
        for uid, data in self.active_mechanics.items():
            # Нужно знать, какой имплант в каком слоте
            # Можно хранить mapping: slot_name -> uid
            pass 

    def on_equip(self, implant, implant_uid):
        for mechanic_key in getattr(implant, "mechanics", []):
            self._load_mechanic(mechanic_key)
            
            # 🆕 Берём конфиг из implant.mechanic_config (если есть), иначе стандартный
            if hasattr(implant, "mechanic_config"):
                config = implant.mechanic_config
            else:
                # Старый способ для обратной совместимости
                config = {
                    "cooldown": getattr(implant, "cooldown", 0),
                    "energy_cost": getattr(implant, "energy_cost", 0)
                }
            
            instance = self.mechanic_classes[mechanic_key](self.player, config)
            instance.activate()
            
            self.active_mechanics[implant_uid] = {
                "instance": instance,
                "key": mechanic_key
            }
            print(f"[IMPLANT] Механика '{mechanic_key}' активирована")
    
    def on_unequip(self, implant_uid):
        if implant_uid in self.active_mechanics:
            self.active_mechanics[implant_uid]["instance"].deactivate()
            del self.active_mechanics[implant_uid]
    
    def _load_mechanic(self, key):
        if key not in self.mechanic_classes:
            module = importlib.import_module(f"systems.implants.mechanics.{key}")
            self.mechanic_classes[key] = getattr(module, "Mechanic")
    
    def update(self, delta_time):
        for data in self.active_mechanics.values():
            data["instance"].update(delta_time)
    
    def use_mechanic_by_key(self, key):
        print(f"[IMPLANT] Поиск механики: {key}")
        for uid, data in self.active_mechanics.items():
            mechanic_key = data["key"]
            mechanic = data["instance"]
            print(f"  - key: {mechanic_key}, active: {mechanic.active}")
            if mechanic_key == key:
                return mechanic.use()
        return False