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
    
# updatování
    def update(self):
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