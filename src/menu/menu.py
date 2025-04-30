import pygame
from menu.base_state import BaseState
from utils.button import Button

class MainMenuState(BaseState):
    def __init__(self, screen, start_button_img, exit_button_img):
        super().__init__(screen)
        self.play_button = Button(300, 200  , start_button_img, 1)
        self.quit_button = Button(300, 300, exit_button_img, 1)

        self.space_img = pygame.image.load("assets/background/space.png").convert_alpha()
        self.space_img = pygame.transform.scale(self.space_img, (800, 600))

        play_img = pygame.image.load("assets/buttons/play_button.png").convert_alpha()
        learn_img = pygame.image.load("assets/buttons/learn_button.png").convert_alpha()
        leaderboard_img = pygame.image.load("assets/buttons/leaderboard_button.png").convert_alpha()
        quit_img = pygame.image.load("assets/buttons/quit_button.png").convert_alpha()
        options_img = pygame.image.load("assets/buttons/options_button.png").convert_alpha()

        self.play_button = Button(325, 350, play_img, 1 * 0.5)
        self.learn_button = Button(325, 450, learn_img, 1 * 0.5)
        self.leaderboard_button = Button(325, 550, leaderboard_img, 1 * 0.5)
        self.quit_button = Button(325, 650, quit_img, 1 * 0.5)
        self.options_button = Button(0, 0, options_img, 1 * 0.5)

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Handle button clicks specific to MainMenuState
        if self.play_button.draw(self.screen):
            print("Play button clicked")
            return "login"  # Transition to the login state
        if self.learn_button.draw(self.screen):
            print("Learn button clicked")
            # Add logic for Learn button if needed
        if self.leaderboard_button.draw(self.screen):
            print("Leaderboard button clicked")
            # Add logic for Leaderboard button if needed
        if self.quit_button.draw(self.screen):
            pygame.quit()
            exit()
        if self.options_button.draw(self.screen):
            print("Options button clicked")

    def update(self):
        if self.play_button.draw(self.screen):
            print("Play button clicked")
            return "login"
        if self.quit_button.draw(self.screen):
            pygame.quit()
            exit()

    def render(self):
        self.screen.blit(self.space_img, (0, 0))  
        
        self.play_button.draw(self.screen)
        self.learn_button.draw(self.screen)
        self.leaderboard_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        self.options_button.draw(self.screen)