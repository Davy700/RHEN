import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, size, scroll):
        super().__init__()
        self.scroll = scroll
        self.tile_size = size
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.scroll_x = 0
