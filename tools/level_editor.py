#pip install pygame -pre
#https://www.aqa.org.uk/subjects/computer-science/a-level/computer-science-7517/specification/non-exam-assessment-administration

#Non-SQL table access ------------- 
#Dictionary defined --------------- 
#Generation of objects(OOP) ------- 
#Simple user defined algorithms --- 
#Writing and reading from files --- 
#Simple OOP model -----------------
#Recursive algorithms ------------- 
#List operations ------------------

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

#================================================================================
#load images
#================================================================================

space_img = pygame.image.load('assets/space.png').convert_alpha()

def draw_bgd():
    screen.blit(space_img, (0, 0))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, width + side_margin, height + low_margin), 2)
    pygame.draw.rect(screen, (255, 255, 255), (side_margin - 5, 0, side_margin - 5, height + low_margin), 2)
    pygame.draw.rect(screen, (255, 255, 255), (0, height - low_margin + 5, width + side_margin - 5, low_margin - 5), 2)

#================================================================================
#main game loop
#================================================================================

run = True
while run:
    
    sys_clock.tick(FPS)
    draw_bgd()

#================================================================================
#event handler
#================================================================================

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        

pygame.quit()