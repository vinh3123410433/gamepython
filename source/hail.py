import pygame
import random
import math
from setting import screenWidth, screenHeight, hailList
# Pre-load meteor images to avoid heavy disk I/O per frame
_METEOR_IMAGES = None

def get_meteor_images():
    global _METEOR_IMAGES
    if _METEOR_IMAGES is None:
        _METEOR_IMAGES = [
            pygame.image.load("images/meteor1.png").convert_alpha(),
            pygame.image.load("images/meteor2.png").convert_alpha(),
            pygame.image.load("images/meteor3.png").convert_alpha()
        ]
    return _METEOR_IMAGES

class Hail:
    def __init__(self, x, y):
        self.x, self.y = random.choice([
            (0, random.randint(-10, int(screenHeight/10))), 
            (random.randint(-10, screenWidth), 0)
        ])
        self.target = (x, y)
        self.speed = 10
        self.base_image = random.choice(get_meteor_images())
        self.image = pygame.transform.scale(self.base_image, (100, 100))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.angle = 0

    def draw(self, screen):
        deg = 90 - math.degrees(math.atan2(self.y, self.x))
        rotated = pygame.transform.rotate(self.base_image, deg)
        scaled = pygame.transform.scale(rotated, (100, 100))
        if -180 < (self.angle / math.pi * 180) < -90:
            scaled = pygame.transform.flip(scaled, True, False)
        self.rect = scaled.get_rect(center=(self.x, self.y)) 
        screen.blit(scaled, self.rect)

    def move(self, screen):
        dx = self.target[0] - self.x
        dy = self.target[1] - self.y

        self.angle = -math.atan2(dy, dx)
        x_target = math.cos(self.angle) * self.speed
        y_target = -math.sin(self.angle) * self.speed
        distance = math.sqrt(dx**2 + dy**2)
        if distance < self.speed:
            self.x, self.y = self.target
        else:
            self.x += x_target
            self.y += y_target

        self.rect.center = (self.x, self.y)
