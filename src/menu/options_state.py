#================================================================================
#modules being imported
#================================================================================

import pygame
from menu.base_state import BaseState

#================================================================================
#options state class
#================================================================================

class OptionsState(BaseState):
    def __init__(self, screen, username, password):
        super().__init__(screen)
        self.username = username
        self.password = password
        self.font = pygame.font.SysFont('Arial', 30)

#================================================================================
#render method
#================================================================================

    def render(self):
            self.screen.fill((50, 50, 50))
            username_text = self.font.render(f"Username: {self.username}", True, (255, 255, 255))
            password_text = self.font.render(f"Password: {self.password}", True, (255, 255, 255))
            instructions_text = self.font.render("Instructions: Use WASD to move, SPACE to shoot.", True, (255, 255, 255))

            self.screen.blit(username_text, (50, 50))
            self.screen.blit(password_text, (50, 100))
            self.screen.blit(instructions_text, (50, 150))

#================================================================================
#event handler 
#================================================================================

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "main_menu"
        return None