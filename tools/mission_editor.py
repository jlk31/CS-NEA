#pip install pygame -pre
#https://www.aqa.org.uk/subjects/computer-science/a-level/computer-science-7517/specification/non-exam-assessment-administration

#===============================================================================
#modules being imported
#===============================================================================

import pygame
from src.utils.button import Button
import csv

#================================================================================
#main game parameters
#================================================================================

pygame.init()

FPS = 60
sys_clock = pygame.time.Clock()

width = 800
height = 640
low_margin = 100
side_margin = 300

screen = pygame.display.set_mode((width + side_margin, height + low_margin))
pygame.display.set_caption("Cosmic Survivor mission editor")
ROW_COUNTER = 16
COLUMN_COUNTER = 150
TILE_MAGNITUIDE = height // ROW_COUNTER
TILE_VARIANTS = 6
mission = 0
selected_tile = 0
screen_scroll_left = False
screen_scroll_right = False
screen_scroll = 0
screen_scroll_speed = 1

#================================================================================
#define colors
#================================================================================

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#===============================================================================
#define font(s)
#===============================================================================

font = pygame.font.SysFont('Arial', 30)

#================================================================================
#load images
#================================================================================

space_img = pygame.image.load('assets/background/space.png').convert_alpha()

img_list = []
for i in range(TILE_VARIANTS):
    img = pygame.image.load(f'assets/tiles/{i}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_MAGNITUIDE, TILE_MAGNITUIDE))
    img_list.append(img)

save_img = pygame.image.load('assets/save_button.png').convert_alpha()
load_img = pygame.image.load('assets/load_button.png').convert_alpha()

level_data = []
for row in range(ROW_COUNTER):
    r = [-1] * COLUMN_COUNTER
    level_data.append(r)

for tile in range(0, COLUMN_COUNTER):
    level_data[ROW_COUNTER - 1][tile] = 0

def draw_text(text, font, color, surface, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_bgd():
    screen.fill(BLACK)
    width = space_img.get_width()
    for i in range(4):
        screen.blit(space_img, ((i * width) - screen_scroll, 0))

def draw_grid():
    for c in range(COLUMN_COUNTER + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_MAGNITUIDE - screen_scroll, 0), (c * TILE_MAGNITUIDE - screen_scroll, height))
    for r in range(ROW_COUNTER + 1):
        pygame.draw.line(screen, WHITE, (0, r * TILE_MAGNITUIDE), (width, r * TILE_MAGNITUIDE))

def draw_level():
    for x, row in enumerate(level_data):
        for y, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_MAGNITUIDE - screen_scroll, y * TILE_MAGNITUIDE)) 

#===============================================================================
#create buttons
#===============================================================================

save_button = Button(width // 2, height + low_margin - 50, save_img, None)
load_button = Button(width // 2 + 200, height + low_margin - 50, load_img, None)

button_list = []
button_column = 0
button_row = 0

for j in range(len(img_list)):
    button = button.Button(width + (75 * button_column) + 50, (75 * button_row) + 50, img_list[j], None)
    button_list.append(button)
    button_column += 1
    if button_column == 3:
        button_row += 1
        button_column = 0

#================================================================================
#main game loop
#================================================================================

run = True
while run:
    
    sys_clock.tick(FPS)
    draw_bgd()
    draw_grid()
    draw_level()
    draw_text(f'Level: {mission}', font, WHITE, 10, height + low_margin - 90)
    draw_text('Press W or S to change mission', font, WHITE, 10, height + low_margin - 90)

    if save_button.draw(screen):
        with open(f'level{mission}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in level_data:
                writer.writerow(row)
    if load_button.draw(screen):
        screen_scroll = 0
        with open(f'level{mission}_data.csv', newline='') as csvfile:
            reader = csv.writer(csvfile, delimiter=',')
            for row in level_data:
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        level_data[x][y] = int(tile)

#===============================================================================
#draw tile panel
#===============================================================================

pygame.draw.rect(screen, BLACK, (width, 0, side_margin, height))

button_counter = 0
for button_counter, x in enumerate(button_list):
    if x.draw(screen):
        selected_tile = button_counter

pygame.draw.rect(screen, RED, button_list[selected_tile].rect, 3)

#================================================================================
#map scrolling
#================================================================================

if screen_scroll_left and screen_scroll > 0:
    screen_scroll -= 5 * screen_scroll_speed
if screen_scroll_right and screen_scroll < (COLUMN_COUNTER * TILE_MAGNITUIDE) - width:
    screen_scroll += 5 * screen_scroll_speed

#===============================================================================
#convert mouse position to tile position
#===============================================================================

    pos = pygame.mouse.get_pos()
    x = (pos[0] + screen_scroll) // TILE_MAGNITUIDE
    y = pos[1] // TILE_MAGNITUIDE
    if pos[0] < width and pos[1] < height:
        if pygame.mouse.get_pressed()[0] == 1:
            if level_data[y][x] != selected_tile:
                level_data[y][x] = selected_tile
        if pygame.mouse.get_pressed()[2] == 1:
            level_data[y][x] = -1

#================================================================================
#event handler
#================================================================================

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                screen_scroll_left = True
            if event.key == pygame.K_d:
                screen_scroll_right = True
            if event.key == pygame.K_LSHIFT:
                screen_scroll_speed = 5
            if event.key == pygame.K_w:
                mission += 1
            if event.key == pygame.K_s and mission > 0:
                mission -= 1
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                screen_scroll_left = False
            if event.key == pygame.K_d:
                screen_scroll_right = False
            if event.key == pygame.K_LSHIFT:
                screen_scroll_speed = 1
        
    pygame.display.update()

pygame.quit()