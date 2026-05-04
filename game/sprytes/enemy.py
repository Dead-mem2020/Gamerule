import pygame
import os
from config import *



class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_name, fallback_color=ENEMY_COLOUR):
        super().__init__()

        image_loaded = False

        for name in image_name:
            for ext in ["png", "jpg"]:
                try:
                    image_path = os.path.join("img", f"{name}.{ext}")
                    self.image = pygame.image.load(image_path).convert_alpha()
                    self.image = pygame.transform.scale(self.image, (ENEMY_WIDTH, ENEMY_HEIGHT))
                    print(f"Načten obrázek nepřítele: {image_path}")
                    image_loaded = True
                    break
                except (pygame.error, FileNotFoundError):
                    continue
            
            if image_loaded:
                break 

        if not image_loaded:
            print(f"Obrázek nepřítele pro {image_name} nenalezen, používám zástupnou barvu.")
            self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
            self.image.fill(fallback_color) # Každý typ nepřítele může mít jinou zástupnou barvu

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity_y = 0

    def apply_gravity(self, platforms):
        self.velocity_y += GRAVITY
        if self.velocity_y > 15:
            self.velocity_y = 15

        self.rect.y += self.velocity_y

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0


    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Enemy1(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, ["enemy1"])

    def update(self, platforms):
        self.apply_gravity(platforms)



class Enemy2(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, ["enemy2"], fallback_color=(100, 100, 100))
        self.velocity_x = 1

    def update(self, platforms):
        self.rect.x += self.velocity_x

        if self.rect.left <= 0:
            self.rect.left = 0
            self.velocity_x *= -1 # Změní směr doprava
            
        elif self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.velocity_x *= -1 # Změní směr doleva


        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_x > 0: 
                    self.rect.right = platform.rect.left
                    self.velocity_x *= -1 
                elif self.velocity_x < 0: 
                    self.rect.left = platform.rect.right
                    self.velocity_x *= -1 

        self.apply_gravity(platforms)