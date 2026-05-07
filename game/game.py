import pygame
from config import *
from game.sprytes.player import Player
from game.levels import Level

class Game:
    def __init__(self, screen, skin=0):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_level_num = 1
        self.max_levels = 3
        self.won = False
        
        self.all_sprites = pygame.sprite.Group()
        self.platform = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        self.viruses = pygame.sprite.Group()
        
        # Časovač pro spawnování virů (začne na náhodném čísle např. mezi 2 a 5 vteřinami)
        self.virus_spawn_timer = random.randint(4 * FPS, 10 * FPS)
        
        floor = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        self.platform.add(floor)
        self.all_sprites.add(floor)

        # předat vybraný skin do Player
        self.player = Player(100, 100, skin)
        self.load_level(self.current_level_num)

    def load_level(self, level_num):
        self.level = Level(level_num)
        # Add player to level sprites
        self.level.all_sprites.add(self.player)
        # Reset player position
        self.player.rect.x = 100
        self.player.rect.y = 100
        self.player.vx = 0
        self.player.vy = 0
        self.player.on_ground = False 

# eventy
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                evt_name = pygame.key.name(event.key)
                print(f"{evt_name}: {event.key}")

            elif event.type == pygame.MOUSEMOTION:
                print(f"{evt_name}: {event.pos}")

            # SPOJENÁ KONTROLA KLIKNUTÍ:
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(f"{evt_name}: {event.button} at {event.pos}")
                if event.button == 1:  # Lmb
                    for virus in self.viruses:
                        # Uložíme si, co nám virus po kliknutí odpověděl
                        result = virus.handle_click(event.pos)
                        if result == "game_over":
                            print("Vypustil jsi virus! Game over!")
                            self.running = False

            elif event.type == pygame.MOUSEBUTTONUP:
                print(f"{evt_name}: {event.button} at {event.pos}")
    
# updatování
    def update(self):
        self.level.platforms.update()
        game_over = self.player.update(self.level.platforms, self.level.enemies)
        if game_over:
            self.running = False
            return

        # Check for goal collision
        if pygame.sprite.spritecollideany(self.player, self.level.goals):
            self.current_level_num += 1
            if self.current_level_num > self.max_levels:
                self.won = True
                self.running = False
                return
            self.load_level(self.current_level_num)

        hits = pygame.sprite.spritecollide(self.player, self.projectiles, True)
        if hits:
            if self.player.take_damage():
                self.running = False

        for enemy in self.enemies:
            enemy.update(self.platform, self.player, self.projectiles)

        self.viruses.update(self.player)


        # Časovač pro vytvoření nového viru
        self.virus_spawn_timer -= 1
        if self.virus_spawn_timer <= 0:
            new_virus = Virus()
            self.viruses.add(new_virus)
            self.all_sprites.add(new_virus)
            self.virus_spawn_timer = random.randint(3 * FPS, 10 * FPS)

        self.level.projectiles.update()

        for enemy in self.level.enemies:
            enemy.update(self.level.platforms, self.player, self.level.projectiles)

    def draw(self):
        self.level.draw(self.screen)

        self.level.projectiles.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)