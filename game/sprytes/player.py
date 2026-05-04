import os
import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, skin=0):
        super().__init__()
        self.skin = int(skin)
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        self.max_health = 3
        self.health = self.max_health
        self.invincible_timer = 0

        # assets dir: c:\... \game\assets
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

        # map skin index to filename
        skin_files = {
            0: "Musk.png",
            1: "Trump.png"
        }
        filename = skin_files.get(self.skin, skin_files[0])
        img_path = os.path.join(assets_dir, filename)

        try:
            img = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.scale(img, (self.width, self.height))
        except Exception:
            # fallback - barvy dle náhledu v menu
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            if self.skin == 0:
                self.image.fill((0, 255, 0))  # zelený fallback
            else:
                self.image.fill((0, 0, 255))  # modrý fallback

        self.rect = self.image.get_rect(topleft=(x, y))

        # fyzika / pohyb
        self.vx = 0
        self.vy = 0
        self.on_ground = False


    def take_damage(self):
        if self.invincible_timer <= 0:
            self.health -= 1
            self.invincible_timer = 60 # 60 snímků nesmrtelnosti (cca 1 sekunda)
            print(f"Au! Zbývají životy: {self.health}")
            
            if self.health <= 0:
                return True # Vrací True, pokud hráč zemřel
        return False

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
        # 1. Odpočet nesmrtelnosti
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        self.handle_input()
        
        # --- 2. POHYB V OSE X (Do stran) ---
        self.rect.x += self.vx

        # Kolize s nepřáteli v ose X
        if enemies_group is not None:
            for enemy in enemies_group:
                if self.rect.colliderect(enemy.rect):
                    if getattr(enemy, 'is_deadly', False):
                        if self.take_damage():
                            return True # Game over
                            
                    if self.vx > 0: 
                        self.rect.right = enemy.rect.left
                    elif self.vx < 0: 
                        self.rect.left = enemy.rect.right

        # --- 3. POHYB V OSE Y (Gravitace) ---
        self.vy += GRAVITY
        if self.vy > 15:
            self.vy = 15
        self.rect.y += int(self.vy)

        # Kolize s plošinami v ose Y
        for plat in platforms_group:
            if self.rect.colliderect(plat.rect):
                if self.vy > 0: # Padá dolů
                    self.rect.bottom = plat.rect.top
                    self.vy = 0
                elif self.vy < 0: # Letí nahoru
                    self.rect.top = plat.rect.bottom
                    self.vy = 0

        # Kolize s nepřáteli v ose Y
        if enemies_group is not None:
            for enemy in enemies_group:
                if self.rect.colliderect(enemy.rect):
                    if getattr(enemy, 'is_deadly', False):
                        if self.take_damage():
                            return True
                            
                    if self.vy > 0: 
                        self.rect.bottom = enemy.rect.top
                        self.vy = 0
                    elif self.vy < 0: 
                        self.rect.top = enemy.rect.bottom
                        self.vy = 0

        # --- 4. OPRAVA SKÁKÁNÍ (Detekce země) ---
        # Posuneme hráče o 1 pixel dolů
        self.rect.y += 1
        self.on_ground = False
        
        # Zkontrolujeme, jestli se něčeho dotýká
        for plat in platforms_group:
            if self.rect.colliderect(plat.rect):
                self.on_ground = True
                break
                
        if not self.on_ground and enemies_group is not None:
            for enemy in enemies_group:
                if self.rect.colliderect(enemy.rect):
                    self.on_ground = True
                    break
                    
        # A vrátíme ho nepozorovaně zpět!
        self.rect.y -= 1

        # Ochrana proti propadnutí mapou
        if self.rect.top > SCREEN_HEIGHT:
            return True

        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)