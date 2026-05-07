import pygame
import pygame.font
import os
from config import *
import random


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
        self.is_deadly = True

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
        self.is_deadly = True
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
            
            # Zraňování hráčů
            player.take_damage()
            
            # self.kill() odstraní tento objekt ze všech pygame.sprite.Group
            self.kill() 

        self.apply_gravity(platforms)


# virus
class Virus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # --- 1. VELIKOST 40% OBRAZOVKY ---
        self.v_width = int(SCREEN_WIDTH * 0.4)
        self.v_height = int(SCREEN_HEIGHT * 0.4)
        
        # Příprava fontu pro tlačítka
        pygame.font.init()
        self.font = pygame.font.SysFont('arial', 28, bold=True)
        if self.font is None:
            self.font = pygame.font.Font(None, 28)

        # Načítání POUZE ŽLUTÉHO viru
        def load_virus_img(filename, fallback_color):
            try:
                path = os.path.join("textures", "enemies", "virus", filename)
                if not os.path.exists(path):
                    path = os.path.join("game", "textures", "enemies", "virus", filename)
                
                img = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(img, (self.v_width, self.v_height))
            except Exception:
                surf = pygame.Surface((self.v_width, self.v_height))
                surf.fill(fallback_color)
                return surf

        # Tady už se načítá čistě jen žlutý obrázek
        self.image_active = load_virus_img("virus_yellow.png", (200, 200, 0))
        self.image_destroyed = load_virus_img("virus_solved.png", (100, 100, 100))
        self.image = self.image_active
        
        # --- 2. POZICE VIRU A TLAČÍTEK ---
        spawn_x = random.randint(0, SCREEN_WIDTH - self.v_width)
        spawn_y = random.randint(0, SCREEN_HEIGHT - self.v_height)
        self.rect = self.image.get_rect(topleft=(spawn_x, spawn_y))

        btn_width = (self.v_width // 2) - 20
        btn_height = 40
        
        self.btn_solve_rect = pygame.Rect(self.rect.left + 10, self.rect.bottom - btn_height - 10, btn_width, btn_height)
        self.btn_release_rect = pygame.Rect(self.rect.right - btn_width - 10, self.rect.bottom - btn_height - 10, btn_width, btn_height)

        self.state = "active"
        self.death_timer = 15 # Jak dlouho zůstane šedý po odkliknutí

    def update(self, player, *args):
        # ŽÁDNÝ ČASOVÝ LIMIT! Virus tu bude strašit tak dlouho, dokud ho neodklikneš.
        if self.state == "destroyed":
            self.death_timer -= 1
            if self.death_timer <= 0:
                self.kill()

    def handle_click(self, mouse_pos):
        if self.state == "active":
            if self.btn_solve_rect.collidepoint(mouse_pos):
                self.state = "destroyed"
                self.image = self.image_destroyed
                return "solved"
            elif self.btn_release_rect.collidepoint(mouse_pos):
                return "game_over" # Past!
        return None

    def draw(self, screen):
        # 1. Vykreslí hlavní obrázek viru
        screen.blit(self.image, self.rect)
        
        if self.state == "active":
            # 2. Vykreslí obdélníky pro tlačítka (Zelený a Temně červený)
            pygame.draw.rect(screen, (0, 200, 0), self.btn_solve_rect)
            pygame.draw.rect(screen, (50, 0, 0), self.btn_release_rect)
            
            # 3. Vygeneruje a vycentruje bílý text do tlačítek
            text_s = self.font.render("ODSTRANIT", True, (255, 255, 255))
            text_r = self.font.render("VYPUSTIT", True, (255, 255, 255))
            
            screen.blit(text_s, text_s.get_rect(center=self.btn_solve_rect.center))
            screen.blit(text_r, text_r.get_rect(center=self.btn_release_rect.center))