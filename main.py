import pygame
from game import Game

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
    main()