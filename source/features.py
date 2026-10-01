import pygame
import json
import os
from datetime import datetime
from save_system import SaveSystem
from setting import screenWidth, screenHeight

# Hệ thống Achievements
class AchievementSystem:
    def __init__(self):
        self.save_system = SaveSystem()
        self.achievements = self.save_system.get_achievements()
        self.notifications = []
        self.notification_duration = 3000  # 3 giây
        self.fonts = {}
        
    def get_font(self, size):
        if size not in self.fonts:
            self.fonts[size] = pygame.font.Font(None, size)
        return self.fonts[size]
        
    def check_achievements(self, player):
        current_time = pygame.time.get_ticks()
        
        # Kiểm tra và cập nhật thành tích
        if not self.achievements['kill_100']['unlocked'] and player.score >= 1000:
            self.unlock_achievement('kill_100')
        if not self.achievements['survive_10']['unlocked'] and player.wave >= 10:
            self.unlock_achievement('survive_10')
        if not self.achievements['level_10']['unlocked'] and player.level >= 10:
            self.unlock_achievement('level_10')
        if not self.achievements['money_1000']['unlocked'] and player.money >= 1000:
            self.unlock_achievement('money_1000')
            
        # Cập nhật thông báo
        self.notifications = [n for n in self.notifications if current_time - n['time'] < self.notification_duration]
                
    def unlock_achievement(self, achievement_id):
        if achievement_id in self.achievements and not self.achievements[achievement_id]['unlocked']:
            self.achievements[achievement_id]['unlocked'] = True
            self.save_system.update_achievement(achievement_id, True)
            self.notifications.append({
                'text': f"Thanh tich moi: {self.achievements[achievement_id]['name']}",
                'time': pygame.time.get_ticks()
            })
            return self.achievements[achievement_id]['name']
        return None

    def draw_notifications(self, screen):
        if not self.notifications:
            return
            
        font = self.get_font(32)
        y_offset = 10
        
        for notification in self.notifications:
            text = font.render(notification['text'], True, (255, 255, 255))
            text_rect = text.get_rect(topright=(screen.get_width() - 10, y_offset))
            
            # Vẽ background
            padding = 10
            bg_rect = text_rect.inflate(padding * 2, padding * 2)
            bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 180))
            screen.blit(bg_surface, bg_rect)
            
            # Vẽ text
            screen.blit(text, text_rect)
            y_offset += bg_rect.height + 5

    def draw_progress(self, screen):
        font = self.get_font(24)
        y_offset = screen.get_height() - 150
        x_offset = 10
        
        # Vẽ background cho tất cả thanh tiến độ
        visible_achievements = [a for a in self.achievements.values() if not a['unlocked']]
        if not visible_achievements:
            return
            
        total_height = len(visible_achievements) * 30
        bg_rect = pygame.Rect(x_offset, y_offset, 200, total_height + 10)
        bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 180))
        screen.blit(bg_surface, bg_rect)
        
        for achievement in visible_achievements:
            # Vẽ tên thành tích
            text = font.render(achievement['name'], True, (255, 255, 255))
            screen.blit(text, (x_offset + 5, y_offset + 5))
            
            # Vẽ thanh tiến độ
            progress_rect = pygame.Rect(x_offset + 5, y_offset + 25, 190, 5)
            pygame.draw.rect(screen, (100, 100, 100), progress_rect)
            
            # Tính phần trăm hoàn thành
            if achievement['name'] == 'SAT THU':
                progress = min(1.0, player.score / 1000)
            elif achievement['name'] == 'KIEN NGHI':
                progress = min(1.0, player.wave / 10)
            elif achievement['name'] == 'HUYEN THOAI':
                progress = min(1.0, player.level / 10)
            elif achievement['name'] == 'TY PHU':
                progress = min(1.0, player.money / 1000)
                
            if progress > 0:
                progress_width = int(190 * progress)
                progress_rect = pygame.Rect(x_offset + 5, y_offset + 25, progress_width, 5)
                pygame.draw.rect(screen, (0, 255, 0), progress_rect)
                
            y_offset += 30

# Hệ thống Power-ups
class PowerUpSystem:
    def __init__(self):
        self.active_powerups = {}
        self.powerup_types = {
            'speed': {'duration': 10, 'effect': lambda player: setattr(player, 'speed', player.speed * 1.5)},
            'damage': {'duration': 15, 'effect': lambda player: setattr(player, 'damage', player.damage * 2)},
            'heal': {'duration': 0, 'effect': lambda player: setattr(player, 'health', min(player.health + 1, player.max_health))}
        }
        
    def spawn_powerup(self, x, y):
        powerup_type = random.choice(list(self.powerup_types.keys()))
        return {'type': powerup_type, 'x': x, 'y': y, 'rect': pygame.Rect(x, y, 20, 20)}
        
    def activate_powerup(self, powerup_type, player):
        if powerup_type in self.powerup_types:
            self.powerup_types[powerup_type]['effect'](player)
            if self.powerup_types[powerup_type]['duration'] > 0:
                self.active_powerups[powerup_type] = {
                    'start_time': pygame.time.get_ticks(),
                    'duration': self.powerup_types[powerup_type]['duration']
                }
                
    def update_powerups(self, player):
        current_time = pygame.time.get_ticks()
        for powerup_type in list(self.active_powerups.keys()):
            if current_time - self.active_powerups[powerup_type]['start_time'] >= self.active_powerups[powerup_type]['duration'] * 1000:
                del self.active_powerups[powerup_type]
                # Reset effect
                if powerup_type == 'speed':
                    player.speed = player.speed / 1.5
                elif powerup_type == 'damage':
                    player.damage = player.damage / 2

# Hệ thống Shop
class ShopSystem:
    def __init__(self):
        self.save_system = SaveSystem()
        self.items = self.save_system.get_shop_items()
        self.fonts = {}
        try:
            self.background = pygame.image.load("background/Background_MergedForReference.jpg")
            if pygame.display.get_init():
                self.background = self.background.convert()
            self.background = pygame.transform.scale(self.background, (screenWidth, screenHeight))
        except Exception:
            self.background = None

        from ui_framework import ModernButton
        self.btn_back = ModernButton((16, 16, 110, 38), "QUAY LẠI", icon="arrow_left", style="glass", font_size=13, radius=8)
        self.buy_buttons = {}
        
    def get_font(self, size, bold=True):
        from ui_framework import get_font
        return get_font(size, bold=bold)
        
    def draw_shop(self, screen):
        from ui_framework import (
            COLORS, get_font, draw_glass_card, draw_rounded_rect, 
            draw_text_with_shadow, draw_icon, ModernButton
        )

        mouse_pos = pygame.mouse.get_pos()

        # Background
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(COLORS['bg_dark'])

        # Dark overlay
        overlay = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
        overlay.fill((10, 15, 28, 220))
        screen.blit(overlay, (0, 0))

        # Top Header Bar
        header_rect = pygame.Rect(0, 0, screenWidth, 70)
        draw_glass_card(screen, header_rect, radius=0, bg_color=(15, 23, 42, 230), border_color=COLORS['border_subtle'])

        # Back button
        self.btn_back.draw(screen, mouse_pos)

        # Title & Subtitle (Left side next to Back button - Never overlaps badges on right)
        title_font = get_font(20, bold=True)
        draw_text_with_shadow(screen, "CỬA HÀNG NÂNG CẤP", title_font, COLORS['gold_light'], 
                              (138, 17), align='topleft')
        sub_font = get_font(12, bold=False)
        draw_text_with_shadow(screen, "Gia tăng chỉ số sinh tồn và năng lực phòng thủ căn cứ", sub_font, COLORS['text_muted'], 
                              (138, 43), align='topleft')

        # Status Badges (Right side of header) - Clean typography, minimal icon usage
        current_money = self.save_system.get_money()
        current_health = self.save_system.get_total_health()

        money_badge = pygame.Rect(screenWidth - 256, 16, 120, 38)
        draw_glass_card(screen, money_badge, radius=8, bg_color=(20, 30, 48, 220), border_color=COLORS['gold_glow'])
        draw_text_with_shadow(screen, f"{current_money:,} Vàng", get_font(13, bold=True), COLORS['gold_light'], 
                              (money_badge.centerx, money_badge.centery), align='center')

        hp_badge = pygame.Rect(screenWidth - 126, 16, 110, 38)
        draw_glass_card(screen, hp_badge, radius=8, bg_color=(20, 30, 48, 220), border_color=COLORS['red_glow'])
        draw_text_with_shadow(screen, f"Máu: {current_health} HP", get_font(13, bold=True), COLORS['white'], 
                              (hp_badge.centerx, hp_badge.centery), align='center')

        # Shop Item Cards
        card_w = 600
        card_h = 86
        card_x = (screenWidth - card_w) // 2
        y_offset = 100
        spacing = 98

        item_descs = {
            'health_1': "Tăng thêm +1 Máu tối đa vĩnh viễn cho căn cứ",
            'health_2': "Tăng thêm +2 Máu tối đa vĩnh viễn cho căn cứ (Ưu đãi 100 G)",
            'health_3': "Tăng thêm +3 Máu tối đa vĩnh viễn cho căn cứ (Ưu đãi 300 G)"
        }

        for item_id, item in self.items.items():
            card_rect = pygame.Rect(card_x, y_offset, card_w, card_h)
            is_hovered = card_rect.collidepoint(mouse_pos)
            
            # Card background
            card_bg = (30, 45, 70, 240) if is_hovered else (20, 30, 48, 220)
            card_border = COLORS['border_light'] if is_hovered else COLORS['border_subtle']
            draw_glass_card(screen, card_rect, radius=12, bg_color=card_bg, border_color=card_border, border_width=1)

            # Item Name and Level (Clean left alignment, no oversized icon container)
            name_font = get_font(17, bold=True)
            draw_text_with_shadow(screen, item['name'], name_font, COLORS['white'], 
                                  (card_rect.x + 24, card_rect.y + 18), align='topleft')

            # Level badge
            bought_count = item.get('bought', 0)
            lvl_text = f"Cấp {bought_count}"
            lvl_font = get_font(11, bold=True)
            lvl_w = lvl_font.size(lvl_text)[0] + 16
            lvl_badge = pygame.Rect(card_rect.x + 24 + name_font.size(item['name'])[0] + 10, card_rect.y + 18, lvl_w, 20)
            draw_rounded_rect(screen, (40, 60, 90), lvl_badge, radius=4, border_color=COLORS['cyan_glow'])
            draw_text_with_shadow(screen, lvl_text, lvl_font, COLORS['cyan_light'], 
                                  (lvl_badge.centerx, lvl_badge.centery), align='center')

            # Description
            desc = item_descs.get(item_id, "Vật phẩm nâng cấp hữu ích")
            desc_font = get_font(13, bold=False)
            draw_text_with_shadow(screen, desc, desc_font, COLORS['text_muted'], 
                                  (card_rect.x + 24, card_rect.y + 46), align='topleft')

            # Cost pill with Gold coin icon
            cost = item['cost']
            can_afford = current_money >= cost
            cost_rect = pygame.Rect(card_rect.right - 235, card_rect.centery - 16, 105, 32)
            draw_rounded_rect(screen, (15, 23, 42, 200), cost_rect, radius=6, border_color=COLORS['gold_glow'])
            draw_icon(screen, "gold", cost_rect.x + 16, cost_rect.centery, size=16)
            draw_text_with_shadow(screen, f"{cost:,} Vàng", get_font(13, bold=True), COLORS['gold_light'], 
                                  (cost_rect.centerx + 8, cost_rect.centery), align='center')

            # Buy button with tactile press feedback
            buy_rect = pygame.Rect(card_rect.right - 120, card_rect.centery - 20, 104, 40)
            btn_style = 'success' if can_afford else 'glass'
            btn_text = "MUA" if can_afford else "THIẾU TIỀN"
            if item_id not in self.buy_buttons:
                self.buy_buttons[item_id] = ModernButton(buy_rect, btn_text, icon=None, 
                                                         style=btn_style, font_size=13, radius=8, enabled=can_afford)
            else:
                self.buy_buttons[item_id].rect = buy_rect
                self.buy_buttons[item_id].text = btn_text
                self.buy_buttons[item_id].style = btn_style
                self.buy_buttons[item_id].enabled = can_afford
            self.buy_buttons[item_id].draw(screen, mouse_pos)

            y_offset += spacing

        # Footer guide
        guide_font = get_font(13, bold=False)
        draw_text_with_shadow(screen, "Mẹo: Máu được nâng cấp sẽ có hiệu lực vĩnh viễn trong mọi màn chơi!", 
                              guide_font, COLORS['gold_light'], (screenWidth // 2, screenHeight - 48), align='center')
        draw_text_with_shadow(screen, "Nhấn phím ESC hoặc nút 'QUAY LẠI' ở góc trên để trở về Menu chính", 
                              get_font(11, bold=False), COLORS['text_dim'], (screenWidth // 2, screenHeight - 26), align='center')

    def handle_event(self, event, player):
        if self.btn_back.handle_event(event):
            return 'back'

        for item_id, btn in self.buy_buttons.items():
            if btn.handle_event(event):
                item = self.items.get(item_id)
                if item and player.money >= item['cost']:
                    if self.buy_item(item_id, player):
                        try:
                            from setting import play_sound
                            play_sound('sounds/buy.mp3', 0.4)
                        except Exception:
                            pass
                else:
                    try:
                        from setting import play_sound
                        play_sound('sounds/life_lost.mp3', 0.3)
                    except Exception:
                        pass
                return True
        return False

    def buy_item(self, item_id, player):
        if item_id in self.items:
            item = self.items[item_id]
            if player.money >= item['cost']:
                # Trừ tiền và cập nhật vào save system
                player.money -= item['cost']
                self.save_system.update_money(player.money)
                
                # Tăng số lần mua và cập nhật vào save system
                self.items[item_id]['bought'] += 1
                self.save_system.update_shop_items(self.items)
                
                # Cập nhật sức khỏe
                total_health = self.get_total_health()
                player.health = total_health
                player.max_health = total_health
                    
                return True
        return False
        
    def get_total_health(self):
        return self.save_system.get_total_health()

# Hệ thống Daily Challenges
class DailyChallengeSystem:
    def __init__(self):
        self.challenges = {
            'kill_50': {'name': 'Tiêu Diệt 50 Quái', 'reward': 100, 'progress': 0, 'completed': False},
            'survive_5': {'name': 'Sống Sót 5 Wave', 'reward': 200, 'progress': 0, 'completed': False},
            'earn_500': {'name': 'Kiếm 500 Tiền', 'reward': 300, 'progress': 0, 'completed': False}
        }
        self.last_reset = None
        self.load_progress()
        
    def load_progress(self):
        if os.path.exists('daily_challenges.json'):
            with open('daily_challenges.json', 'r') as f:
                data = json.load(f)
                self.challenges = data['challenges']
                self.last_reset = datetime.fromisoformat(data['last_reset'])
                
    def save_progress(self):
        with open('daily_challenges.json', 'w') as f:
            json.dump({
                'challenges': self.challenges,
                'last_reset': self.last_reset.isoformat() if self.last_reset else None
            }, f)
            
    def check_reset(self):
        current_date = datetime.now().date()
        if self.last_reset is None or self.last_reset.date() < current_date:
            self.reset_challenges()
            
    def reset_challenges(self):
        for challenge in self.challenges.values():
            challenge['progress'] = 0
            challenge['completed'] = False
        self.last_reset = datetime.now()
        self.save_progress()
        
    def update_progress(self, challenge_id, amount, player):
        if challenge_id in self.challenges and not self.challenges[challenge_id]['completed']:
            self.challenges[challenge_id]['progress'] += amount
            if self.check_completion(challenge_id):
                self.complete_challenge(challenge_id, player)
                
    def check_completion(self, challenge_id):
        challenge = self.challenges[challenge_id]
        if challenge_id == 'kill_50' and challenge['progress'] >= 50:
            return True
        elif challenge_id == 'survive_5' and challenge['progress'] >= 5:
            return True
        elif challenge_id == 'earn_500' and challenge['progress'] >= 500:
            return True
        return False
        
    def complete_challenge(self, challenge_id, player):
        self.challenges[challenge_id]['completed'] = True
        player.money += self.challenges[challenge_id]['reward']
        self.save_progress()

# Hệ thống Sound Effects
class SoundSystem:
    def __init__(self):
        self.sounds = {}
        self.volume = 0.5
        self.load_sounds()
        
    def load_sounds(self):
        sound_files = {
            'kill': 'sounds/kill.mp3',
            'level_up': 'sounds/level_up.mp3',
            'buy': 'sounds/buy.mp3',
            'achievement': 'sounds/achievement.mp3'
        }
        
        for sound_id, file_path in sound_files.items():
            try:
                self.sounds[sound_id] = pygame.mixer.Sound(file_path)
            except:
                print(f"Không thể tải âm thanh: {file_path}")
                
    def play_sound(self, sound_id):
        if sound_id in self.sounds:
            self.sounds[sound_id].set_volume(self.volume)
            self.sounds[sound_id].play()
            
    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume) 