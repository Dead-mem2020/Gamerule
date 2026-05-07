import os
import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, skin=0):
        super().__init__()
        self.skin = int(skin)
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "textures", "player")

        skin_files = {
            0: "Trump.png",
            1: "Musk.png"
        }
        filename = skin_files.get(self.skin, skin_files[0])
        img_path = os.path.join(assets_dir, filename)

        try:
            img = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.scale(img, (self.width, self.height))
        except Exception as e:
            print(f"Chyba načtení hráčova skinu: {img_path} -> {e}")
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            if self.skin == 0:
                self.image.fill((0, 255, 0))
            else:
                self.image.fill((0, 0, 255))

        self.rect = self.image.get_rect(topleft=(x, y))

        # fyzika / pohyb
        self.vx = 0
        self.vy = 0
        self.on_ground = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vx = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = PLAYER_SPEED
        if (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vy = -JUMP_POWER
            self.on_ground = False

    def update(self, platforms_group, enemies_group=None):
        self.handle_input()
        self.rect.x += self.vx
        self.vy += GRAVITY
        self.rect.y += int(self.vy)

        self.on_ground = False
        for plat in platforms_group:
            if self.rect.colliderect(plat.rect):
                if self.vy >= 0 and self.rect.bottom <= plat.rect.bottom:
                    self.rect.bottom = plat.rect.top
                    self.vy = 0
                    self.on_ground = True

        if enemies_group is not None:
            if pygame.sprite.spritecollideany(self, enemies_group):
                return True

        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)