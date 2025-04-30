import pygame
from menu.base_state import BaseState

class LoginState(BaseState):
    def __init__(self, screen):
        super().__init__(screen)
        self.username = ""

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.username.strip():
                    return "main_menu"
                elif event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    self.username += event.unicode

    def render(self):
        self.screen.fill((144, 201, 120))
        font = pygame.font.SysFont("Arial", 30)
        text_surface = font.render(f"Username: {self.username}", True, (255, 255, 255))
        self.screen.blit(text_surface, (200, 200))