import pygame
from striker import Striker
from ball import Ball
import RPi.GPIO as GPIO
from mpu6050 import mpu6050

class Game:
    def __init__(self):
        """Initialize game settings and objects"""
        pygame.init()
        
        # Constants
        self.WIDTH = 900
        self.HEIGHT = 600
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.FPS = 60
        self.BUZZER_PIN = 19
        
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUZZER_PIN, GPIO.OUT)
        
        # Setup MPU6050 sensors
        self.joy1 = mpu6050(0x68)  # First sensor address
        self.joy2 = mpu6050(0x69)  # Second sensor address
        
        # Setup display
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong")
        
        # Setup fonts
        self.titlefont = pygame.font.Font('freesansbold.ttf', 80)
        self.mediumfont = pygame.font.Font('freesansbold.ttf', 40)
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        
        self.clock = pygame.time.Clock()

    def start_screen(self):
        """Display and handle the start screen"""
        FPS = 30
        player1ready = False
        player2ready = False
        timer = 4
        
        while timer > 0:
            self.screen.fill(self.BLACK)
            
            # Draw title
            title_text = self.titlefont.render("PONG", True, self.WHITE)
            text_rect = title_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 30))
            self.screen.blit(title_text, text_rect)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_w, pygame.K_s]:
                        player1ready = True
                    if event.key in [pygame.K_UP, pygame.K_DOWN]:
                        player2ready = True
            
            # Display ready status
            self._display_ready_status(player1ready, player2ready)
            
            if player1ready and player2ready:
                FPS = 1
                timer -= 1
                self._display_countdown(timer)
            
            pygame.display.update()
            self.clock.tick(FPS)
        
        return True

    def game_loop(self):
        """Main game loop"""
        # Initialize game objects
        player1 = Striker(20, self.HEIGHT // 2 - 50, 10, 100, 10, self.GREEN)
        player2 = Striker(self.WIDTH - 30, self.HEIGHT // 2 - 50, 10, 100, 10, self.GREEN)
        ball = Ball(self.WIDTH // 2, self.HEIGHT // 2, 7, 7, self.WHITE)
        
        players = [player1, player2]
        player1Score = player2Score = 0
        scored = False
        gameend = False
        timer = -1
        
        while True:
            if gameend:
                pygame.time.delay(2000)
                return
            
            self.screen.fill(self.BLACK)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            # Update game objects
            player1.update(self.joy1)
            player2.update(self.joy2)
            ball.checkCollision(players)
            point = ball.update(self.HEIGHT)
            
            # Handle scoring
            if point != 0:
                scored, timer = self._handle_scoring(point, player1Score, player2Score)
            
            # Draw everything
            self._draw_game_objects(player1, player2, ball, player1Score, player2Score)
            
            # Handle timer and ball reset
            timer = self._handle_timer(timer, ball, scored)
            
            pygame.display.update()
            self.clock.tick(self.FPS)

    def _display_ready_status(self, player1ready, player2ready):
        """Helper method to display player ready status"""
        if player1ready:
            text = "Player 1 Ready!"
            pos = (40, self.HEIGHT - 40)
        else:
            text = "Waiting for Player 1"
            pos = (40, self.HEIGHT - 40)
        self.screen.blit(self.font.render(text, True, self.GREEN), pos)
        
        if player2ready:
            text = "Player 2 Ready!"
            pos = (self.WIDTH - 200, self.HEIGHT - 40)
        else:
            text = "Waiting for Player 2"
            pos = (self.WIDTH - 240, self.HEIGHT - 40)
        self.screen.blit(self.font.render(text, True, self.GREEN), pos)

    def _display_countdown(self, timer):
        """Helper method to display countdown timer"""
        text = self.mediumfont.render(str(timer), True, self.WHITE)
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 50))
        self.screen.blit(text, text_rect)

    def cleanup(self):
        """Cleanup GPIO pins"""
        GPIO.cleanup()