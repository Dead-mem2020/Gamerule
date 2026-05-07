import pygame
from config import *
from game.game import Game
from game.menu import Menu

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("American day")

    while True:
        menu = Menu(screen)
        start, chosen_skin = menu.run()
        if not start:
            break

        game = Game(screen, chosen_skin)
        game.run()

        if game.won:
            font = pygame.font.SysFont(None, 48)
            text = font.render("You Won! Washington Saved!", True, (0, 255, 0))
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
            pygame.display.flip()
            pygame.time.wait(3000)
            break

    pygame.quit()

if __name__ == "__main__":
    main()