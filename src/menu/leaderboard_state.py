import pygame
from menu.base_state import BaseState

class LeaderboardState(BaseState):
    def __init__(self, screen, db_connection):
        super().__init__(screen)
        self.db_connection = db_connection
        self.font = pygame.font.SysFont('Arial', 30)
        self.scores = []
        self.ensure_table_exists()

    def ensure_table_exists(self):
        cursor = self.db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS high_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        """)
        self.db_connection.commit()

    def load_scores(self):
        cursor = self.db_connection.cursor()
        cursor.execute("""
            SELECT username, MAX(score) as highest_score
            FROM high_scores
            GROUP BY username
            ORDER BY highest_score DESC
            LIMIT 10
        """)
        self.scores = cursor.fetchall()

    def render(self):
        self.screen.fill((0, 0, 0))
        
        title = self.font.render("Leaderboard", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 50))

        #display the scores
        for i, (player_name, high_score) in enumerate(self.scores):
            text = self.font.render(f"{i + 1}. {player_name}: {high_score}", True, (255, 255, 255))
            self.screen.blit(text, (100, 100 + i * 40))

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "main_menu"
        return None