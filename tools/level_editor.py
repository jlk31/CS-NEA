import pygame
import csv

pygame.init()

#================================================================
#set up game window
#================================================================

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900
TILE_SIZE = 100
screen = pygame.display.set_mode([SCREEN_HEIGHT, SCREEN_HEIGHT])
fps = 60
fps_clock = pygame.time.Clock()
active_level = 0
active_phase = 3
level = [[0 for _ in range(18)] for _ in range(7)]
level.append([2 for _ in range(18)])
level.append([1 for _ in range(18)])

pygame.display.set_caption('Cosmic Survivor Level Editor')

#================================================================
#set up editor
#================================================================

level = [[0 for _ in range(18)] for _ in range(7)]
level.append([2 for _ in range(18)])
level.append([1 for _ in range(18)])

#================================================================
#image loading
#================================================================

background = pygame.image.load('assets/background/space.png')
moon_rock = pygame.transform.scale(pygame.image.load('assets/levels/tiles/moon_rock.png'), (100, 100))
ground_rock = pygame.transform.scale(pygame.image.load('assets/levels/tiles/ground_rock.png'), (100, 100))
platform = pygame.transform.scale(pygame.image.load('assets/levels/tiles/platform.png'), (100, 50))
med_box = pygame.transform.scale(pygame.image.load('assets/levels/tiles/med_box.png'), (100, 50))
laser_box = pygame.transform.scale(pygame.image.load('assets/levels/tiles/laser_box.png'), (100, 50))
plasma_grenade_box = pygame.transform.scale(pygame.image.load('assets/levels/tiles/plasma_grenade_box.png'), (100, 50))
exit_door = pygame.transform.scale(pygame.image.load('assets/levels/tiles/exit_door.png'), (100, 50))

tiles = ['', moon_rock, ground_rock, platform]
frames = []
player_scale = 14
for _ in range(1, 5):
    frames.append(pygame.transform.scale(pygame.image.load(f'assets/levels/tiles/aow.png'),
                                        (player_scale * 5, player_scale * 8)))

#================================================================
#inventory drawing
#================================================================

def draw_inventory():
    font = pygame.font.Font('freesansbold.ttf', 20)
    colors = ['blue', 'green', 'red', 'yellow']
    pygame.draw.rect(screen, 'black', [5, SCREEN_HEIGHT - 120, SCREEN_WIDTH - 10, 110], 0, 5)
    pygame.draw.rect(screen, 'purple', [5, SCREEN_HEIGHT - 120, SCREEN_WIDTH - 10, 110], 3, 5)
    pygame.draw.rect(screen, 'white', [8, SCREEN_HEIGHT - 117, 340, 104], 3, 5)
    pygame.draw.rect(screen, 'white', [348, SCREEN_HEIGHT - 117, 532, 104], 3, 5)
    pygame.draw.rect(screen, 'white', [880, SCREEN_HEIGHT - 117, 910, 104], 3, 5)
    font.italic = True
    inst_text = font.render('M1/M2 click on spaces', True, 'white')
    inst_text2 = font.render('or scroll wheel', True, 'white')
    inst_text3 = font.render('Press enter to output in console', True, 'white')
    inst_text4 = font.render('then copy to levels.py', True, 'white')
    screen.blit(inst_text, (14, SCREEN_HEIGHT - 113))
    screen.blit(inst_text2, (14, SCREEN_HEIGHT - 88))
    screen.blit(inst_text3, (14, SCREEN_HEIGHT - 63))
    screen.blit(inst_text4, (14, SCREEN_HEIGHT - 38))
    font = pygame.font.Font('freesansbold.ttf', 32)
    level_text = font.render(f'Level: {active_level + 1}', True, 'white')
    screen.blit(level_text, (354, SCREEN_HEIGHT - 105))
    plus_lvl = pygame.draw.rect(screen, 'gray', [600, SCREEN_HEIGHT - 110, 40, 40], 0, 5)
    minus_lvl = pygame.draw.rect(screen, 'gray', [660, SCREEN_HEIGHT - 110, 40, 40], 0, 5)
    plus_text = font.render('+', True, 'black')
    screen.blit(plus_text, (613, SCREEN_HEIGHT - 107))
    screen.blit(plus_text, (613, SCREEN_HEIGHT - 57))
    minus_text = font.render('-', True, 'black')
    screen.blit(minus_text, (675, SCREEN_HEIGHT - 107))
    screen.blit(minus_text, (675, SCREEN_HEIGHT - 57))

    font = pygame.font.Font('freesansbold.ttf', 44)
    enter_text = font.render('Use the mouse to design the levels', True, 'white')
    screen.blit(enter_text, (900, SCREEN_HEIGHT - 90))

    return [plus_lvl, minus_lvl]

def draw_tiles(level):
    #0 = space, 1 = moon rock, 3 = platform, 4 = player spawn
    for i in range(len(level)):
        for p in range(len(level[i])):
            if level[i][p] != 0:
                value = level[i][p]
                if 0 < value < 4:
                    screen.blit(tiles[value], (p * TILE_SIZE, i * TILE_SIZE))
                elif value == 4:
                    screen.blit(tiles[value], (p * TILE_SIZE, i * TILE_SIZE + 75))

def save_level_data(level_data, level_number):
    with open(f'level{level_number}_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for row in level_data:
            writer.writerow(row)
    print(f"Level {level_number} data saved successfully!")
#================================================================
#main game loop
#================================================================

run = True
while run:
    fps_clock.tick(fps)
    screen.fill('black')
    screen.blit(background, (0, 0))

#================================================================
#draw tiles
#================================================================

    draw_tiles(level)
    buttons = draw_inventory()

#================================================================
#event handler
#================================================================

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                level_str = '['
                for i in range(len(level)):
                    level_str += str(level[i]) + ',\n'
                print(f'Level: {active_level}\nPhase: {active_phase}\nLevel: {level_str}')
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_press = False
            for i in range(len(buttons)):
                if buttons[i].collidepoint(event.pos):
                    button_press = True
                    if i == 0:
                        active_level += 1
                    else:
                        i == 1
                        if active_level > 0:
                            active_level -= 1
            if not button_press:
                coords = pygame.mouse.get_pos()[0] // 100, pygame.mouse.get_pos()[1] // 100
                if event.button == 1 or event.button == 4:
                    if level[coords[1]][coords[0]] < 3:
                        level[coords[1]][coords[0]] += 1
                    else:
                        level[coords[1]][coords[0]] = 0
                if event.button == 3 or event.button == 5:
                    if level[coords[1]][coords[0]] > 0:
                        level[coords[1]][coords[0]] -= 1
                    else:
                        level[coords[1]][coords[0]] = 3        

    pygame.display.flip()
pygame.quit()