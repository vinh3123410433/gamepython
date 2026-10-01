import pygame
from setting import play_sound

_BOOM_IMAGES = None

def get_boom_images():
    global _BOOM_IMAGES
    if _BOOM_IMAGES is None:
        _BOOM_IMAGES = [
            pygame.transform.scale(pygame.image.load("images/boom1.png").convert_alpha(), (100, 100)),
            pygame.transform.scale(pygame.image.load("images/boom2.png").convert_alpha(), (100, 100)),
            pygame.transform.scale(pygame.image.load("images/boom3.png").convert_alpha(), (100, 100))
        ]
    return _BOOM_IMAGES

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_time = pygame.time.get_ticks()
        self.img = None
        self.duration = 300  
        try:
            play_sound('sounds/explosion.wav', 0.4)
        except Exception:
            pass

    def draw(self, screen):
        frames = get_boom_images()
        current_time = pygame.time.get_ticks() - self.start_time
        frame_idx = min(2, current_time // 100)
        self.img = frames[frame_idx]
        self.rect = self.img.get_rect(center=(self.x, self.y))
        screen.blit(self.img, self.rect)

    def is_done(self):
        return pygame.time.get_ticks() - self.start_time > self.duration