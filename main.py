import pygame
import RPi.GPIO as GPIO
from mpu6050 import mpu6050
from src.game_manager import GameManager

def main():
    try:
        game_manager = GameManager()
        game_manager.run()
    except IOError:
        print("Error reading from MPU6050 sensors. Exiting.")
    finally:
        GPIO.cleanup()
        pygame.quit()

if __name__ == "__main__":
    main()