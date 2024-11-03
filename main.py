import pygame
from game import Game
import RPi.GPIO as GPIO

def main():
    """Main entry point of the game"""
    game = Game()
    try:
        while True:
            if game.start_screen():
                game.game_loop()
            else:
                break
    finally:
        game.cleanup()
        pygame.quit()

if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
        GPIO.cleanup()