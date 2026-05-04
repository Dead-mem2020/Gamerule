import pygame
from config import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont(None, 64)
        self.font_button = pygame.font.SysFont(None, 36)
        self.running = True

        self.title_text = self.font_title.render("American day", True, (255, 255, 255))

        self.play_rect = pygame.Rect(0, 0, 200, 60)
        self.skins_rect = pygame.Rect(0, 0, 200, 60)
        self.quit_rect = pygame.Rect(0, 0, 200, 60)

        screen_w, screen_h = self.screen.get_size()
        self.play_rect.center = (screen_w // 2, screen_h // 2 - 60)
        self.skins_rect.center = (screen_w // 2, screen_h // 2 + 0)
        self.quit_rect.center = (screen_w // 2, screen_h // 2 + 60)

        self.selected_skin = 0  # 0 nebo 1

    def run_skins(self):
        # jednoduché menu pro výběr skinů
        choosing = True
        while choosing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    # tlačítka pro 2 skiny a "Back"
                    if self.skin1_rect.collidepoint((mx, my)):
                        self.selected_skin = 0
                        choosing = False
                    if self.skin2_rect.collidepoint((mx, my)):
                        self.selected_skin = 1
                        choosing = False
                    if self.back_rect.collidepoint((mx, my)):
                        choosing = False

            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(SKY_BLUE)
            title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 80))
            self.screen.blit(self.title_text, title_rect)

            # dvě ukázky skinů
            w, h = 140, 140
            screen_w = self.screen.get_width()
            y = 200
            self.skin1_rect = pygame.Rect(screen_w//2 - 180, y, w, h)
            self.skin2_rect = pygame.Rect(screen_w//2 + 40, y, w, h)
            pygame.draw.rect(self.screen, (0,255,0) if self.selected_skin==0 else (100,200,100), self.skin1_rect)
            pygame.draw.rect(self.screen, (0,0,255) if self.selected_skin==1 else (100,100,200), self.skin2_rect)
            s1 = self.font_button.render("Skin 1", True, (0,0,0))
            s2 = self.font_button.render("Skin 2", True, (0,0,0))
            self.screen.blit(s1, s1.get_rect(center=self.skin1_rect.center))
            self.screen.blit(s2, s2.get_rect(center=self.skin2_rect.center))

            # Back button
            self.back_rect = pygame.Rect(self.screen.get_width()//2 - 100, y + h + 30, 200, 50)
            back_color = (170,170,170) if self.back_rect.collidepoint(mouse_pos) else (200,200,200)
            pygame.draw.rect(self.screen, back_color, self.back_rect)
            back_text = self.font_button.render("Back", True, (0,0,0))
            self.screen.blit(back_text, back_text.get_rect(center=self.back_rect.center))

            pygame.display.flip()
            self.clock.tick(FPS)

        return True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return (False, self.selected_skin)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.play_rect.collidepoint(event.pos):
                        return (True, self.selected_skin)
                    if self.skins_rect.collidepoint(event.pos):
                        ok = self.run_skins()
                        if not ok:
                            return (False, self.selected_skin)
                    if self.quit_rect.collidepoint(event.pos):
                        return (False, self.selected_skin)

            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(SKY_BLUE)

            # Title
            title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 100))
            self.screen.blit(self.title_text, title_rect)

            # Play button
            play_color = (170, 170, 170) if self.play_rect.collidepoint(mouse_pos) else (200, 200, 200)
            pygame.draw.rect(self.screen, play_color, self.play_rect)
            play_text = self.font_button.render("Play", True, (0, 0, 0))
            self.screen.blit(play_text, play_text.get_rect(center=self.play_rect.center))

            # Skins button
            skins_color = (170,170,170) if self.skins_rect.collidepoint(mouse_pos) else (200,200,200)
            pygame.draw.rect(self.screen, skins_color, self.skins_rect)
            skins_text = self.font_button.render("Skins", True, (0,0,0))
            self.screen.blit(skins_text, skins_text.get_rect(center=self.skins_rect.center))

            # Quit button
            quit_color = (170, 170, 170) if self.quit_rect.collidepoint(mouse_pos) else (200, 200, 200)
            pygame.draw.rect(self.screen, quit_color, self.quit_rect)
            quit_text = self.font_button.render("Quit", True, (0, 0, 0))
            self.screen.blit(quit_text, quit_text.get_rect(center=self.quit_rect.center))

            # small preview of selected skin
            preview_rect = pygame.Rect(self.screen.get_width()-120, 20, 100, 100)
            if self.selected_skin == 0:
                pygame.draw.rect(self.screen, (0,255,0), preview_rect)
            else:
                pygame.draw.rect(self.screen, (0,0,255), preview_rect)
            pygame.display.flip()
            self.clock.tick(FPS)

        return (False, self.selected_skin)