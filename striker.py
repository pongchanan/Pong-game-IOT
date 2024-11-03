import pygame

class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        """
        Initialize a striker (paddle) with position, dimensions, speed and color
        
        Args:
            posx (int): Initial x position
            posy (int): Initial y position 
            width (int): Width of striker
            height (int): Height of striker
            speed (int): Movement speed
            color (tuple): RGB color value
        """
        self.posx = posx
        self.posy = posy
        self.width = width 
        self.height = height
        self.speed = speed
        self.color = color
        self.Rect = pygame.Rect(posx, posy, width, height)
        
    def display(self, screen):
        """Draw the striker on the screen"""
        pygame.draw.rect(screen, self.color, self.Rect)

    def update(self, sensor):
        """
        Update striker position based on MPU6050 sensor data
        
        Args:
            sensor: MPU6050 sensor object
        """
        accel_data = sensor.get_accel_data()
        y_acceleration = accel_data['y']
        
        # Adjust this value to change sensitivity
        sensitivity = 2
        
        self.posy += y_acceleration * sensitivity

        # Keep striker within screen bounds
        if self.posy <= 0:
            self.posy = 0
        if self.posy + self.height >= 600:  # HEIGHT constant
            self.posy = 600 - self.height

        self.Rect.topleft = (self.posx, self.posy)

    def displayScore(self, screen, font, text, score, x, y, color):
        """
        Display the player's score
        
        Args:
            screen: Pygame screen surface
            font: Pygame font object
            text (str): Score label
            score (int): Player's score
            x (int): X position
            y (int): Y position
            color (tuple): RGB color value
        """
        text = font.render(text+str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
        screen.blit(text, textRect)

    def getRect(self):
        """Return the pygame Rect object for collision detection"""
        return self.Rect