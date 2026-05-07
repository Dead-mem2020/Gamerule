import os
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

        assets_dir = os.path.join(os.path.dirname(__file__), "textures", "player")
        self.skin_images = {}
        skin_files = {0: "Trump.png", 1: "Musk.png"}
        for idx, filename in skin_files.items():
            try:
                img = pygame.image.load(os.path.join(assets_dir, filename)).convert_alpha()
                self.skin_images[idx] = pygame.transform.scale(img, (100, 100))
            except Exception as e:
                print(f"Chyba načtení skinu menu: {filename} -> {e}")
                surf = pygame.Surface((100, 100))
                surf.fill((0, 255, 0) if idx == 0 else (0, 0, 255))
                self.skin_images[idx] = surf

        self.play_rect = pygame.Rect(0, 0, 260, 60)
        self.skins_rect = pygame.Rect(0, 0, 260, 60)
        self.settings_rect = pygame.Rect(0, 0, 260, 60)
        self.quit_rect = pygame.Rect(0, 0, 260, 60)

        screen_w, screen_h = self.screen.get_size()
        self.play_rect.center = (screen_w // 2, screen_h // 2 - 120)
        self.skins_rect.center = (screen_w // 2, screen_h // 2 - 40)
        self.settings_rect.center = (screen_w // 2, screen_h // 2 + 40)
        self.quit_rect.center = (screen_w // 2, screen_h // 2 + 120)

        self.selected_skin = 0  # 0 nebo 1
        self.volume = 70
        self.interface_index = 0
        self.interface_options = ["Classic", "Dark"]
        self.controls_info = [
            "W / ↑   - Jump",
            "A / ←   - Move left",
            "D / →   - Move right",
            "SPACE   - Jump",
            "ESC     - Quit",
            "",
            "Dev: Your Name Here"
        ]
        self.vol_minus_rect = pygame.Rect(0, 0, 0, 0)
        self.vol_plus_rect = pygame.Rect(0, 0, 0, 0)
        self.theme_rect = pygame.Rect(0, 0, 0, 0)
        self.keyboard_rect = pygame.Rect(0, 0, 0, 0)
        self.back_rect = pygame.Rect(0, 0, 0, 0)

    def draw_button(self, rect, text, hover=False, color=(220, 220, 255), text_color=(10, 10, 10)):
        shadow_rect = pygame.Rect(rect.x + 4, rect.y + 4, rect.width, rect.height)
        pygame.draw.rect(self.screen, (20, 20, 30), shadow_rect, border_radius=18)
        bg_color = (245, 245, 255) if hover else color
        pygame.draw.rect(self.screen, bg_color, rect, border_radius=18)
        pygame.draw.rect(self.screen, (50, 50, 80), rect, 2, border_radius=18)
        txt = self.font_button.render(text, True, text_color)
        self.screen.blit(txt, txt.get_rect(center=rect.center))

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
            self.screen.blit(self.skin_images[0], self.skin1_rect)
            self.screen.blit(self.skin_images[1], self.skin2_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), self.skin1_rect, 4 if self.selected_skin == 0 else 2, border_radius=18)
            pygame.draw.rect(self.screen, (255, 255, 255), self.skin2_rect, 4 if self.selected_skin == 1 else 2, border_radius=18)
            s1 = self.font_button.render("Trump", True, (0,0,0))
            s2 = self.font_button.render("Musk", True, (0,0,0))
            self.screen.blit(s1, s1.get_rect(midbottom=(self.skin1_rect.centerx, self.skin1_rect.bottom + 20)))
            self.screen.blit(s2, s2.get_rect(midbottom=(self.skin2_rect.centerx, self.skin2_rect.bottom + 20)))

            self.back_rect = pygame.Rect(self.screen.get_width()//2 - 100, y + h + 30, 200, 50)
            self.draw_button(self.back_rect, "Back", self.back_rect.collidepoint(mouse_pos), color=(210, 210, 230))

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
                    if self.settings_rect.collidepoint(event.pos):
                        ok = self.run_settings()
                        if not ok:
                            return (False, self.selected_skin)
                    if self.quit_rect.collidepoint(event.pos):
                        return (False, self.selected_skin)

            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(SKY_BLUE)

            # Title
            title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 100))
            self.screen.blit(self.title_text, title_rect)

            self.draw_button(self.play_rect, "Play", self.play_rect.collidepoint(mouse_pos))
            self.draw_button(self.skins_rect, "Skins", self.skins_rect.collidepoint(mouse_pos))
            self.draw_button(self.settings_rect, "Settings", self.settings_rect.collidepoint(mouse_pos))
            self.draw_button(self.quit_rect, "Quit", self.quit_rect.collidepoint(mouse_pos))

            # small preview of selected skin
            preview_rect = pygame.Rect(self.screen.get_width()-120, 20, 100, 100)
            self.screen.blit(self.skin_images[self.selected_skin], preview_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), preview_rect, 2)
            pygame.display.flip()
            self.clock.tick(FPS)

        return (False, self.selected_skin)

    def run_settings(self):
        choosing = True
        while choosing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    if self.vol_minus_rect.collidepoint((mx, my)):
                        self.volume = max(0, self.volume - 10)
                    if self.vol_plus_rect.collidepoint((mx, my)):
                        self.volume = min(100, self.volume + 10)
                    if self.theme_rect.collidepoint((mx, my)):
                        self.interface_index = (self.interface_index + 1) % len(self.interface_options)
                    if self.keyboard_rect.collidepoint((mx, my)):
                        self.run_dev_keyboard()
                    if self.back_rect.collidepoint((mx, my)):
                        choosing = False

            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill((30, 35, 50))
            title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 70))
            self.screen.blit(self.title_text, title_rect)

            settings_title = self.font_button.render("Settings", True, (255, 255, 255))
            self.screen.blit(settings_title, settings_title.get_rect(center=(self.screen.get_width() // 2, 140)))

            center_x = self.screen.get_width() // 2
            base_y = 210
            label = self.font_button.render(f"Volume: {self.volume}%", True, (255, 255, 255))
            self.screen.blit(label, label.get_rect(center=(center_x, base_y)))
            self.vol_minus_rect = pygame.Rect(center_x - 120, base_y + 40, 80, 40)
            self.vol_plus_rect = pygame.Rect(center_x + 40, base_y + 40, 80, 40)
            self.draw_button(self.vol_minus_rect, "-", self.vol_minus_rect.collidepoint(mouse_pos), color=(220,220,220))
            self.draw_button(self.vol_plus_rect, "+", self.vol_plus_rect.collidepoint(mouse_pos), color=(220,220,220))

            theme_label = self.font_button.render(f"Interface: {self.interface_options[self.interface_index]}", True, (255, 255, 255))
            self.screen.blit(theme_label, theme_label.get_rect(center=(center_x, base_y + 120)))
            self.theme_rect = pygame.Rect(center_x - 120, base_y + 150, 240, 50)
            self.draw_button(self.theme_rect, "Change theme", self.theme_rect.collidepoint(mouse_pos), color=(200,200,240))

            self.keyboard_rect = pygame.Rect(center_x - 120, base_y + 220, 240, 50)
            self.draw_button(self.keyboard_rect, "Dev keyboard", self.keyboard_rect.collidepoint(mouse_pos), color=(200,200,240))

            self.back_rect = pygame.Rect(center_x - 100, base_y + 300, 200, 50)
            self.draw_button(self.back_rect, "Back", self.back_rect.collidepoint(mouse_pos), color=(210,210,230))

            pygame.display.flip()
            self.clock.tick(FPS)

        return True

    def run_dev_keyboard(self):
        viewing = True
        while viewing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    viewing = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_rect.collidepoint(event.pos):
                        viewing = False

            self.screen.fill((20, 25, 40))
            title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 70))
            self.screen.blit(self.title_text, title_rect)
            header = self.font_button.render("Dev keyboard / Controls", True, (255, 255, 255))
            self.screen.blit(header, header.get_rect(center=(self.screen.get_width() // 2, 130)))

            y = 190
            for line in self.controls_info:
                text = self.font_button.render(line, True, (230, 230, 230))
                self.screen.blit(text, text.get_rect(center=(self.screen.get_width() // 2, y)))
                y += 40

            self.back_rect = pygame.Rect(self.screen.get_width()//2 - 100, y + 20, 200, 50)
            self.draw_button(self.back_rect, "Back", self.back_rect.collidepoint(pygame.mouse.get_pos()), color=(210,210,230))

            pygame.display.flip()
            self.clock.tick(FPS)

        return True
