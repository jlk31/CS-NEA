#pip install pygame -pre
#https://www.aqa.org.uk/subjects/computer-science/a-level/computer-science-7517/specification/non-exam-assessment-administration

#Non-SQL table access ------------- (539)
#Dictionary defined --------------- (95)
#Generation of objects(OOP) ------- (138), (318), (349), (383), (413), (464)
#Simple user defined algorithms --- (63), (115), (122), (199), (499)
#Writing and reading from files --- (499), (541)
#Simple OOP model ----------------- (138), (318), (349), (383), (413), (464)
#Recursive algorithms ------------- (381), (507), (542)
#List operations ------------------ (82), (156), (172), (176), (185), (283), (289), (291), (321), (324), (329), (468), (474), (494), (542), (544), (552)

#line numbers will change as program is amended/tested/updated

#===============================================================================
#modules being imported
#===============================================================================

import pygame
import sys
import os
import sqlite3
import random
import csv
from utils.button import Button
from menu.base_state import BaseState
from menu.login_state import LoginState
from menu.menu_state import MainMenuState
from menu.game_state import GameState

#================================================================================
#main game parameters
#================================================================================

#initialising pygame
pygame.init()

#set framerate
FPS = 60
sys_clock = pygame.time.Clock()
#set screen resolution and program caption
WIDTH = 800
HEIGHT = int(WIDTH * 0.8)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Cosmic Survivor')
HOST = '127.0.0.1'
PORT = 65432
GRAVITY_UNI = 1.00
SCROLL_THRESH = 200
screen_scroll = 0
bgd_scroll = 0
TILE_VARIANTS = 5
ROW_COUNTER = 16
TILE_MAGNITUDE = HEIGHT // ROW_COUNTER
MAX_LEVEL = 5
COLUMN_COUNTER = 150
level = 0
start_game = False
start_opening = False

print(f"start_game: {start_game}")

#================================================================================
#draw background subroutine
#================================================================================

def draw_bgd():
    screen.fill(BGD_COLOUR)
    WIDTH = space_img.get_width()
    for j in range(5):  
        screen.blit(space_img, ((j * WIDTH) - bgd_scroll, 0))

#define player action variables
moving_left = False
moving_right = False
shoot = False
plasma_grenade = False
plasma_grenade_is_thrown = False

#================================================================================
#load images and store in lists
#================================================================================

play_button_img = pygame.image.load('assets/buttons/play_button.png').convert_alpha()
quit_button_img = pygame.image.load('assets/buttons/quit_button.png').convert_alpha()
restart_button_img = pygame.image.load('assets/buttons/restart_button.png').convert_alpha()
space_img = pygame.image.load('assets/background/space.png').convert_alpha()
space_img = pygame.transform.scale(space_img, (WIDTH, HEIGHT))

img_list = []
for i in range(TILE_VARIANTS):
    img = pygame.image.load(f'assets/levels/tiles/{i}.png')
    img = pygame.transform.scale(img, (TILE_MAGNITUDE, TILE_MAGNITUDE))
    img_list.append(img)

med_img = pygame.image.load('assets/levels/tiles/2.png').convert_alpha()
laser_img = pygame.image.load('assets/blaster/laser.png').convert_alpha()
plasma_grenade_img = pygame.image.load('assets/grenade/plasma_grenade.png').convert_alpha()
med_box_img = pygame.image.load('assets/levels/tiles/2.png').convert_alpha()
plasma_box_img = pygame.image.load('assets/levels/tiles/3.png').convert_alpha()
plasma_grenade_box_img = pygame.image.load('assets/levels/tiles/4.png').convert_alpha()
supply_boxes = {
    'Med'               : med_box_img,
    'Laser'             : plasma_box_img,
    'Plasma_grenade'             :plasma_grenade_box_img
}


font = pygame.font.SysFont('Arial', 50)

#================================================================================
#define colours
#================================================================================

BGD_COLOUR = (33, 31, 31)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

#define the font
font = pygame.font.SysFont('Futura', 30)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#resetting level
def reset_level():
    global bgd_scroll, screen_scroll, level, player, enemy
    bgd_scroll = 0
    screen_scroll = 0
    level = 1
    player.health = 100
    player.ammo = player.start_ammo
    player.plasma_grenades = 5
    player.alive = True
    enemy_soldier_group.empty()
    laser_group.empty()
    plasma_grenade_group.empty()
    plasma_explosion_group.empty()
    supply_box_group.empty()
    exit_portal_group.empty()

#creating list of empty tiles
    data = []
    for row in range(ROW_COUNTER):
        r = [-1] * COLUMN_COUNTER
        print(r)
        data.append(r)

    return data

#================================================================================
#method to load mission data 
#================================================================================

def load_mission(mission_number):
    global level_data, level, player
    level_data = []
    for row in range(ROW_COUNTER):
        r = [-1] * COLUMN_COUNTER
        level_data.append(r)

    try:
        with open(f'level{mission_number}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    level_data[x][y] = int(tile)
    except FileNotFoundError:
        print(f"Mission file level{mission_number}_data.csv not found!")
        return False

    level = Level()
    player = level.process_data(level_data)
    return True

#================================================================================
#create button instances
#================================================================================
restart_button = Button(300, 400, restart_button_img, 1)

#================================================================================
#state management
#================================================================================

states = {
    "login": LoginState(screen),
    "main_menu": MainMenuState(screen, play_button_img, quit_button_img),
    "game": GameState(screen, None, None, None),
}

current_state = "login"

#================================================================================
#soldier class for player and enemies
#================================================================================

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, plasma_grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.plasma_grenades = plasma_grenades
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks() 
        #create variables for the enemy soldier ai class
        self.move_index = 0
        self.fov = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_index = 0


#================================================================
#player animation
#================================================================

        #load all images for the players
        animation_types = ['idle', 'run', 'jump', 'death']
        #0: idle, 1:run, 2:jump, 3:death
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            num_of_frames = len(os.listdir(f'assets/{self.char_type}/{animation}'))
            for i in range(1):
                img = pygame.image.load(f'assets/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
        self.image = self.animation_list[self.action][self.frame_index] 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)    
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.scale_down(0.5)

    def scale_down(self, scale_factor):
        """Scale down the player's sprite."""
        self.image = pygame.transform.scale(self.image, (int(self.width * scale_factor), int(self.height * scale_factor)))
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1  

#================================================================
#player movement
#================================================================

    def move(self, moving_left, moving_right):
        #reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        #assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        #jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        #apply gravitational force constant 
        self.vel_y += GRAVITY_UNI
        if self.vel_y > 10:
            self.vel_y  
        dy += self.vel_y

        #collision checking
        for tile in level.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                #change direction of enemy trooper if collision occurs
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_index = 0
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom
                    self.in_air = False
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        #check if player has fallen off the map
        if self.rect.bottom > HEIGHT:
            self.health = 0
            self.update_action(3)

        #check if player has made contact with exit door
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_portal_group, False):
            level_complete = True
            print('Player has reached the exit')
            self.kill()

        #check if player has left the screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > WIDTH:
                dx = 0

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        #update scroll based on player's position
        if self.char_type == 'player':
            if (self.rect.right < WIDTH - SCROLL_THRESH and bgd_scroll < (level.level_length * TILE_MAGNITUDE) - WIDTH) or (self.rect.left < SCROLL_THRESH and bgd_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            laser = Laser(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            laser_group.add(laser)
            #reduce ammo
            self.ammo -= 1

    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 150) == 3:
                self.update_action(0)#call idle animation when conditions are met
                self.idling = True
                self.idling_index = 100
            #check if enemy is in close proximity to the player
            if self.fov.colliderect(player.rect):
                #enemy stop movement and face player
                self.update_action(0)#call idle animation when conditions are met
                self.shoot()
            else:
                if self.direction == 1:
                    ai_moving_right = True
                else:
                    ai_moving_right = False
                ai_moving_left = not ai_moving_right
                self.move(ai_moving_left, ai_moving_right)
                self.update_action(1)#call run animation when conditions are met
                self.move_index += 1
                #update ai fov as enemy soldier moves
                self.fov.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)


                if self.move_index > TILE_MAGNITUDE:
                    self.direction *= -1
                    self.move_index *= -1
                else:
                    self.idling_index -= 1
                    if self.idling_index <= 0:
                        self.idling = False

        #scroll
        self.rect.x += screen_scroll



    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has ran out, reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

            

    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)        

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

#================================================================================
#level class
#================================================================================

class Level():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        self.level_data = []
        for y, row in enumerate(data):
            self.level_data.append([])
            for x, tile in enumerate(row):
                if 0 <= tile < len(img_list):
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_MAGNITUDE
                    img_rect.y = y * TILE_MAGNITUDE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 4:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 5:
                        supply_box = supply_box('Med', x * TILE_MAGNITUDE, y * TILE_MAGNITUDE)
                        supply_box_group.add(supply_box)
                    elif tile >= 6:
                        supply_box = supply_box('Laser', x * TILE_MAGNITUDE, y * TILE_MAGNITUDE)
                        supply_box_group.add(supply_box)
                    elif tile >= 7:
                        supply_box = supply_box('Plasma Grenade', x * TILE_MAGNITUDE, y * TILE_MAGNITUDE)
                        supply_box_group.add(supply_box)
                    elif tile == 8:
                        exit_portal = ExitPortal(img, x * TILE_MAGNITUDE, y * TILE_MAGNITUDE)
                        exit_portal_group.add(exit_portal)            
            
        return player

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

        return player

#================================================================================
#exit class
#================================================================================

class ExitPortal(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_MAGNITUDE // 2, y + (TILE_MAGNITUDE - self.image.get_height()))

#================================================================================
#supply box class
#================================================================================

class SupplyBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = supply_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_MAGNITUDE // 2, y + (TILE_MAGNITUDE - self.image.get_height()))


    def update(self):
        #scroll supply boxes
        self.rect.x += screen_scroll
        #checking for player collision with the refill box
        if pygame.sprite.collide_rect(self, player):
            #check for box type
            if self.item_type == 'Med':
                print(player.health)
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
                print(player.health)
            elif self.item_type == 'Laser':
                player.ammo += 20
                if player.ammo > player.start_ammo:
                    player.ammo = player.start_ammo
            elif self.item_type == 'Plasma_grenade':
                player.plasma_grenades += 5

            #remove box
            self.kill() 

#================================================================
#laser class
#================================================================

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = laser_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        #give the laser motion
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #check if laser has left the screen
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

        #level collision checking
        for tile in level.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        #character collision checking
        if pygame.sprite.spritecollide(player, laser_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemy_soldier_group:
            if pygame.sprite.spritecollide(enemy, laser_group, False):
                    if player.alive:
                        enemy.health -= 25
                        self.kill()

#================================================================
#plasma grenade class
#================================================================

class Plasma_Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = plasma_grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self):
        self.vel_y += GRAVITY_UNI
        dx = self.direction * self.speed
        dy = self.vel_y

        #level collision checking
        for tile in level.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed

            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.speed = 0
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        #check if plasma grenade has collided with the floor tile
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0

        #check if plasma grenade has made contact with horizontal borders
        if self.rect.left + dx < 0 or self.rect.left + dx > WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed

        #update positional vector of plasma grenade
        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        #countdown timer for plasma grenade
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            plasma_explosion = Plasma_Explosion(self.rect.x, self.rect.y, 0.5)
            plasma_explosion_group.add(plasma_explosion)
            #damage soldiers nearby (player + enemy)
            if abs(self.rect.centerx - player.rect.centerx) < TILE_MAGNITUDE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILE_MAGNITUDE * 2:
                player.health -= 75
            for enemy_soldier in enemy_soldier_group:
               if abs(self.rect.centerx - enemy.rect.centerx) < TILE_MAGNITUDE * 2 and \
                abs(self.rect.centery - enemy.rect.centery) < TILE_MAGNITUDE * 2:
                enemy.health -= 75
                print(enemy.health)

#================================================================
#plasma grenade explosion class
#================================================================

class Plasma_Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1,6):
            img = pygame.image.load(f'assets/explosion/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.image = plasma_grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        #scroll plasma explosion
        self.rect.x += screen_scroll
        PLASMA_EXPLOSION_SPEED = 4
        #update plasma explosion animation
        self.counter += 1

        if self.counter >= PLASMA_EXPLOSION_SPEED == 0:
            self.counter = 0
            self.frame_index += 1
            #delete explosion if animation has been completed
            if self.frame_index >= len(self.images):
                self.kill()
                return
            else:
                self.image = self.images[self.frame_index]

#================================================================
#screen transition class
#================================================================        

class Transition():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.transition_counter = 0

    def fade(self):
        fade_complete = False
        self.transition_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(screen, self.colour, (0 - self.transition_counter, 0, WIDTH // 2, HEIGHT))
            pygame.draw.rect(screen, self.colour, (WIDTH // 2 + self.transition_counter, 0, WIDTH, HEIGHT))
            pygame.draw.rect(screen, self.colour, (0, 0 - self.transition_counter, WIDTH, HEIGHT // 2))
            pygame.draw.rect(screen, self.colour, (0, HEIGHT // 2 + self.transition_counter, WIDTH, HEIGHT))
        if self.direction == 2:
            pygame.draw.rect(screen, self.colour, (0, 0, WIDTH, 0 + self.transition_counter))
        if self.transition_counter >= WIDTH:
            fade_complete = True

        return fade_complete

opening_transition = Transition(1, BLACK, 4)
death_transition = Transition(2, RED, 4)

#================================================================
#create sprite groups
#================================================================

enemy_soldier_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
plasma_grenade_group = pygame.sprite.Group()
plasma_explosion_group = pygame.sprite.Group()
supply_box_group = pygame.sprite.Group()
exit_portal_group = pygame.sprite.Group()

#temp - create plasma boxes
supply_box = SupplyBox('Med', 100, 260)
supply_box_group.add(supply_box)
supply_box = SupplyBox('Laser', 400, 260)
supply_box_group.add(supply_box)
supply_box = SupplyBox('Plasma_grenade', 500, 260)
supply_box_group.add(supply_box)

player = Soldier('player', 200, 200, 1.65, 2, 20, 5)


enemy = Soldier('enemy', 500, 200, 1.65, 2, 20, 0)
enemy_soldier_group.add(enemy)

x = 200
y = 200
scale = 3

#================================================================
#create empty list for tiles
#================================================================

level_data = []
for row in range(ROW_COUNTER):
    r = [-1] * COLUMN_COUNTER
    level_data.append(r)


with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            level_data[x][y] = int(tile)
level = Level()
player = level.process_data(level_data)

states["game"] = GameState(screen, level, player, level_data)

#================================================================
#main game loop
#================================================================

run = True
while run:
    sys_clock.tick(FPS)

    state = states[current_state]

    events = pygame.event.get()
    next_state = states[current_state].event_handler(events)

    if next_state:
        current_state = next_state
        continue

    if current_state == "game":
        state.update(moving_left, moving_right, shoot, plasma_grenade)
        state.render()
    else:
        states[current_state].update()
        states[current_state].render()

    if start_game == True: 
        draw_bgd()
        level.draw()
        #show health count
        draw_text('HEALTH: ', font, WHITE, 15, 20)
        for x in range(player.max_health):
            screen.blit(med_box_img, (100 + (x * 20), 25))
        #show ammo count
        draw_text('AMMO: ', font, WHITE, 15, 30)
        for x in range(player.ammo):
            screen.blit(laser_img, (100 + (x * 20), 35))
        #show grenade count
        draw_text(f'PLASMA GRENADES: ', font, WHITE, 20, 50)
        for x in range(player.plasma_grenades):
            screen.blit(plasma_grenade_img, (100 + (x * 25), 55))

            player.update()
            player.draw()

            for enemy in enemy_soldier_group:
                enemy.ai()
                enemy.update()
                enemy.draw()

#================================================================================
#update and draw sprite groups
#================================================================================

        laser_group.update()
        plasma_grenade_group.update()
        plasma_explosion_group.update()
        supply_box_group.update()
        exit_portal_group.update()
        laser_group.draw(screen)
        plasma_grenade_group.draw(screen)
        plasma_explosion_group.draw(screen)
        supply_box_group.draw(screen)
        exit_portal_group.draw(screen)
        
        if start_opening == True:
            if opening_transition.fade():
                start_opening = False
                opening_transition.transition_counter = 0

        #update player actions
        if player.alive:
            #shoot lasers
            if shoot:
                player.shoot()
            #throw grenades
            elif plasma_grenade and plasma_grenade_isthrown == False and player.plasma_grenades > 0:
                plasma_grenade = Plasma_Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
                                player.rect.top , player.direction)
                plasma_grenade_group.add(plasma_grenade)
                #subtract plasma grenades
                player.plasma_grenades -= 1
                plasma_grenade_isthrown = True
                print(player.plasma_grenades)
            if player.in_air:
                player.update_action(2)#2: jump
            elif moving_left or moving_right:
                player.update_action(1)#1: run
            else:
                player.update_action(0)#0: idle
            bgd_scroll -= screen_scroll
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            if level_complete == True:
                start_opening = True
                level += 1
                bgd_scroll = 0
                screen_scroll = 0
                level_data = reset_level()
                level = Level()
                player = level.process_data(level_data)

                states["game"] = GameState(
                    screen,
                    level,
                    player,
                    level_data,
                    laser_group,
                    plasma_grenade_group,
                    plasma_explosion_group,
                    supply_box_group,
                    exit_portal_group
                )

                if level <= MAX_LEVEL:
                    with open(f'level{level}_data.csv', newline='') as csv:
                        reader = csv.reader(csv, delimiter=',')
                        for x, row in enumerate(reader):
                            if x >= ROW_COUNTER:
                                break
                            for y, tile in enumerate(row):
                                if y >= COLUMN_COUNTER:
                                    break
                                level_data[x][y] = int(tile)
                    
                    level = Level()
                    player = level.process_data(level_data)
        else:
            screen_scroll = 0
            if death_transition.fade():
                if restart_button_img.draw(screen):
                    death_transition.transition_counter = 0
                    start_opening = True
                    bgd_scroll = 0
                    level_data = reset_level()

#================================================================
#event handler
#================================================================

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                plasma_grenade = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
        #mouse presses
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
                        

        #keyboard button released            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                plasma_grenade = False
                plasma_grenade_is_thrown = False

        pygame.display.flip()

pygame.quit()