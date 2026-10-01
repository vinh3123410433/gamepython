import pygame
import math
import random
from setting import screenWidth, screenHeight
from ui_framework import (
    COLORS, get_font, draw_glass_card, draw_rounded_rect, 
    draw_text_with_shadow, draw_icon, ModernButton
)

class GameOver:
    def __init__(self):
        try:
            self.background_image = pygame.image.load("background/bg_open_meadow.png")
            if pygame.display.get_init():
                self.background_image = self.background_image.convert()
            self.background_image = pygame.transform.scale(self.background_image, (screenWidth, screenHeight))
        except Exception:
            self.background_image = None

        self.loss_sound = None
        self.victory_sound = None
        try:
            self.loss_sound = pygame.mixer.Sound("sounds/gameover2.wav")
            self.loss_sound.set_volume(0.6)
        except Exception:
            pass

        try:
            self.victory_sound = pygame.mixer.Sound("sounds/new upgrade.mp3")
            self.victory_sound.set_volume(0.6)
        except Exception:
            pass

        self.sound_played = False
        self.is_victory = False
        self.time_counter = 0.0

        # Buttons
        btn_w = 200
        btn_h = 44
        center_x = screenWidth // 2
        
        self.btn_menu = ModernButton(
            (center_x - btn_w // 2, screenHeight - 90, btn_w, btn_h),
            "VỀ MENU CHÍNH", icon="home", style="primary", font_size=16, radius=10
        )

    def reset_sound(self, is_victory=False):
        self.sound_played = False
        self.is_victory = is_victory

    def draw(self, screen, mouse_pos, player=None):
        self.time_counter += 0.03

        # Draw Background
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill((10, 15, 25))

        # Atmospheric Color Vignette
        overlay = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
        if self.is_victory:
            # Golden celebratory backdrop
            overlay.fill((15, 23, 42, 210))
            # Subtle gold rays / aura
            pygame.draw.circle(overlay, (245, 158, 11, 40), (screenWidth // 2, 160), 300)
        else:
            # Crimson defeat backdrop
            overlay.fill((20, 10, 15, 225))
            pygame.draw.circle(overlay, (239, 68, 68, 35), (screenWidth // 2, 160), 280)
        screen.blit(overlay, (0, 0))

        # Title with floating bounce
        float_y = int(math.sin(self.time_counter * 2.0) * 3)
        title_y = 120 + float_y

        if self.is_victory:
            title_text = "CHIẾN THẮNG HUY HOÀNG!"
            title_color = COLORS['gold_light']
            shadow_color = (245, 158, 11, 90)
            sub_text = "Bạn đã kiên cường đẩy lùi toàn bộ các đợt quái vật xâm lăng!"
            sub_color = COLORS['cyan_light']
        else:
            title_text = "THẤT BẠI (DEFEAT)"
            title_color = COLORS['red_light']
            shadow_color = (239, 68, 68, 90)
            sub_text = "Căn cứ của bạn đã bị chọc thủng! Hãy nâng cấp và thử lại."
            sub_color = COLORS['text_muted']

        # Title (Clean text, no bulky icons)
        title_font = get_font(38, bold=True)
        draw_text_with_shadow(screen, title_text, title_font, title_color, (screenWidth // 2, title_y), 
                              align='center', shadow_color=shadow_color, offset=(0, 0))
        draw_text_with_shadow(screen, title_text, title_font, title_color, (screenWidth // 2, title_y), 
                              align='center', shadow_color=(0, 0, 0, 220), offset=(2, 3))

        # Subtitle
        sub_font = get_font(14, bold=False)
        draw_text_with_shadow(screen, sub_text, sub_font, sub_color, (screenWidth // 2, title_y + 36), align='center')

        # ----------------------------------------------------------------------
        # Stats Breakdown Card
        # ----------------------------------------------------------------------
        card_w = 440
        card_h = 190
        card_rect = pygame.Rect((screenWidth - card_w) // 2, 210, card_w, card_h)
        border_col = COLORS['gold_glow'] if self.is_victory else COLORS['border_subtle']
        draw_glass_card(screen, card_rect, radius=14, bg_color=(15, 23, 42, 235), border_color=border_col, border_width=2)

        # Card Header
        ch_font = get_font(14, bold=True)
        draw_text_with_shadow(screen, "TỔNG KẾT TRẬN CHIẾN", ch_font, COLORS['text_secondary'], 
                              (card_rect.centerx, card_rect.y + 18), align='center')
        pygame.draw.line(screen, COLORS['border_subtle'], 
                         (card_rect.x + 20, card_rect.y + 32), (card_rect.right - 20, card_rect.y + 32), 1)

        # Stat items
        wave_val = player.wave if player else 1
        score_val = player.score if player else 0
        money_val = player.money if player else 0
        level_val = player.level if player else 1

        stats = [
            ("Đợt sóng sinh tồn:", f"Wave {wave_val}"),
            ("Điểm số tích lũy:", f"{score_val:,} Điểm"),
            ("Ngân khố chiến đấu:", f"{money_val:,} G"),
            ("Cấp độ chiến binh:", f"Level {level_val}")
        ]

        label_font = get_font(14, bold=False)
        val_font = get_font(15, bold=True)

        for idx, (label, val_str) in enumerate(stats):
            row_y = card_rect.y + 54 + idx * 30
            # Label
            draw_text_with_shadow(screen, label, label_font, COLORS['text_muted'], (card_rect.x + 36, row_y + 4), align='midleft')
            # Value
            draw_text_with_shadow(screen, val_str, val_font, COLORS['white'], (card_rect.right - 36, row_y + 4), align='midright')

        # ----------------------------------------------------------------------
        # Action Button
        # ----------------------------------------------------------------------
        self.btn_menu.draw(screen, mouse_pos)

        # Audio handling
        if not self.sound_played:
            try:
                pygame.mixer.music.stop()
                if self.is_victory and self.victory_sound:
                    self.victory_sound.play()
                elif not self.is_victory and self.loss_sound:
                    self.loss_sound.play()
            except Exception:
                pass
            self.sound_played = True

    def handle_event(self, event):
        return self.btn_menu.handle_event(event)

    def handle_click(self, mouse_pos):
        if self.btn_menu.rect.collidepoint(mouse_pos):
            try:
                sound = pygame.mixer.Sound('sounds/click.mp3')
                sound.set_volume(0.4)
                sound.play()
            except Exception:
                pass
            return True
        return False