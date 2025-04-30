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
        self.username = []
        self.username_str = ""

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
                if event.key == pygame.K_RETURN and self.username:
                    return "main_menu"
                elif event.key == pygame.K_BACKSPACE and self.username:
                    self.username.pop()
                elif event.unicode.isprintable() and len(self.username) < 15:
                    self.username.append(event.unicode)

        self.username_str = ''.join(self.username)

#================================================================================
#handle user sign in 
#================================================================================

        if self.sign_in_button.draw(self.screen):
            if self.username:
                if self.sign_in(self.username):
                    print("Sign in successful")
                    return "main_menu"
                else:
                    print("Username not found. Please sign up.")

#================================================================================
#handle user sign up
#================================================================================

        if self.sign_up_button.draw(self.screen):
            if self.username:
                if self.sign_up(self.username):
                    print("Sign up successful")
                else:
                    print("Username already exists. Please choose another.")

        return None

#================================================================================
#database setup
#================================================================================

    def initialize_database(self):
        """Create the users table if it doesn't exist."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )
    """)
    conn.commit()
    conn.close()

#================================================================================
#sign in and sign up methods
#================================================================================

    def sign_in(self, username):
        username_str = ''.join(username)
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username_str,))
        user = cursor.fetchone()
        conn.close()
        return user is not None
    
    def sign_up(self, username):
        try:
            username_str = ''.join(username)
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username) VALUES (?)", (username_str,))
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
        text_surface = font.render(f"Username: {self.username_str}", True, (255, 255, 255))
        self.screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

        self.sign_in_button.draw(self.screen)
        self.sign_up_button.draw(self.screen)

        self.initialize_database()