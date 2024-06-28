import pygame
import math
import random

class Wizard(pygame.sprite.Sprite):
    def __init__(self, x, y, size, scroll, tile_size):
        super().__init__()
        self.scroll = scroll
        self.tile_size = size
        self.val = (tile_size*24/5)/384
        self.width = 108*self.val
        self.height = 180*self.val
        self.image = pygame.Surface((size, size))
        self.image = pygame.image.load(r"Graphics/objects/wizard.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200*self.val, 200*self.val))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.scroll_x = 0

        self.hitbox = pygame.Surface([self.width,self.height])
        self.hitbox_rect = self.hitbox.get_rect(center=self.rect.center)
        self.hitbox.fill((0,0,255))

    def update(self, win_width, win_height, scroll_minus_x, scroll_minus_y, scroll):
        self.blit_x = (self.rect.x - scroll[0] - self.tile_size/2) + math.floor((win_width/1920*971) - scroll_minus_x)
        self.blit_y = (self.rect.y - scroll[1] - self.tile_size) + math.floor((win_height/1080*559) - scroll_minus_y)

        self.hitbox_rect.x = self.blit_x
        self.hitbox_rect.y = self.blit_y

class Minecart(pygame.sprite.Sprite):
    def __init__(self, x, y, size, scroll, tile_size):
        super().__init__()
        self.scroll = scroll
        self.tile_size = size
        self.val = (tile_size*24/5)/384
        self.image = pygame.Surface((size, size))
        self.image = pygame.image.load(r"Graphics/objects/minecart.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200*self.val, 200*self.val))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.scroll_x = 0

    def update(self, win_width, win_height, scroll_minus_x, scroll_minus_y, scroll):
        self.blit_x = (self.rect.x - scroll[0] - self.tile_size/2) + math.floor((win_width/1920*971) - scroll_minus_x)
        self.blit_y = (self.rect.y - scroll[1] - self.tile_size) + math.floor((win_height/1080*559) - scroll_minus_y)

class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y, size, scroll, tile_size):
        super().__init__()
        self.scroll = scroll
        self.tile_size = size
        self.val = (tile_size * 24 / 5) / 384
        self.width = 84*self.val
        self.height = 30*self.val
        self.image = pygame.Surface((self.width, self.height))
        self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

        self.slime_left = pygame.image.load(r"Graphics/objects/slime_left.png").convert_alpha()
        self.slime_left = pygame.transform.scale(self.slime_left, (300*self.val, 300*self.val))

        self.slime_right = pygame.image.load(r"Graphics/objects/slime_right.png").convert_alpha()
        self.slime_right = pygame.transform.scale(self.slime_right, (300*self.val, 300*self.val))

        self.image = self.slime_right

        self.speed = self.val
        self.dur = random.choice([1,2,4])

        self.distance = self.tile_size*2/self.dur

        self.direction = pygame.math.Vector2(0, 0)

        self.counter = 0
        self.side = True

        self.blit_x = 0
        self.blit_y = 0

        self.hitbox = pygame.Surface([self.width,self.height])
        self.hitbox_rect = self.hitbox.get_rect(center=self.rect.center)
        self.hitbox.fill((0,0,255))

        self.health = 100

    def update(self, win_width, win_height, scroll_minus_x, scroll_minus_y, scroll):
        if self.direction.x * self.speed < 0:
            self.rect.x += math.floor(self.direction.x * self.speed*self.dur)
        else:
            self.rect.x += math.ceil(self.direction.x * self.speed*self.dur)

        if self.counter < self.distance/2 and self.counter % self.dur == 0:
            self.direction.x = 1
            self.image = self.slime_right
        elif self.counter > self.distance/2 and self.counter % self.dur == 0:
            self.direction.x = -1
            self.image = self.slime_left
        if self.counter == self.distance:
            self.counter = 0
        self.counter += 1

        self.blit_x = (self.rect.x - scroll[0] - self.tile_size/2) + math.floor((win_width/1920*871) - scroll_minus_x)
        self.blit_y = (self.rect.y - scroll[1] - self.tile_size) + math.floor((win_height/1080*497) - scroll_minus_y)

        self.hitbox_rect.x = round(self.blit_x+108*self.val)
        self.hitbox_rect.y = round(self.blit_y+132*self.val)

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, size, scroll, tile_size):
        super().__init__()
        self.scroll = scroll
        self.tile_size = size
        self.val = (tile_size*24/5)/384
        self.image = pygame.Surface((size, size))
        self.image = pygame.image.load(r"Graphics/objects/portal.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200*self.val, 200*self.val))

        self.red_image = pygame.image.load(r"Graphics/objects/portal_red.png").convert_alpha()
        self.red_image = pygame.transform.scale(self.red_image, (200*self.val, 200*self.val))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.scroll_x = 0

    def update(self, win_width, win_height, scroll_minus_x, scroll_minus_y, scroll):
        self.blit_x = (self.rect.x - scroll[0] - self.tile_size/2) + math.floor((win_width/1920*971) - scroll_minus_x)
        self.blit_y = (self.rect.y - scroll[1] - self.tile_size) + math.floor((win_height/1080*559) - scroll_minus_y)


class Droid(pygame.sprite.Sprite):
    def __init__(self, x, y, size, scroll, tile_size, king):
        super().__init__()
        self.scroll = scroll
        self.tile_size = size
        self.val = (tile_size*24/5)/384
        if king:
            self.size = self.tile_size*8
            self.health = 5000
            self.width = 256 * self.val
            self.height = 396 * self.val
        else:
            self.size = self.tile_size + 120*self.val
            self.health = 100
            self.width = 80 * self.val
            self.height = 124 * self.val
        self.image = pygame.Surface((self.width, self.height))
        self.image = pygame.image.load(r"Graphics/objects/droid.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.scroll_x = 0
        self.direction = pygame.math.Vector2(0, 0)

        self.hitbox = pygame.Surface([self.width,self.height])
        self.hitbox_rect = self.hitbox.get_rect(center=self.rect.center)
        self.hitbox.fill((0,0,255))

        self.king = king

        self.speed = 3*self.val

    def update(self, win_width, win_height, scroll_minus_x, scroll_minus_y, scroll):
        self.blit_x = (self.rect.x - scroll[0] - self.tile_size/2) + math.floor((win_width/1920*871) - scroll_minus_x)
        self.blit_y = (self.rect.y - scroll[1] - self.tile_size) + math.floor((win_height/1080*497) - scroll_minus_y)

        if self.king:
            self.hitbox_rect.x = round(self.blit_x + 192 * self.val)
            self.hitbox_rect.y = round(self.blit_y + 115 * self.val)
        else:
            self.hitbox_rect.x = round(self.blit_x+60*self.val)
            self.hitbox_rect.y = round(self.blit_y+36*self.val)

            self.rect.x += math.floor(self.direction.x*self.speed)
            self.rect.y += math.floor(self.direction.y*self.speed)

class Orb(pygame.sprite.Sprite):
    def __init__(self, x, y, size, scroll, tile_size, direction, orb_right):
        super().__init__()
        self.scroll = scroll
        self.tile_size = size
        self.val = (tile_size*24/5)/384
        self.width = 40*self.val
        self.height = 40*self.val
        self.scroll = scroll
        self.image = pygame.Surface((size, size))
        self.image = pygame.image.load(r'Graphics/objects/orb.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40 * self.val, 40 * self.val))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.scroll_x = 0
        self.direction = pygame.math.Vector2(0, 0)

        self.speed = 3*self.val
        self.direction = pygame.math.Vector2(0, 0)

        self.dist_x = direction[0] - self.rect.x
        self.dist_y = direction[1] - self.rect.y
        self.move_x = 1
        self.move_y = 1

        if abs(self.dist_x) > abs(self.dist_y):
            if self.dist_x != 0:
                self.move_y = self.dist_y / self.dist_x
        else:
            if self.dist_y != 0:
                self.move_x = self.dist_x / self.dist_y

        if self.dist_x < 0 and self.dist_y < 0:
            if self.move_x > 0:
                self.move_x = -self.move_x
            if self.move_y > 0:
                self.move_y = -self.move_y

        if self.dist_x < 0:
            self.move_x = -abs(self.move_x)
        else:
            self.move_x = abs(self.move_x)
        if self.dist_y < 0:
            self.move_y = -abs(self.move_y)
        else:
            self.move_y = abs(self.move_y)

        self.speed = 30*self.val

        self.hitbox = pygame.Surface([self.width,self.height])
        self.hitbox_rect = self.hitbox.get_rect(center=self.rect.center)
        self.hitbox.fill((0,0,255))

        self.times_x = 0
        self.times_y = 0

        self.org_x = x
        self.org_y = y

        self.health = 200

    def update(self, win_width, win_height, scroll_minus_x, scroll_minus_y, scroll):
        self.times_x += self.move_x * self.speed
        self.times_y += self.move_y * self.speed

        self.rect.x = self.org_x + self.times_x + (self.scroll[0] - scroll[0])
        self.rect.y = self.org_y + self.times_y + (self.scroll[1] - scroll[1])

        self.hitbox_rect.x = self.rect.x
        self.hitbox_rect.y = self.rect.y