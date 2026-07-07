import pygame
import math


class Joystick:

    def __init__(self, x, y, size):

        # центр джойстика
        self.x = x
        self.y = y

        # радиус
        self.radius = size
        self.handle_radius = size // 2

        # позиция ручки
        self.handle_x = x
        self.handle_y = y

        # направление
        self.dx = 0
        self.dy = 0

        # состояние
        self.active = False
        self.finger_id = None

        # цвета
        self.bg_color = (50, 50, 50, 160)
        self.border_color = (120, 120, 120)
        self.handle_color = (220, 220, 220)

    # -----------------------------------------

    def _distance(self, x1, y1, x2, y2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    # -----------------------------------------

    def _update_handle(self, px, py):

        dx = px - self.x
        dy = py - self.y

        dist = math.sqrt(dx*dx + dy*dy)

        if dist > self.radius:
            dx = dx / dist * self.radius
            dy = dy / dist * self.radius

        self.handle_x = self.x + dx
        self.handle_y = self.y + dy

        self.dx = dx / self.radius
        self.dy = dy / self.radius

    # -----------------------------------------

    def handle_event(self, event):
       
        # --- МЫШЬ ---
        # print(f"handle_event вызван, self.x={self.x}, self.y={self.y}, id={id(self)}") 

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            
            
            px, py = event.pos

            if self._distance(px, py, self.x, self.y) <= self.radius:
                self.active = True
                self._update_handle(px, py)

        elif event.type == pygame.MOUSEMOTION and self.active:

            if self.active:
                px, py = event.pos
                self._update_handle(px, py)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:

            self.reset()

        # --- TOUCH ---

        elif event.type == pygame.FINGERDOWN:

            screen = pygame.display.get_surface()

            px = event.x * screen.get_width()
            py = event.y * screen.get_height()

            if self._distance(px, py, self.x, self.y) <= self.radius:

                self.active = True
                self.finger_id = event.finger_id

                self._update_handle(px, py)

        elif event.type == pygame.FINGERMOTION:

            if self.active and event.finger_id == self.finger_id:

                screen = pygame.display.get_surface()

                px = event.x * screen.get_width()
                py = event.y * screen.get_height()

                self._update_handle(px, py)

        elif event.type == pygame.FINGERUP:

            if event.finger_id == self.finger_id:
                self.reset()

    # -----------------------------------------

    def reset(self):

        self.active = False
        self.finger_id = None

        self.handle_x = self.x
        self.handle_y = self.y

        self.dx = 0
        self.dy = 0

    # -----------------------------------------

    def get_direction(self):

        return (self.dx, self.dy)

    # -----------------------------------------

    def draw(self, screen):
        

        bg = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)

        pygame.draw.circle(
            bg,
            self.bg_color,
            (self.radius, self.radius),
            self.radius
        )

        screen.blit(bg, (self.x - self.radius, self.y - self.radius))

        pygame.draw.circle(
            screen,
            self.border_color,
            (int(self.x), int(self.y)),
            self.radius,
            2
        )

        pygame.draw.circle(
            screen,
            self.handle_color,
            (int(self.handle_x), int(self.handle_y)),
            self.handle_radius
        )

