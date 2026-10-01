import pygame
import math
import time
from setting import screenWidth, screenHeight, sound_manager
from ui_framework import (
    COLORS, get_font, draw_glass_card, draw_rounded_rect, 
    draw_text_with_shadow, draw_icon, draw_modern_bar, ModernButton
)
from setting_ui import SettingsModal

# ==============================================================================
# GAMEPLAY HUD (TOP STATUS DOCK & BOTTOM TACTICAL BAR)
# ==============================================================================
class GameplayHUD:
    def __init__(self):
        self.time_counter = 0.0

        # Top Buttons
        self.btn_pause = ModernButton((screenWidth - 50, 10, 40, 36), "", icon="pause", style="glass", radius=8, tooltip="Tạm dừng (ESC)")
        self.btn_sound = ModernButton((screenWidth - 98, 10, 40, 36), "", icon="sound_on" if sound_manager.music_enabled else "sound_off", style="glass", radius=8, tooltip="Âm thanh")

        # Bottom Buttons (Clean text, no extra vector icons)
        self.btn_speed_down = ModernButton((screenWidth - 260, screenHeight - 48, 36, 36), "S", icon=None, style="glass", font_size=13, radius=8, tooltip="Giảm tốc độ (S)")
        self.btn_speed_up = ModernButton((screenWidth - 150, screenHeight - 48, 36, 36), "W", icon=None, style="glass", font_size=13, radius=8, tooltip="Tăng tốc độ (W)")
        self.btn_hail = ModernButton((screenWidth - 106, screenHeight - 48, 96, 36), "MƯA ĐÁ [H]", icon="spark", style="purple", font_size=11, radius=8, tooltip="Thiên thạch (2000 G)")

        # Gesture feedback state
        self.feedback_text = None
        self.feedback_icon = None
        self.feedback_time = 0
        self.feedback_duration = 1.6

    def show_feedback(self, shape_name):
        labels = {
            "horizontal": ("✦ GẠCH NGANG CHÍNH XÁC! ✦", "star", COLORS['cyan_light']),
            "vertical": ("✦ GẠCH ĐỨNG CHÍNH XÁC! ✦", "star", COLORS['gold_light']),
            "diagonal_right": ("✦ GẠCH CHÉO PHẢI CHÍNH XÁC! ✦", "star", COLORS['purple_light']),
            "v_shape": ("✦ HÌNH CHỮ V CHÍNH XÁC! ✦", "star", COLORS['red_light']),
            "circle": ("✦ HÌNH TRÒN CHÍNH XÁC! ✦", "star", COLORS['green_light'])
        }
        if shape_name in labels:
            self.feedback_text, self.feedback_icon, self.feedback_color = labels[shape_name]
            self.feedback_time = time.time()

    def draw(self, screen, player, wave, max_waves, speed, is_wave_active, mouse_pos):
        self.time_counter += 0.03

        # ----------------------------------------------------------------------
        # Top Floating Island HUD Bar
        # ----------------------------------------------------------------------
        top_bar_rect = pygame.Rect(8, 8, screenWidth - 16, 44)
        draw_glass_card(screen, top_bar_rect, radius=10, bg_color=(15, 23, 42, 230), border_color=COLORS['border_subtle'])

        # 1. Health Bar (Left)
        hp_rect = pygame.Rect(top_bar_rect.x + 8, top_bar_rect.y + 7, 130, 30)
        hp_ratio = player.health / max(1, player.max_health)
        hp_color = COLORS['red'] if hp_ratio > 0.25 else COLORS['red_light']
        draw_modern_bar(screen, hp_rect, player.health, player.max_health, fill_color=hp_color, 
                        radius=6, label=f"HP {player.health}/{player.max_health}", icon="heart")

        # 2. EXP Bar & Level Badge
        exp_rect = pygame.Rect(hp_rect.right + 10, top_bar_rect.y + 7, 140, 30)
        draw_modern_bar(screen, exp_rect, player.exp, player.exp_to_next_level, fill_color=COLORS['cyan'],
                        radius=6, label=f"Lv.{player.level} [{player.exp}/{player.exp_to_next_level}]", icon=None)

        # 3. Wave Counter (Center)
        wave_pill = pygame.Rect(screenWidth // 2 - 80, top_bar_rect.y + 7, 85, 30)
        draw_rounded_rect(screen, (25, 38, 58), wave_pill, radius=6, border_color=COLORS['cyan_glow'])
        draw_text_with_shadow(screen, f"Wave {wave}/{max_waves}", get_font(12, bold=True), COLORS['white'], 
                              (wave_pill.centerx, wave_pill.centery), align='center')

        # 4. Score Display
        score_pill = pygame.Rect(wave_pill.right + 6, top_bar_rect.y + 7, 95, 30)
        draw_rounded_rect(screen, (25, 38, 58), score_pill, radius=6, border_color=COLORS['border_subtle'])
        draw_text_with_shadow(screen, f"{player.score:,}", get_font(12, bold=True), COLORS['gold_light'], 
                              (score_pill.centerx, score_pill.centery), align='center')

        # 5. Money Gold Badge with coin icon
        money_rect = pygame.Rect(score_pill.right + 10, top_bar_rect.y + 7, 120, 30)
        draw_rounded_rect(screen, (25, 35, 20), money_rect, radius=6, border_color=COLORS['gold_glow'])
        draw_icon(screen, "gold", money_rect.x + 18, money_rect.centery, size=18)
        draw_text_with_shadow(screen, f"{player.money:,} G", get_font(13, bold=True), COLORS['gold_light'], 
                              (money_rect.centerx + 8, money_rect.centery), align='center')

        # 6. Action buttons (Sound toggle and Pause)
        self.btn_sound.icon = "sound_on" if sound_manager.music_enabled else "sound_off"
        self.btn_sound.draw(screen, mouse_pos)
        self.btn_pause.draw(screen, mouse_pos)

        # ----------------------------------------------------------------------
        # Bottom Tactical Dock (Speed controls & Hail skill)
        # ----------------------------------------------------------------------
        dock_rect = pygame.Rect(screenWidth - 270, screenHeight - 54, 262, 46)
        draw_glass_card(screen, dock_rect, radius=10, bg_color=(15, 23, 42, 225), border_color=COLORS['border_subtle'])

        # Speed down button
        self.btn_speed_down.draw(screen, mouse_pos)

        # Speed pill
        speed_rect = pygame.Rect(screenWidth - 220, screenHeight - 48, 66, 36)
        draw_rounded_rect(screen, (25, 35, 55), speed_rect, radius=6, border_color=COLORS['border_subtle'])
        draw_text_with_shadow(screen, f"{speed}x", get_font(14, bold=True), COLORS['cyan_light'], 
                              (speed_rect.centerx, speed_rect.centery), align='center')

        # Speed up button
        self.btn_speed_up.draw(screen, mouse_pos)

        # Hail Skill button
        can_afford_hail = player.money >= 2000
        self.btn_hail.set_enabled(can_afford_hail)
        self.btn_hail.style = 'purple' if can_afford_hail else 'glass'
        self.btn_hail.draw(screen, mouse_pos)

        # ----------------------------------------------------------------------
        # Wave Start Prompt (When idle)
        # ----------------------------------------------------------------------
        if not is_wave_active and wave <= max_waves:
            pulse = (math.sin(self.time_counter * 3.5) + 1.0) * 0.5
            banner_w = 340
            banner_h = 36
            banner_rect = pygame.Rect((screenWidth - banner_w) // 2, screenHeight - 52, banner_w, banner_h)
            
            # Glowing border
            border_alpha = int(120 + 135 * pulse)
            border_c = (245, 158, 11, border_alpha)
            draw_glass_card(screen, banner_rect, radius=8, bg_color=(20, 30, 48, 230), border_color=border_c, border_width=2)
            
            p_font = get_font(13, bold=True)
            text = f"✦ NHẤN SPACE ĐỂ BẮT ĐẦU WAVE {wave} ✦"
            t_color = (255, 220 + int(35 * pulse), 100 + int(155 * pulse))
            draw_text_with_shadow(screen, text, p_font, t_color, (banner_rect.centerx, banner_rect.centery), align='center')

        # ----------------------------------------------------------------------
        # Gesture Feedback Banner
        # ----------------------------------------------------------------------
        if self.feedback_text and (time.time() - self.feedback_time) < self.feedback_duration:
            elapsed = time.time() - self.feedback_time
            alpha = max(0, min(255, int(255 * (1.0 - (elapsed / self.feedback_duration) ** 2))))
            
            card_w = 300
            card_h = 40
            fb_rect = pygame.Rect((screenWidth - card_w) // 2, screenHeight - 110, card_w, card_h)
            
            fb_surf = pygame.Surface(fb_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(fb_surf, (15, 23, 42, min(230, alpha)), fb_surf.get_rect(), border_radius=10)
            pygame.draw.rect(fb_surf, self.feedback_color[:3] + (min(255, alpha),), fb_surf.get_rect(), width=2, border_radius=10)
            screen.blit(fb_surf, fb_rect.topleft)
            
            fb_font = get_font(13, bold=True)
            text_surf = fb_font.render(self.feedback_text, True, self.feedback_color)
            text_surf.set_alpha(alpha)
            screen.blit(text_surf, text_surf.get_rect(center=fb_rect.center))
        else:
            self.feedback_text = None

    def draw_magic_trail(self, screen, pos_list):
        if len(pos_list) > 1:
            # Outer cyan glow
            glow_surf = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
            pygame.draw.lines(glow_surf, (56, 189, 248, 60), False, pos_list, 14)
            pygame.draw.lines(glow_surf, (56, 189, 248, 120), False, pos_list, 10)
            # Core bright beam
            pygame.draw.lines(glow_surf, (224, 242, 254, 240), False, pos_list, 5)
            screen.blit(glow_surf, (0, 0))

# ==============================================================================
# PAUSE MODAL OVERLAY
# ==============================================================================
class PauseModal:
    def __init__(self, on_resume=None, on_restart=None, on_menu=None):
        self.on_resume = on_resume
        self.on_restart = on_restart
        self.on_menu = on_menu

        self.width = 380
        self.height = 360
        self.rect = pygame.Rect((screenWidth - self.width) // 2, (screenHeight - self.height) // 2, self.width, self.height)

        btn_w = 260
        btn_h = 44
        btn_x = (screenWidth - btn_w) // 2
        start_y = self.rect.y + 105
        spacing = 54

        self.btn_resume = ModernButton((btn_x, start_y, btn_w, btn_h), "TIẾP TỤC", icon="play", style="primary", font_size=16)
        self.btn_settings = ModernButton((btn_x, start_y + spacing, btn_w, btn_h), "CÀI ĐẶT", icon=None, style="glass", font_size=16)
        self.btn_restart = ModernButton((btn_x, start_y + spacing * 2, btn_w, btn_h), "CHƠI LẠI TRẬN NÀY", icon="replay", style="glass", font_size=15)
        self.btn_menu = ModernButton((btn_x, start_y + spacing * 3, btn_w, btn_h), "VỀ MENU CHÍNH", icon="home", style="danger", font_size=15)

        self.show_settings = False
        self.settings_modal = SettingsModal(on_close=self.close_settings)

    def close_settings(self):
        self.show_settings = False

    def draw(self, screen, mouse_pos, player, wave):
        # Frosted glass dark overlay
        backdrop = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
        backdrop.fill((8, 12, 22, 195))
        screen.blit(backdrop, (0, 0))

        if self.show_settings:
            self.settings_modal.draw(screen, mouse_pos)
            return

        # Modal Container
        draw_glass_card(screen, self.rect, radius=16, bg_color=(15, 23, 42, 245), border_color=COLORS['border_light'], border_width=2)

        # Header Title
        title_font = get_font(26, bold=True)
        draw_text_with_shadow(screen, "TẠM DỪNG (PAUSED)", title_font, COLORS['gold_light'], 
                              (self.rect.centerx, self.rect.y + 35), align='center')
        
        # Subtitle Status
        sub_font = get_font(13, bold=False)
        sub_text = f"Wave hiện tại: {wave} • Điểm số: {player.score:,} • Vàng: {player.money:,} G"
        draw_text_with_shadow(screen, sub_text, sub_font, COLORS['text_secondary'], 
                              (self.rect.centerx, self.rect.y + 65), align='center')

        pygame.draw.line(screen, COLORS['border_subtle'], 
                         (self.rect.x + 25, self.rect.y + 85), (self.rect.right - 25, self.rect.y + 85), 1)

        # Buttons
        self.btn_resume.draw(screen, mouse_pos)
        self.btn_settings.draw(screen, mouse_pos)
        self.btn_restart.draw(screen, mouse_pos)
        self.btn_menu.draw(screen, mouse_pos)

    def handle_event(self, event):
        if self.show_settings:
            res = self.settings_modal.handle_event(event)
            if res == 'close':
                self.show_settings = False
            return 'settings_active'

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'resume'

        if self.btn_resume.handle_event(event):
            return 'resume'
        if self.btn_settings.handle_event(event):
            self.show_settings = True
            return 'settings'
        if self.btn_restart.handle_event(event):
            return 'restart'
        if self.btn_menu.handle_event(event):
            return 'menu'

        return None

# ==============================================================================
# TUTORIAL / INSTRUCTIONS SCREEN
# ==============================================================================
class TutorialScreen:
    def __init__(self):
        self.btn_back = ModernButton((16, 16, 110, 38), "QUAY LẠI", icon="arrow_left", style="glass", font_size=13, radius=8)
        try:
            self.bg_image = pygame.image.load("background/Background_MergedForReference.jpg")
            if pygame.display.get_init():
                self.bg_image = self.bg_image.convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (screenWidth, screenHeight))
        except Exception:
            self.bg_image = None

    def draw(self, screen, mouse_pos):
        if self.bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
            screen.fill((15, 23, 42))

        overlay = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
        overlay.fill((10, 15, 28, 220))
        screen.blit(overlay, (0, 0))

        # Top Header Bar
        header_rect = pygame.Rect(0, 0, screenWidth, 70)
        draw_glass_card(screen, header_rect, radius=0, bg_color=(15, 23, 42, 230), border_color=COLORS['border_subtle'])

        self.btn_back.draw(screen, mouse_pos)

        title_font = get_font(26, bold=True)
        draw_text_with_shadow(screen, "CẨM NANG HƯỚNG DẪN CHI TIẾT", title_font, COLORS['gold_light'], 
                              (screenWidth // 2, 26), align='center')
        sub_font = get_font(12, bold=False)
        draw_text_with_shadow(screen, "Nắm vững kỹ năng vẽ ký hiệu ma thuật để bảo vệ vương quốc", sub_font, COLORS['text_muted'], 
                              (screenWidth // 2, 50), align='center')

        # ----------------------------------------------------------------------
        # Card 1: Drawing Spells / Runes (Left)
        # ----------------------------------------------------------------------
        c1_rect = pygame.Rect(30, 85, 360, 420)
        draw_glass_card(screen, c1_rect, radius=12, bg_color=(20, 30, 48, 225), border_color=COLORS['cyan_glow'])
        draw_text_with_shadow(screen, "CƠ CHẾ VẼ KÝ HIỆU DIỆT QUÁI", get_font(16, bold=True), COLORS['cyan_light'], 
                              (c1_rect.centerx, c1_rect.y + 20), align='center')
        pygame.draw.line(screen, COLORS['border_subtle'], (c1_rect.x + 20, c1_rect.y + 36), (c1_rect.right - 20, c1_rect.y + 36), 1)

        runes_info = [
            ("Gạch ngang (—)", "Vẽ một nét ngang dài từ trái qua phải", (56, 189, 248)),
            ("Gạch đứng (|)", "Vẽ một nét thẳng đứng từ trên xuống dưới", (251, 191, 36)),
            ("Gạch chéo (/)", "Vẽ một nét chéo hướng lên về bên phải", (168, 85, 247)),
            ("Chữ V (V)", "Vẽ nét chữ V góc nhọn xuống dưới", (244, 63, 94)),
            ("Hình tròn (O)", "Vẽ một vòng cung hoặc vòng tròn khép kín", (52, 211, 153))
        ]

        cur_y = c1_rect.y + 50
        for name, guide, col in runes_info:
            # Rune sample box
            r_box = pygame.Rect(c1_rect.x + 16, cur_y, 44, 44)
            draw_rounded_rect(screen, (15, 23, 42), r_box, radius=8, border_color=col)
            
            # Draw sample symbol inside box
            cx, cy = r_box.centerx, r_box.centery
            if "ngang" in name:
                pygame.draw.line(screen, col, (cx - 14, cy), (cx + 14, cy), 3)
            elif "đứng" in name:
                pygame.draw.line(screen, col, (cx, cy - 14), (cx, cy + 14), 3)
            elif "chéo" in name:
                pygame.draw.line(screen, col, (cx - 10, cy + 10), (cx + 10, cy - 10), 3)
            elif "V" in name:
                pygame.draw.lines(screen, col, False, [(cx - 10, cy - 8), (cx, cy + 10), (cx + 10, cy - 8)], 3)
            elif "tròn" in name:
                pygame.draw.circle(screen, col, (cx, cy), 12, 3)

            draw_text_with_shadow(screen, name, get_font(14, bold=True), COLORS['white'], 
                                  (c1_rect.x + 70, cur_y + 10), align='topleft')
            draw_text_with_shadow(screen, guide, get_font(11, bold=False), COLORS['text_muted'], 
                                  (c1_rect.x + 70, cur_y + 28), align='topleft')
            cur_y += 56

        hint_box = pygame.Rect(c1_rect.x + 16, cur_y + 10, c1_rect.width - 32, 58)
        draw_rounded_rect(screen, (15, 23, 42, 200), hint_box, radius=6, border_color=COLORS['gold_glow'])
        draw_text_with_shadow(screen, "★ Lưu ý: Vẽ nét dứt khoát trên màn hình", get_font(12, bold=True), COLORS['gold_light'], 
                              (hint_box.centerx, hint_box.y + 16), align='center')
        draw_text_with_shadow(screen, "Hệ thống AI sẽ nhận diện tự động khi bạn thả chuột!", get_font(11, bold=False), COLORS['text_secondary'], 
                              (hint_box.centerx, hint_box.y + 36), align='center')

        # ----------------------------------------------------------------------
        # Card 2: Controls & Tactics (Right)
        # ----------------------------------------------------------------------
        c2_rect = pygame.Rect(410, 85, 360, 420)
        draw_glass_card(screen, c2_rect, radius=12, bg_color=(20, 30, 48, 225), border_color=COLORS['gold_glow'])
        draw_text_with_shadow(screen, "ĐIỀU KHIỂN & CHIẾN LƯỢC", get_font(16, bold=True), COLORS['gold_light'], 
                              (c2_rect.centerx, c2_rect.y + 20), align='center')
        pygame.draw.line(screen, COLORS['border_subtle'], (c2_rect.x + 20, c2_rect.y + 36), (c2_rect.right - 20, c2_rect.y + 36), 1)

        keys_info = [
            ("SPACE", "Bắt đầu đợt quái (Wave) mới"),
            ("Chuột Trái", "Nhấn giữ và kéo để vẽ phép thuật diệt quái"),
            ("W / S", "Tăng / Giảm tốc độ trò chơi (1x đến 10x)"),
            ("H", "Mua Cơn Mưa Thiên Thạch cứu nguy (2,000 G)"),
            ("ESC", "Tạm dừng trò chơi / Mở tùy chỉnh cấu hình")
        ]

        cur_y = c2_rect.y + 50
        for key_text, desc in keys_info:
            kb_rect = pygame.Rect(c2_rect.x + 16, cur_y, 76, 26)
            draw_rounded_rect(screen, (35, 50, 75), kb_rect, radius=4, border_color=COLORS['border_light'])
            draw_text_with_shadow(screen, key_text, get_font(12, bold=True), COLORS['white'], (kb_rect.centerx, kb_rect.centery), align='center')

            draw_text_with_shadow(screen, desc, get_font(12, bold=False), COLORS['text_secondary'], 
                                  (c2_rect.x + 102, cur_y + 13), align='midleft')
            cur_y += 42

        # Shop tip card
        shop_tip_rect = pygame.Rect(c2_rect.x + 16, cur_y + 10, c2_rect.width - 32, 110)
        draw_rounded_rect(screen, (15, 23, 42, 200), shop_tip_rect, radius=8, border_color=COLORS['green_glow'])
        draw_text_with_shadow(screen, "BÍ QUYẾT BẤT BẠI:", get_font(13, bold=True), COLORS['green_light'], 
                              (shop_tip_rect.x + 18, shop_tip_rect.y + 22), align='midleft')
        
        tips = [
            "• Tiêu diệt quái vật để tích lũy tiền vàng và thăng cấp.",
            "• Vào Cửa Hàng (Shop) ở Menu chính để tăng Máu tối đa.",
            "• Mở khóa đầy đủ các Thành tích để nhận vinh danh cao quý!"
        ]
        for idx, tip in enumerate(tips):
            draw_text_with_shadow(screen, tip, get_font(11, bold=False), COLORS['text_secondary'], 
                                  (shop_tip_rect.x + 14, shop_tip_rect.y + 44 + idx * 20), align='topleft')

        # Footer guide
        draw_text_with_shadow(screen, "Nhấn ESC hoặc nút 'QUAY LẠI' ở trên để trở về Menu chính", 
                              get_font(12, bold=False), COLORS['text_dim'], (screenWidth // 2, screenHeight - 24), align='center')

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'back'
        if self.btn_back.handle_event(event):
            return 'back'
        return None
