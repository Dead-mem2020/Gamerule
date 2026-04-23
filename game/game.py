from os import name
import pygame
from config import *
from game.player import Player
from game.platform import Platform
from game.enemy import Enemy
import random

print(ENEMY_WIDTH)

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.all_sprites = pygame.sprite.Group()
        self.platform = pygame.sprite.Group()
        
        ### NOVÉ: Skupina pro nepřátele ###
        self.enemies = pygame.sprite.Group()
        
        ### NOVÉ: Vytvoření testovací plošiny (podlahy) ###
        # Předpokládám, že Platform bere parametry (x, y, šířka, výška)
        # Uprav si podle toho, jak máš definovaný init ve své třídě Platform
        floor = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        self.platform.add(floor)
        self.all_sprites.add(floor)

        self.player = Player(100, 100)
        self.all_sprites.add(self.player)

        ### NOVÉ: Vygenerování nepřátel po vytvoření plošin ###
        self.spawn_enemies(3) # Číslo udává počet nepřátel

    ### NOVÉ: Metoda pro náhodné generování nepřátel ###
    def spawn_enemies(self, count):
        # Převedeme skupinu plošin na seznam, aby z něj šlo náhodně vybírat
        platforms_list = self.platform.sprites()
        
        # Pojistka: pokud nejsou žádné plošiny, nepřátele negenerujeme
        if not platforms_list:
            print("Nejsou vytvořeny žádné plošiny pro nepřátele!")
            return

        for _ in range(count):
            random_plat = random.choice(platforms_list)
            
            # Vygenerujeme X pozici. Musíme si dát pozor, aby plošina nebyla 
            # užší než nepřítel (jinak by random.randint vyhodil chybu).
            max_x = max(random_plat.rect.left, random_plat.rect.right - ENEMY_WIDTH)
            spawn_x = random.randint(random_plat.rect.left, max_x)
            
            spawn_y = random_plat.rect.top - ENEMY_HEIGHT
            
            new_enemy = Enemy(spawn_x, spawn_y)
            self.enemies.add(new_enemy)
            self.all_sprites.add(new_enemy) # Přidáme je i sem, aby se automaticky vykreslili

    def handle_events(self):
        for event in pygame.event.get():
            evt_name = pygame.event.event_name(event.type)

            if event.type == pygame.QUIT:
                self.running = False

            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                evt_name = pygame.key.name(event.key)
                print(f"{evt_name}: {event.key}")

            elif event.type == pygame.MOUSEMOTION:
                print(f"{evt_name}: {event.pos}")

            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                print(f"{evt_name}: {event.button} at {event.pos}")
    
                
    def update(self):
        game_over = self.player.update(self.platform, self.enemies)
        if game_over:
            self.running = False

        ### NOVÉ: Aktualizace nepřátel ###
        # Jelikož tvůj Enemy.update() bere jako argument plošiny (stejně jako Player),
        # musíme je updatovat manuálně v cyklu.
        for enemy in self.enemies:
            enemy.update(self.platform)


    def draw(self):
        self.screen.fill(SKY_BLUE)
        
        for sprite in self.all_sprites:
            sprite.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)