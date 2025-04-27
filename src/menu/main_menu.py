import pygame
from utils.button import Button
from main import start_game, show_leaderboard, quit_game, show_options


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

pygame.font.init()
FONT = pygame.font.Font(None, 36)

def main_menu(screen):
    screen_width, screen_height = screen.get_size()
    button_width, button_height = 200, 50
    spacing = 10

#================================================================
#create buttons
#================================================================

    play_button = Button("Play", screen_width - button_width - 20, 20, button_width, button_height, start_game)
    leaderboard_button = Button("Leaderboard", screen_width - button_width - 20, 20 + button_height + spacing, button_width, button_height, show_leaderboard)
    revision_button = Button("Learn", screen_width - button_width - 20, 20 + 2 * (button_height + spacing), button_width, button_height, start_game)
    quit_button = Button("Quit", screen_width - button_width - 20, 20 + 2 * (button_height + spacing), button_width, button_height, quit_game)
    options_button = Button("Options", 20, screen_height - button_height - 20, button_width, button_height, show_options)

    buttons = [play_button, leaderboard_button, revision_button, quit_button, options_button]

    running = True
    while running:
        screen.fill(WHITE)

#================================================================
#event handler
#================================================================

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    button.check_click(mouse_pos)

#================================================================
#update button states
#================================================================

        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)

        pygame.display.flip()

    pygame.quit()
