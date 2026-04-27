import pygame
import os
from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        image_loaded = False

        # Pokusí se načíst obrázek nepřítele (např. enemy.png, monster.jpg)
        for name in ["enemy", "monster", "slime"]:
            for ext in ["png", "jpg"]:
                try:
                    image_path = os.path.join("img", f"{name}.{ext}")
                    self.image = pygame.image.load(image_path).convert_alpha()
                    # Předpokládá, že máš ENEMY_WIDTH a ENEMY_HEIGHT v config.py
                    self.image = pygame.transform.scale(self.image, (ENEMY_WIDTH, ENEMY_HEIGHT))
                    print(f"Načten obrázek nepřítele: {image_path}")
                    image_loaded = True
                    break # Ukočí vnitřní cyklus
                except (pygame.error, FileNotFoundError):
                    continue
            
            if image_loaded:
                break # Ukončí vnější cyklus, pokud jsme úspěšně načetli obrázek

        # Fallback: Pokud se obrázek nenačte, vytvoříme barevný obdélník
        if not image_loaded:
            print("Obrázek nepřítele nenalezen, používám zástupnou barvu.")
            self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
            self.image.fill(ENEMY_COLOUR) # Předpokládá ENEMY_COLOUR v config.py

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity_y = 0

    def update(self, platforms):
        # Aplikace gravitace - nepřítel padá, dokud nenarazí na plošinu
        self.velocity_y += GRAVITY
        if self.velocity_y > 15:
            self.velocity_y = 15

        self.rect.y += self.velocity_y

        # Kontrola kolizí s plošinami pro udržení na povrchu
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0: # Pokud padá dolů
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)