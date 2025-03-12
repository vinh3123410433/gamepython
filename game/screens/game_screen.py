import pygame
import math
from game.entities.soldier import Soldier
from game.entities.enemy import Enemy

class GameScreen:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 36)  # Font lớn hơn cho câu hỏi
        
        # Khởi tạo các đối tượng game
        self.soldiers = []  # Danh sách lính của người chơi
        self.enemies = []   # Danh sách quái của đối phương
        
        # Giao diện câu hỏi toán
        self.answer_input = ""  # Câu trả lời người dùng nhập
        self.input_active = True  # Trạng thái ô nhập liệu
        self.input_rect = pygame.Rect(540, 650, 200, 40)  # Vị trí ô nhập liệu
        
        # Nút chọn độ khó câu hỏi
        self.difficulty_buttons = [
            {"text": "Easy", "rect": pygame.Rect(440, 600, 100, 40)},
            {"text": "Medium", "rect": pygame.Rect(550, 600, 100, 40)},
            {"text": "Hard", "rect": pygame.Rect(660, 600, 100, 40)},
            {"text": "Very Hard", "rect": pygame.Rect(770, 600, 100, 40)}
        ]
        
        # Quản lý thời gian
        self.last_spawn_time = 0  # Thời điểm sinh quái cuối cùng
        self.spawn_interval = 7.0  # Khoảng thời gian giữa các lần sinh quái
        self.enemy_delay = 2.0     # Độ trễ giữa các quái
        
        # Cài đặt chiến đấu
        self.combat_range = 30     # Phạm vi tấn công
        self.current_time = 0      # Thời gian hiện tại
        
        # Cài đặt câu hỏi
        self.current_difficulty = 1  # Độ khó hiện tại
        
    def handle_event(self, event):
        # Xử lý sự kiện chuột
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Kiểm tra click vào nút độ khó
            for button in self.difficulty_buttons:
                if button["rect"].collidepoint(mouse_pos):
                    difficulty = {
                        "Easy": 1,
                        "Medium": 2,
                        "Hard": 3,
                        "Very Hard": 4
                    }[button["text"]]
                    self.current_difficulty = difficulty
                    self.game_state.generate_math_problem(difficulty)
                    self.input_active = True
                    self.answer_input = ""
                    
        # Xử lý sự kiện bàn phím
        elif event.type == pygame.KEYDOWN:
            if self.input_active:
                if event.key == pygame.K_RETURN:  # Nhấn Enter để trả lời
                    # Kiểm tra câu trả lời
                    if self.game_state.check_answer(self.answer_input):
                        # Trả lời đúng: sinh lính và bắt đầu hồi chiêu
                        self.soldiers.append(Soldier(100, 360, self.game_state.problem_difficulty))
                        self.answer_input = ""
                        self.input_active = True
                        self.game_state.cooldown = self.game_state.cooldown_times[self.game_state.problem_difficulty]
                    else:
                        # Trả lời sai: hồi chiêu lâu hơn
                        self.game_state.start_cooldown()
                        self.answer_input = ""
                        self.input_active = True
                elif event.key == pygame.K_BACKSPACE:  # Xóa ký tự
                    self.answer_input = self.answer_input[:-1]
                else:
                    # Chỉ cho phép nhập số và dấu chấm
                    if event.unicode.isnumeric() or event.unicode == '.':
                        self.answer_input += event.unicode
                        
        # Thoát game với phím ESC
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                return "menu"
                
        return None
        
    def update(self, dt):
        # Cập nhật thời gian
        self.current_time = pygame.time.get_ticks() / 1000.0
        
        # Sinh quái theo thời gian
        if self.current_time - self.last_spawn_time >= self.spawn_interval:
            if not self.game_state.enemy_spawn_blocked:
                # Tăng level quái theo wave
                enemy_level = min(4, self.game_state.wave // 5 + 1)
                self.enemies.append(Enemy(1180, 360, enemy_level))
                self.last_spawn_time = self.current_time
                self.spawn_interval = self.enemy_delay
            else:
                self.spawn_interval = 7.0
                
        # Cập nhật quái và xử lý chiến đấu
        for enemy in self.enemies[:]:
            # Kiểm tra quái có đang chiến đấu không
            in_combat = False
            for soldier in self.soldiers:
                distance = math.sqrt((enemy.x - soldier.x)**2 + (enemy.y - soldier.y)**2)
                if distance < self.combat_range:
                    in_combat = True
                    # Quái tấn công lính
                    if enemy.attack(soldier, self.current_time):
                        if soldier.health <= 0:
                            self.soldiers.remove(soldier)
                    # Lính tấn công quái
                    if soldier.attack(enemy, self.current_time):
                        if enemy.health <= 0:
                            self.enemies.remove(enemy)
                            self.game_state.score += 10
                            break
                    break
            
            # Chỉ di chuyển khi không chiến đấu
            if not in_combat:
                enemy.move(100, 360, self.game_state.enemy_speed_multiplier)
                            
            # Kiểm tra quái chạm vào thành
            if math.sqrt((enemy.x - 100)**2 + (enemy.y - 360)**2) < 30:
                self.game_state.castle_health -= enemy.damage
                self.enemies.remove(enemy)  # Xóa quái sau khi tấn công thành
                if self.game_state.castle_health <= 0:
                    return "game_over"
                    
        # Cập nhật lính và kiểm tra sát thương thành địch
        for soldier in self.soldiers[:]:
            # Kiểm tra lính có đang chiến đấu không
            in_combat = False
            for enemy in self.enemies:
                distance = math.sqrt((soldier.x - enemy.x)**2 + (soldier.y - enemy.y)**2)
                if distance < self.combat_range:
                    in_combat = True
                    break
            
            # Chỉ di chuyển khi không chiến đấu
            if not in_combat:
                soldier.move(1180, 360)
                
            # Xóa lính khi hết máu
            if soldier.health <= 0:
                self.soldiers.remove(soldier)
                
            # Kiểm tra lính chạm vào thành địch
            if math.sqrt((soldier.x - 1180)**2 + (soldier.y - 360)**2) < 30:
                self.game_state.enemy_castle_health -= soldier.damage
                self.soldiers.remove(soldier)  # Xóa lính sau khi tấn công thành
                if self.game_state.enemy_castle_health <= 0:
                    self.game_state.game_mode = "victory"
                    
        # Cập nhật trạng thái game
        self.game_state.update(dt)
        
    def draw(self):
        # Vẽ nền
        self.screen.fill((50, 50, 50))
        
        # Vẽ đường đi
        pygame.draw.rect(self.screen, (100, 100, 100), (100, 300, 1080, 120))
        
        # Vẽ thành
        pygame.draw.rect(self.screen, (0, 0, 255), (50, 300, 50, 120))  # Thành người chơi
        pygame.draw.rect(self.screen, (255, 0, 0), (1180, 300, 50, 120))  # Thành địch
        
        # Vẽ thanh máu thành
        pygame.draw.rect(self.screen, (0, 255, 0), (50, 280, 50 * (self.game_state.castle_health / 100), 10))
        pygame.draw.rect(self.screen, (0, 255, 0), (1180, 280, 50 * (self.game_state.enemy_castle_health / 100), 10))
        
        # Vẽ quái và thanh máu
        for enemy in self.enemies:
            enemy.draw(self.screen)
            # Vẽ thanh máu quái
            health_width = (enemy.health / enemy.max_health) * (enemy.radius * 2)
            pygame.draw.rect(self.screen, (255, 0, 0),
                           (enemy.x - enemy.radius, enemy.y - enemy.radius - 10,
                            health_width, 5))
            # Vẽ level quái
            level_text = self.font.render(str(enemy.level), True, (255, 255, 255))
            text_rect = level_text.get_rect(center=(enemy.x, enemy.y))
            self.screen.blit(level_text, text_rect)
            
        # Vẽ lính và thanh máu
        for soldier in self.soldiers:
            soldier.draw(self.screen)
            # Vẽ thanh máu lính
            health_width = (soldier.health / soldier.max_health) * (soldier.radius * 2)
            pygame.draw.rect(self.screen, (0, 255, 0),
                           (soldier.x - soldier.radius, soldier.y - soldier.radius - 10,
                            health_width, 5))
            # Vẽ level lính
            level_text = self.font.render(str(soldier.level), True, (255, 255, 255))
            text_rect = level_text.get_rect(center=(soldier.x, soldier.y))
            self.screen.blit(level_text, text_rect)
            
        # Vẽ giao diện câu hỏi
        if self.game_state.current_problem:
            # Vẽ khung câu hỏi
            question_bg = pygame.Rect(440, 500, 400, 100)
            pygame.draw.rect(self.screen, (30, 30, 30), question_bg)
            pygame.draw.rect(self.screen, (255, 255, 255), question_bg, 2)
            
            # Vẽ câu hỏi
            problem_text = self.large_font.render(self.game_state.current_problem, True, (255, 255, 255))
            problem_rect = problem_text.get_rect(center=(640, 540))
            self.screen.blit(problem_text, problem_rect)
            
            # Vẽ thời gian hồi chiêu
            if self.game_state.cooldown > 0:
                cooldown_text = self.font.render(f"Cooldown: {self.game_state.cooldown:.1f}s", True, (255, 255, 0))
                cooldown_rect = cooldown_text.get_rect(center=(640, 580))
                self.screen.blit(cooldown_text, cooldown_rect)
            
        # Vẽ ô nhập liệu
        color = (150, 150, 150) if self.input_active else (100, 100, 100)
        pygame.draw.rect(self.screen, color, self.input_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        answer_text = self.font.render(self.answer_input, True, (255, 255, 255))
        self.screen.blit(answer_text, (self.input_rect.x + 5, self.input_rect.y + 5))
        
        # Vẽ nút độ khó
        for button in self.difficulty_buttons:
            color = (100, 100, 100)
            if self.game_state.cooldown <= 0:
                color = (150, 150, 150)
            pygame.draw.rect(self.screen, color, button["rect"])
            pygame.draw.rect(self.screen, (255, 255, 255), button["rect"], 2)
            text = self.font.render(button["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
            
        # Vẽ thông tin game
        score_text = f"Score: {self.game_state.score}"
        wave_text = f"Wave: {self.game_state.wave}"
        wave_time = f"Wave Time: {self.game_state.wave_duration - self.game_state.wave_timer:.1f}s"
        
        self.screen.blit(self.font.render(score_text, True, (255, 255, 0)), (20, 20))
        self.screen.blit(self.font.render(wave_text, True, (0, 255, 0)), (20, 50))
        self.screen.blit(self.font.render(wave_time, True, (255, 0, 255)), (20, 80)) 