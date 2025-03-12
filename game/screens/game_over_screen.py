import pygame

class GameOverScreen:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 48)
        
        # Buttons
        self.buttons = [
            {"text": "Play Again", "rect": pygame.Rect(540, 400, 200, 50)},
            {"text": "Main Menu", "rect": pygame.Rect(540, 470, 200, 50)}
        ]
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button["rect"].collidepoint(mouse_pos):
                    if button["text"] == "Play Again":
                        # Reset game state
                        self.game_state.__init__()
                        return "game"
                    elif button["text"] == "Main Menu":
                        return "menu"
        return None
        
    def update(self, dt):
        pass
        
    def draw(self):
        # Draw background
        self.screen.fill((0, 0, 0))
        
        # Draw title
        title = self.large_font.render("GAME OVER", True, (255, 0, 0))
        title_rect = title.get_rect(center=(640, 200))
        self.screen.blit(title, title_rect)
        
        # Draw score
        score_text = self.font.render(f"Final Score: {self.game_state.score}", True, (255, 255, 0))
        score_rect = score_text.get_rect(center=(640, 300))
        self.screen.blit(score_text, score_rect)
        
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