import pygame
import math
import random
import sys
from setting import screenWidth, screenHeight, play_music, stop_music, sound_manager
from ui_framework import (
    COLORS, get_font, draw_glass_card, draw_rounded_rect, 
    draw_text_with_shadow, draw_icon, ModernButton
)
from setting_ui import SettingsModal

class Particle:
    def __init__(self):
        self.x = random.randint(0, screenWidth)
        self.y = random.randint(0, screenHeight)
        self.size = random.uniform(1.5, 3.5)
        self.speed_y = random.uniform(-0.6, -0.2)
        self.speed_x = random.uniform(-0.2, 0.2)
        self.alpha = random.randint(60, 180)
        self.color = random.choice([COLORS['gold_light'], COLORS['cyan_light'], (255, 255, 255)])

    def update(self):
        self.y += self.speed_y
        self.x += self.speed_x
        if self.y < -10:
            self.y = screenHeight + 10
            self.x = random.randint(0, screenWidth)

    def draw(self, surface):
        surf = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        col = self.color + (self.alpha,)
        pygame.draw.circle(surf, col, (int(self.size), int(self.size)), int(self.size))
        surface.blit(surf, (self.x, self.y))

class Menu:
    def __init__(self, player):
        self.player = player
        self.bg_image = pygame.image.load("background/Background_MergedForReference.jpg")
        if pygame.display.get_init():
            try:
                self.bg_image = self.bg_image.convert()
            except Exception:
                pass
        self.bg_image = pygame.transform.scale(self.bg_image, (screenWidth, screenHeight))
        self.bg_x = 0
        self.bg_speed = 0.5

        # Floating ambient dust particles
        self.particles = [Particle() for _ in range(35)]

        # Settings modal instance
        self.show_settings = False
        self.settings_modal = SettingsModal(on_close=self.close_settings)

        # Buttons setup
        btn_w = 260
        btn_h = 48
        btn_x = (screenWidth - btn_w) // 2
        start_y = 230
        spacing = 58

        self.btn_start = ModernButton(
            (btn_x, start_y, btn_w, btn_h),
            "BẮT ĐẦU CHƠI", icon="play", style="primary", font_size=18, radius=10
        )
        self.btn_shop = ModernButton(
            (btn_x, start_y + spacing, btn_w, btn_h),
            "CỬA HÀNG (SHOP)", icon="gold", style="cyan", font_size=17, radius=10
        )
        self.btn_instructions = ModernButton(
            (btn_x, start_y + spacing * 2, btn_w, btn_h),
            "HƯỚNG DẪN", icon="star", style="purple", font_size=17, radius=10
        )
        self.btn_settings = ModernButton(
            (btn_x, start_y + spacing * 3, btn_w, btn_h),
            "CÀI ĐẶT", icon=None, style="glass", font_size=16, radius=10
        )
        self.btn_quit = ModernButton(
            (btn_x, start_y + spacing * 4, btn_w, btn_h),
            "THOÁT GAME", icon="close", style="danger", font_size=16, radius=10
        )

        # Quick Sound Toggle in top-right
        self.btn_sound_quick = ModernButton(
            (screenWidth - 130, 16, 114, 34),
            "NHẠC: BẬT" if sound_manager.music_enabled else "NHẠC: TẮT",
            icon="sound_on" if sound_manager.music_enabled else "sound_off",
            style="glass", font_size=12, radius=8
        )

        self.time_counter = 0.0

    def close_settings(self):
        self.show_settings = False

    def draw(self, screen, mouse_pos):
        self.time_counter += 0.03

        # Scrolling dynamic background
        self.bg_x -= self.bg_speed
        if self.bg_x <= -screenWidth:
            self.bg_x = 0

        screen.blit(self.bg_image, (self.bg_x, 0))
        screen.blit(self.bg_image, (self.bg_x + screenWidth, 0))

        # Dark cinematic vignette / overlay to ensure buttons pop
        overlay = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
        overlay.fill((10, 15, 28, 140))
        # Top and bottom dark gradients
        pygame.draw.rect(overlay, (5, 8, 15, 180), (0, 0, screenWidth, 120))
        pygame.draw.rect(overlay, (5, 8, 15, 160), (0, screenHeight - 80, screenWidth, 80))
        screen.blit(overlay, (0, 0))

        # Ambient floating particles
        for p in self.particles:
            p.update()
            p.draw(screen)

        # ----------------------------------------------------------------------
        # Top Player Profile Badge (Left) - Clean typography, no bloated icons
        # ----------------------------------------------------------------------
        profile_rect = pygame.Rect(16, 14, 230, 40)
        draw_glass_card(screen, profile_rect, radius=10, bg_color=(15, 23, 42, 220), border_color=COLORS['border_subtle'])
        
        gold_font = get_font(14, bold=True)
        gold_str = f"Vàng: {self.player.money:,} G"
        draw_text_with_shadow(screen, gold_str, gold_font, COLORS['gold_light'], (profile_rect.x + 16, profile_rect.centery), align='midleft')
        
        # Max HP indicator
        hp_font = get_font(14, bold=True)
        draw_text_with_shadow(screen, f"Máu: {self.player.health} HP", hp_font, COLORS['white'], (profile_rect.x + 130, profile_rect.centery), align='midleft')

        # Top Quick Sound Toggle (Right)
        is_on = sound_manager.music_enabled
        self.btn_sound_quick.text = "NHẠC: BẬT" if is_on else "NHẠC: TẮT"
        self.btn_sound_quick.icon = None
        self.btn_sound_quick.draw(screen, mouse_pos)

        # ----------------------------------------------------------------------
        # Game Title Banner with subtle floating glow
        # ----------------------------------------------------------------------
        float_y = int(math.sin(self.time_counter * 1.5) * 4)
        title_y = 100 + float_y

        title_font = get_font(44, bold=True)
        # Glowing shadow
        draw_text_with_shadow(screen, "TOWER DEFENSE", title_font, COLORS['gold_light'], 
                              (screenWidth // 2, title_y), align='center', shadow_color=(245, 158, 11, 80), offset=(0, 0))
        draw_text_with_shadow(screen, "TOWER DEFENSE", title_font, COLORS['gold_light'], 
                              (screenWidth // 2, title_y), align='center', shadow_color=(0, 0, 0, 200), offset=(2, 3))

        # Subtitle Pill
        sub_rect = pygame.Rect(screenWidth // 2 - 130, title_y + 32, 260, 24)
        draw_rounded_rect(screen, (20, 30, 48, 200), sub_rect, radius=6, border_color=COLORS['cyan_glow'])
        sub_font = get_font(12, bold=True)
        draw_text_with_shadow(screen, "SPELL RUSH • VẼ PHÉP DIỆT QUÁI", sub_font, COLORS['cyan_light'], (sub_rect.centerx, sub_rect.centery), align='center')

        # ----------------------------------------------------------------------
        # Menu Central Glass Container
        # ----------------------------------------------------------------------
        panel_rect = pygame.Rect(screenWidth // 2 - 160, 210, 320, 325)
        draw_glass_card(screen, panel_rect, radius=16, bg_color=(15, 23, 42, 210), border_color=COLORS['border_subtle'], border_width=1)

        # Draw Menu Buttons
        self.btn_start.draw(screen, mouse_pos)
        self.btn_shop.draw(screen, mouse_pos)
        self.btn_instructions.draw(screen, mouse_pos)
        self.btn_settings.draw(screen, mouse_pos)
        self.btn_quit.draw(screen, mouse_pos)

        # Footer Version & Credits
        ver_font = get_font(12, bold=False)
        draw_text_with_shadow(screen, "Phiên bản Hiện đại v2.0 • Được tối ưu UI/UX chuyên nghiệp", ver_font, COLORS['text_dim'], 
                              (screenWidth // 2, screenHeight - 20), align='center')

        # ----------------------------------------------------------------------
        # Settings Modal (if opened)
        # ----------------------------------------------------------------------
        if self.show_settings:
            self.settings_modal.draw(screen, mouse_pos)

    def handle_click(self, mouse_pos):
        # If settings modal is open, forward click to modal
        if self.show_settings:
            # We will handle this in handle_event or check click
            return None

        # Check Quick Sound Toggle
        if self.btn_sound_quick.rect.collidepoint(mouse_pos):
            sound_manager.toggle_music()
            try:
                sound = pygame.mixer.Sound('sounds/click.mp3')
                sound.set_volume(0.3)
                sound.play()
            except Exception:
                pass
            return None

        # Check Start
        if self.btn_start.rect.collidepoint(mouse_pos):
            try:
                sound = pygame.mixer.Sound('sounds/click.mp3')
                sound.set_volume(0.4)
                sound.play()
            except Exception:
                pass
            return 0  # Start game

        # Check Shop
        if self.btn_shop.rect.collidepoint(mouse_pos):
            try:
                sound = pygame.mixer.Sound('sounds/click.mp3')
                sound.set_volume(0.4)
                sound.play()
            except Exception:
                pass
            return 1  # Shop

        # Check Instructions
        if self.btn_instructions.rect.collidepoint(mouse_pos):
            try:
                sound = pygame.mixer.Sound('sounds/click.mp3')
                sound.set_volume(0.4)
                sound.play()
            except Exception:
                pass
            return 2  # Instructions

        # Check Settings
        if self.btn_settings.rect.collidepoint(mouse_pos):
            try:
                sound = pygame.mixer.Sound('sounds/click.mp3')
                sound.set_volume(0.4)
                sound.play()
            except Exception:
                pass
            self.show_settings = True
            return None

        # Check Quit
        if self.btn_quit.rect.collidepoint(mouse_pos):
            try:
                sound = pygame.mixer.Sound('sounds/click.mp3')
                sound.set_volume(0.4)
                sound.play()
            except Exception:
                pass
            return 'quit'

        return None

    def handle_event(self, event):
        if self.show_settings:
            res = self.settings_modal.handle_event(event)
            if res == 'close':
                self.show_settings = False
            return None

        if self.btn_sound_quick.handle_event(event):
            sound_manager.toggle_music()
            self.btn_sound_quick.text = "NHẠC: BẬT" if sound_manager.music_enabled else "NHẠC: TẮT"
            self.btn_sound_quick.icon = "sound_on" if sound_manager.music_enabled else "sound_off"
            return None

        if self.btn_start.handle_event(event):
            return 0  # Start game
        if self.btn_shop.handle_event(event):
            return 1  # Shop
        if self.btn_instructions.handle_event(event):
            return 2  # Instructions
        if self.btn_settings.handle_event(event):
            self.show_settings = True
            return None
        if self.btn_quit.handle_event(event):
            return 'quit'

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.handle_click(event.pos)
            
        return None
