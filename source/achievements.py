import pygame
import json
import os
import time
from ui_framework import (
    COLORS, get_font, draw_glass_card, draw_rounded_rect, 
    draw_text_with_shadow, draw_icon, draw_modern_bar, ToastNotification
)

class AchievementSystem:
    def __init__(self):
        self.achievements = {
            'kill_10': {'name': 'Sát Thủ Tập Sự', 'desc': 'Tiêu diệt 10 quái vật', 'target': 10, 'current': 0, 'unlocked': False},
            'survive_5': {'name': 'Kiên Nghị Bất Khuất', 'desc': 'Sống sót qua 5 wave', 'target': 5, 'current': 0, 'unlocked': False},
            'level_5': {'name': 'Huyền Thoại Trỗi Dậy', 'desc': 'Đạt nhân vật cấp 5', 'target': 5, 'current': 0, 'unlocked': False},
            'money_500': {'name': 'Nhà Tài Phiệt', 'desc': 'Tích lũy 500 tiền vàng', 'target': 500, 'current': 0, 'unlocked': False},
            'kill_50': {'name': 'Chiến Binh Quả Cảm', 'desc': 'Tiêu diệt 50 quái vật', 'target': 50, 'current': 0, 'unlocked': False},
            'survive_10': {'name': 'Anh Hùng Bảo Quốc', 'desc': 'Sống sót qua 10 wave', 'target': 10, 'current': 0, 'unlocked': False}
        }
        self.toasts = []
        self.load_achievements()
        
    def load_achievements(self):
        if os.path.exists('achievements.json'):
            try:
                with open('achievements.json', 'r', encoding='utf-8') as f:
                    saved = json.load(f)
                    for k, v in saved.items():
                        if k in self.achievements:
                            self.achievements[k]['current'] = v.get('current', 0)
                            self.achievements[k]['unlocked'] = v.get('unlocked', False)
            except Exception:
                pass
                
    def save_achievements(self):
        try:
            with open('achievements.json', 'w', encoding='utf-8') as f:
                json.dump(self.achievements, f, indent=4, ensure_ascii=False)
        except Exception:
            pass
            
    def check_achievements(self, player):
        kill_count = player.score // 100
        self.achievements['kill_10']['current'] = min(kill_count, 10)
        self.achievements['kill_50']['current'] = min(kill_count, 50)
        self.achievements['survive_5']['current'] = min(player.wave, 5)
        self.achievements['survive_10']['current'] = min(player.wave, 10)
        self.achievements['level_5']['current'] = min(player.level, 5)
        self.achievements['money_500']['current'] = min(player.money, 500)
        
        for ach_id, data in self.achievements.items():
            if not data['unlocked'] and data['current'] >= data['target']:
                self.unlock_achievement(ach_id)
                
    def unlock_achievement(self, achievement_id):
        if achievement_id in self.achievements and not self.achievements[achievement_id]['unlocked']:
            self.achievements[achievement_id]['unlocked'] = True
            name = self.achievements[achievement_id]['name']
            desc = self.achievements[achievement_id]['desc']
            
            # Create modern toast
            self.toasts.append(ToastNotification(
                title=f"THÀNH TÍCH: {name}",
                message=desc,
                icon="trophy",
                duration=3.5,
                border_color=COLORS['gold_light']
            ))
            
            # Sound notification
            try:
                s = pygame.mixer.Sound('sounds/new upgrade.mp3')
                s.set_volume(0.4)
                s.play()
            except Exception:
                pass
                
            self.save_achievements()
            
    def draw_notifications(self, screen):
        # Clean expired toasts
        self.toasts = [t for t in self.toasts if not t.is_expired()]
        
        y_offset = 75
        for toast in self.toasts:
            toast_x = screen.get_width() - toast.width - 16
            toast.draw(screen, toast_x, y_offset)
            y_offset += toast.height + 10
            
    def draw_progress(self, screen):
        # Find active (in-progress) achievements
        visible_achievements = [ach for ach in self.achievements.values() if not ach['unlocked']]
        if not visible_achievements:
            return

        # Show at most 2 closest achievements to keep screen clean
        visible_achievements.sort(key=lambda a: a['current'] / max(1, a['target']), reverse=True)
        tracked = visible_achievements[:2]

        card_w = 210
        item_h = 36
        card_h = 24 + len(tracked) * item_h
        card_x = 14
        card_y = screen.get_height() - card_h - 14

        card_rect = pygame.Rect(card_x, card_y, card_w, card_h)
        draw_glass_card(screen, card_rect, radius=8, bg_color=(15, 23, 42, 210), border_color=COLORS['border_subtle'])

        # Header (Clean text)
        header_font = get_font(11, bold=True)
        draw_text_with_shadow(screen, "TIẾN ĐỘ THÀNH TÍCH", header_font, COLORS['text_secondary'], 
                              (card_rect.x + 12, card_rect.y + 12), align='midleft')

        cur_y = card_rect.y + 24
        for ach in tracked:
            cur = ach['current']
            target = ach['target']
            name = ach['name']

            # Text
            name_font = get_font(11, bold=True)
            draw_text_with_shadow(screen, name, name_font, COLORS['white'], (card_rect.x + 12, cur_y + 4), align='topleft')
            
            cnt_font = get_font(10, bold=False)
            draw_text_with_shadow(screen, f"{cur}/{target}", cnt_font, COLORS['gold_light'], (card_rect.right - 12, cur_y + 4), align='topright')

            # Bar
            bar_rect = pygame.Rect(card_rect.x + 12, cur_y + 20, card_w - 24, 6)
            draw_modern_bar(screen, bar_rect, cur, target, fill_color=COLORS['cyan'], radius=3)

            cur_y += item_h