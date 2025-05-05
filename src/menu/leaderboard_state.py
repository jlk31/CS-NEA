import pygame
from menu.base_state import BaseState

class LeaderboardState(BaseState):
    def __init__(self, screen, db_connection):
        super().__init__(screen)
        self.db_connection = db_connection
        self.font = pygame.font.SysFont('Arial', 30)
        self.scores = []

    def load_scores(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT player_name, high_score FROM players ORDER BY high_score DESC LIMIT 10")
        self.scores = cursor.fetchall()

    def render(self):
        self.screen.fill((0, 0, 0))
        title = self.font.render("Leaderboard", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 50))

        # Display the scores
        for i, (player_name, high_score) in enumerate(self.scores):
            text = self.font.render(f"{i + 1}. {player_name}: {high_score}", True, (255, 255, 255))
            self.screen.blit(text, (100, 100 + i * 40))

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "main_menu"
        return None