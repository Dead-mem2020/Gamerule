import pygame
import os
from config import *
import random



class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_name, fallback_color=ENEMY_COLOUR):
        super().__init__()

        image_loaded = False
        image_dirs = ["img", os.path.join("game", "textures", "enemies")]

        for name in image_name:
            for image_dir in image_dirs:
                for ext in ["png", "jpg"]:
                    try:
                        image_path = os.path.join(image_dir, f"{name}.{ext}")
                        self.image = pygame.image.load(image_path).convert_alpha()
                        self.image = pygame.transform.scale(self.image, (ENEMY_WIDTH, ENEMY_HEIGHT))
                        print(f"Načten obrázek nepřítele: {image_path}")
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
        super().__init__(x, y, ["enemy1"], fallback_color=(200, 200, 200))

    def update(self, platforms, *args):
        self.apply_gravity(platforms)


# liberal
class Enemy2(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, ["enemy2"], fallback_color=(100, 100, 100))
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
        super().__init__(x, y, ["shooter", "enemy3"], fallback_color=(0, 0, 255)) 
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
        super().__init__(x, y, ["chaser", "enemy4"], fallback_color=(255, 140, 0))
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
        self.is_timed = random.choice([True, False])
        
        # --- 1. VELIKOST 40% OBRAZOVKY ---
        self.v_width = int(SCREEN_WIDTH * 0.4)
        self.v_height = int(SCREEN_HEIGHT * 0.4)
        
        # Pomocná funkce pro bezpečné načtení obrázku s fallbackem
        def load_virus_img(filename, fallback_color):
            try:
                # Zkusí najít soubor ve složce img nebo texturách
                path = os.path.join("img", filename)
                if not os.path.exists(path):
                    path = os.path.join("game", "textures", "enemies", filename)
                
                img = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(img, (self.v_width, self.v_height))
            except Exception:
                surf = pygame.Surface((self.v_width, self.v_height))
                surf.fill(fallback_color)
                return surf

        # --- 2. NAČTENÍ TEXTUR ---
        if self.is_timed:
            self.image_active = load_virus_img("textures/enemies/virus/virus_red.png", (255, 0, 0))
        else:
            self.image_active = load_virus_img("virus_yellow.png", (255, 255, 0))
            
        self.image_destroyed = load_virus_img("virus_solved.png", (100, 100, 100))

        self.image = self.image_active
        
        # --- 3. POZICE A TLAČÍTKA ---
        spawn_x = random.randint(0, SCREEN_WIDTH - self.v_width)
        spawn_y = random.randint(0, SCREEN_HEIGHT - self.v_height)
        self.rect = self.image.get_rect(topleft=(spawn_x, spawn_y))

        # Výpočet velikosti tlačítek (budou dole uvnitř viru)
        btn_width = (self.v_width // 2) - 20
        btn_height = 40
        
        # Zelené tlačítko ODSTRANIT (Vlevo dole)
        self.btn_solve_rect = pygame.Rect(self.rect.left + 10, self.rect.bottom - btn_height - 10, btn_width, btn_height)
        # Černé tlačítko VYPUSTIT (Vpravo dole)
        self.btn_release_rect = pygame.Rect(self.rect.right - btn_width - 10, self.rect.bottom - btn_height - 10, btn_width, btn_height)

        self.state = "active"
        self.death_timer = 30 # Doba zobrazení "Solved" obrázku (půl vteřiny)
        self.time_limit = 3 * FPS if self.is_timed else 0

    def update(self, player, *args):
        if self.state == "active":
            if self.is_timed:
                self.time_limit -= 1
                if self.time_limit <= 0:
                    print("Čas vypršel! Virus tě zranil.")
                    player.take_damage() 
                    self.kill() 
                    
        elif self.state == "destroyed":
            self.death_timer -= 1
            if self.death_timer <= 0:
                self.kill()

    def handle_click(self, mouse_pos):
        if self.state == "active":
            # Hráč klikl na tlačítko ODSTRANIT
            if self.btn_solve_rect.collidepoint(mouse_pos):
                self.state = "destroyed"
                self.image = self.image_destroyed
                print("Virus úspěšně zničen!")
                return "solved"
            
            # Hráč klikl na tlačítko VYPUSTIT (Past!)
            elif self.btn_release_rect.collidepoint(mouse_pos):
                return "game_over"
                
        return None

    def draw(self, screen):
        # 1. Vykreslí hlavní obrázek viru
        screen.blit(self.image, self.rect)
        
        # 2. Vykreslí tlačítka navrch (pouze pokud je virus aktivní)
        if self.state == "active":
            # Tlačítko ODSTRANIT (Zelené)
            pygame.draw.rect(screen, (0, 200, 0), self.btn_solve_rect)
            # Tlačítko VYPUSTIT (Černé/Temně červené)
            pygame.draw.rect(screen, (50, 0, 0), self.btn_release_rect)