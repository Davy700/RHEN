import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, tile_size):
        super().__init__()
        pygame.sprite.Sprite()
        pygame.sprite.Sprite.__init__(self)
        self.val = (tile_size*24/5)/384
        self.width = 83*self.val
        self.height = 133*self.val
        self.image = pygame.Surface((self.width, self.height))
        self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.speed = 12*self.val
        self.gravity = 0.9*self.val
        self.jumping = False
        self.jump_speed = -28*self.val
        self.jump_time = 0
        self.direction = pygame.math.Vector2(0,0)
        self.original_pos = pos

        self.moving_right = False
        self.moving_left = False

        self.dash_val = 5
        self.e_cooldown = 2
        self.dash = True
        self.e_counter = 0
        self.inair = False
        self.e_timer = 0
        self.q_timer = 0
        self.double_jump = False
        self.q_cooldown = 5

        self.counter = 0
        self.last_updated = 0
        self.sword_counter = 0
        self.sword_last_updated = 0

        self.stand_right = pygame.image.load(r'Graphics/character/sprite_0.png').convert_alpha()
        self.stand_right = pygame.transform.scale(self.stand_right, (200 * self.val, 200 * self.val))

        self.running_right_2 = pygame.image.load(r'Graphics/character/sprite_2.png').convert_alpha()
        self.running_right_2 = pygame.transform.scale(self.running_right_2, (200 * self.val, 200 * self.val))

        self.running_right_3 = pygame.image.load(r'Graphics/character/sprite_3.png').convert_alpha()
        self.running_right_3 = pygame.transform.scale(self.running_right_3, (200 * self.val, 200 * self.val))

        self.jump_right = pygame.image.load(r'Graphics/character/sprite_6.png').convert_alpha()
        self.jump_right = pygame.transform.scale(self.jump_right, (200 * self.val, 200 * self.val))

        self.stand_left = self.stand_right.copy()
        self.stand_left = pygame.transform.flip(self.stand_left, True, False)

        self.running_left_2 = self.running_right_2.copy()
        self.running_left_2 = pygame.transform.flip(self.running_left_2, True, False)

        self.running_left_3 = self.running_right_3.copy()
        self.running_left_3 = pygame.transform.flip(self.running_left_3, True, False)

        self.jump_left = self.jump_right.copy()
        self.jump_left = pygame.transform.flip(self.jump_left, True, False)

        self.running_2 = self.running_left_2
        self.stand = self.stand_left
        self.jump_side = self.jump_left

        self.sword_width = 90*self.val
        self.sword_height = 110*self.val
        self.sword_image = pygame.Surface((self.sword_width, self.sword_height))
        self.sword_image.convert_alpha()
        self.sword_rect = self.sword_image.get_rect(topleft = pos)

        self.sword_left = pygame.image.load(r'Graphics/character/sword_left.png').convert_alpha()
        self.sword_left = pygame.transform.scale(self.sword_left, (200 * self.val, 200 * self.val))

        self.sword_mid_left = pygame.image.load(r'Graphics/character/sword_mid_left.png').convert_alpha()
        self.sword_mid_left = pygame.transform.scale(self.sword_mid_left, (200 * self.val, 200 * self.val))

        self.sword_low_left = pygame.image.load(r'Graphics/character/sword_low_left.png').convert_alpha()
        self.sword_low_left = pygame.transform.scale(self.sword_low_left, (200 * self.val, 200 * self.val))

        self.sword_right = pygame.image.load(r'Graphics/character/sword_right.png').convert_alpha()
        self.sword_right = pygame.transform.scale(self.sword_right, (200 * self.val, 200 * self.val))

        self.sword_mid_right = pygame.image.load(r'Graphics/character/sword_mid_right.png').convert_alpha()
        self.sword_mid_right = pygame.transform.scale(self.sword_mid_right, (200 * self.val, 200 * self.val))

        self.sword_low_right = pygame.image.load(r'Graphics/character/sword_low_right.png').convert_alpha()
        self.sword_low_right = pygame.transform.scale(self.sword_low_right, (200 * self.val, 200 * self.val))

        self.sword = self.sword_left
        self.sword_rect = self.sword.get_rect()
        self.sword_mid = self.sword_mid_left
        self.sword_low = self.sword_low_left
        self.sword_direction = self.sword_left
        self.sword_attack = [self.sword_mid_left, self.sword_mid_right, self.sword_low_left, self.sword_low_right]

        self.sword_blit_val_x = -45*self.val
        self.sword_blit_val_y = -10*self.val
        self.sword_swish = False
        self.sword_last_updated_animation = 0
        self.sword_animation_counter = 0

        self.orb_width = 200 * self.val
        self.orb_height = 200 * self.val
        self.orb_image = pygame.Surface((self.orb_width, self.orb_height))
        self.orb_image.convert_alpha()
        self.orb_rect = self.orb_image.get_rect(topleft=pos)

        self.orb_image = pygame.image.load(r'Graphics/objects/orb.png').convert_alpha()
        self.orb_image = pygame.transform.scale(self.orb_image, (40 * self.val, 40 * self.val))

        self.orb_x = 0
        self.orb_y = 0
        self.orb_right = True

        self.show_sword = False
        self.got_sword = False

        self.show_orb = False
        self.got_orb = False

        self.got_dash = False
        self.got_jump = False

        self.sword_hitbox = pygame.Surface([self.sword_width,self.sword_height])
        self.sword_hitbox_rect = self.sword_hitbox.get_rect(center=self.sword_rect.center)
        self.sword_hitbox.fill((255,0,0))
        self.sword_hitbox_blit_val_x = 0
        self.health = 100

        self.hitbox = pygame.Surface([self.width,self.height])
        self.hitbox_rect = self.hitbox.get_rect(center=self.rect.center)
        self.hitbox.fill((0,255,0))

        self.tile_size = tile_size
        self.blit_x, self.blit_y = 0, 0

    def get_input(self):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_d] or self.keys[pygame.K_a]:
            if self.keys[pygame.K_d]:
                self.direction.x = 1
                self.moving_right = True
                self.moving_left = False
                if self.got_dash and self.keys[pygame.K_e] and self.dash:
                    self.direction.x = self.dash_val
                    self.e_counter += 1

            if self.keys[pygame.K_a]:
                self.direction.x = -1
                self.moving_left = True
                self.moving_right = False
                if self.got_dash and self.keys[pygame.K_e] and self.dash:
                    self.direction.x = -self.dash_val
                    self.e_counter += 1
        else:
            self.direction.x = 0
            self.moving_left = False
            self.moving_right = False

        if self.keys[pygame.K_w] and self.jumping and self.jump_time <= 0:
            self.jump()

        if self.got_jump and self.keys[pygame.K_q] and self.q_timer <= 0:
            self.double_jump = True
            self.double_jump_cooldown()
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        self.sword_rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_time = 0.5

    def dash_cooldown(self):
        self.e_timer += self.time
        if self.e_timer > self.e_cooldown*1000:
            self.e_timer = 0
            self.e_counter = 0
            return True

    def double_jump_cooldown(self):
        self.q_timer = self.q_cooldown * 60

    def sword_animation(self):
        if (self.now - self.sword_last_updated_animation) > 80:
            self.sword_last_updated_animation = self.now
            self.sword_animation_counter += 1

            if self.sword_animation_counter == 1:
                self.sword = self.sword_mid
            elif self.sword_animation_counter == 2:
                self.sword = self.sword_low

            elif self.sword_animation_counter == 3:
                self.sword = self.sword_direction
                self.sword_animation_counter = 0
                self.sword_swish = 0

    def update(self, win_width, win_height, scroll_minus_x, scroll_minus_y, scroll, tiles, time):
        self.mouse_keys = pygame.mouse.get_pressed()
        if self.q_timer > 0:
            self.q_timer -= 1

        if self.direction.y == 0 or self.direction.y == self.gravity:
            self.inair = False
        else:
            self.inair = True

        self.time = time
        if self.e_counter == 10:
            self.dash = False
            self.dash = self.dash_cooldown()

        self.get_input()
        if not self.jump_time <= 0:
            self.jump_time -= 0.1

        self.now = pygame.time.get_ticks()
        if self.show_sword:
            if self.sword_swish:
                self.sword_animation()
            else:
                self.sword = self.sword_direction
                if (self.now - self.sword_last_updated) > 200 and self.mouse_keys[0]:
                    self.sword_last_updated = self.now
                    self.sword_swish = True

        if self.moving_right:
            self.running_2 = self.running_right_2
            self.running_3 = self.running_right_3
            self.stand = self.stand_right
            self.sword_direction = self.sword_right
            self.jump_side = self.jump_right
            self.sword_mid = self.sword_mid_right
            self.sword_low = self.sword_low_right
            self.sword_blit_val_x = 45*self.val
            self.sword_hitbox_blit_val_x = -10*self.val
            self.orb_right = True
        if self.moving_left:
            self.running_2 = self.running_left_2
            self.running_3 = self.running_left_3
            self.stand = self.stand_left
            self.jump_side = self.jump_left
            self.sword_direction = self.sword_left
            self.sword_mid = self.sword_mid_left
            self.sword_low = self.sword_low_left
            self.sword_blit_val_x = -45*self.val
            self.sword_hitbox_blit_val_x = 0*self.val
            self.orb_right = False

        if self.inair == False:
            if (self.now - self.last_updated > 200):
                self.last_updated = self.now
                if (self.moving_right or self.moving_left):
                    if self.counter == 1:
                        self.image = self.running_2
                    elif self.counter == 2:
                        self.image = self.stand
                    elif self.counter == 3:
                        self.counter = 0
                        self.image = self.running_3
                else:
                    self.image = self.stand
                    self.counter = 0
                    if self.counter > 2:
                        self.counter = 0
                self.counter = round(self.counter+1, 1)
        else:
            self.image = self.jump_side

        self.blit_x = (self.rect.x - scroll[0]) + ((win_width/2 - self.tile_size/4) - scroll_minus_x)
        self.blit_y = (self.rect.y - scroll[1]) + ((win_height/2 - self.tile_size/2) - scroll_minus_y)

        self.hitbox_rect.x = self.blit_x
        self.hitbox_rect.y = self.blit_y

        self.sword_blit_x = self.blit_x+self.sword_blit_val_x
        self.sword_blit_y = self.blit_y+self.sword_blit_val_y

        self.sword_hitbox_rect.x = self.sword_blit_x+self.sword_hitbox_blit_val_x
        self.sword_hitbox_rect.y = self.sword_blit_y+33*self.val

        if self.orb_right:
            self.orb_x = self.hitbox_rect.x + self.hitbox_rect.width - 10*self.val
            self.orb_y = self.hitbox_rect.y + self.hitbox_rect.height/2 - 15*self.val
        else:
            self.orb_x = self.hitbox_rect.x - 33*self.val
            self.orb_y = self.hitbox_rect.y + self.hitbox_rect.height/2 - 20*self.val
