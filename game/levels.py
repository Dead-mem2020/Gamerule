import pygame
from config import *
from game.platform import Platform, MovingPlatform
from game.sprytes.enemy import Enemy1, Enemy2, Enemy3, Enemy4

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 120), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        # Neprůhledný vnitřek portálu
        pygame.draw.ellipse(self.image, (40, 0, 100), (0, 10, 50, 100))
        pygame.draw.ellipse(self.image, (80, 0, 180), (4, 16, 42, 88), 4)
        pygame.draw.ellipse(self.image, (140, 100, 255), (8, 24, 34, 76), 4)
        pygame.draw.circle(self.image, (200, 220, 255, 180), (25, 60), 10)
        pygame.draw.circle(self.image, (120, 0, 200), (25, 60), 4)

        # Světelný prstenec kolem pozadí portálu
        pygame.draw.ellipse(self.image, (120, 80, 255, 120), (-4, 6, 58, 108), 5)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 10

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Cloud:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.ellipse(screen, (255, 255, 255), (self.x, self.y, 80, 40))
        pygame.draw.ellipse(screen, (255, 255, 255), (self.x + 30, self.y - 15, 90, 45))
        pygame.draw.ellipse(screen, (255, 255, 255), (self.x + 60, self.y, 80, 40))

class Bush:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, (34, 139, 34), (self.x, self.y), 18)
        pygame.draw.circle(screen, (0, 100, 0), (self.x + 16, self.y + 5), 14)
        pygame.draw.circle(screen, (0, 128, 0), (self.x - 16, self.y + 5), 14)

class Flower:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), 3)
        pygame.draw.line(screen, (0, 120, 0), (self.x, self.y + 3), (self.x, self.y + 12), 2)
        for dx, dy, color in [(-4, -4, (255, 0, 0)), (4, -4, (255, 0, 0)), (-4, 4, (255, 192, 203)), (4, 4, (255, 192, 203))]:
            pygame.draw.circle(screen, color, (self.x + dx, self.y + dy), 3)

class Level:
    def __init__(self, level_num):
        self.level_num = level_num
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.decorations = []
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
            house_top = Platform(350, 320, 100, 20)
            self.platforms.add(house_top)
            self.all_sprites.add(house_top)
            # Background decorations for White House level
            self.decorations.append(Cloud(100, 80))
            self.decorations.append(Cloud(280, 60))
            self.decorations.append(Cloud(550, 100))
            self.decorations.append(Bush(180, SCREEN_HEIGHT - 40))
            self.decorations.append(Bush(720, SCREEN_HEIGHT - 40))
            self.decorations.append(Flower(140, SCREEN_HEIGHT - 50))
            self.decorations.append(Flower(760, SCREEN_HEIGHT - 50))
            # Moving platform before the goal
            moving_platform = MovingPlatform(520, 260, 120, 20, dx=2, min_x=500, max_x=700)
            self.platforms.add(moving_platform)
            self.all_sprites.add(moving_platform)
            # Enemies
            enemy3 = Enemy3(400, 360)
            self.enemies.add(enemy3)
            self.all_sprites.add(enemy3)
            enemy4 = Enemy4(500, 260)
            self.enemies.add(enemy4)
            self.all_sprites.add(enemy4)
            # Goal
            goal = Goal(750, 180)
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
        for deco in self.decorations:
            deco.draw(screen)
        for sprite in self.all_sprites:
            sprite.draw(screen)