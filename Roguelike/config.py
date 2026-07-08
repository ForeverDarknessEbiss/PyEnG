# config.py
import pygame

# Инициализируем pygame только для получения информации об экране
pygame.display.init()

# Получаем реальные размеры экрана 
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Убедимся, что ширина больше высоты (альбомная ориентация)
if SCREEN_HEIGHT > SCREEN_WIDTH:
    # Если телефон в портретном режиме, меняем местами
    SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_HEIGHT, SCREEN_WIDTH

# Теперь рассчитываем все размеры относительно экрана
# Размер тайла (клетки) - 1/20 от ширины экрана
TILE_SIZE = max(30, SCREEN_WIDTH // 16)  # минимум 30 пикселей

# Цвета (R, G, B)
COLORS = {
    'WALL': (101, 67, 33),    # коричневый
    'FLOOR': (34, 139, 34),   # зеленый
    'PLAYER': (255, 0, 0),     # красный
    'BG': (0, 0, 0),           # черный (фон)
    'JOYSTICK_BG': (50, 50, 50, 128)  # полупрозрачный серый
}

# Размер игрока (относительно тайла)
PLAYER_RADIUS = TILE_SIZE // 2

PLAYER_SPEED = 10.0  # пикселей за кадр (чем меньше, тем медленнее)
MOVE_DELAY = 0.2    # задержка между шагами в секундах

# Настройки джойстика
JOYSTICK_SIZE = SCREEN_WIDTH // 9  # 1/9 ширины экрана
JOYSTICK_POS = (JOYSTICK_SIZE, SCREEN_HEIGHT - 400)