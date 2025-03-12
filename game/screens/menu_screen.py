import pygame

class MenuScreen:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.font = pygame.font.Font(None, 36)
        
        # Menu buttons
        self.buttons = [
            {"text": "Start Game", "rect": pygame.Rect(500, 300, 280, 50)},
            {"text": "How to Play", "rect": pygame.Rect(500, 400, 280, 50)},
            {"text": "Exit", "rect": pygame.Rect(500, 500, 280, 50)}
        ]
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button["rect"].collidepoint(mouse_pos):
                    if button["text"] == "Start Game":
                        self.game_state.game_mode = "playing"
                        return "game"
                    elif button["text"] == "How to Play":
                        self.game_state.game_mode = "tutorial"
                        return "tutorial"
                    elif button["text"] == "Exit":
                        pygame.quit()
                        exit()
        return None
        
    def update(self, dt):
        pass
        
    def draw(self):
        # Draw background
        self.screen.fill((0, 0, 0))
        
        # Draw title
        title = self.font.render("Math Tower Defense", True, (255, 255, 255))
        title_rect = title.get_rect(center=(640, 100))
        self.screen.blit(title, title_rect)
        
        # Draw subtitle
        subtitle = self.font.render("Solve Math Problems to Defend Your Castle!", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(640, 150))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Draw buttons
        for button in self.buttons:
            # Draw button background
            pygame.draw.rect(self.screen, (100, 100, 100), button["rect"])
            # Draw button border
            pygame.draw.rect(self.screen, (255, 255, 255), button["rect"], 2)
            # Draw text
            text = self.font.render(button["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
            
        # Draw difficulty levels
        difficulties = [
            "Easy: Basic arithmetic (+, -, *)",
            "Medium: Square roots and powers",
            "Hard: Simple equations",
            "Very Hard: Basic calculus"
        ]
        
        for i, diff in enumerate(difficulties):
            text = self.font.render(diff, True, (200, 200, 200))
            self.screen.blit(text, (50, 300 + i * 40)) 