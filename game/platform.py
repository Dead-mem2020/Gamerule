import pygame
from config import *

class Platform(pygame.sprite.Sprite):
    """
    Třída platform¨
    Sprite - základní herní objekt v Pygamu, metody .image, .rect automaticky
    """
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image .fill(Platform_color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)