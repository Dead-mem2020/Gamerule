import pygame
import os
from config import *


class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_name, fallback_color=ENEMY_COLOUR):
        super().__init__()

        image_loaded = False
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "textures", "enemies")

        for name in image_name:
            for root, _, files in os.walk(assets_dir):
                for ext in ["png", "jpg", "jpeg"]:
                    candidate = os.path.join(root, f"{name}.{ext}")
                    if os.path.isfile(candidate):
                        try:
                            self.image = pygame.image.load(candidate).convert_alpha()
                            self.image = pygame.transform.scale(self.image, (ENEMY_WIDTH, ENEMY_HEIGHT))
                            image_loaded = True
                            break
                        except (pygame.error, FileNotFoundError):
                            continue
                if image_loaded:
                    break
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

# Nepřátelé

# Projektil
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction_x):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 5 * direction_x # Směr

    def update(self):
        self.rect.x += self.speed
        # Smazání projektilu
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

# protestující
class Enemy1(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, ["protestor"], fallback_color=(200, 200, 200))

    def update(self, platforms, *args):
        self.apply_gravity(platforms)


# liberal
class Enemy2(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, ["muslim"], fallback_color=(100, 100, 100))
        self.velocity_x = 1

    def update(self, platforms, *args):
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

# doktor
class Enemy3(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, ["doktor"], fallback_color=(0, 0, 255))
        self.velocity_x = 1
        self.vision_range = 250 # Vzdálenost vize
        self.shoot_cooldown = 0
        self.shoot_delay = 60 # počet snímků u střely
        self.facing_right = True # pamatovák směru

    def update(self, platforms, player, projectiles_group, *args):
        # vzdálenost od hráče
        distance_x = player.rect.centerx - self.rect.centerx
        distance_y = abs(player.rect.centery - self.rect.centery)

        # Rozhodnutí mezi chůzí a střelbou
        if abs(distance_x) < self.vision_range and distance_y < 50:
            self.velocity_x = 0
            
            # Otočení k hráči
            direction_x = 1 if distance_x > 0 else -1

            # Střelba
            if self.shoot_cooldown <= 0:
                projectile = Projectile(self.rect.centerx, self.rect.centery, direction_x)
                projectiles_group.add(projectile)
                self.shoot_cooldown = self.shoot_delay
        else:
            if self.velocity_x == 0:
                self.velocity_x = 1 if self.facing_right else -1

            self.rect.x += self.velocity_x
            
            # Uložení směru chůze
            if self.velocity_x > 0: self.facing_right = True
            elif self.velocity_x < 0: self.facing_right = False


            if self.rect.left <= 0:
                self.rect.left = 0
                self.velocity_x *= -1
            elif self.rect.right >= SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
                self.velocity_x *= -1

            
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    if self.velocity_x > 0:
                        self.rect.right = platform.rect.left
                        self.velocity_x *= -1
                    elif self.velocity_x < 0:
                        self.rect.left = platform.rect.right
                        self.velocity_x *= -1

        # Cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        self.apply_gravity(platforms)

# boom race
class Enemy4(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, ["virus_yellow", "virus_red", "virus"], fallback_color=(255, 140, 0))
        self.speed = 3 
        self.vision_range = 300 # Vzdálenost spatření
        self.is_chasing = False # Defaultně není v režimu stíhání
        self.velocity_x = 0

    def update(self, platforms, player, projectiles_group, *args):
        # Vzdálenost od hráče
        distance_x = player.rect.centerx - self.rect.centerx
        distance_y = abs(player.rect.centery - self.rect.centery)

        if abs(distance_x) < self.vision_range and distance_y < 100:
            self.is_chasing = True

        
        if self.is_chasing:
            # Rozhodnutí, kterým směrem jít
            if distance_x > 5: 
                self.velocity_x = self.speed
            elif distance_x < -5: 
                self.velocity_x = -self.speed
            else:
                self.velocity_x = 0

            # Pohyb
            self.rect.x += self.velocity_x

    
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    if self.velocity_x > 0:
                        self.rect.right = platform.rect.left
                    elif self.velocity_x < 0:
                        self.rect.left = platform.rect.right

        # 4. ÚTOK A VYMAZÁNÍ (Zničení)
        if self.rect.colliderect(player.rect):
            print("BUM! Nepřítel explodoval a zranil hráče!")
            # zde pak ubírání životů
            
            # self.kill() odstraní tento objekt ze všech pygame.sprite.Group
            self.kill() 

        self.apply_gravity(platforms)