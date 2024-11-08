import pygame
import random
from math import sqrt, pow
import RPi.GPIO as GPIO
from mpu6050 import mpu6050
import time

pygame.init()
BUZZER_PIN = 19
mpu6050_1_address = 0x68
mpu6050_2_address = 0x69

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

try:
    joy1 = mpu6050(mpu6050_1_address)
except IOError:
    print("Error initializing MPU6050 sensors in " + "0x68" + ". Exiting.")
    GPIO.cleanup()
    pygame.quit()
    exit()
try:
    joy2 = mpu6050(mpu6050_2_address)
except IOError:
    print("Error initializing MPU6050 sensors in " + "0x69" + ". Exiting.")
    GPIO.cleanup()
    pygame.quit()
    exit()


# Font that is used to render the text
titlefont = pygame.font.Font('freesansbold.ttf', 80)
mediumfont = pygame.font.Font('freesansbold.ttf', 40)
font = pygame.font.Font('freesansbold.ttf', 20)

# RGB values of standard colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Basic parameters of the screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

def read_sensor_data(joy):
    try:
        # Read the accelerometer values
        accelerometer_data = joy.get_accel_data()

        # Read the gyroscope values
        gyroscope_data = joy.get_gyro_data()

        # Read temp
        temperature = joy.get_temp()

        return accelerometer_data, gyroscope_data, temperature
    except IOError:
        print(f"Error reading from MPU6050 sensor at address {hex(joy.address)}.")
        return None, None, None

def beep(duration=0.1):
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(BUZZER_PIN, GPIO.LOW)

class Striker:
    # Take the initial position, dimensions, speed and color of the object
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.Rect = pygame.Rect(posx, posy, width, height)
        self.display()

    # Used to display the object on the screen
    def display(self):
        pygame.draw.rect(screen, self.color, self.Rect)

    def update(self, sensor):
        accel_data = sensor.get_accel_data()
        if accel_data:
            y_acceleration = accel_data['y']
            
            # Adjust this value to change sensitivity
            sensitivity = 2
            
            self.posy += y_acceleration * sensitivity

            if self.posy <= 0:
                self.posy = 0
            if self.posy + self.height >= HEIGHT:
                self.posy = HEIGHT - self.height

            self.Rect.topleft = (self.posx, self.posy)

    def displayScore(self, text, score, x, y, color):
        text = font.render(text+str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        screen.blit(text, textRect)

    # to be used for collision
    def getRect(self):
        return self.Rect

class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.basespeed = speed
        self.netspeed = speed
        self.color = color
        self.xFac = 1
        self.yFac = -1
        self.firstTime = 1
        self.lasthit = None 
        self.yspeed = random.randrange(0, int(self.netspeed-2))
        
        self.update_xspeed()
        self.display()

    def update_xspeed(self):
        # Calculate yspeed based on netspeed and xspeed
        self.xspeed = sqrt(pow(self.netspeed, 2) - pow(self.yspeed, 2))

    def display(self):
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        # move
        self.posx += self.xspeed*self.xFac
        self.posy += self.yspeed*self.yFac

        # flip yFac
        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1

        # if ball goes out if bound on either players' sides, set firsttime to 0 so score only increments once
        # return 1 if player 1 scores
        # return -1 if player 2 scores
        # return 0 if neither scored yet
        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        if self.posx >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def reset(self):
        # reset ball position to the middle of the screen
        self.posx = WIDTH//2
        self.posy = HEIGHT//2
        self.lasthit = None
        self.netspeed = self.basespeed
        self.yspeed = random.randrange(0, int(self.netspeed-2))
        self.update_xspeed()
        # ball goes to the side that scored
        self.xFac *= -1
        self.firstTime = 1

    def hit(self, striker):
        beep()
        striker_center = striker.posy + striker.height // 2
        hit_distance = self.posy - striker_center
        ratio = hit_distance/75
        if ratio > 0:
            self.yFac = 1
        if ratio < 0:
            self.yFac = -1
        self.yspeed = abs(ratio * self.netspeed)
        self.netspeed += 0.5
        self.update_xspeed()
        self.xFac *= -1
        self.lasthit = striker

        print(f"Hit distance: {hit_distance}")
        print(f"Ratio: {ratio}")
        print(f"netspeed: {self.netspeed}")
        print(f"yspeed: {self.yspeed}")
  
    def checkCollision(self, players):
        for player in players:
            if self.getRect().colliderect(player.getRect()):
                if self.lasthit != player:
                    self.hit(player)
                    break

    # to be used for collision
    def getRect(self):
        return pygame.Rect(self.posx - self.radius, self.posy - self.radius, self.radius * 2, self.radius * 2)

def start_screen():
    FPS = 30

    player1ready = False
    player2ready = False
    timer = 4
    
    while timer > 0:
        screen.fill(BLACK)
        title_text = titlefont.render("PONG", True, WHITE)
        text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        screen.blit(title_text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GPIO.cleanup()
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player1ready = True
                if event.key == pygame.K_s:
                    player1ready = True
                if event.key == pygame.K_UP:
                    player2ready = True
                if event.key == pygame.K_DOWN:
                    player2ready = True

        # Display player readiness
        if player1ready:
            player1_ready_text = font.render("Player 1 Ready!", True, GREEN)
            screen.blit(player1_ready_text, (40, HEIGHT - 40))
        else:
            player1_ready_text = font.render("Waiting for Player 1", True, GREEN)
            screen.blit(player1_ready_text, (40, HEIGHT - 40))

        if player2ready:
            player2_ready_text = font.render("Player 2 Ready!", True, GREEN)
            screen.blit(player2_ready_text, (WIDTH - 200, HEIGHT - 40))
        else:
            player2_ready_text = font.render("Waiting for Player 2", True, GREEN)
            screen.blit(player2_ready_text, (WIDTH - 240, HEIGHT - 40))

        if player1ready and player2ready:
               FPS = 1
               timer -= 1
               title_text = mediumfont.render(str(timer), True, WHITE)
               text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
               screen.blit(title_text, text_rect)

        pygame.display.update()
        clock.tick(FPS)

    return player1ready, player2ready

def game():
    FPS = 60

    scored = False
    gameend = False
    timer = -1
    
    # Put players in the middle of the screen
    player1 = Striker(20, HEIGHT // 2 - 50, 10, 100, 10, GREEN)
    player2 = Striker(WIDTH - 30, HEIGHT // 2 - 50, 10, 100, 10, GREEN)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 7, WHITE)
    
    players = [player1, player2]
    player1Score, player2Score = 0, 0
    
    while True:
        if gameend:
            pygame.time.delay(2000)
            return

        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GPIO.cleanup()
                pygame.quit()
                return

        # Handle key states
        keys = pygame.key.get_pressed()
        player1YFac = (keys[pygame.K_s] - keys[pygame.K_w])
        player2YFac = (keys[pygame.K_DOWN] - keys[pygame.K_UP])

        # Update player positions and ball
        player1.update(joy1)
        player2.update(joy2)
        
        ball.checkCollision(players)
        point = ball.update()

        if point == -1:
            player1Score += 1
            title_text = mediumfont.render("Player 1 Scores!", True, WHITE)
            timer = 5
            scored = True

        if point == 1:
            player2Score += 1
            title_text = mediumfont.render("Player 2 Scores!", True, WHITE)
            timer = 5
            scored = True

        if scored:
            if player1Score >= 3 or player2Score >= 3:
                victory_text = mediumfont.render("Victory!", True, WHITE)
                victory_text_rect = title_text.get_rect(center=(WIDTH // 2 + 70, HEIGHT // 2 + 50))
                screen.blit(victory_text, victory_text_rect)
                gameend = True
                timer = 0
        
        # Draw game objects
        player1.display()
        player2.display()
        ball.display()
        player1.displayScore("Player 1: ", player1Score, 100, 20, WHITE)
        player2.displayScore("Player 2: ", player2Score, WIDTH - 100, 20, WHITE)

        if timer > 0 and timer <= 4:
            title_text = mediumfont.render(str(timer-1), True, WHITE)
            text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(title_text, text_rect)
            timer -= 1

        if timer >= 4:
            FPS = 1
            text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(title_text, text_rect)
            timer -= 1

        if timer == 0:
            FPS = 60
            timer -= 1
            ball.reset()

        pygame.display.update()
        clock.tick(FPS)

def main():
    try:
        while True:
            player1ready, player2ready = start_screen()
            if player1ready and player2ready:
                game()
    except IOError:
        print("Error reading from MPU6050 sensors. Exiting.")
    finally:
        GPIO.cleanup()
        pygame.quit()
        
if __name__ == "__main__":
    main()