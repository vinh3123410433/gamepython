import pygame
import sys
from game.game_state import GameState
from game.screens.menu_screen import MenuScreen
from game.screens.game_screen import GameScreen
from game.screens.game_over_screen import GameOverScreen

class MathTowerDefense:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Math Tower Defense")
        self.clock = pygame.time.Clock()
        self.game_state = GameState()
        self.current_screen = MenuScreen(self.screen, self.game_state)
        
    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000.0  # Convert to seconds
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                # Handle screen transitions
                result = self.current_screen.handle_event(event)
                if result == "game":
                    self.current_screen = GameScreen(self.screen, self.game_state)
                elif result == "menu":
                    self.current_screen = MenuScreen(self.screen, self.game_state)
                elif result == "game_over":
                    self.current_screen = GameOverScreen(self.screen, self.game_state)
            
            # Update current screen
            self.current_screen.update(dt)
            
            # Draw current screen
            self.current_screen.draw()
            pygame.display.flip()

if __name__ == "__main__":
    game = MathTowerDefense()
    game.run() 