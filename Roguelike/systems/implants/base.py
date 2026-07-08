# systems/implants/base.py
class BaseMechanic:
    def __init__(self, player, config=None):
        self.player = player
        self.config = config or {}
        self.active = False
        self.enabled = True          # ВКЛ/ВЫКЛ от пользователя
        self.cooldown_timer = 0.0

        # 🆕 Параметры зарядки
        self.charge_time = self.config.get("charge_time", 0)      # время зарядки (сек)
        self.cooldown = self.config.get("cooldown", 0)            # время кулдауна (сек)
        self.charge_drain = self.config.get("charge_drain", 0)    # трата энергии в сек
        self.min_energy = self.config.get("min_energy", 20)       # мин % энергии для зарядки
        
        # 🆕 Состояния
        self.state = "passive"      # passive, charging, cooldown, ready, active
        self.charge_progress = 0.0  # 0..charge_time
        self.cooldown_progress = 0.0
        self.active_timer = 0.0
        self.active_time = self.config.get("active_time", 0)
        
        self.is_charging_implant = (self.charge_time > 0)

    def activate(self):
        self.active = True
    
    def deactivate(self):
        self.active = False
    
    def set_enabled(self, enabled):
        self.enabled = enabled
        if not enabled:
            self.cooldown_timer = 0

    def _start_charging(self):
        """Начинает зарядку (вызывается при надевании или после кулдауна)"""
        if not self.enabled or not self.active:
            return
        
        # Проверяем достаточно ли энергии для начала зарядки
        max_energy = self.player.max_energy
        current_energy = self.player.energy
        min_required = max_energy * self.min_energy / 100
        
        if current_energy < min_required:
            self.state = "passive"
            return
        
        self.state = "charging"

    def _check_energy_for_charging(self):
        """Проверяет, хватает ли энергии для продолжения зарядки"""
        max_energy = self.player.max_energy
        current_energy = self.player.energy
        min_required = max_energy * self.min_energy / 100
        
        return current_energy >= min_required

    def update(self, delta_time):
        if not self.active or not self.enabled:
            return

        # 🆕 Для обычного импланта (без зарядки) - просто обновляем кулдаун
        if not self.is_charging_implant:
            if self.cooldown_timer > 0:
                self.cooldown_timer -= delta_time
            return

        # Активный режим
        if self.state == "active":
            self.active_timer -= delta_time
            if self.active_timer <= 0:
                self._on_deactivate()
                # 🆕 При окончании активности запускаем И кулдаун, И зарядку
                self.state = "charging"
                self.cooldown_timer = self.cooldown
                self.charge_progress = 0.0
            return
        
        # 🆕 Кулдаун и зарядка идут ПАРАЛЛЕЛЬНО
        if self.state in ["cooldown", "charging"]:
            # Обновляем кулдаун
            if self.cooldown_timer > 0:
                self.cooldown_timer -= delta_time
            
            # Обновляем зарядку (если есть энергия)
            if self.state == "charging":
                if self._check_energy_for_charging():
                    energy_cost = self.charge_drain * delta_time
                    if self.player.energy >= energy_cost:
                        self.player.energy -= energy_cost
                        self.charge_progress += delta_time
                    else:
                        self.state = "passive"
                        return
                    
                    if self.charge_progress >= self.charge_time:
                        self.charge_progress = self.charge_time
                        # Зарядка завершена, проверяем кулдаун
                        if self.cooldown_timer <= 0:
                            self.state = "ready"
                        else:
                            self.state = "cooldown"
                else:
                    self.state = "passive"
                    return
            
            # Если кулдаун закончился, а зарядка ещё идёт
            if self.cooldown_timer <= 0 and self.state == "cooldown":
                if self.charge_progress >= self.charge_time:
                    self.state = "ready"
                else:
                    self.state = "charging"
            
            # Если зарядка закончилась, а кулдаун ещё идёт
            if self.charge_progress >= self.charge_time and self.state == "charging":
                if self.cooldown_timer <= 0:
                    self.state = "ready"
                else:
                    self.state = "cooldown"
            return
        
        # Готов к использованию
        if self.state == "ready":
            pass
        
        # Пассивный режим
        if self.state == "passive" and self.is_charging_implant:
            self.state = "charging"
            self.charge_progress = 0.0
            self.cooldown_timer = 0.0

    def get_charge_percent(self):
        """Процент заряда (0-100)"""
        if self.charge_time <= 0:
            return 100 if self.state == "ready" else 0
        return int((self.charge_progress / self.charge_time) * 100)
    
    def get_cooldown_percent(self):
        """Процент кулдауна (0-100)"""
        if self.cooldown <= 0:
            return 0
        return int((self.cooldown_timer / self.cooldown) * 100)
    
    def can_use(self):
        """Можно ли использовать способность"""
        if not self.enabled or not self.active:
            return False
        
        if self.is_charging_implant:
            # Заряжаемый: нужен статус "ready"
            return self.state == "ready"
        else:
            # Обычный: проверяем кулдаун (как в старом методе)
            return self.cooldown_timer <= 0

    def use(self, **kwargs):
        """Использование способности"""
        if not self.can_use():
            return False
        
        if self.is_charging_implant:
            # Заряжаемый имплант
            self.state = "active"
            self.active_timer = self.active_time
            self._on_activate()
            self.cooldown_timer = self.cooldown
            self.charge_progress = 0.0
            return True
        else:
            # Обычный имплант (как в старом методе)
            if not self.player.use_energy(self.config.get("energy_cost", 0)):
                return False
            self.cooldown_timer = self.config.get("cooldown", 0)
            self._on_use(**kwargs)
            return True

    def _on_activate(self):
        """Вызывается при активации заряжаемого импланта"""
        pass
    
    def _on_deactivate(self):
        """Вызывается при окончании работы заряжаемого импланта"""
        pass

    def _on_use(self):
        pass