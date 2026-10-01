import pygame
from setting import sound_manager, play_music, stop_music
from ui_framework import (
    COLORS, get_font, draw_glass_card, draw_rounded_rect, 
    draw_text_with_shadow, draw_icon
)

class SoundButton:
    def __init__(self, x, y, width=120, height=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.hover_progress = 0.0
        self.is_pressed = False
        
    def draw(self, screen, mouse_pos):
        is_hovered = self.rect.collidepoint(mouse_pos)
        target = 1.0 if is_hovered else 0.0
        self.hover_progress += (target - self.hover_progress) * 0.3

        is_on = sound_manager.music_enabled
        icon_type = 'sound_on' if is_on else 'sound_off'
        icon_color = COLORS['green_light'] if is_on else COLORS['red_light']

        # Base surface
        bg_alpha = int(180 + 50 * self.hover_progress)
        bg_color = (20, 30, 48, bg_alpha)
        border_color = (56, 189, 248, int(120 + 135 * self.hover_progress)) if is_on else (148, 163, 184, 140)

        draw_rect = self.rect.copy()
        if self.is_pressed:
            draw_rect.y += 1
        elif self.hover_progress > 0.1:
            draw_rect.y -= int(self.hover_progress * 1.5)

        draw_rounded_rect(screen, bg_color, draw_rect, radius=8, 
                          border_color=border_color, border_width=1)

        # Text
        font = get_font(13, bold=True)
        text = "NHẠC: BẬT" if is_on else "NHẠC: TẮT"
        text_color = COLORS['white'] if is_hovered else COLORS['text_secondary']
        draw_text_with_shadow(screen, text, font, text_color, (draw_rect.centerx, draw_rect.centery), align='center')

    def handle_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            try:
                sound_manager.toggle_music()
                try:
                    sound = pygame.mixer.Sound('sounds/click.mp3')
                    sound.set_volume(0.3)
                    sound.play()
                except Exception:
                    pass
                return True
            except Exception as e:
                print(f"Lỗi khi xử lý âm thanh: {str(e)}")
                return False
        return False