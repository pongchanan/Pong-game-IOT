import pygame

class Renderer:
    def __init__(self, screen, players, ball, game_state):
        self.screen = screen
        self.players = players
        self.ball = ball
        self.game_state = game_state

        # Font that is used to render the text
        self.titlefont = pygame.font.Font('freesansbold.ttf', 80)
        self.mediumfont = pygame.font.Font('freesansbold.ttf', 40)
        self.font = pygame.font.Font('freesansbold.ttf', 20)

        # RGB values of standard colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)

    def render(self):
        self.screen.fill(self.black)

        # Draw game objects
        for player in self.players:
            player.display()
        self.ball.display()

        # Display scores
        self.display_score("Player 1: ", self.game_state.player1_score, 100, 20, self.white)
        self.display_score("Player 2: ", self.game_state.player2_score, self.screen.get_width() - 100, 20, self.white)

        # Display game over message
        if self.game_state.is_game_over():
            self.display_game_over()

        # Display countdown timer
        if self.game_state.timer > 0 and self.game_state.timer <= 4:
            self.display_countdown()

    def display_score(self, text, score, x, y, color):
        score_text = self.font.render(text + str(score), True, color)
        score_rect = score_text.get_rect()
        score_rect.center = (x, y)
        self.screen.blit(score_text, score_rect)

    def display_countdown(self):
        countdown_text = self.mediumfont.render(str(self.game_state.timer - 1), True, self.white)
        countdown_rect = countdown_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(countdown_text, countdown_rect)
        self.game_state.timer -= 1

    def display_game_over(self):
        victory_text = self.mediumfont.render("Victory!", True, self.white)
        victory_rect = victory_text.get_rect(center=(self.screen.get_width() // 2 + 70, self.screen.get_height() // 2 + 50))
        self.screen.blit(victory_text, victory_rect)
        self.game_state.timer = 0