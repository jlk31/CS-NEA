#================================================================================
#modules being imported
#================================================================================

import pygame
import sys
from database.db_manager import DBManager

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Leaderboard')

font = pygame.font.Font('Arial', 30)

#================================================================================
#fetch data query from db
#================================================================================

def fetch_leaderboard_data(db_manager):
    query = 'SELECT username, score FROM users ORDER BY score DESC'
    return db_manager.fetch_all(query)

#================================================================================
#leaderboard drawing
#================================================================================

def draw_leaderboard(leaderboard_data):
    screen.fill((0, 0, 0))
    title = font.render('Leaderboard', True, (255, 255, 255))
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 50))

    for i, (name, score) in enumerate(leaderboard_data):
        text = font.render(f'{i + 1}. {name} - {score}', True, (255, 255, 255))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, 100 + i * 40))

    pygame.display.flip()

#================================================================================
#bubble sort 
#================================================================================

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j][1] < arr[j + 1][1]:
                arr[j], arr[j + 1], arr[j]

def leaderboard_window():
    db_manager = DBManager('user_db.db')
    db_manager.create_connection()
    leaderboard_data = fetch_leaderboard_data(db_manager)
    db_manager.close_connection()

    bubble_sort(leaderboard_data)

#================================================================================
#main loop
#================================================================================

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        draw_leaderboard(leaderboard_data)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    leaderboard_window()
