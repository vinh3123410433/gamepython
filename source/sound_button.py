import pygame
from setting import sound_manager, play_music, stop_music

class SoundButton:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 30)
        self.update_text()
        
    def update_text(self):
        self.text = self.font.render('AM THANH: BAT' if sound_manager.music_enabled else 'AM THANH: TAT', True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=self.rect.center)
        
    def draw(self, screen, mouse_pos):
        # Vẽ nền nút
        color = (0, 255, 0) if self.rect.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        # Vẽ text
        screen.blit(self.text, self.text_rect)
        
    def handle_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            sound_manager.music_enabled = not sound_manager.music_enabled
            if sound_manager.music_enabled:
                play_music('music/maintheme.mp3')
            else:
                stop_music()
            sound_manager.save_settings()
            self.update_text()
            return True
        return False 