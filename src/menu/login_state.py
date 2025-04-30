import pygame
import sqlite3
from menu.base_state import BaseState
from utils.button import Button

class LoginState(BaseState):
    def __init__(self, screen):
        super().__init__(screen)
        self.username = ""

        self.space_img = pygame.image.load("assets/background/space.png").convert_alpha()

        sign_in_img = pygame.image.load("assets/buttons/sign_in_button.png").convert_alpha()
        sign_up_img = pygame.image.load("assets/buttons/sign_up_button.png").convert_alpha()

        self.sign_in_button = Button(200, 300, sign_in_img, 1)
        self.sign_up_button = Button(400, 300, sign_up_img, 1)

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

        if self.sign_in_button.draw(self.screen):
            if self.username.strip():
                if self.sign_in(self.username.strip()):
                    print("Sign in successful")
                    return "main_menu"
                else:
                    print("Username not found. Please sign up.")

        if self.sign_up_button.draw(self.screen):
            if self.username.strip():
                if self.sign_up(self.username.strip()):
                    print("Sign up successful")
                else:
                    print("Username already exists. Please choose another.")

        return None
    
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

    def render(self):
        self.screen.blit(self.space_img, (0, 0))

        font = pygame.font.SysFont("Arial", 30)

        font = pygame.font.SysFont("Arial", 30)
        text_surface = font.render(f"Username: {self.username}", True, (255, 255, 255))
        self.screen.blit(text_surface, (200, 200))

        self.sign_in_button.draw(self.screen)
        self.sign_up_button.draw(self.screen)