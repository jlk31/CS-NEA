#pip install pygame -pre
#https://www.aqa.org.uk/subjects/computer-science/a-level/computer-science-7517/specification/non-exam-assessment-administration

#Simple mathematical calculations - 
#Linear Search --------------------
#Non-SQL table access -------------
#Web service APIs -----------------
#Simple client-server model -------
#Server-side scripting ------------
#Generation of objects(OOP) -------
#Simple user defined algorithms ---
#Writing and reading from files ---
#Binary search --------------------
#Bubble sort ----------------------
#Simple OOP model ----------------- (201), (390), (424), (454), (505), (540)
#Intermediate stack operations ---- ()
#Recursive algorithms ------------- (381), (507), (542)
#Cross-table parameterised SQL ---- ()
#Aggregate SQL functions 
#List operations ------------------ (218), (237), (508)


#line numbers will change as program is amended/tested/updated

#===============================================================================
#Modules being imported
#===============================================================================
import pygame
import sys
import os
import sqlite3
import time
import random
import math 

#================================================================================
#parameters
#================================================================================
#initialising pygame
pygame.init()

#set framerate
FPS = 60
fpsclock = pygame.time.Clock()
#set screen resolution and program caption
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Combat Cosmonaut')
#define game variables
GRAVITYFORCE = 1.00
TILE_MAGNITUDE = 50

#================================================================================
#draw background subroutine
#================================================================================

def draw_bg():
    screen.fill(BG_COLOUR)

#define player action variables
moving_left = False
moving_right = False
shoot = False
plasmagrenade = False
plasmagrenade_isthrown = False


#load images
#laser
laser_img = pygame.image.load('img/icons/laser.png').convert_alpha()
#grenade
plasmagrenade_img = pygame.image.load('img/icons/plasmagrenade.png').convert_alpha()
#plasma boxes
med_box_img = pygame.image.load('img/icons/med_box.png').convert_alpha()
laser_box_img = pygame.image.load('img/icons/med_box.png').convert_alpha()
plasmagrenade_box_img = pygame.image.load('img/icons/med_box.png').convert_alpha()
plasma_boxes = {
    'Med'               : med_box_img,
    'Laser'             : laser_box_img,
    'Plasmagrenade'             :plasmagrenade_box_img
}


#set up font
font = pygame.font.SysFont('Arial', 50)


#define colours
BG_COLOUR = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)


#define the font
font = pygame.font.SysFont('Futura', 30)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
#================================================================================
#display background image
#================================================================================



#================================================================================
# main menu
#================================================================================
BG = pygame.image.load("assets/Background.png")



def get_font(size): #returns Press-Start and the size
    return pygame.font.Font("assets/font.ttf", size)



def play():
    player_render()



def options():
    while True:
        REVISION_MOUSE_POS = pygame.mouse.get_pos() #gets position of the mouse


        screen.blit(BG, (0, 0)) #turns screen black


        REVISION_TEXT = get_font(45).render("This is the options window.", True, "White") #renders the options screen's text
        REVISION_RECT = REVISION_TEXT.get_rect(center=(400, 320))
        screen.blit(REVISION_TEXT, REVISION_RECT)

        REVISION_BACK = Button(image=None, pos = (400, 420), text_input = "BACK", font = get_font(75), base_colour = "White", contact_colour = "Blue") #displays the back button
        
        REVISION_BACK.changeColor(REVISION_MOUSE_POS)
        REVISION_BACK.update(screen)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if PLAY_BUTTON.is_clicked(REVISION_MOUSE_POS):
                    play()
                elif LEADERBOARD_BUTTON.is_clicked(REVISION_MOUSE_POS):
                    leaderboard()
                elif QUIT_BUTTON.is_clicked(REVISION_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                elif REVISION_BACK.is_clicked(REVISION_MOUSE_POS):
                    return
                
        pygame.display.update() #updates the display

def main_menu():
    while True:
        screen.blit(BG, (0, 0)) #turns screen black


        MENU_MOUSE_POS = pygame.mouse.get_pos() # gets position of mouse on screen


        MENU_TEXT = get_font(100).render("Cosmic Survivor", True, "#000000") #main menu text
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 200)) #location of menu text onscreen


        PLAY_BUTTON = Button(image = pygame.image.load("assets/ ---PLACEHOLDER---")), pos = (400, 200), text_input = "PLAY", font = get_font(75), base_colour = "White", contact_colour = "Blue" #draws the play button on screen
        REVISION_BUTTON = Button(image = pygame.image.load("assets/ ---PLACEHOLDER---")), pos = (400, 200),  text_input = "REVISION", font = get_font(75), base_colour = "White", contact_colour = "Blue" # draws the revision button on screen
        QUIT_BUTTON = Button(image = pygame.image.load("assets/ ---PLACEHOLDER---")), pos = (400, 200), text_input = "QUIT", font = get_font(75), base_colour = "White", contact_colour = "Blue" #draws the leaderboard button on screen
        

        screen.blit(MENU_TEXT, MENU_RECT)


        for Button in [PLAY_BUTTON, REVISION_BUTTON, QUIT_BUTTON]:
             Button.changeColour(MENU_MOUSE_POS)
             Button.update(screen) #updates the buttons colour on screen if contacted with by the player
        
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 pygame.quit()
                 sys.exit()
             elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                 if PLAY_BUTTON.is_clicked(MENU_MOUSE_POS):
                     play()
                 elif REVISION_BUTTON.is_clicked(MENU_MOUSE_POS):
                     options()
                 elif QUIT_BUTTON.is_clicked(MENU_MOUSE_POS):
                     pygame.quit()
                     sys.exit()

        pygame.display.update() #updates the display




#================================================================================

#================================================================================
#soldier class for player and enemies
#================================================================================

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, plasmagrenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.plasmagrenades = plasmagrenades
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
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        #0: idle, 1:run, 2:jump, 3:death
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):    
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
        self.img = self.animation_list[self.action][self.frame_index] 
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)    

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

        #apply gravity downwards to 
        self.vel_y += GRAVITYFORCE
        if self.vel_y > 10:
            self.vel_y  
        dy += self.vel_y

        #check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

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
            if self.fov.collide_rect(player.rect):
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




    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last udpate
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
#plasma box class
#================================================================================

class PlasmaBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = plasma_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.centertop = (x + TILE_MAGNITUDE // 2, y + (TILE_MAGNITUDE - self.image.get_height()))


    def update(self):
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
            elif self.item_type == 'Plasmagrenade':
                player.plasmagrenades += 5

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
        self.rect.x += (self.direction * self.speed)
        #check if laser has left the screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        #check collision with characters
        if pygame.sprite.spritecollide(player, laser_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemysoldier_group:
            if pygame.sprite.spritecollide(enemy, laser_group, False):
                    if player.alive:
                        enemy.health -= 25
                        self.kill()
#================================================================
#plasma grenade class
#================================================================

class PlasmaGrenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = plasmagrenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.vel_y += GRAVITYFORCE
        dx = self.direction * self.speed
        dy = self.vel_y

        #check if plasma grenade has collided with the floor tile
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0

        #check if plasma grenade has made contact with horizontal borders
        if self.rect.left + dx < 0 or self.rect.left + dx > SCREEN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed


        #update positional vector of plasma grenade
        self.rect.x += dx
        self.rect.y += dy

        #countdown timer for plasma grenade
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            plasmaexplosion = PlasmaExplosion(self.rect.x, self.rect.y, 0.5)
            plasmaexplosion_group.add(plasmaexplosion)
            #damage soldiers nearby (player + enemy)
            if abs(self.rect.centerx - player.rect.centerx) < TILE_MAGNITUDE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILE_MAGNITUDE * 2:
                player.health -= 75
            for enemysoldier in enemysoldier_group:
               if abs(self.rect.centerx - enemy.rect.centerx) < TILE_MAGNITUDE * 2 and \
                abs(self.rect.centery - enemy.rect.centery) < TILE_MAGNITUDE * 2:
                enemy.health -= 75
                print(enemy.health)

#================================================================
#plasma grenade explosion class
#================================================================

class PlasmaExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1,6):
            img = pygame.image.load(f'img/explosion/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.image = plasmagrenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        PLASMAEXPLOSION_SPEED = 4
        #update plasma explosion animation
        self.counter += 1

        if self.counter >= PLASMAEXPLOSION_SPEED == 0:
            self.counter = 0
            self.frame_index += 1
            #delete explosion if animation has been completed
            if self.frame_index >= len(self.images):
                self.kill()
                return
            else:
                self.image = self.images[self.frame_index]

#================================================================
#tile class
#================================================================

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(tile_img, (width, 10))
        self.rect =self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#================================================================
#create sprite groups
#================================================================

enemysoldier_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
plasmagrenade_group = pygame.sprite.Group()
plasmaexplosion_group = pygame.sprite.Group()
plasma_box_group = pygame.sprite.Group()

#temp - create plasma boxes
plasma_box = PlasmaBox('Med', 100, 260)
plasma_box_group.add(plasma_box)
plasma_box = PlasmaBox('Laser', 400, 260)
plasma_box_group.add(plasma_box)
plasma_box = PlasmaBox('Plasmagrenade', 500, 260)
plasma_box_group.add(plasma_box)


player = Soldier('player', 200, 200, 1.65, 2, 20, 5)


enemy = Soldier('enemy', 500, 200, 1.65, 2, 20, 0)
enemysoldier_group.add(enemy)


x = 200
y = 200
scale = 3

#================================================================
#main game loop
#================================================================

run = True
while run:

    fpsclock.tick(FPS)

    draw_bg()
    #show health count
    draw_text('HEALTH: ', font, WHITE, 15, 20)
    for x in range(player.max_health):
        screen.blit(health_img, (100 + (x * 20, 25)))
    #show ammo count
    draw_text('AMMO: ', font, WHITE, 15, 30)
    for x in range(player.ammo):
        screen.blit(laser_img, (100 + (x * 20), 35))
    #show grenade count
    draw_text(f'PLASMA GRENADES: ', font, WHITE, 20, 50)
    for x in range(player.plasmagrenades):
        screen.blit(plasmagrenade_img, (100 + (x * 25), 55))

    player.update()
    player.draw()

    for enemy in enemysoldier_group:
        enemy.ai()
        enemy.update()
        enemy.draw()

    
    #update and draw groups
    laser_group.update()
    plasmagrenade_group.update()
    plasmaexplosion_group.update()
    plasma_box_group.update()
    laser_group.draw(screen)
    plasmagrenade_group.draw(screen)
    plasmaexplosion_group.draw(screen)
    plasma_box_group.draw(screen)

    #update player actions
    if player.alive:
        #shoot lasers
        if shoot:
            player.shoot()
        #throw grenades
        elif plasmagrenade and plasmagrenade_isthrown == False and player.plasmagrenades > 0:
            plasmagrenade = PlasmaGrenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
                              player.rect.top , player.direction)
            plasmagrenade_group.add(plasmagrenade)
            #subtract plasmagrenades
            player.plasmagrenades -= 1
            plasmagrenade_isthrown = True
            print(player.plasmagrenades)
        if player.in_air:
            player.update_action(2)#2: jump
        elif moving_left or moving_right:
            player.update_action(1)#1: run
        else:
            player.update_action(0)#0: idle
        player.move(moving_left, moving_right)


#================================================================
#levels
#================================================================


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
                plasmagrenade = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
        #mouse presses
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if play_button.is_clicked(mouse_pos):
                play_game()
            if leaderboard_button.is_clicked(mouse_pos):
                show_leaderboard()
            if quit_button.is_clicked(mouse_pos):
                pygame.quit()
                sys.exit()            

        #keyboard button released            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                plasmagrenade = False
                plasmagrenade_isthrown = False
        

        pygame.display.update()

pygame.quit()