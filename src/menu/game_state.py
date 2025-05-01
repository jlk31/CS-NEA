import pygame
import csv
import sys

class GameState:
    def __init__(self, screen, level, player, level_data):
        """Initialize the game state."""
        self.screen = screen
        self.level = level
        self.player = player
        self.level_data = level_data

    def load_level(self, level_id):
        """
        Load the specified level.
        
        Args:
            level_id (int): The ID of the level to load.
        """

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

    def event_handler(self, events):
        """
        Handle events for the game state.
        
        Args:
            events (list): A list of pygame events.
        
        Returns:
            str: The next state to transition to, or None to stay in the current state.
        """
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "main_menu"  #return to the main menu if ESC is pressed
        return None
    
    def update(self, moving_left, moving_right, shoot, plasma_grenade):
        """Update the game state."""
        self.player.update()
        self.level.draw()
        if moving_left or moving_right or shoot or plasma_grenade:
            print("Player actions are being processed")

    def render(self):
        """Render the game state."""
        self.player.draw()