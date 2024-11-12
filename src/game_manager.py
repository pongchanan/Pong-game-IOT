import pygame
import RPi.GPIO as GPIO
from striker import Striker
from ball import Ball
from game_state import GameState
from renderer import Renderer
from mpu6050 import mpu6050

class GameManager:
    def __init__(self):
        # Initialize Pygame and set up the game window
        pygame.init()
        self.width, self.height = 900, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pong")

        # Initialize sensors
        try:
            self.joy1 = mpu6050(0x68)
            self.joy2 = mpu6050(0x69)
        except IOError as e:
            print(f"Error initializing MPU6050 sensors: {e}")
            GPIO.cleanup()
            pygame.quit()
            exit()

        # Initialize font
        self.font = pygame.font.Font('freesansbold.ttf', 20)

        # Initialize game objects
        self.player1 = Striker(20, self.height // 2 - 50, 10, 100, 10, (0, 255, 0), self.screen, self.height, self.font, self.joy1)
        self.player2 = Striker(self.width - 30, self.height // 2 - 50, 10, 100, 10, (0, 255, 0), self.screen, self.height, self.font, self.joy2)
        self.ball = Ball(self.width // 2, self.height // 2, 7, 7, (255, 255, 255), self.screen, self.height)
        self.players = [self.player1, self.player2]

        # Initialize game state and renderer
        self.game_state = GameState()
        self.renderer = Renderer(self.screen, self.players, self.ball, self.game_state)

    def run(self):
        clock = pygame.time.Clock()

        while True:
            self.handle_events()
            self.update_game()
            self.renderer.render()
            pygame.display.update()
            clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GPIO.cleanup()
                pygame.quit()
                exit()

    def update_game(self):
        # Handle player input
        self.player1.update()
        self.player2.update()

        # Update ball
        self.ball.checkCollision(self.players)
        point = self.ball.update()

        # Update game state
        self.game_state.update(point)

        if self.game_state.is_game_over():
            self.game_state.reset()
            self.ball.reset()