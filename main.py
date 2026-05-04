import pygame
from config import *
from game.game import Game
from game.menu import Menu

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("American day")

    menu = Menu(screen)
    start, chosen_skin = menu.run()
    if not start:
        pygame.quit()
        return

    game = Game(screen, chosen_skin)
    game.run()

    pygame.quit()

if __name__ == "__main__":
    main()