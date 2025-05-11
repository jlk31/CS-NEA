#================================================================================
#modules being imported
#================================================================================

import pygame
from menu.base_state import BaseState

username = ""
password = ""

#================================================================================
#options state class
#================================================================================

class OptionsState(BaseState):
    def __init__(self, screen, username, password):
        super().__init__(screen)
        self.username = username
        self.password = password
        self.font = pygame.font.SysFont('Arial', 30)

        self.instructions_img = pygame.image.load("assets/instructions/instructions.png").convert_alpha()
        self.instructions_img = pygame.transform.scale(self.instructions_img, (400, 300))

        self.instructions_x = (self.screen.get_width() - self.instructions_img.get_width()) // 2
        self.instructions_y = (self.screen.get_height() - self.instructions_img.get_height()) // 2

    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password
    
#================================================================================
#render method
#================================================================================

    def render(self):
            self.screen.fill((0, 0, 0))
            username_text = self.font.render(f"Username: {self.username}", True, (255, 255, 255))
            password_text = self.font.render(f"Password: {self.password}", True, (255, 255, 255))

            self.screen.blit(username_text, (50, 50))
            self.screen.blit(password_text, (50, 100))
            self.screen.blit(self.instructions_img, (self.instructions_x, self.instructions_y))

#================================================================================
#event handler 
#================================================================================

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "main_menu"
        return None