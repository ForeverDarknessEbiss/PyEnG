#проводник между логикой (что выпало) и визуалом (как рисовать)

import random
import math
import pygame
import uuid

class ItemEntity:

    def __init__(self, x, y, item, amount):

        self.x = x
        self.y = y

        self.item = item 
        self.color = item.color  
        self.name = item.name
        self.amount = amount
        self.vx = 0.0      
        self.vy = 0.0   
        self.size = 30
        self.uid = str(uuid.uuid4())
                # 🆕 ЗАДЕРЖКА ПОДБОРА
        self.pickup_delay = 0.5

        # --- РАЗБРОС (как у XPOrb) ---
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(100, 200)
        distance = random.uniform(10, 40)

        offset_x = math.cos(angle) * distance
        offset_y = math.sin(angle) * distance

        self.x = x + offset_x
        self.y = y + offset_y

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
 
    def update(self, dt):

        self.x += self.vx * dt
        self.y += self.vy * dt

        # затухание (трение)
        self.vx *= 0.90
        self.vy *= 0.90


    def draw(self, screen, camera):

        import pygame

        screen_x, screen_y = camera.world_to_screen(self.x, self.y)

        pygame.draw.rect(
            screen,
            (255, 255, 0),
            (int(screen_x), int(screen_y), 20, 20)
        )