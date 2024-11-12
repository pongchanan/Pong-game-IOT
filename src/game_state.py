class GameState:
    def __init__(self):
        self.player1_score = 0
        self.player2_score = 0
        self.scored = False
        self.game_over = False
        self.timer = -1

    def update(self, point):
        if point == -1:
            self.player1_score += 1
            self.scored = True
        elif point == 1:
            self.player2_score += 1
            self.scored = True

        if self.scored:
            self.timer = 5
            self.scored = False

        if self.player1_score >= 3 or self.player2_score >= 3:
            self.game_over = True

    def is_game_over(self):
        return self.game_over

    def reset(self):
        self.player1_score = 0
        self.player2_score = 0
        self.game_over = False
        self.timer = -1