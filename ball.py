import pygame
import random
from math import sqrt, pow
import RPi.GPIO as GPIO
import time

class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        """
        Initialize the ball with position, size, speed and color
        
        Args:
            posx (int): Initial x position
            posy (int): Initial y position
            radius (int): Ball radius
            speed (int): Initial speed
            color (tuple): RGB color value
        """
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
        # Vertical speed (angle)
        self.yspeed = random.randrange(0, int(self.netspeed-2))
        self.update_xspeed()

    def update_xspeed(self):
        """Calculate horizontal speed based on net speed and vertical speed"""
        self.xspeed = sqrt(pow(self.netspeed, 2) - pow(self.yspeed, 2))

    def display(self, screen):
        """Draw the ball on the screen"""
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)

    def update(self, HEIGHT):
        """
        Update ball position and check for scoring
        
        Returns:
            int: 1 if player 2 scores, -1 if player 1 scores, 0 if no score
        """
        self.posx += self.xspeed * self.xFac
        self.posy += self.yspeed * self.yFac

        # Bounce off top and bottom
        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1

        # Check for scoring
        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        if self.posx >= 900 and self.firstTime:  # WIDTH constant
            self.firstTime = 0
            return -1
        return 0

    def reset(self, WIDTH, HEIGHT):
        """Reset ball to center position with initial speed"""
        self.posx = WIDTH//2
        self.posy = HEIGHT//2
        self.lasthit = None
        self.netspeed = self.basespeed
        self.yspeed = random.randrange(0, int(self.netspeed-2))
        self.update_xspeed()
        self.xFac *= -1
        self.firstTime = 1

    def hit(self, striker, BUZZER_PIN):
        """
        Handle collision with striker
        
        Args:
            striker: Striker object that was hit
            BUZZER_PIN: GPIO pin for buzzer
        """
        # Play sound
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(BUZZER_PIN, GPIO.LOW)

        # Calculate new direction based on where ball hits paddle
        striker_center = striker.posy + striker.height // 2
        hit_distance = self.posy - striker_center
        ratio = hit_distance/75
        
        # Set vertical direction
        self.yFac = 1 if ratio > 0 else -1
        
        # Update speeds
        self.yspeed = abs(ratio * self.netspeed)
        self.netspeed += 0.5
        self.update_xspeed()
        self.xFac *= -1
        self.lasthit = striker

    def checkCollision(self, players):
        """Check for collisions with all players"""
        for player in players:
            if self.getRect().colliderect(player.getRect()):
                if self.lasthit != player:
                    self.hit(player)
                    break

    def getRect(self):
        """Return pygame Rect object for collision detection"""
        return pygame.Rect(self.posx - self.radius, self.posy - self.radius, 
                         self.radius * 2, self.radius * 2)