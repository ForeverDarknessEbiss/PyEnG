from ..base import BaseMechanic

class Mechanic(BaseMechanic):
    def _on_activate(self):
        """Активация ЭМИ-импульса"""
        print("[EMP] ЭМИ-импульс активирован!")
        # TODO: найти всех механических врагов вокруг и отключить их
        
    def _on_deactivate(self):
        """Окончание работы ЭМИ-импульса"""
        print("[EMP] ЭМИ-импульс завершён")