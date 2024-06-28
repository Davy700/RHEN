import pygame
import math
from random import randint
from settings import starting, mine, second, third, fourth
from Player import Player
from Tile import Tile
from program_tools import RenderText
from Objects import Wizard, Minecart, Slime, Portal, Droid, Orb

class StartingPoint():
    def __init__(self, win, tile_size):
        self.tile_size = tile_size
        self.win = win
        self.val = round((self.tile_size*24/5)/384, 3)
        self.tiles = pygame.sprite.Group()
        self.sprite_player = pygame.sprite.GroupSingle()
        self.portal_group = pygame.sprite.GroupSingle()
        self.scroll = [0,0]
        self.true_scroll = [0,0]
        self.cursor = pygame.image.load(r"Graphics/cursor.png").convert_alpha()
        self.cursor = pygame.transform.scale(self.cursor, (35*self.val, 35*self.val))

        self.tile_top_design = pygame.image.load(r"Graphics/tiles_top.png").convert_alpha()
        self.tile_top_design = pygame.transform.scale(self.tile_top_design, (80*self.val, 80*self.val))

        self.tile_left_design = self.tile_top_design
        self.tile_left_design = pygame.transform.rotate(self.tile_left_design, 90)

        self.tile_right_design = self.tile_top_design
        self.tile_right_design = pygame.transform.rotate(self.tile_right_design, 270)

        self.tile_bottom_design = self.tile_top_design
        self.tile_bottom_design = pygame.transform.rotate(self.tile_bottom_design, 180)

        self.green_grass_design = pygame.image.load(r"Graphics/grass.png").convert_alpha()
        self.green_grass_design = pygame.transform.scale(self.green_grass_design, (80*self.val, 80*self.val))

        self.mine_design = pygame.image.load(r"Graphics/mine.png").convert_alpha()
        self.mine_design = pygame.transform.scale(self.mine_design, (80*self.val, 80*self.val))

        self.dist_design = pygame.image.load(r"Graphics/dystopia.png").convert_alpha()
        self.dist_design = pygame.transform.scale(self.dist_design, (80*self.val, 80*self.val))

        self.sword_tool = pygame.image.load(r"Graphics/tools/sword_tool.png").convert_alpha()
        self.sword_tool = pygame.transform.scale(self.sword_tool, (40 * self.val, 40 * self.val))

        self.orb_tool = pygame.image.load(r"Graphics/objects/orb.png").convert_alpha()
        self.orb_tool = pygame.transform.scale(self.orb_tool, (30 * self.val, 30 * self.val))

        self.dash_tool = pygame.image.load(r"Graphics/tools/dash_tool.png").convert_alpha()
        self.dash_tool = pygame.transform.scale(self.dash_tool, (60 * self.val, 60 * self.val))

        self.jump_tool = pygame.image.load(r"Graphics/tools/jump_tool.png").convert_alpha()
        self.jump_tool = pygame.transform.scale(self.jump_tool, (60 * self.val, 60 * self.val))

        self.frame_pos = None
        self.tiles_top = pygame.sprite.Group()
        self.tiles_bottom = pygame.sprite.Group()
        self.tiles_left = pygame.sprite.Group()
        self.tiles_right = pygame.sprite.Group()
        self.orb_group = pygame.sprite.Group()

        self.number_color = (255,0,0)
        self.tool_number_size = round(12*self.val)

        self.tool_numbers = []
        self.ability_letters = []

        self.numbers_size = math.floor(self.tile_size*24/26.5)
        self.numbers_gap = math.floor(self.numbers_size/24)
        self.numbers_frame_width = math.floor(self.numbers_size/14.4)

        self.e_cooldown_box_value = self.numbers_size-2*self.numbers_frame_width
        self.q_cooldown_box_value = self.numbers_size-2*self.numbers_frame_width

        self.current_place = 0
        self.switch_place = False
        self.places = [starting, mine, second, third, fourth]

        self.player_counter = 0
        self.slime_counter = 0
        self.droid_counter = 0
        self.droid_spawn_counter = 0

        self.white_screen = pygame.Surface((self.tile_size*24,self.tile_size*13.5))
        self.white_screen.set_alpha(0)
        self.white_screen.fill((255,255,255))
        self.alpha_value = 0
        self.alp = 5
        self.white_screen_bool = False
        self.whiteness_reached_max = False
        self.last_updated_white = 0
        self.white_measure = 12.75
        self.last_updated = 0

        self.background_colors = [(135,220,235), (36,36,36), (135,220,235), (67,49,49), (67,49,66)]
        self.current_background_color = (135,220,235)

        self.tile_designs = [r"Graphics/tiles_top.png", r"Graphics/mine.png", r"Graphics/tiles_top.png", r"Graphics/dystopia.png", r"Graphics/forth.png"]
        self.tile_fills = ['#743e0c', '#494949', '#743e0c', '#703626', '#67446b']
        self.place_creator()
        self.orb_counter = 0
        self.show_text = False
        self.dead = False

        self.wizard_script = ["HEEEELLPP!!! Finally somebody!! |My mine was raided by evil slimes! |I give you my legacy sword that steals energy from your opponents when you hit them. |Furthermore, I give you the knowledge of dash. |Go down with the minecart and kill them!! ",
                              "Thank you! |Don't rest yet because I need your help! |Enemy droids appeared in my magical dimensions! |But be careful! |The Droid King is with them! | I give you my magical orb that you can shoot with. |And the knowledge of double jump! |Jump on the ground above the minecart with your double jump skill. |There's a portal waiting for you... "]

        for i in range(9):
            self.text = RenderText(str(i+1), math.floor(12*self.val), self.number_color)
            self.tool_numbers.append(self.text)

        self.text = RenderText("E", self.tool_number_size, self.number_color)
        self.ability_letters.append(self.text)
        self.text = RenderText("Q", self.tool_number_size, self.number_color)
        self.ability_letters.append(self.text)
        self.end = False

    def place_creator(self):
        level_map = None
        for i in range (len(self.places)):
            if self.current_place == i:
                place = self.places[i]
                level_map = place
                self.current_background_color = self.background_colors[i]
                self.current_tile_design = self.design_maker(self.tile_designs[i])
                self.current_tile_fill = self.tile_fills[i]
                self.tiles_top = pygame.sprite.Group()
                self.tiles_bottom = pygame.sprite.Group()
                self.tiles_left = pygame.sprite.Group()
                self.tiles_right = pygame.sprite.Group()
                self.tiles = pygame.sprite.Group()
                self.ghost_objects = pygame.sprite.Group()
                self.slime_group = pygame.sprite.Group()
                self.droid_group = pygame.sprite.Group()
                self.portal_group = pygame.sprite.GroupSingle()
                self.orb_group = pygame.sprite.Group()
                self.show_text = False

        for row_index, row in enumerate(level_map):
            for col_index, cell in enumerate(row):
                if cell == 'X':
                    x = col_index * self.tile_size
                    y = row_index * self.tile_size
                    tile = Tile(x, y, self.tile_size, self.scroll)
                    tile.image.fill(self.current_tile_fill)
                    self.tiles.add(tile)

                    if not level_map[row_index-1][col_index] == 'X':
                        self.tiles_top.add(tile)

                    try:
                        if level_map[row_index+1][col_index] == ' ':
                            self.tiles_bottom.add(tile)

                        if level_map[row_index][col_index+1] == ' ':
                            self.tiles_right.add(tile)

                        if level_map[row_index][col_index-1] == ' ':
                            self.tiles_left.add(tile)
                    except:
                        pass

                if cell == 'P':
                    if self.current_place == 0:
                        x = col_index * self.tile_size
                        y = row_index * self.tile_size
                        self.player = Player((x, y), self.tile_size)
                        self.sprite_player.add(self.player)
                    else:
                        self.player.rect.x = col_index * self.tile_size
                        self.player.rect.y = row_index * self.tile_size
                if cell == 'W':
                    x = col_index * self.tile_size
                    y = row_index * self.tile_size
                    self.wizard = Wizard(x, y, self.tile_size, self.scroll, self.tile_size)
                    self.ghost_objects.add(self.wizard)
                if cell == 'M':
                    x = col_index * self.tile_size
                    y = row_index * self.tile_size
                    self.minecart = Minecart(x, y, self.tile_size, self.scroll, self.tile_size)
                    self.tiles.add(self.minecart)
                if cell == 'S':
                    x = col_index * self.tile_size
                    y = row_index * self.tile_size
                    self.slime = Slime(x, y, self.tile_size, self.scroll, self.tile_size)
                    self.slime_group.add(self.slime)
                if cell == 'T':
                    x = col_index * self.tile_size
                    y = row_index * self.tile_size
                    self.portal = Portal(x, y, self.tile_size, self.scroll, self.tile_size)
                    self.portal_group.add(self.portal)
                if cell == 'D':
                    x = col_index * self.tile_size
                    y = row_index * self.tile_size
                    self.droid = Droid(x, y, self.tile_size, self.scroll, self.tile_size, False)
                    self.droid_group.add(self.droid)
                if cell == 'K':
                    x = col_index * self.tile_size
                    y = row_index * self.tile_size
                    self.king = Droid(x, y, self.tile_size, self.scroll, self.tile_size, True)

    def design_maker(self, pic):
        design_list = []
        tile_top_design = pygame.image.load(pic).convert_alpha()
        for i in range(4):
            tile_top_design = pygame.transform.scale(tile_top_design, (80*self.val, 80*self.val))
            tile_top_design = pygame.transform.rotate(tile_top_design, i*90)
            design_list.append(tile_top_design)
            tile_top_design = pygame.transform.rotate(tile_top_design, -(i*90))
        return design_list

    def horizontal_movement_collision(self):
        player = self.player
        player.rect.x += player.direction.x * player.speed
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
            player.jumping = True

    def vertical_movement_collision(self):
        player = self.player
        player.apply_gravity()
        player.jumping = False
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    self.player.inair = False
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                player.jumping = True

    def ToolBar(self):
        self.number_positions = []
        for i in range(9):
            x_position = math.floor((self.tile_size*12)-(self.numbers_size/2)-4*(self.numbers_size+self.numbers_gap))+(i*(self.numbers_size + self.numbers_gap))
            y_position = math.floor(self.tile_size*24/16*9/1.1365)
            self.number_positions.append((x_position, y_position))
            pygame.draw.rect(self.win, (50,50,50), (x_position, y_position, self.numbers_size,self.numbers_size), self.numbers_frame_width)
            pygame.draw.rect(self.win, (230,230,230), (x_position+self.numbers_frame_width, y_position+self.numbers_frame_width, self.numbers_size-2*self.numbers_frame_width,self.numbers_size-2*self.numbers_frame_width))

        pygame.draw.rect(self.win, (0, 0, 0), (self.number_positions[self.frame_pos][0] + self.numbers_frame_width, self.number_positions[self.frame_pos][1] + self.numbers_frame_width, self.numbers_size - 2 * self.numbers_frame_width, self.numbers_size - 2 * self.numbers_frame_width), math.floor(self.numbers_frame_width * 1.3))

        self.ability_positions = []
        x_position, y_position = (self.tile_size*0.8+self.numbers_frame_width, math.floor(self.tile_size*24/16*9/1.1365)+self.numbers_frame_width)
        self.ability_positions.append((x_position, y_position))

        x_position, y_position = (self.tile_size * 0.8 + self.numbers_frame_width, math.floor(self.tile_size * 24 / 16 * 9 / 1.1365) - (self.numbers_size+self.numbers_gap) + self.numbers_frame_width)
        self.ability_positions.append((x_position, y_position))

        self.e_tool = pygame.draw.rect(self.win, (50, 50, 50), (self.tile_size * 0.8, math.floor(self.tile_size*24/16*9/1.1365), self.numbers_size, self.numbers_size), self.numbers_frame_width)
        pygame.draw.rect(self.win, (230, 230, 230), (self.tile_size*0.8+self.numbers_frame_width, math.floor(self.tile_size*24/16*9/1.1365)+self.numbers_frame_width, self.numbers_size-2*self.numbers_frame_width, self.numbers_size-2*self.numbers_frame_width))
        if self.player.got_dash:
            self.win.blit(self.dash_tool, (self.e_tool.x + self.numbers_size / 2 - self.dash_tool.get_width() / 2,self.e_tool.y + self.numbers_size / 2 - self.dash_tool.get_height() / 2))
        pygame.draw.rect(self.win, (0,0,0), (self.tile_size*0.8+self.numbers_frame_width, math.floor(self.tile_size*24/16*9/1.1365)+self.numbers_frame_width, self.numbers_size-2*self.numbers_frame_width, self.numbers_size-2*self.numbers_frame_width-self.e_cooldown_box_value))

        self.q_tool = pygame.draw.rect(self.win, (50, 50, 50), (self.tile_size * 0.8, math.floor(self.tile_size * 24 / 16 * 9 / 1.1365)-(self.numbers_size+self.numbers_gap), self.numbers_size, self.numbers_size), self.numbers_frame_width)
        pygame.draw.rect(self.win, (230, 230, 230), (self.tile_size * 0.8 + self.numbers_frame_width, math.floor(self.tile_size * 24 / 16 * 9 / 1.1365) - (self.numbers_size+self.numbers_gap) + self.numbers_frame_width, self.numbers_size - 2 * self.numbers_frame_width, self.numbers_size - 2 * self.numbers_frame_width))
        if self.player.got_jump:
            self.win.blit(self.jump_tool, (self.q_tool.x + self.numbers_size / 2 - self.jump_tool.get_width() / 2,self.q_tool.y + self.numbers_size / 2 - self.jump_tool.get_height() / 2))

        pygame.draw.rect(self.win, (0,0,0), (self.tile_size * 0.8 + self.numbers_frame_width, math.floor(self.tile_size * 24 / 16 * 9 / 1.1365) - (self.numbers_size+self.numbers_gap) + self.numbers_frame_width, self.numbers_size - 2 * self.numbers_frame_width, self.numbers_size - 2 * self.numbers_frame_width-self.q_cooldown_box_value))

        if self.player.got_sword:
            self.win.blit(self.sword_tool, (self.number_positions[0][0] + self.numbers_size/2-self.sword_tool.get_width()/2,self.number_positions[0][1] + self.numbers_size/2-self.sword_tool.get_height()/2))
            if self.frame_pos == 0:
                self.player.show_sword = True
            else:
                self.player.show_sword = False

        if self.player.got_orb:
            self.win.blit(self.orb_tool, (self.number_positions[1][0] + self.numbers_size / 2 - self.orb_tool.get_width() / 2, self.number_positions[1][1] + self.numbers_size / 2 - self.orb_tool.get_height() / 2))
            if self.frame_pos == 1:
                self.player.show_orb = True
            else:
                self.player.show_orb = False

    def box_cooldown(self):
        if self.player.e_timer != 0:
            self.e_cooldown_box_value = self.player.e_timer/(self.player.e_cooldown*1000) * (self.numbers_size - 2 * self.numbers_frame_width)

        if self.player.q_timer != 0:
            self.q_cooldown_box_value = (self.player.q_cooldown*60 - self.player.q_timer)/(self.player.q_cooldown*60) * (self.numbers_size - 2 * self.numbers_frame_width)

    def change_place(self):
        if self.switch_place:
            if not self.dead:
                self.current_place += 1
            else:
                self.dead = False
            self.switch_place = False
            self.place_creator()

    def loading_screen(self):
        if self.alpha_value == 0:
            self.alp = abs(self.white_measure)
            self.last_updated_white = self.now
            if self.whiteness_reached_max == True:
                self.alp = 0
                self.white_screen_bool = False
                self.whiteness_reached_max = False

        if self.alpha_value == 255:
            if self.dead:
                self.player.health = 100
            self.alp = 0
            self.change_place()
            if (self.now - self.last_updated_white > 2250):
                self.alp = -self.white_measure
                self.whiteness_reached_max = True

        self.alpha_value += self.alp
        self.white_screen.set_alpha(self.alpha_value)

    def wizard_text_first(self):
        text = RenderText(self.wizard_script[self.text_which][self.text_from:self.character_counter], math.floor(20*self.val), (0, 0, 0), "MS Gothic", True)
        text_rect = text.get_rect(topright=(self.wizard.blit_x, self.wizard.blit_y))
        return text, text_rect

    def update(self, win_width, win_height, frame_pos, time):
        self.win.fill(self.current_background_color)
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.scroll_minus_x = win_width/2 + self.player.width/2
        self.scroll_minus_y = win_height/2 + self.player.height/2
        self.true_scroll[0] += (self.player.rect.x - self.true_scroll[0] - self.scroll_minus_x) / 20
        self.true_scroll[1] += (self.player.rect.y - self.true_scroll[1] - self.scroll_minus_y) / 20

        self.frame_pos = frame_pos
        self.time = time

        self.scroll = self.true_scroll.copy()
        self.scroll[0] = int(self.scroll[0])
        self.scroll[1] = int(self.scroll[1])

        self.sprite_player.update(win_width, win_height, self.scroll_minus_x, self.scroll_minus_y, self.scroll, self.tiles, self.time)
        self.win.blit(self.player.image, (self.player.blit_x, self.player.blit_y), (math.floor(self.tile_size/4*3), math.floor(self.tile_size/80*33), self.tile_size, math.floor(self.tile_size/80*167)))

        if self.player.show_sword:
            self.win.blit(self.player.sword, (self.player.sword_blit_x, self.player.sword_blit_y), (math.floor(self.tile_size/4*3), math.floor(self.tile_size/80*33), self.tile_size, math.floor(self.tile_size/80*167)))
        elif self.player.show_orb:
            self.win.blit(self.player.orb_image, (self.player.orb_x, self.player.orb_y))
            if self.player.mouse_keys[0]:
                if self.orb_counter == 0:
                    self.orb = Orb(self.player.orb_x, self.player.orb_y, self.tile_size, self.scroll, self.tile_size, self.mouse_pos, self.player.orb_right)
                    self.orb_group.add(self.orb)
                    self.orb_counter = 10

        if self.orb_counter > 0:
            self.orb_counter -= 1

        self.now = self.player.now

        for sprite in self.tiles:
            if self.current_place == 0 or self.current_place == 2 or self.current_place == 3 or self.current_place == 4:
                if sprite == self.minecart:
                    self.minecart.update(win_width, win_height, self.scroll_minus_x, self.scroll_minus_y, self.scroll)
                    self.win.blit(self.minecart.image, ((sprite.rect.x - self.scroll[0] - self.tile_size / 2) + math.floor((win_width / 1920 * 947) - self.scroll_minus_x), (sprite.rect.y - self.scroll[1] - self.tile_size) + math.floor((win_height / 1080 * 520) - self.scroll_minus_y)))
                else:
                    self.win.blit(sprite.image, ((sprite.rect.x - self.scroll[0] - self.tile_size / 2) + math.floor((win_width / 1.961) - self.scroll_minus_x), (sprite.rect.y - self.scroll[1] - self.tile_size) + math.floor((win_height / 1.865) - self.scroll_minus_y)))

            elif self.current_place == 1:
                if sprite == self.minecart:
                    self.win.blit(self.minecart.image, ((sprite.rect.x - self.scroll[0] - self.tile_size / 2) + math.floor((win_width / 1920 * 1014) - self.scroll_minus_x), (sprite.rect.y - self.scroll[1] - self.tile_size) + math.floor((win_height / 1080 * 520) - self.scroll_minus_y)))
                else:
                    self.win.blit(sprite.image, ((sprite.rect.x - self.scroll[0] - self.tile_size / 2) + math.floor((win_width / 1.961) - self.scroll_minus_x),(sprite.rect.y - self.scroll[1] - self.tile_size) + math.floor((win_height / 1.865) - self.scroll_minus_y)))

        if self.current_place == 4:
            self.king.update(win_width, win_height, self.scroll_minus_x, self.scroll_minus_y, self.scroll)
            if self.king.health > 0:
                self.win.blit(self.king.image, (self.king.blit_x, self.king.blit_y))
                pygame.draw.rect(self.win, (255, 0, 0), (self.king.hitbox_rect.x - 122 * self.val, self.king.hitbox_rect.y - 15 * self.val, 500 * self.val, 5 * self.val))
                pygame.draw.rect(self.win, (0, 255, 0), (self.king.hitbox_rect.x - 122 * self.val, self.king.hitbox_rect.y - 15 * self.val, self.king.health * 0.1 * self.val,5 * self.val))
            else:
                self.king.kill()

            if self.droid_spawn_counter == 0 and self.king.health > 0:
                x = randint(30*self.tile_size, 42*self.tile_size)
                y = randint(10*self.tile_size, 20*self.tile_size)
                self.droid = Droid(x, y, self.tile_size, self.scroll, self.tile_size, False)
                self.droid_group.add(self.droid)
                self.droid_spawn_counter = 300
            else:
                self.droid_spawn_counter -= 1

            if self.king.hitbox_rect.colliderect(self.player.sword_hitbox_rect) and not (self.player.sword == self.player.sword_left or self.player.sword == self.player.sword_right) and self.droid_counter == 0:
                self.king.health -= 70
                self.droid_counter = 50
                if self.player.health < 100:
                    self.player.health += 2

        for ghost in self.ghost_objects:
            self.wizard.update(win_width, win_height, self.scroll_minus_x, self.scroll_minus_y, self.scroll)
            self.win.blit(ghost.image, ((self.wizard.rect.x - self.scroll[0] - self.tile_size/2) + math.floor((win_width/1920*919) - self.scroll_minus_x), (self.wizard.rect.y - self.scroll[1] - self.tile_size) + math.floor((win_height/1080*539) - self.scroll_minus_y)))
            pygame.draw.rect(self.win, (255,0,0), (self.wizard.rect.x, self.wizard.rect.y, 100, 100))

        for portal in self.portal_group:
            portal.update(win_width, win_height, self.scroll_minus_x, self.scroll_minus_y, self.scroll)

        for portal in self.portal_group:
            if self.current_place == 3 and len(self.droid_group) == 0:
                    self.win.blit(portal.red_image, ((self.portal.rect.x - self.scroll[0] - self.tile_size / 2) + math.floor((win_width / 1920 * 895) - self.scroll_minus_x), (self.portal.rect.y - self.scroll[1] - self.tile_size) + math.floor((win_height / 1080 * 465) - self.scroll_minus_y)))
            else:
                if len(self.slime_group) == 0 and self.current_place != 3:
                    self.win.blit(portal.image, ((self.portal.rect.x - self.scroll[0] - self.tile_size / 2) + math.floor((win_width / 1920 * 895) - self.scroll_minus_x), (self.portal.rect.y - self.scroll[1] - self.tile_size) + math.floor((win_height / 1080 * 465) - self.scroll_minus_y)))

        pygame.draw.rect(self.win, (255,0,0),((self.player.rect.x - self.scroll[0]) + ((win_width/2 - self.tile_size/4) - self.scroll_minus_x)+10*self.val, (self.player.rect.y - self.scroll[1]) + ((win_height/2 - self.tile_size/2) - self.scroll_minus_y)-15*self.val,60*self.val,5*self.val))
        pygame.draw.rect(self.win, (40,255,40),((self.player.rect.x - self.scroll[0]) + ((win_width/2 - self.tile_size/4) - self.scroll_minus_x)+10*self.val, (self.player.rect.y - self.scroll[1]) + ((win_height/2 - self.tile_size/2) - self.scroll_minus_y)-15*self.val,self.player.health*0.6*self.val,5*self.val))

        for sprite in self.tiles_right:
            sprite.image.blit(self.current_tile_design[3], (0, 0))
        for sprite in self.tiles_bottom:
            sprite.image.blit(self.current_tile_design[2], (0, 0))
        for sprite in self.tiles_left:
            sprite.image.blit(self.current_tile_design[1], (0, 0))
        for sprite in self.tiles_top:
            sprite.image.blit(self.current_tile_design[0], (0, 0))
            if self.current_place == 0 or self.current_place == 2:
                sprite.image.blit(self.green_grass_design, (0, 0))

        for slime in self.slime_group:
            slime.update(win_width, win_height, self.scroll_minus_x, self.scroll_minus_y, self.scroll)
            pygame.draw.rect(self.win, (255,0,0), (slime.hitbox_rect.x+12*self.val,slime.hitbox_rect.y-15*self.val, 60*self.val,5*self.val))
            pygame.draw.rect(self.win, (0,255,0), (slime.hitbox_rect.x+12*self.val,slime.hitbox_rect.y-15*self.val, slime.health*0.6*self.val,5*self.val))

            if slime.hitbox_rect.colliderect(self.player.hitbox_rect) and self.player_counter == 0:
                self.player.health -= 2
                self.player_counter = 10

            if slime.hitbox_rect.colliderect(self.player.sword_hitbox_rect) and not (self.player.sword == self.player.sword_left or self.player.sword == self.player.sword_right) and self.slime_counter == 0:
                slime.health -= 40
                self.slime_counter = 50
                self.player.health += 2

            if slime.health > 0:
                self.win.blit(slime.image, (slime.blit_x, slime.blit_y))
            else:
                slime.kill()

        for droid in self.droid_group:
            droid.update(win_width, win_height, self.scroll_minus_x, self.scroll_minus_y, self.scroll)

            pygame.draw.rect(self.win, (255,0,0), (droid.hitbox_rect.x+10*self.val,droid.hitbox_rect.y-15*self.val, 60*self.val,5*self.val))
            pygame.draw.rect(self.win, (0,255,0), (droid.hitbox_rect.x+10*self.val,droid.hitbox_rect.y-15*self.val, droid.health*0.6*self.val,5*self.val))

            if droid.hitbox_rect.colliderect(self.player.hitbox_rect) and self.player_counter == 0:
                self.player.health -= 5
                self.player_counter = 10

            if droid.hitbox_rect.colliderect(self.player.sword_hitbox_rect) and not (self.player.sword == self.player.sword_left or self.player.sword == self.player.sword_right) and self.droid_counter == 0:
                droid.health -= 70
                self.droid_counter = 50
                self.player.health += 2

            if droid.health > 0:
                self.win.blit(droid.image, (droid.blit_x, droid.blit_y))
            else:
                droid.kill()

            if (abs(droid.hitbox_rect.x - self.player.hitbox_rect.x) < 1152*self.val) and (abs(droid.hitbox_rect.y - self.player.hitbox_rect.y) < 648*self.val):
                if not (droid.rect.x > self.player.rect.x and droid.rect.x < self.player.rect.x+self.player.rect.width):
                    if droid.rect.x > self.player.rect.x:
                        droid.direction.x = -1
                    if droid.rect.x < self.player.rect.x:
                        droid.direction.x = 1
                else:
                    droid.direction.x = 0
                if not (droid.rect.y > self.player.rect.y and droid.rect.y < self.player.rect.y+self.player.rect.height):
                    if droid.rect.y > self.player.rect.y:
                        droid.direction.y = -1
                    if droid.rect.y < self.player.rect.y:
                        droid.direction.y = 1
                else:
                    droid.direction.y = 0
            else:
                droid.direction.x = 0
                droid.direction.y = 0

        for orb in self.orb_group:
            orb.update(win_width, win_height, self.scroll_minus_x, self.scroll_minus_y, self.scroll)
            self.win.blit(orb.image, (orb.rect.x, orb.rect.y))

            for slime in self.slime_group:
                if orb.hitbox_rect.colliderect(slime.hitbox_rect):
                    orb.kill()
                    slime.health -= 3

            for droid in self.droid_group:
                if orb.hitbox_rect.colliderect(droid.hitbox_rect):
                    orb.kill()
                    droid.health -= 5

            if self.current_place == 4:
                if orb.hitbox_rect.colliderect(self.king.hitbox_rect) and self.king.health > 0:
                    orb.kill()
                    self.king.health -= 5

            if abs(orb.times_x) > 2016*self.val or abs(orb.times_y) > 1134*self.val:
                orb.kill()

        if self.player_counter != 0:
            self.player_counter -= 1

        if self.slime_counter != 0:
            self.slime_counter -= 1

        if self.droid_counter != 0:
            self.droid_counter -= 1

        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.ToolBar()
        self.box_cooldown()

        self.win.blit(self.cursor, self.mouse_pos)
        for i, number in enumerate(self.tool_numbers):
            self.number_rect = number.get_rect(topright=(self.number_positions[i][0]-self.numbers_frame_width+self.numbers_size, self.number_positions[i][1]+self.numbers_frame_width))
            self.win.blit(number, self.number_rect)
        for i, ability in enumerate(self.ability_letters):
            self.ability_rect = ability.get_rect(topright=(self.ability_positions[i][0]-self.numbers_frame_width+self.numbers_size-self.tile_size/16, self.ability_positions[i][1]+self.numbers_frame_width-self.tile_size/16))
            self.win.blit(ability, self.ability_rect)

        if self.keys[pygame.K_y]:
            self.white_screen_bool = True

        if (self.player.rect.right == self.minecart.rect.left):
            if self.player.got_sword:
                text = RenderText("Press SPACE", math.floor(20*self.val), (0, 0, 0), "MS Gothic", True)
                text_rect = text.get_rect(topright=(self.minecart.blit_x, self.minecart.blit_y))
                self.win.blit(text, text_rect)
                if self.keys[pygame.K_SPACE]:
                    self.white_screen_bool = True
                    self.switch_place = True
            else:
                text = RenderText("Go to the Wizard", math.floor(20*self.val), (0, 0, 0), "MS Gothic", True)
                text_rect = text.get_rect(topright=(self.minecart.blit_x, self.minecart.blit_y))
                self.win.blit(text, text_rect)

        if self.current_place == 1 or self.current_place == 2 or self.current_place == 3:
            if ((self.current_place == 1 and len(self.slime_group) == 0) or (self.current_place == 3 and len(self.droid_group) == 0) or self.current_place == 2)  and self.player.rect.colliderect(self.portal.rect):
                if self.keys[pygame.K_SPACE]:
                    self.white_screen_bool = True
                    self.switch_place = True
                else:
                    text = RenderText("Press SPACE", math.floor(20*self.val), (0, 0, 0), "MS Gothic", True)
                    text_rect = text.get_rect(topright=(self.portal.blit_x, self.portal.blit_y))
                    self.win.blit(text, text_rect)

        if (self.current_place == 0 or self.current_place == 2) and self.player.hitbox_rect.colliderect(self.wizard.hitbox_rect):
            if self.keys[pygame.K_SPACE]:
                self.character_counter = 1
                self.character_wait = 3
                self.text_from = 0
                self.show_text = True
                if self.current_place == 0:
                    self.text_which = 0
                else:
                    self.text_which = 1
            elif not self.show_text:
                text = RenderText("Press SPACE", math.floor(20*self.val), (0, 0, 0), "MS Gothic", True)
                text_rect = text.get_rect(topright=(self.wizard.blit_x, self.wizard.blit_y))
                self.win.blit(text, text_rect)

        if self.white_screen_bool:
            if (self.now - self.last_updated > 15):
                self.last_updated = self.now
                self.loading_screen()
        self.win.blit(self.white_screen, (0,0))

        if self.show_text:
            self.text, self.text_rect = self.wizard_text_first()
            self.win.blit(self.text, self.text_rect)
            if self.character_wait == 0:
                if self.character_counter < len(self.wizard_script[self.text_which])-1 and ((self.wizard_script[self.text_which][self.character_counter]+self.wizard_script[self.text_which][self.character_counter+1]) == "! " or (self.wizard_script[self.text_which][self.character_counter]+self.wizard_script[self.text_which][self.character_counter+1] == ". ")):
                    self.character_wait = 70
                else:
                    self.character_wait = 3
                self.character_counter += 1
                if self.character_counter < len(self.wizard_script[self.text_which]) and self.wizard_script[self.text_which][self.character_counter] == "|":
                    self.text_from = self.character_counter+1

                if self.character_counter == len(self.wizard_script[self.text_which]):
                    if self.text_which == 0:
                        self.show_text = False
                        self.player.got_sword = True
                        self.player.got_dash = True
                    else:
                        self.show_text = False
                        self.player.got_orb = True
                        self.player.got_jump = True
            else:
                self.character_wait -= 1

        if self.player.blit_y > 2000*self.val:
            self.player.health = 0

        if self.player.health <= 0:
            self.white_screen_bool = True
            self.dead = True
            self.switch_place = True

        if self.current_place == 4 and self.king.health <= 0 and len(self.droid_group) == 0:
            self.end = True

        return self.end
