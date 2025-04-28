#pip install pygame -pre
#https://www.aqa.org.uk/subjects/computer-science/a-level/computer-science-7517/specification/non-exam-assessment-administration

#===============================================================================
#Modules being imported
#===============================================================================

import pygame
from utils.button import Button
import pickle
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
pygame.display.set_caption("Cosmic Survivor level editor")
ROW_COUNTER = 16
COLUMN_COUNTER = 150
TILE_MAGNITUIDE = height // ROW_COUNTER
screen_scroll_left = False
screen_scroll_right = False
screen_scroll = 0
screen_scroll_speed = 1

#================================================================================
#define colors
#================================================================================

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#================================================================================
#load images
#================================================================================

space_img = pygame.image.load('assets/background/space.png').convert_alpha()

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

#================================================================================
#main game loop
#================================================================================

run = True
while run:
    
    sys_clock.tick(FPS)
    draw_bgd()
    draw_grid()

#================================================================================
#map scrolling
#================================================================================

if screen_scroll_left and screen_scroll > 0:
    screen_scroll -= 5 * screen_scroll_speed
if screen_scroll_right:
    screen_scroll += 5 * screen_scroll_speed


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
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                screen_scroll_left = False
            if event.key == pygame.K_d:
                screen_scroll_right = False
            if event.key == pygame.K_LSHIFT:
                screen_scroll_speed = 1
        
    pygame.display.update()

pygame.quit()