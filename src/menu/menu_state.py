#===============================================================================
#modules being imported
#===============================================================================

import pygame
from menu.base_state import BaseState
from utils.button import Button

#===============================================================================
#main menu state class
#===============================================================================

class MainMenuState(BaseState):
    def __init__(self, screen, play_button_img, quit_button_img, username):
        super().__init__(screen)

        self.space_img = pygame.image.load("assets/background/space.png").convert_alpha()
        self.space_img = pygame.transform.scale(self.space_img, (800, 700))

        self.logo_img = pygame.image.load("assets/logo/logo.png").convert_alpha()
        self.logo_img = pygame.transform.scale(self.logo_img, (300, 150))

        play_img = pygame.image.load("assets/buttons/play_button.png").convert_alpha()
        learn_img = pygame.image.load("assets/buttons/learn_button.png").convert_alpha()
        leaderboard_img = pygame.image.load("assets/buttons/leaderboard_button.png").convert_alpha()
        quit_img = pygame.image.load("assets/buttons/quit_button.png").convert_alpha()
        options_img = pygame.image.load("assets/buttons/options_button.png").convert_alpha()

        self.play_button = Button(590, 30, play_img, 1 * 0.5)
        self.learn_button = Button(590, 100, learn_img, 1 * 0.5)
        self.leaderboard_button = Button(590, 170, leaderboard_img, 1 * 0.5)
        self.quit_button = Button(590, 240, quit_img, 1 * 0.5)
        self.options_button = Button(0, 590, options_img, 1 * 0.5)

        self.username = username

#===============================================================================
#update method
#===============================================================================

    def update(self):
        if self.play_button.draw(self.screen):
            print("Play button clicked")
            return "login"
        elif self.leaderboard_button.draw(self.screen):
            print("Leaderboard button clicked")
            return "leaderboard"
        elif self.learn_button.draw(self.screen):
            print("Learn button clicked")
            return "learn"
        if self.quit_button.draw(self.screen):
            pygame.quit()
            exit()
        if self.options_button.draw(self.screen):
            print("Options button clicked")
            return "options"
        
        return None

#===============================================================================
#render method
#===============================================================================

    def render(self):
        self.screen.blit(self.space_img, (0, 0))  

        logo_x = (self.screen.get_width() - self.logo_img.get_width()) // 2
        logo_y = 50 
        self.screen.blit(self.logo_img, (logo_x, logo_y))

        self.play_button.draw(self.screen)
        self.learn_button.draw(self.screen)
        self.leaderboard_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        self.options_button.draw(self.screen)

        font = pygame.font.SysFont('Arial', 30)
        username_text = font.render(f"Logged in as: {self.username}", True, (255, 255, 255))
        self.screen.blit(username_text, (10, 10))

#===============================================================================
#event handler
#===============================================================================

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if self.play_button.draw(self.screen):
            print("Play button clicked")
            return "game"
        if self.learn_button.draw(self.screen):
            print("Learn button clicked")
            return "learn"
        if self.leaderboard_button.draw(self.screen):
            print("Leaderboard button clicked")
            return "leaderboard"
        if self.quit_button.draw(self.screen):
            pygame.quit()
            exit()
        if self.options_button.draw(self.screen):
            print("Options button clicked")
            return "options"