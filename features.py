import pygame
import json
import os
from datetime import datetime

# Hệ thống Achievements
class AchievementSystem:
    def __init__(self):
        self.achievements = {
            'kill_100': {'name': 'Sát Thủ', 'desc': 'Tiêu diệt 100 quái', 'unlocked': False},
            'survive_10': {'name': 'Kiên Nghị', 'desc': 'Sống sót 10 wave', 'unlocked': False},
            'level_10': {'name': 'Huyền Thoại', 'desc': 'Đạt level 10', 'unlocked': False},
            'money_1000': {'name': 'Tỷ Phú', 'desc': 'Có 1000 tiền', 'unlocked': False}
        }
        self.load_achievements()
        
    def load_achievements(self):
        if os.path.exists('achievements.json'):
            with open('achievements.json', 'r') as f:
                self.achievements = json.load(f)
                
    def save_achievements(self):
        with open('achievements.json', 'w') as f:
            json.dump(self.achievements, f)
            
    def check_achievement(self, achievement_id, player):
        if not self.achievements[achievement_id]['unlocked']:
            if achievement_id == 'kill_100' and player.score >= 1000:
                self.unlock_achievement(achievement_id)
            elif achievement_id == 'survive_10' and player.wave >= 10:
                self.unlock_achievement(achievement_id)
            elif achievement_id == 'level_10' and player.level >= 10:
                self.unlock_achievement(achievement_id)
            elif achievement_id == 'money_1000' and player.money >= 1000:
                self.unlock_achievement(achievement_id)
                
    def unlock_achievement(self, achievement_id):
        self.achievements[achievement_id]['unlocked'] = True
        self.save_achievements()
        return self.achievements[achievement_id]['name']

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
        self.items = {
            'max_health': {'name': 'Tăng Máu Tối Đa', 'cost': 500, 'effect': lambda player: setattr(player, 'max_health', player.max_health + 1)},
            'move_speed': {'name': 'Tăng Tốc Độ', 'cost': 300, 'effect': lambda player: setattr(player, 'move_speed', player.move_speed + 0.5)},
            'base_damage': {'name': 'Tăng Sát Thương', 'cost': 400, 'effect': lambda player: setattr(player, 'damage', player.damage + 1)}
        }
        
    def buy_item(self, item_id, player):
        if item_id in self.items and player.money >= self.items[item_id]['cost']:
            player.money -= self.items[item_id]['cost']
            self.items[item_id]['effect'](player)
            return True
        return False

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