import pygame
from config import *
from game.sprytes.player import Player
from game.platform import Platform
from game.sprytes.enemy import Enemy1, Enemy2
import random

class Game:
    def __init__(self, screen, skin=0):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.all_sprites = pygame.sprite.Group()
        self.platform = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        floor = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        self.platform.add(floor)
        self.all_sprites.add(floor)

        # předat vybraný skin do Player
        self.player = Player(100, 100, skin)
        self.all_sprites.add(self.player)

        self.spawn_enemies(3) 

   
    def spawn_enemies(self, count):
       
        platforms_list = self.platform.sprites()
        
        
        if not platforms_list:
            print("Nejsou vytvořeny žádné plošiny pro nepřátele!")
            return

# spawnování nepřítele
        for _ in range(count):
            random_plat = random.choice(platforms_list)
            max_x = max(random_plat.rect.left, random_plat.rect.right - ENEMY_WIDTH)
            spawn_x = random.randint(random_plat.rect.left, max_x)
            spawn_y = random_plat.rect.top - ENEMY_HEIGHT

            if random.choice([True, False]):
                new_enemy = Enemy1(spawn_x, spawn_y)
            else:
                new_enemy = Enemy2(spawn_x, spawn_y)

            self.enemies.add(new_enemy)
            self.all_sprites.add(new_enemy)

# eventy
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
# updatování
    def update(self):
        game_over = self.player.update(self.platform, self.enemies)
        if game_over:
            self.running = False

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