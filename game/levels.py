import pygame
from config import *
from game.platform import Platform
from game.sprytes.enemy import Enemy1, Enemy2, Enemy3, Enemy4

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill((255, 215, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Level:
    def __init__(self, level_num):
        self.level_num = level_num
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.background_color = SKY_BLUE
        self.setup_level()

    def setup_level(self):
        if self.level_num == 1:
            # Streets of D.C.
            self.background_color = (135, 206, 235)  # Light blue
            # Floor
            floor = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
            self.platforms.add(floor)
            self.all_sprites.add(floor)
            # Buildings/platforms
            plat1 = Platform(200, 400, 100, 20)
            self.platforms.add(plat1)
            self.all_sprites.add(plat1)
            plat2 = Platform(400, 300, 100, 20)
            self.platforms.add(plat2)
            self.all_sprites.add(plat2)
            plat3 = Platform(600, 200, 100, 20)
            self.platforms.add(plat3)
            self.all_sprites.add(plat3)
            # Enemies
            enemy1 = Enemy1(250, 360)
            self.enemies.add(enemy1)
            self.all_sprites.add(enemy1)
            enemy2 = Enemy2(450, 260)
            self.enemies.add(enemy2)
            self.all_sprites.add(enemy2)
            # Goal
            goal = Goal(750, 100)
            self.goals.add(goal)
            self.all_sprites.add(goal)

        elif self.level_num == 2:
            # White House
            self.background_color = (255, 255, 255)  # White
            # Floor
            floor = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
            self.platforms.add(floor)
            self.all_sprites.add(floor)
            # White House structure
            house_base = Platform(300, 400, 200, 20)
            self.platforms.add(house_base)
            self.all_sprites.add(house_base)
            house_top = Platform(350, 300, 100, 20)
            self.platforms.add(house_top)
            self.all_sprites.add(house_top)
            # Extra jumping platforms for level progression
            mid_platform = Platform(520, 320, 120, 20)
            self.platforms.add(mid_platform)
            self.all_sprites.add(mid_platform)
            upper_platform = Platform(650, 240, 100, 20)
            self.platforms.add(upper_platform)
            self.all_sprites.add(upper_platform)
            # Enemies
            enemy3 = Enemy3(400, 360)
            self.enemies.add(enemy3)
            self.all_sprites.add(enemy3)
            enemy4 = Enemy4(500, 260)
            self.enemies.add(enemy4)
            self.all_sprites.add(enemy4)
            # Goal
            goal = Goal(750, 200)
            self.goals.add(goal)
            self.all_sprites.add(goal)

        elif self.level_num == 3:
            # Monuments
            self.background_color = (178, 34, 52)  # Red for monuments
            # Floor
            floor = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
            self.platforms.add(floor)
            self.all_sprites.add(floor)
            # Monument pillars
            pillar1 = Platform(150, 350, 50, 150)
            self.platforms.add(pillar1)
            self.all_sprites.add(pillar1)
            pillar2 = Platform(350, 250, 50, 250)
            self.platforms.add(pillar2)
            self.all_sprites.add(pillar2)
            pillar3 = Platform(550, 200, 50, 300)
            self.platforms.add(pillar3)
            self.all_sprites.add(pillar3)
            # Enemies
            enemy1 = Enemy1(200, 310)
            self.enemies.add(enemy1)
            self.all_sprites.add(enemy1)
            enemy2 = Enemy2(400, 210)
            self.enemies.add(enemy2)
            self.all_sprites.add(enemy2)
            enemy3 = Enemy3(600, 160)
            self.enemies.add(enemy3)
            self.all_sprites.add(enemy3)
            # Goal
            goal = Goal(750, 100)
            self.goals.add(goal)
            self.all_sprites.add(goal)

        elif self.level_num == 4:
        # Future levels can be added here
            pass

    def draw(self, screen):
        screen.fill(self.background_color)
        for sprite in self.all_sprites:
            sprite.draw(screen)