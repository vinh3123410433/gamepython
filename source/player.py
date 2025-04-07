import pygame
from setting import screenWidth, screenHeight
from achievements import AchievementSystem  # Thêm import
from features import ShopSystem
from save_system import SaveSystem

class Player:
    def __init__(self):
        self.save_system = SaveSystem()
        self.shop_system = ShopSystem()
        self.health = self.shop_system.get_total_health()
        self.money = self.save_system.get_money()
        self.score = 0
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 1000
        self.wave = 1  # Thêm thuộc tính wave
        self.font = None  # Khởi tạo font là None
        self.x = screenWidth // 2
        self.y = screenHeight // 2
        self.speed = 5
        self.max_health = self.health

    def get_font(self):
        if self.font is None:
            self.font = pygame.font.Font(None, 36)
        return self.font

    def add_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        self.health += 1
        self.money += 1000
        print(f"Level Up! Bạn đã đạt level {self.level}!")

    def update_money(self, amount):
        if isinstance(amount, (int, float)) and amount >= 0:
            self.money = amount
            self.save_system.update_money(amount)
        else:
            print("Số tiền không hợp lệ")

    def draw(self, screen):
        # Vẽ player
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), 20)
        
        # Vẽ thanh máu
        health_width = 40
        health_height = 5
        health_x = self.x - health_width // 2
        health_y = self.y - 30
        
        # Vẽ background thanh máu
        pygame.draw.rect(screen, (255, 0, 0), (health_x, health_y, health_width, health_height))
        # Vẽ máu hiện tại
        current_health_width = int(health_width * (self.health / self.max_health))
        pygame.draw.rect(screen, (0, 255, 0), (health_x, health_y, current_health_width, health_height))
        
        # Vẽ điểm số
        score_text = self.get_font().render(f"Diem: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # Vẽ level
        level_text = self.get_font().render(f"Level: {self.level}", True, (255, 255, 255))
        screen.blit(level_text, (10, 50))
        
        # Vẽ wave
        wave_text = self.get_font().render(f"Wave: {self.wave}", True, (255, 255, 255))
        screen.blit(wave_text, (10, 90))
        
        # Vẽ tiền
        money_text = self.get_font().render(f"Tien: {self.money}", True, (255, 215, 0))
        screen.blit(money_text, (10, 130))
