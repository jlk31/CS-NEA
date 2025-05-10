#================================================================================
#modules being imported
#================================================================================

import pygame
from menu.base_state import BaseState

#================================================================================
#learn state class
#================================================================================

class LearnState(BaseState):
    def __init__(self, screen):
        super().__init__(screen)
        self.font = pygame.font.SysFont('Arial', 40)
        self.text = "Learn Menu - Press ESC to return to Main Menu"

#================================================================================
#render method
#================================================================================

    def render(self):
        self.screen.fill((0, 0, 50))  # Set background color
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.screen.blit(text_surface, (50, 200))

#================================================================================
#event handler
#================================================================================

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "main_menu"  # Return to main menu
        return None