import pygame
from setting import screenWidth, screenHeight

class GameOver:
    def __init__(self):
        self.font_big = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        self.game_over_text = self.font_big.render('GAME OVER', True, (255, 0, 0))
        self.title_rect = self.game_over_text.get_rect(center=(screenWidth // 2, 200))
        
        self.menu_button = {
            'text': 'QUAY LAI MENU',
            'color': (255, 255, 255),
            'hover_color': (0, 255, 0),
            'rect': None
        }
        self.initialize_button()

    def initialize_button(self):
        text_surface = self.font_small.render(self.menu_button['text'], True, self.menu_button['color'])
        text_rect = text_surface.get_rect(center=(screenWidth // 2, 300))
        self.menu_button['rect'] = text_rect

    def draw(self, screen, mouse_pos):
        screen.fill((0, 0, 0))
        screen.blit(self.game_over_text, self.title_rect)
        
        color = self.menu_button['hover_color'] if self.menu_button['rect'].collidepoint(mouse_pos) else self.menu_button['color']
        text_surface = self.font_small.render(self.menu_button['text'], True, color)
        screen.blit(text_surface, self.menu_button['rect'])

    def handle_click(self, mouse_pos):
        if self.menu_button['rect'].collidepoint(mouse_pos):
            return True
        return False