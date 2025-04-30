import pygame
from menu.base_state import BaseState
from utils.button import Button

class MainMenuState(BaseState):
    def __init__(self, screen, start_button_img, exit_button_img):
        super().__init__(screen)
        self.start_button = Button(300, 200, start_button_img, 1)
        self.exit_button = Button(300, 300, exit_button_img, 1)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def update(self):
        if self.start_button.draw(self.screen):
            return "gameplay"
        if self.exit_button.draw(self.screen):
            pygame.quit()
            exit()

    def render(self):
        self.screen.fill((144, 201, 120))