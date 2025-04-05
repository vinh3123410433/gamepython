import pygame
from setting import play_sound

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_time = pygame.time.get_ticks()
        self.img= None
        self.duration = 300  
        try:
            play_sound('sounds/explosion.wav', 0.4 )
        except:
            print("Không tìm thấy file âm thanh explosion ")

    def draw(self, screen):
        boom1 = pygame.image.load("images/boom1.png").convert_alpha()
        boom1= pygame.transform.scale(boom1, (100, 100))
        boom2 = pygame.image.load("images/boom2.png").convert_alpha()
        boom2= pygame.transform.scale(boom2, (100, 100))
        boom3 = pygame.image.load("images/boom3.png").convert_alpha()
        boom3= pygame.transform.scale(boom3, (100, 100))
        current_time = pygame.time.get_ticks() - self.start_time
        if current_time < 100:
            self.img = boom1
            self.rect= self.img.get_rect(center=(self.x, self.y))
            screen.blit(self.img, self.rect)
        elif current_time < 200:
            self.img = boom2
            self.rect= self.img.get_rect(center=(self.x, self.y))
            screen.blit(self.img, self.rect)
        elif current_time < 300:
            self.img = boom3
            self.rect= self.img.get_rect(center=(self.x, self.y))
            screen.blit(self.img, self.rect)

    def is_done(self):
        return pygame.time.get_ticks() - self.start_time > self.duration