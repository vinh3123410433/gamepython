import random
import math

class GameState:
    def __init__(self):
        # Game settings
        self.gold = 100
        self.lives = 10
        self.wave = 1
        self.score = 0
        self.game_mode = "menu"
        
        # Math problem settings
        self.current_problem = None
        self.current_answer = None
        self.problem_difficulty = 1
        self.cooldown = 0
        self.cooldown_times = {
            1: 3,  # Easy: 3 seconds
            2: 5,  # Medium: 5 seconds
            3: 8,  # Hard: 8 seconds
            4: 12  # Very hard: 12 seconds
        }
        
        # Question cooldown settings
        self.question_cooldowns = {
            1: 3,  # Easy: 3 seconds
            2: 5,  # Medium: 5 seconds
            3: 8,  # Hard: 8 seconds
            4: 12  # Very hard: 12 seconds
        }
        self.question_cooldown = 0
        
        # Enemy settings
        self.enemy_spawn_timer = 0
        self.enemy_spawn_interval = 3.0
        self.enemy_speed_multiplier = 1.0
        self.enemy_spawn_blocked = False
        self.enemy_spawn_block_timer = 0
        
        # Castle settings
        self.castle_health = 100
        self.enemy_castle_health = 100
        self.castle_health_increase = 0.1  # Tăng máu thành mỗi giây
        self.enemy_castle_health_increase = 0.1
        
        # Wave settings
        self.wave_timer = 0
        self.wave_duration = 30  # Thời gian mỗi wave
        self.enemy_speed_increase = 0.1  # Tăng tốc độ quái mỗi wave
        self.enemy_health_increase = 0.2  # Tăng máu quái mỗi wave
        
        # Special effects
        self.slow_effect_active = False
        self.slow_effect_timer = 0
        
        # Question history
        self.question_history = []
        
    def generate_math_problem(self, difficulty):
        self.problem_difficulty = difficulty
        self.cooldown = 0  # Reset cooldown khi chọn câu hỏi mới
        
        if difficulty == 1:  # Easy
            a = random.randint(1, 100)
            b = random.randint(1, 100)

            if 10 <= a <= 99 and 10 <= b <= 99:
                operator = random.choice(['+', '-', '*'])
            elif a % b == 0 or b % a == 0: 
                if a < b:
                    a, b = b, a 
                operator = random.choice(['+', '-', '*', '/'])
            else:
                operator = random.choice(['+', '-'])

            # Tính toán kết quả
            if operator == '+':
                self.current_answer = a + b
            elif operator == '-':
                self.current_answer = a - b
            elif operator == '/':
                self.current_answer = a / b  
            else:
                self.current_answer = a * b

            self.current_problem = f"{a} {operator} {b} = ?"

            
        elif difficulty == 2:  # Medium
            a = random.randint(2, 20)
            b = random.randint(2, 20)
            if random.random() < 0.5:
                self.current_answer = a ** 2
                self.current_problem = f"{a}² = ?"
            else:
                self.current_answer = int(math.sqrt(a * a))
                self.current_problem = f"√{a * a} = ?"
                
        elif difficulty == 3:  # Hard
            a = random.randint(2, 10)
            b = random.randint(2, 10)
            c = random.randint(1, 5)
            self.current_answer = a * b + c
            self.current_problem = f"{a}x + {c} = {self.current_answer}, x = ?"
            
        else:  # Very hard
            a = random.randint(1, 3)
            b = random.randint(1, 3)
            self.current_answer = (a * b * b) / 2
            self.current_problem = f"tich phan {a}x dx (0 tien toi {b}) = ?"
            
        # Thêm vào lịch sử câu hỏi
        self.question_history.append(self.current_problem)
        if len(self.question_history) > 10:
            self.question_history.pop(0)
            
    def check_answer(self, answer):
        try:
            user_answer = float(answer)
            if abs(user_answer - self.current_answer) < 0.01:
                return True
            return False
        except:
            return False
            
    def start_cooldown(self):
        self.cooldown = self.cooldown_times[self.problem_difficulty] * 2  # Nhân đôi thời gian hồi khi sai
        
    def update(self, dt):
        # Update cooldown
        if self.cooldown > 0:
            self.cooldown -= dt
            
        # Update wave timer
        self.wave_timer += dt
        if self.wave_timer >= self.wave_duration:
            self.wave += 1
            self.wave_timer = 0
            self.enemy_speed_multiplier += self.enemy_speed_increase
            
        # Update castle health
        self.castle_health = min(100, self.castle_health + self.castle_health_increase * dt)
        self.enemy_castle_health = min(100, self.enemy_castle_health + self.enemy_castle_health_increase * dt)
            
        # Update enemy spawn timer
        if not self.enemy_spawn_blocked:
            self.enemy_spawn_timer += dt
            
        # Update special effects
        if self.slow_effect_active:
            self.slow_effect_timer -= dt
            if self.slow_effect_timer <= 0:
                self.slow_effect_active = False
                self.enemy_speed_multiplier = 1.0 + (self.wave - 1) * self.enemy_speed_increase
                
        if self.enemy_spawn_blocked:
            self.enemy_spawn_block_timer -= dt
            if self.enemy_spawn_block_timer <= 0:
                self.enemy_spawn_blocked = False
                
    def activate_slow_effect(self, duration):
        self.slow_effect_active = True
        self.slow_effect_timer = duration
        self.enemy_speed_multiplier = 0.5
        
    def block_enemy_spawn(self, duration):
        self.enemy_spawn_blocked = True
        self.enemy_spawn_block_timer = duration 