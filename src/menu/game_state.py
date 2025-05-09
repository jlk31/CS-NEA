#===============================================================================
#modules being imported
#===============================================================================

import pygame
import csv
import sys
import pygame

pygame.init()

#===============================================================================
#main game state parameters
#===============================================================================

WIDTH = 800
HEIGHT = int(WIDTH * 0.8)
BGD_COLOUR = (0, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
space_img = pygame.image.load('assets/background/space.png').convert_alpha()
space_img = pygame.transform.scale(space_img, (WIDTH, HEIGHT))

#===============================================================================
#game state class
#===============================================================================

class GameState:
    def __init__(self, screen, level, player, level_data):
        self.screen = screen
        self.level = level
        self.player = player
        self.level_data = level_data

#===============================================================================
#load level data 
#===============================================================================

    def load_level(self, level_id):
        self.level_data = []
        try:
            with open(f'level{level_id}_data.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for x, row in enumerate(reader):
                    self.level_data.append([int(tile) for tile in row])
        except FileNotFoundError:
            print(f"Level {level_id} data file not found!")
            return False

        self.level = Level()
        self.player = self.level.process_data(self.level_data)

        return True

#===============================================================================
#update method
#===============================================================================

    def update(self, moving_left, moving_right, shoot, plasma_grenade):
        self.player.update()
        self.level.draw()
        if moving_left or moving_right or shoot or plasma_grenade:
            print("Player actions are being processed")

#===============================================================================
#render method
#===============================================================================

    def render(self):
        screen.blit(space_img, (0, 0))
        self.level.draw()
        self.player.draw()
        pygame.display.flip()

#===============================================================================
#event handler
#===============================================================================

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "main_menu"
        return None