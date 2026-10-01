import pygame
from setting import sound_manager, screenWidth, screenHeight
from ui_framework import (
    COLORS, get_font, draw_glass_card, draw_text_with_shadow, 
    draw_rounded_rect, draw_icon, ModernButton, ModernSlider, ModernToggle
)

class SettingsModal:
    def __init__(self, on_close=None):
        self.on_close = on_close
        self.width = 540
        self.height = 480
        self.x = (screenWidth - self.width) // 2
        self.y = (screenHeight - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Sliders & Toggles
        self.music_slider = ModernSlider(
            (self.x + 30, self.y + 110, self.width - 60, 36),
            min_val=0.0, max_val=1.0, current_val=sound_manager.music_volume,
            label="Nhạc nền (BGM):",
            on_change=lambda val: sound_manager.set_music_volume(val)
        )
        self.music_toggle = ModernToggle(
            (self.x + 30, self.y + 155, self.width - 60, 32),
            is_on=sound_manager.music_enabled,
            label="Bật/Tắt nhạc nền:",
            on_toggle=lambda is_on: sound_manager.set_music_enabled(is_on)
        )

        self.sound_slider = ModernSlider(
            (self.x + 30, self.y + 205, self.width - 60, 36),
            min_val=0.0, max_val=1.0, current_val=sound_manager.sound_volume,
            label="Hiệu ứng (SFX):",
            on_change=lambda val: sound_manager.set_sound_volume(val)
        )
        self.sound_toggle = ModernToggle(
            (self.x + 30, self.y + 250, self.width - 60, 32),
            is_on=sound_manager.sound_enabled,
            label="Bật/Tắt hiệu ứng:",
            on_toggle=lambda is_on: sound_manager.set_sound_enabled(is_on)
        )

        # Close / Save button
        self.btn_close = ModernButton(
            (self.x + (self.width - 180) // 2, self.y + self.height - 60, 180, 42),
            "LƯU & ĐÓNG", icon="close", style="primary", font_size=16
        )

    def draw(self, surface, mouse_pos):
        # Dim backdrop
        backdrop = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
        backdrop.fill((8, 12, 22, 195))
        surface.blit(backdrop, (0, 0))

        # Main modal window
        draw_glass_card(surface, self.rect, radius=16, bg_color=(15, 23, 42, 245), 
                        border_color=COLORS['border_light'], border_width=2)

        # Header Title
        title_font = get_font(24, bold=True)
        draw_text_with_shadow(surface, "CÀI ĐẶT HỆ THỐNG", title_font, COLORS['gold_light'], 
                              (self.rect.centerx, self.y + 35), align='center')
        
        sub_font = get_font(13, bold=False)
        draw_text_with_shadow(surface, "Tùy chỉnh âm lượng và cấu hình trò chơi", sub_font, COLORS['text_muted'],
                              (self.rect.centerx, self.y + 60), align='center')

        # Divider line
        pygame.draw.line(surface, COLORS['border_subtle'], 
                         (self.x + 30, self.y + 80), (self.x + self.width - 30, self.y + 80), 1)

        # Controls
        self.music_slider.draw(surface, mouse_pos)
        self.music_toggle.draw(surface, mouse_pos)
        self.sound_slider.draw(surface, mouse_pos)
        self.sound_toggle.draw(surface, mouse_pos)

        # Shortcut reference card
        key_rect = pygame.Rect(self.x + 30, self.y + 295, self.width - 60, 110)
        draw_rounded_rect(surface, (22, 32, 50, 220), key_rect, radius=8, 
                          border_color=COLORS['border_subtle'], border_width=1)
        
        kh_font = get_font(13, bold=True)
        kd_font = get_font(12, bold=False)
        draw_text_with_shadow(surface, "PHÍM TẮT ĐIỀU KHIỂN:", kh_font, COLORS['cyan_light'], 
                              (key_rect.x + 12, key_rect.y + 12), align='topleft')
        
        shortcuts = [
            ("SPACE", "Bắt đầu wave quái vật"),
            ("W / S", "Tăng / Giảm tốc độ game (1x - 10x)"),
            ("H", "Mua triệu hồi Thiên thạch (2000 G)"),
            ("ESC", "Mở Menu Tạm dừng / Quay lại")
        ]
        
        for idx, (key, desc) in enumerate(shortcuts):
            col = idx % 2
            row = idx // 2
            item_x = key_rect.x + 12 + col * 240
            item_y = key_rect.y + 36 + row * 32
            
            # Key badge
            k_rect = pygame.Rect(item_x, item_y, 55, 22)
            draw_rounded_rect(surface, (40, 55, 80), k_rect, radius=4, border_color=COLORS['border_light'])
            draw_text_with_shadow(surface, key, kh_font, COLORS['white'], (k_rect.centerx, k_rect.centery), align='center')
            
            # Desc
            draw_text_with_shadow(surface, desc, kd_font, COLORS['text_secondary'], (item_x + 62, item_y + 11), align='midleft')

        # Close button
        self.btn_close.draw(surface, mouse_pos)

    def handle_event(self, event):
        if self.music_slider.handle_event(event):
            return True
        if self.music_toggle.handle_event(event):
            return True
        if self.sound_slider.handle_event(event):
            # Test sound effect on drag release
            if event.type == pygame.MOUSEBUTTONUP:
                try:
                    sound_manager.play_sound('sounds/click.mp3')
                except Exception:
                    pass
            return True
        if self.sound_toggle.handle_event(event):
            return True
        if self.btn_close.handle_event(event):
            sound_manager.save_settings()
            if self.on_close:
                self.on_close()
            return 'close'
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sound_manager.save_settings()
            if self.on_close:
                self.on_close()
            return 'close'
        return False
