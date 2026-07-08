import pygame

class DamageText:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y 
        self.text = str(int(text))

        self.lifetime = 0.7

        self.vy = -50 # поднимается вверх 
        self.font = pygame.font.SysFont(None, 36) # sysfont(шрифт, размер)

    def update(self, dt):
        self.y +=self.vy * dt
        self.lifetime -= dt

    def draw(self, screen, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y

        surface = self.font.render(self.text, True, (255, 255, 0))
        screen.blit(surface, (screen_x, screen_y))
         
class DamageTextSystem:
    def __init__(self):
        self.texts = []

    def add(self, x, y, value):
        self.texts.append(DamageText(x, y, value))

    def update(self, dt):
        for text in self.texts[:]:
            text.update(dt)
            if text.lifetime <= 0:
                self.texts.remove(text)

    def draw(self, screen, camera):
        for text in self.texts:
            text.draw(screen, camera)