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


class MovingPlatform(Platform):
    def __init__(self, x, y, width, height, dx=0, dy=0, min_x=None, max_x=None, min_y=None, max_y=None):
        super().__init__(x, y, width, height)
        self.dx = dx
        self.dy = dy
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.min_x is not None and self.rect.x < self.min_x:
            self.rect.x = self.min_x
            self.dx *= -1
        if self.max_x is not None and self.rect.x > self.max_x:
            self.rect.x = self.max_x
            self.dx *= -1
        if self.min_y is not None and self.rect.y < self.min_y:
            self.rect.y = self.min_y
            self.dy *= -1
        if self.max_y is not None and self.rect.y > self.max_y:
            self.rect.y = self.max_y
            self.dy *= -1
