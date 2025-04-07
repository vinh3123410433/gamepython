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
        self.background = pygame.image.load("background/WDT1.PNG")
        self.background = pygame.transform.scale(self.background, (screenWidth, screenHeight))
        
    def get_font(self, size):
        if size not in self.fonts:
            self.fonts[size] = pygame.font.Font(None, size)
        return self.fonts[size]
        
    def draw_shop(self, screen):
        # Vẽ background
        screen.blit(self.background, (0, 0))
        
        # Vẽ tiêu đề
        title = self.get_font(48).render("CUA HANG", True, (255, 215, 0))
        title_rect = title.get_rect(centerx=screen.get_width() // 2, y=70)
        screen.blit(title, title_rect)
        
        # Vẽ số tiền hiện tại
        current_money = self.save_system.get_money()
        money_text = self.get_font(36).render(f"Tien: {current_money}", True, (255, 215, 0))
        money_rect = money_text.get_rect(centerx=screen.get_width() // 2, y=100)
        screen.blit(money_text, money_rect)
        
        # Vẽ số máu hiện tại
        current_health = self.save_system.get_total_health()
        health_text = self.get_font(36).render(f"Mau: {current_health}", True, (255, 215, 0))
        health_rect = health_text.get_rect(centerx=screen.get_width() // 2, y=150)
        screen.blit(health_text, health_rect)
        
        # Vẽ hướng dẫn
        guide_text = self.get_font(24).render("Nhan ESC de quay lai menu", True, (200, 200, 200))
        guide_rect = guide_text.get_rect(centerx=screen.get_width() // 2, y=screen.get_height() - 50)
        screen.blit(guide_text, guide_rect)
        
        # Vẽ các item
        y_offset = 200
        for item_id, item in self.items.items():
            # Vẽ background cho item
            item_bg_image = pygame.image.load('background/Tab2.PNG')
            item_rect = pygame.Rect(screen.get_width() // 4, y_offset, screen.get_width() // 2, 80)
            item_bg_scaled = pygame.transform.scale(item_bg_image, item_rect.size)
            screen.blit(item_bg_scaled, item_rect.topleft)
            
            # Vẽ tên item và số lần đã mua
            name_text = self.get_font(36).render(f"{item['name']} (Da mua: {item['bought']})", True, (255, 255, 255))
            name_rect = name_text.get_rect(midleft=(item_rect.left + 20, item_rect.centery - 15))
            screen.blit(name_text, name_rect)
            
            # Vẽ giá
            cost_text = self.get_font(24).render(f"Gia: {item['cost']} tien", True, (255, 215, 0))
            cost_rect = cost_text.get_rect(midleft=(item_rect.left + 20, item_rect.centery + 15))
            screen.blit(cost_text, cost_rect)
            
            # Vẽ nút mua
            buy_rect = pygame.Rect(item_rect.right - 100, item_rect.centery - 20, 70, 40)
            mouse_pos = pygame.mouse.get_pos()
            
            if buy_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (0, 255, 0), buy_rect)  # Hover màu sáng hơn
            else:
                pygame.draw.rect(screen, (0, 200, 0), buy_rect)

            buy_text = self.get_font(24).render("MUA", True, (255, 255, 255))
            buy_text_rect = buy_text.get_rect(center=buy_rect.center)
            screen.blit(buy_text, buy_text_rect)
            
            y_offset += 100
                
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