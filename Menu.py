import pygame
from program_tools import RenderText
import math

class Menu():
    def __init__(self, win, tile_size, win_width, win_height):
        self.tile_size = tile_size
        self.win = win
        self.val = round((self.tile_size*24/5)/384, 3)

        self.cursor = pygame.image.load(r"Graphics/cursor.png").convert_alpha()
        self.cursor = pygame.transform.scale(self.cursor, (35*self.val, 35*self.val))

        self.start_button = pygame.Surface((300*self.val,150*self.val))
        self.start_button_rect = self.start_button.get_rect(center=(win_width / 2, win_height / 2 + 25*self.val))
        self.start_button.fill((255,255,255))

        self.exit_button = pygame.Surface((300*self.val,150*self.val))
        self.exit_button_rect = self.exit_button.get_rect(center=(win_width / 2, self.start_button_rect.y+self.start_button_rect.height + 175*self.val))
        self.exit_button.fill((255,255,255))

        self.title = RenderText("RHEN", math.floor(300*self.val), (255, 255, 255), "MS Gothic", True)
        self.title_rect = self.title.get_rect(center=(win_width / 2, 250*self.val))

        self.title_background = pygame.Surface((self.title_rect.width, self.title_rect.height-45*self.val))
        self.title_background_rect = self.title_background.get_rect(center=(self.title_rect.centerx, self.title_rect.centery-9*self.val))
        self.title_background.fill("#7e0a05")

        self.start = False
        self.exit = False

    def update(self):
        self.win.fill((0,0,0))
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_keys = pygame.mouse.get_pressed()

        self.win.blit(self.title_background, (self.title_background_rect.x, self.title_background_rect.y))
        self.win.blit(self.title, (self.title_rect.x, self.title_rect.y))

        if self.mouse_pos[0] >  self.start_button_rect.x and self.mouse_pos[0] < self.start_button_rect.x+self.start_button_rect.width and self.mouse_pos[1] >  self.start_button_rect.y and self.mouse_pos[1] < self.start_button_rect.y+self.start_button_rect.height:
            self.start_button.fill("#7e0a05")
            self.start_title = RenderText("START", math.floor(100 * self.val), (255, 255, 255), "MS Gothic", True)
            self.start_title_rect = self.start_title.get_rect(center=self.start_button_rect.center)
            if self.mouse_keys[0]:
                self.start = True
        else:
            self.start_button.fill((255,255,255))
            self.start_title = RenderText("START", math.floor(100 * self.val), (0, 0, 0), "MS Gothic", True)
            self.start_title_rect = self.start_title.get_rect(center=self.start_button_rect.center)

        if self.mouse_pos[0] >  self.exit_button_rect.x and self.mouse_pos[0] < self.exit_button_rect.x+self.exit_button_rect.width and self.mouse_pos[1] >  self.exit_button_rect.y and self.mouse_pos[1] < self.exit_button_rect.y+self.exit_button_rect.height:
            self.exit_button.fill("#7e0a05")
            self.exit_title = RenderText("EXIT", math.floor(100 * self.val), (255, 255, 255), "MS Gothic", True)
            self.exit_title_rect = self.exit_title.get_rect(center=self.exit_button_rect.center)
            if self.mouse_keys[0]:
                self.exit = True
        else:
            self.exit_button.fill((255,255,255))
            self.exit_title = RenderText("EXIT", math.floor(100 * self.val), (0, 0, 0), "MS Gothic", True)
            self.exit_title_rect = self.exit_title.get_rect(center=self.exit_button_rect.center)

        self.win.blit(self.start_button, (self.start_button_rect.x, self.start_button_rect.y))
        self.win.blit(self.exit_button, (self.exit_button_rect.x, self.exit_button_rect.y))
        self.win.blit(self.start_title, (self.start_title_rect.x, self.start_title_rect.y))
        self.win.blit(self.exit_title, (self.exit_title_rect.x, self.exit_title_rect.y))
        self.win.blit(self.cursor, self.mouse_pos)
        return self.start, not self.exit