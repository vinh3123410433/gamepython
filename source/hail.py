import pygame
import random
import math
from setting import screenWidth, screenHeight, hailList
class Hail:
    def __init__(self, x, y):
        self.x, self.y = random.choice([
            (0, random.randint(-10, int(screenHeight/10))), 
            (random.randint(-10, screenWidth), 0)
        ])
        self.target= (x, y)
        self.speed = 10
        self.image = pygame.image.load("images/meteor1.png").convert_alpha()
        self.rect= self.image.get_rect(center=(self.x, self.y))
        self.angle = None

    def draw(self, screen):
        img= random.randint(1, 3)
        if img==1:
            self.image = pygame.image.load("images/meteor1.png").convert_alpha()
        elif img==2:
            self.image = pygame.image.load("images/meteor2.png").convert_alpha()
        elif img==3:
            self.image = pygame.image.load("images/meteor3.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90- math.degrees(math.atan2(self.y, self.x)))
        self.image = pygame.transform.scale(self.image, (100, 100))
        if self.angle/math.pi*180 > -180 and self.angle/math.pi*180 < -90:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=self.rect.center) 
        screen.blit(self.image, self.rect)
        print("angle", self.angle/math.pi*180)

    def move(self, screen):
        dx = self.target[0] - self.x
        dy = self.target[1] - self.y

        self.angle= -math.atan2(dy, dx)
        print("angle chuột", self.angle/math.pi*180)
        print("angle enemy", math.atan2(self.y,self.x)/math.pi*180)
        print(self.target)
        x_target = math.cos(self.angle) * self.speed
        y_target = -math.sin(self.angle) * self.speed
        next_pos = (self.x + x_target, self.y + y_target)
        distance= math.sqrt(dx**2 + dy**2)
        if distance < self.speed:
            self.x, self.y = self.target
            hailList.remove(self)
        else:
            self.x += x_target
            self.y += y_target

        self.rect.center = (self.x, self.y)