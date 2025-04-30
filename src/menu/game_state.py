import pygame

class GameState:
    def __init__(self, screen, level, player, level_data):
        self.screen = screen
        self.level = level
        self.player = player
        self.level_data = level_data
        self.start_opening = False
        self.bg_scroll = 0
        self.screen_scroll = 0

    def update(self, moving_left, moving_right, shoot, plasma_grenade):
        # Draw background
        self.screen.fill((33, 31, 31))  # Replace with your background color
        self.level.draw()

        # Update and draw player
        self.player.update()
        self.player.draw()

        # Handle player movement
        self.screen_scroll, level_complete = self.player.move(moving_left, moving_right)

        # Check if level is complete
        if level_complete:
            self.start_opening = True
            self.level += 1
            self.bg_scroll = 0
            self.screen_scroll = 0
            self.level_data = reset_level()
            self.level = Level()
            self.player = self.level.process_data(self.level_data)

        laser_group.update()
        plasma_grenade_group.update()
        plasma_explosion_group.update()
        supply_box_group.update()
        exit_portal_group.update()

        # Draw sprite groups
        laser_group.draw(self.screen)
        plasma_grenade_group.draw(self.screen)
        plasma_explosion_group.draw(self.screen)
        supply_box_group.draw(self.screen)
        exit_portal_group.draw(self.screen)

    def render(self):
        pygame.display.flip()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            # Handle other events like key presses here
        return None