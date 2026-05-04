import os
import pygame
from config import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont(None, 64)
        self.font_button = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 20)
        self.running = True

        self.title_text = self.font_title.render("American day", True, (255, 255, 255))

        self.play_rect = pygame.Rect(0, 0, 220, 64)
        self.skins_rect = pygame.Rect(0, 0, 220, 64)
        self.settings_rect = pygame.Rect(0, 0, 220, 64)
        self.quit_rect = pygame.Rect(0, 0, 220, 64)

        screen_w, screen_h = self.screen.get_size()
        self.play_rect.center = (screen_w // 2, screen_h // 2 - 90)
        self.skins_rect.center = (screen_w // 2, screen_h // 2 - 20)
        self.settings_rect.center = (screen_w // 2, screen_h // 2 + 50)
        self.quit_rect.center = (screen_w // 2, screen_h // 2 + 120)

        self.selected_skin = 0  # 0 = Trump, 1 = Elon

        # prepare skin images (game/textures/assets/Trump.png, Musk.png)
        assets_dir = os.path.join(os.path.dirname(__file__), "textures", "assets")
        self._skin_files = {0: "Trump.png", 1: "Musk.png"}
        self.skin_images = {}
        for idx, fname in self._skin_files.items():
            path = os.path.join(assets_dir, fname)
            try:
                img = pygame.image.load(path).convert_alpha()
                self.skin_images[idx] = pygame.transform.scale(img, (140, 140))
            except Exception:
                self.skin_images[idx] = None

        # colors
        self.bg_color = SKY_BLUE
        self.btn_base = (40, 40, 60)
        self.btn_accent = (255, 165, 0)   # orange accent
        self.btn_hover = (70, 130, 180)   # steelblue hover

        # settings state
        self.volume = 0.5  # 0.0 - 1.0
        self.show_dev_keys = False
        self._slider_drag = False

    def _draw_button(self, rect, text, mouse_pos, accent=False):
        # shadow
        shadow_rect = rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(self.screen, (0,0,0,120), shadow_rect, border_radius=10)
        # main color
        is_hover = rect.collidepoint(mouse_pos)
        color = self.btn_hover if is_hover else (self.btn_accent if accent else self.btn_base)
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        # inner highlight
        inner = rect.inflate(-6, -8)
        pygame.draw.rect(self.screen, (255,255,255,20), inner, border_radius=8)
        # text (black for better visibility)
        txt = self.font_button.render(text, True, (0,0,0))
        self.screen.blit(txt, txt.get_rect(center=rect.center))

    def run_skins(self):
        choosing = True
        while choosing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    if self.skin1_rect.collidepoint((mx, my)):
                        self.selected_skin = 0
                        choosing = False
                    if self.skin2_rect.collidepoint((mx, my)):
                        self.selected_skin = 1
                        choosing = False
                    if self.back_rect.collidepoint((mx, my)):
                        choosing = False

            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(self.bg_color)
            title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 80))
            self.screen.blit(self.title_text, title_rect)

            # skins preview
            w, h = 160, 160
            screen_w = self.screen.get_width()
            y = 180
            self.skin1_rect = pygame.Rect(screen_w//2 - 200, y, w, h)
            self.skin2_rect = pygame.Rect(screen_w//2 + 40, y, w, h)

            # draw skin1
            if self.skin_images.get(0):
                self.screen.blit(self.skin_images[0], self.skin1_rect.topleft)
            else:
                pygame.draw.rect(self.screen, (200,50,50), self.skin1_rect, border_radius=8)
            # draw skin2
            if self.skin_images.get(1):
                self.screen.blit(self.skin_images[1], self.skin2_rect.topleft)
            else:
                pygame.draw.rect(self.screen, (50,100,200), self.skin2_rect, border_radius=8)

            s1 = self.font_button.render("Trump", True, (0,0,0))
            s2 = self.font_button.render("Elon", True, (0,0,0))
            self.screen.blit(s1, s1.get_rect(center=(self.skin1_rect.centerx, self.skin1_rect.bottom + 20)))
            self.screen.blit(s2, s2.get_rect(center=(self.skin2_rect.centerx, self.skin2_rect.bottom + 20)))

            # Back button
            self.back_rect = pygame.Rect(self.screen.get_width()//2 - 90, y + h + 50, 180, 48)
            self._draw_button(self.back_rect, "Back", mouse_pos, accent=True)

            pygame.display.flip()
            self.clock.tick(FPS)
        return True

    def run_settings(self):
        in_settings = True
        while in_settings:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    # Back button
                    if self.back_rect.collidepoint((mx, my)):
                        in_settings = False
                    # click slider
                    if self.slider_rect.collidepoint((mx, my)):
                        self._slider_drag = True
                        rel = (mx - self.slider_rect.left) / max(1, self.slider_rect.width)
                        self.volume = max(0.0, min(1.0, rel))
                    # toggle dev keys
                    if self.toggle_rect.collidepoint((mx, my)):
                        self.show_dev_keys = not self.show_dev_keys
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self._slider_drag = False
                if event.type == pygame.MOUSEMOTION and self._slider_drag:
                    mx, my = event.pos
                    rel = (mx - self.slider_rect.left) / max(1, self.slider_rect.width)
                    self.volume = max(0.0, min(1.0, rel))

            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(self.bg_color)
            self.screen.blit(self.title_text, self.title_text.get_rect(center=(self.screen.get_width() // 2, 80)))

            # Volume UI
            vol_label = self.font_button.render("Volume", True, (0,0,0))
            self.screen.blit(vol_label, (self.screen.get_width()//2 - 200, 160))

            self.slider_rect = pygame.Rect(self.screen.get_width()//2 - 100, 200, 300, 18)
            pygame.draw.rect(self.screen, (200,200,200), self.slider_rect, border_radius=9)
            filled = pygame.Rect(self.slider_rect.left, self.slider_rect.top, int(self.volume * self.slider_rect.width), self.slider_rect.height)
            pygame.draw.rect(self.screen, (100,180,100), filled, border_radius=9)
            # knob
            knob_x = self.slider_rect.left + int(self.volume * self.slider_rect.width)
            knob_rect = pygame.Rect(0,0,16,28)
            knob_rect.center = (knob_x, self.slider_rect.centery)
            pygame.draw.rect(self.screen, (60,60,60), knob_rect, border_radius=6)
            vol_percent = self.font_small.render(f"{int(self.volume*100)}%", True, (0,0,0))
            self.screen.blit(vol_percent, (self.slider_rect.right + 10, self.slider_rect.top - 2))

            # Dev keyboard toggle
            toggle_label = self.font_button.render("Dev keyboard (show controls)", True, (0,0,0))
            self.screen.blit(toggle_label, (self.screen.get_width()//2 - 200, 260))
            self.toggle_rect = pygame.Rect(self.screen.get_width()//2 + 120, 258, 48, 28)
            pygame.draw.rect(self.screen, (180,180,180), self.toggle_rect, border_radius=6)
            if self.show_dev_keys:
                inner = self.toggle_rect.inflate(-6, -6)
                pygame.draw.rect(self.screen, (100,200,100), inner, border_radius=4)
            else:
                inner = self.toggle_rect.inflate(-6, -6)
                pygame.draw.rect(self.screen, (220,220,220), inner, border_radius=4)

            # small instructions for volume
            hint = self.font_small.render("Drag slider or click to change volume", True, (0,0,0))
            self.screen.blit(hint, (self.screen.get_width()//2 - 200, 230))

            # Back button
            self.back_rect = pygame.Rect(self.screen.get_width()//2 - 90, 340, 180, 48)
            self._draw_button(self.back_rect, "Back", mouse_pos, accent=True)

            # If dev keys enabled, render a small controls layout
            if self.show_dev_keys:
                box = pygame.Rect(self.screen.get_width()//2 - 220, 410, 440, 140)
                pygame.draw.rect(self.screen, (245,245,245), box, border_radius=8)
                pygame.draw.rect(self.screen, (200,200,200), box, 2, border_radius=8)
                # controls content
                keys = [
                    ("A / Left", "Move left"),
                    ("D / Right", "Move right"),
                    ("W / Up / Space", "Jump"),
                    ("Esc", "Pause / Quit menu")
                ]
                y = box.top + 8
                for key, desc in keys:
                    key_rect = pygame.Rect(box.left + 12, y, 120, 32)
                    pygame.draw.rect(self.screen, (220,220,220), key_rect, border_radius=6)
                    ktxt = self.font_small.render(key, True, (0,0,0))
                    self.screen.blit(ktxt, ktxt.get_rect(center=key_rect.center))
                    desc_txt = self.font_small.render(desc, True, (0,0,0))
                    self.screen.blit(desc_txt, (key_rect.right + 12, key_rect.top + 8))
                    y += 36

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
            self.screen.fill(self.bg_color)

            # Title
            title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 100))
            self.screen.blit(self.title_text, title_rect)

            # Draw buttons with nicer colors
            self._draw_button(self.play_rect, "Play", mouse_pos, accent=True)
            self._draw_button(self.skins_rect, "Skins", mouse_pos)
            self._draw_button(self.settings_rect, "Settings", mouse_pos)
            self._draw_button(self.quit_rect, "Quit", mouse_pos)

            # small preview of selected skin
            preview_rect = pygame.Rect(self.screen.get_width()-120, 20, 100, 100)
            preview_img = self.skin_images.get(self.selected_skin)
            if preview_img:
                scaled = pygame.transform.scale(preview_img, (100,100))
                self.screen.blit(scaled, preview_rect.topleft)
            else:
                if self.selected_skin == 0:
                    pygame.draw.rect(self.screen, (200,50,50), preview_rect, border_radius=8)
                else:
                    pygame.draw.rect(self.screen, (50,100,200), preview_rect, border_radius=8)

            pygame.display.flip()
            self.clock.tick(FPS)

        return (False, self.selected_skin)