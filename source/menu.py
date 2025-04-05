from setting import screenWidth, screenHeight, play_music, stop_music, sound_manager
import pygame
import sys

class Menu:
    def __init__(self, player):
        self.player = player
        self.font_big = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        self.buttons = [
            {'text': 'START', 'color': (255, 255, 255), 'hover_color': (0, 255, 0), 'rect': None},
            {'text': 'SHOP', 'color': (255, 255, 255), 'hover_color': (0, 255, 0), 'rect': None},
            {'text': 'HUONG DAN', 'color': (255, 255, 255), 'hover_color': (0, 255, 0), 'rect': None},
            {'text': 'AM THANH: BAT' if sound_manager.music_enabled else 'AM THANH: TAT', 'color': (255, 255, 255), 'hover_color': (0, 255, 0), 'rect': None},
            {'text': 'THOAT', 'color': (255, 255, 255), 'hover_color': (0, 255, 0), 'rect': None}
        ]
        self.game_title = self.font_big.render('TOWER DEFENSE', True, (255, 215, 0))
        self.title_rect = self.game_title.get_rect(center=(screenWidth // 2, 100))
        self.button_spacing = 80
        self.initialize_buttons()

    def initialize_buttons(self):
        for i, button in enumerate(self.buttons):
            text_surface = self.font_small.render(button['text'], True, button['color'])
            text_rect = text_surface.get_rect(center=(screenWidth // 2, 250 + i * self.button_spacing))
            button['rect'] = text_rect

    def draw(self, screen, mouse_pos):
        screen.fill((0, 0, 0))
        screen.blit(self.game_title, self.title_rect)
        
        # Vẽ số tiền hiện tại
        money_font = pygame.font.Font(None, 36)
        money_text = money_font.render(f"MONEY: {self.player.money}", True, (255, 215, 0))
        money_rect = money_text.get_rect(center=(screenWidth // 2, 200))
        screen.blit(money_text, money_rect)
        
        for button in self.buttons:
            color = button['hover_color'] if button['rect'].collidepoint(mouse_pos) else button['color']
            text_surface = self.font_small.render(button['text'], True, color)
            screen.blit(text_surface, button['rect'])

    def handle_click(self, mouse_pos):
        for i, button in enumerate(self.buttons):
            if button['rect'].collidepoint(mouse_pos):
                if i == 3:  # Nút âm thanh
                    try:
                        sound_manager.music_enabled = not sound_manager.music_enabled
                        if sound_manager.music_enabled:
                            play_music('music/maintheme.mp3')
                            self.buttons[3]['text'] = 'AM THANH: BAT'
                        else:
                            stop_music()
                            self.buttons[3]['text'] = 'AM THANH: TAT'
                        sound_manager.save_settings()
                        self.initialize_buttons()
                    except:
                        print("Không thể thay đổi trạng thái âm thanh")
                elif i == 4:  # Nút thoát
                    return 'quit'  # Trả về giá trị đặc biệt để báo hiệu thoát
                return i
        return None
