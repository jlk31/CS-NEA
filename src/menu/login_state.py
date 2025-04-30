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
        self.password = []
        self.username_str = ""

        self.space_img = pygame.image.load("assets/background/space.png").convert_alpha()
        self.space_img = pygame.transform.scale(self.space_img, (800, 600))

        sign_in_img = pygame.image.load("assets/buttons/sign_in_button.png").convert_alpha()
        sign_up_img = pygame.image.load("assets/buttons/sign_up_button.png").convert_alpha()

        self.sign_in_button = Button(325, 350, sign_in_img, 1 * 0.5)
        self.sign_up_button = Button(325, 450, sign_up_img, 1 * 0.5)

        self.active_field = "username"

#================================================================================
#event handler for login state
#================================================================================

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:  # Switch between username and password fields
                    self.active_field = "password" if self.active_field == "username" else "username"
                elif event.key == pygame.K_RETURN and self.username and self.password:
                    return "main_menu"
                elif event.key == pygame.K_BACKSPACE:
                    if self.active_field == "username" and self.username:
                        self.username.pop()
                    elif self.active_field == "password" and self.password:
                        self.password.pop()
                elif event.unicode.isprintable():
                    if self.active_field == "username" and len(self.username) < 15:
                        self.username.append(event.unicode)
                    elif self.active_field == "password" and len(self.password) < 15:
                        self.password.append(event.unicode)

        self.username_str = ''.join(self.username)
        self.password_str = '*' * len(self.password)

#================================================================================
#handle user sign in 
#================================================================================

        if self.sign_in_button.draw(self.screen):
            if self.username and self.password:
                if self.sign_in(self.username, self.password):
                    print("Sign in successful")
                    return "main_menu"
                else:
                    print("Invalid username or password.")

#================================================================================
#handle user sign up
#================================================================================

        if self.sign_up_button.draw(self.screen):
            if self.username and self.password:
                if self.sign_up(self.username, self.password):
                    print("Sign up successful")
                else:
                    print("Username already exists. Please choose another.")

#================================================================================
#database setup
#================================================================================

    def initialize_database(self):
        """Create the users table with the correct schema."""
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Drop the old table if it exists
        cursor.execute("DROP TABLE IF EXISTS users")

        # Create the new table with username and password columns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

#================================================================================
#sign in and sign up methods
#================================================================================

    def sign_in(self, username, password):
        username_str = ''.join(username)
        password_str = ''.join(password)
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username_str, password_str))
        user = cursor.fetchone()
        conn.commit()
        conn.close()
        return user is not None
    
    def sign_up(self, username, password):
        try:
            username_str = ''.join(username)
            password_str = ''.join(password)
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username_str, password_str))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        
    def initialize_database(self):
        """Create the users table with the correct schema."""
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Drop the old table if it exists
        cursor.execute("DROP TABLE IF EXISTS users")

        # Create the new table with username and password columns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

#================================================================================
#render method
#================================================================================

    def render(self):
        self.screen.blit(self.space_img, (0, 0))

        user_box = pygame.Rect(200, 175, 400, 50)
        pygame.draw.rect(self.screen, (0, 0, 0), user_box, border_radius=5)
        pygame.draw.rect(self.screen, (255, 255, 255), user_box, 2, border_radius=5)

        pass_box = pygame.Rect(200, 275, 400, 50)
        pygame.draw.rect(self.screen, (0, 0, 0), pass_box, border_radius=5)
        pygame.draw.rect(self.screen, (255, 255, 255), pass_box, 2, border_radius=5)

        font = pygame.font.SysFont("Futura", 30)
        user_surface = font.render(f"Username: {self.username_str}", True, (255, 255, 255))
        pass_surface = font.render(f"Password: {self.password_str}", True, (255, 255, 255))

        self.screen.blit(user_surface, (user_box.x + 10, user_box.y + 10))
        self.screen.blit(pass_surface, (pass_box.x + 10, pass_box.y + 10))

        self.sign_in_button.draw(self.screen)
        self.sign_up_button.draw(self.screen)

        self.initialize_database()