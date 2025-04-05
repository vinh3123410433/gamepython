import pygame
import json
import os

class AchievementSystem:
    def __init__(self):
        self.achievements = {
            'kill_10': {'name': 'Sat Thu', 'desc': 'Tieu diet 10 quai', 'target': 10, 'current': 0, 'unlocked': False},
            'survive_5': {'name': 'Kien Nghi', 'desc': 'Song sot 5 wave', 'target': 5, 'current': 0, 'unlocked': False},
            'level_5': {'name': 'Huyen Thoai', 'desc': 'Dat level 5', 'target': 5, 'current': 0, 'unlocked': False},
            'money_500': {'name': 'Ty Phu', 'desc': 'Co 500 tien', 'target': 500, 'current': 0, 'unlocked': False},
            'kill_50': {'name': 'Chien Binh', 'desc': 'Tieu diet 50 quai', 'target': 50, 'current': 0, 'unlocked': False},
            'survive_10': {'name': 'Anh Hung', 'desc': 'Song sot 10 wave', 'target': 10, 'current': 0, 'unlocked': False}
        }
        self.notifications = []
        self.load_achievements()
        
    def load_achievements(self):
        if os.path.exists('achievements.json'):
            with open('achievements.json', 'r') as f:
                self.achievements = json.load(f)
                
    def save_achievements(self):
        with open('achievements.json', 'w') as f:
            json.dump(self.achievements, f)
            
    def check_achievements(self, player):
        # Cập nhật tiến độ hiện tại
        # Mỗi quái tăng 100 điểm, nên chia cho 100 để có số quái
        kill_count = player.score // 100
        self.achievements['kill_10']['current'] = min(kill_count, 10)
        self.achievements['kill_50']['current'] = min(kill_count, 50)
        self.achievements['survive_5']['current'] = min(player.wave, 5)
        self.achievements['survive_10']['current'] = min(player.wave, 10)
        self.achievements['level_5']['current'] = min(player.level, 5)
        self.achievements['money_500']['current'] = min(player.money, 500)
        
        # Kiểm tra và mở khóa thành tích
        for achievement_id in self.achievements:
            if not self.achievements[achievement_id]['unlocked']:
                if achievement_id == 'kill_10' and kill_count >= 10:
                    self.unlock_achievement(achievement_id)
                elif achievement_id == 'kill_50' and kill_count >= 50:
                    self.unlock_achievement(achievement_id)
                elif achievement_id == 'survive_5' and player.wave >= 5:
                    self.unlock_achievement(achievement_id)
                elif achievement_id == 'survive_10' and player.wave >= 10:
                    self.unlock_achievement(achievement_id)
                elif achievement_id == 'level_5' and player.level >= 5:
                    self.unlock_achievement(achievement_id)
                elif achievement_id == 'money_500' and player.money >= 500:
                    self.unlock_achievement(achievement_id)
                
    def unlock_achievement(self, achievement_id):
        if not self.achievements[achievement_id]['unlocked']:
            self.achievements[achievement_id]['unlocked'] = True
            self.notifications.append({
                'text': f"Thanh tich moi: {self.achievements[achievement_id]['name']}",
                'desc': self.achievements[achievement_id]['desc'],
                'time': pygame.time.get_ticks()
            })
            self.save_achievements()
            
    def draw_notifications(self, screen):
        current_time = pygame.time.get_ticks()
        y_offset = 10  # Khoảng cách từ trên xuống
        
        for notification in self.notifications[:]:
            if current_time - notification['time'] > 3000:  # Hiển thị trong 3 giây
                self.notifications.remove(notification)
            else:
                alpha = min(255, int(255 * (1 - (current_time - notification['time']) / 3000)))
                font = pygame.font.Font(None, 32)  # Giảm kích thước font
                text = font.render(notification['text'], True, (255, 215, 0))
                desc = font.render(notification['desc'], True, (255, 255, 255))
                
                # Vẽ background với alpha
                padding = 10
                width = max(text.get_width(), desc.get_width()) + padding * 2
                height = text.get_height() + desc.get_height() + padding * 2
                
                s = pygame.Surface((width, height))
                s.set_alpha(min(180, alpha))  # Giảm độ đục của background
                s.fill((0, 0, 0))
                
                # Vị trí ở góc trên bên phải
                x_pos = screen.get_width() - width - 10
                screen.blit(s, (x_pos, y_offset))
                
                # Vẽ text với alpha
                text.set_alpha(alpha)
                desc.set_alpha(alpha)
                screen.blit(text, (x_pos + padding, y_offset + padding))
                screen.blit(desc, (x_pos + padding, y_offset + text.get_height() + padding))
                
                y_offset += height + 5  # Thêm khoảng cách giữa các thông báo
                
    def draw_progress(self, screen):
        # Vẽ tiến độ thành tích ở góc trái dưới
        font = pygame.font.Font(None, 24)
        padding = 10
        bar_height = 20
        bar_spacing = 5
        bar_width = 200
        
        # Tính toán tổng chiều cao cần thiết
        total_height = 0
        visible_achievements = [ach for ach in self.achievements.items() if not ach[1]['unlocked']]
        if not visible_achievements:
            return
            
        total_height = len(visible_achievements) * (bar_height + bar_spacing)
        
        # Vẽ background cho tất cả các thanh tiến độ
        background = pygame.Surface((bar_width + padding * 2, total_height + padding * 2))
        background.set_alpha(180)
        background.fill((0, 0, 0))
        screen.blit(background, (padding, screen.get_height() - total_height - padding * 2))
        
        y_pos = screen.get_height() - total_height - padding
        
        for achievement_id, achievement in visible_achievements:
            progress = achievement['current'] / achievement['target']
            progress_text = f"{achievement['name']}: {achievement['current']}/{achievement['target']}"
            
            # Vẽ thanh tiến độ
            pygame.draw.rect(screen, (50, 50, 50), 
                           (padding * 2, y_pos, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), 
                           (padding * 2, y_pos, bar_width * progress, bar_height))
            
            # Vẽ text
            text = font.render(progress_text, True, (255, 255, 255))
            text_x = padding * 2 + (bar_width - text.get_width()) // 2
            text_y = y_pos + (bar_height - text.get_height()) // 2
            screen.blit(text, (text_x, text_y))
            
            y_pos += bar_height + bar_spacing 