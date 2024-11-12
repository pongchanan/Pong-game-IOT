import pygame
import random
from math import sqrt, pow
from threading import Thread
from utils import beep  # Assuming the beep function is in utils.py

class Ball:
    def __init__(self, posx, posy, radius, speed, color, screen, HEIGHT):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.basespeed = speed
        self.netspeed = speed
        self.color = color
        self.screen = screen
        self.HEIGHT = HEIGHT
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
        pygame.draw.circle(self.screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        # move
        self.posx += self.xspeed * self.xFac
        self.posy += self.yspeed * self.yFac

        # flip yFac
        if self.posy <= 0 or self.posy >= self.HEIGHT:
            self.yFac *= -1

        # if ball goes out if bound on either players' sides, set firsttime to 0 so score only increments once
        # return 1 if player 1 scores
        # return -1 if player 2 scores
        # return 0 if neither scored yet
        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        if self.posx >= self.screen.get_width() and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def reset(self):
        # reset ball position to the middle of the screen
        self.posx = self.screen.get_width() // 2
        self.posy = self.HEIGHT // 2
        self.lasthit = None
        self.netspeed = self.basespeed
        self.yspeed = random.randrange(0, int(self.netspeed-2))
        self.update_xspeed()
        # ball goes to the side that scored
        self.xFac *= -1
        self.firstTime = 1

    def hit(self, striker):
        buzzer_thread = Thread(target=beep)
        buzzer_thread.daemon = True
        buzzer_thread.start()
        
        striker_center = striker.posy + striker.height // 2
        hit_distance = self.posy - striker_center
        ratio = hit_distance / 75
        if ratio > 0:
            self.yFac = 1
        if ratio < 0:
            self.yFac = -1
        self.yspeed = abs(ratio * self.netspeed)
        self.netspeed += 0.5
        self.update_xspeed()
        self.xFac *= -1
        self.lasthit = striker

    def checkCollision(self, players):
        for player in players:
            if self.getRect().colliderect(player.getRect()):
                if self.lasthit != player:
                    self.hit(player)
                    break

    # to be used for collision
    def getRect(self):
        return pygame.Rect(self.posx - self.radius, self.posy - self.radius, self.radius * 2, self.radius * 2)