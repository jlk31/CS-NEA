import pygame
from menu.base_state import BaseState

class LeaderboardState(BaseState):
    def __init__(self, screen, db_connection):
        super().__init__(screen)
        self.db_connection = db_connection
        self.font = pygame.font.SysFont('Arial', 30)
        self.scores = []
        self.ensure_table_exists()

        self.space_img = pygame.image.load("assets/background/space.png").convert_alpha()
        self.space_img = pygame.transform.scale(self.space_img, (800, 700))

        self.gold_medal_img = pygame.image.load("assets/medals/gold_medal.png").convert_alpha()
        self.gold_medal_img = pygame.transform.scale(self.gold_medal_img, (50, 50))

        self.silver_medal_img = pygame.image.load("assets/medals/silver_medal.png").convert_alpha()
        self.silver_medal_img = pygame.transform.scale(self.silver_medal_img, (50, 50))

        self.bronze_medal_img = pygame.image.load("assets/medals/bronze_medal.png").convert_alpha()
        self.bronze_medal_img = pygame.transform.scale(self.bronze_medal_img, (50, 50))

    def ensure_table_exists(self):
        cursor = self.db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS high_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE
        )
    """)

        self.db_connection.commit()

    def load_scores(self):
        cursor = self.db_connection.cursor()
        cursor.execute("""
            SELECT users.username, COALESCE(MAX(high_scores.score), 0) AS highest_score
            FROM users
            LEFT JOIN high_scores ON users.username = high_scores.username
            GROUP BY users.username
            ORDER BY highest_score DESC
            LIMIT 10
        """)
        self.scores = cursor.fetchall()

    def render(self):
        self.screen.blit(self.space_img, (0, 0))

        title = self.font.render("Leaderboard", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 50))

        #display the scores
        for i, (username, high_score) in enumerate(self.scores):
            text = self.font.render(f"{i + 1}. {username}: {high_score}", True, (255, 255, 255))
            self.screen.blit(text, (100, 100 + i * 40))
            y_offset = 100 + i * 60

            if i == 0:
                self.screen.blit(self.gold_medal, (50, y_offset))
            elif i == 1:
                self.screen.blit(self.silver_medal, (50, y_offset))
            elif i == 2:
                self.screen.blit(self.bronze_medal, (50, y_offset))
            else:
                rank_text = self.font.render(f"{i + 1}", True, (255, 255, 255))
                self.screen.blit(rank_text, (60, y_offset))

            self.screen.blit(self.avatar_placeholder, (120, y_offset))

            username_text = self.font.render(username, True, (255, 255, 255))
            self.screen.blit(username_text, (200, y_offset))

            star_count = high_score // 500  # 1 star for every 500 points
            for star in range(min(star_count, 5)):  # Limit to 5 stars
                star_x = 400 + star * 30
                pygame.draw.polygon(self.screen, (255, 215, 0), [
                    (star_x, y_offset + 20),
                    (star_x + 10, y_offset + 40),
                    (star_x - 10, y_offset + 40)
                ])

            score_text = self.font.render(str(high_score), True, (255, 255, 255))
            self.screen.blit(score_text, (600, y_offset))

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "main_menu"
        return None