import pygame

class Striker:
    # Take the initial position, dimensions, speed, color, screen, height, and font of the object
    def __init__(self, posx, posy, width, height, speed, color, screen, HEIGHT, font, sensor):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.screen = screen
        self.HEIGHT = HEIGHT
        self.font = font
        self.sensor = sensor
        self.Rect = pygame.Rect(posx, posy, width, height)
        self.display()

    # Used to display the object on the screen
    def display(self):
        pygame.draw.rect(self.screen, self.color, self.Rect)

    def update(self):
        accel_data = self.sensor.get_accel_data()
        if accel_data:
            y_acceleration = accel_data['y']
            
            # Adjust this value to change sensitivity
            sensitivity = 2
            
            self.posy += y_acceleration * sensitivity

            if self.posy <= 0:
                self.posy = 0
            if self.posy + self.height >= self.HEIGHT:
                self.posy = self.HEIGHT - self.height

            self.Rect.topleft = (self.posx, self.posy)

    def displayScore(self, text, score, x, y, color):
        text = self.font.render(text+str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        self.screen.blit(text, textRect)

    # to be used for collision
    def getRect(self):
        return self.Rect