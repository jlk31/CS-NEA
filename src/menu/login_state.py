#================================================================================
#modules being imported
#================================================================================

import pygame
import sqlite3
from menu.base_state import BaseState
from utils.button import Button

#================================================================================
#login state class
#================================================================================

class LoginState(BaseState):
    def __init__(self, screen):
        super().__init__(screen)
        self.username = ""

        self.space_img = pygame.image.load("assets/background/space.png").convert_alpha()
        self.space_img = pygame.transform.scale(self.space_img, (800, 600))

        sign_in_img = pygame.image.load("assets/buttons/sign_in_button.png").convert_alpha()
        sign_up_img = pygame.image.load("assets/buttons/sign_up_button.png").convert_alpha()

        self.sign_in_button = Button(350, 300, sign_in_img, 1 * 0.5)
        self.sign_up_button = Button(350, 400, sign_up_img, 1 * 0.5)

#================================================================================
#event handler for login state
#================================================================================

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.username.strip():
                    return "main_menu"
                elif event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    self.username += event.unicode

#================================================================================
#handle user sign in 
#================================================================================

        if self.sign_in_button.draw(self.screen):
            if self.username.strip():
                if self.sign_in(self.username.strip()):
                    print("Sign in successful")
                    return "main_menu"
                else:
                    print("Username not found. Please sign up.")

#================================================================================
#handle user sign up
#================================================================================

        if self.sign_up_button.draw(self.screen):
            if self.username.strip():
                if self.sign_up(self.username.strip()):
                    print("Sign up successful")
                else:
                    print("Username already exists. Please choose another.")

        return None

#================================================================================
#sign in and sign up methods
#================================================================================

    def sign_in(self, username):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()
        return user is not None
    
    def sign_up(self, username):
        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

#================================================================================
#render method
#================================================================================

    def render(self):
        self.screen.blit(self.space_img, (0, 0))

        input_box = pygame.Rect(200, 175, 400, 50)
        pygame.draw.rect(self.screen, (0, 0, 0), input_box, border_radius=5)
        pygame.draw.rect(self.screen, (255, 255, 255), input_box, 2, border_radius=5)

        font = pygame.font.SysFont("Futura", 30)
        text_surface = font.render(f"Username: {self.username}", True, (255, 255, 255))
        self.screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

        self.sign_in_button.draw(self.screen)
        self.sign_up_button.draw(self.screen)