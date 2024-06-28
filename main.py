import pygame
import math
from program_tools import RenderText
from StartingPoint import StartingPoint
from Menu import Menu

pygame.init()
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
win_width, win_height = win.get_size()
clock = pygame.time.Clock()
pygame.font.init()

tile_size = win_width/24
val = round((tile_size*24/5)/384, 3)
pygame.mouse.set_visible(False)

fps_now = 0

end_text = RenderText("Thank you for playing with RHEN!", math.floor(90 * val), (255, 255, 255), "MS Gothic", False)
end_text_rect = end_text.get_rect(center=(win_width / 2, win_height / 2 - 100*val))

text1_background = pygame.Surface((end_text_rect.width, end_text_rect.height))
text1_background_rect = text1_background.get_rect(center=(end_text_rect.centerx, end_text_rect.centery))
text1_background.fill("#7e0a05")

end_text2 = RenderText("I hope you enjoyed it :)", math.floor(50 * val), (255, 255, 255), "MS Gothic", False)
end_text2_rect = end_text2.get_rect(center=(win_width / 2, win_height / 2 + 100*val))

end_text3 = RenderText("Press ESC to exit", math.floor(25 * val), (255, 255, 255), "MS Gothic", False)
end_text3_rect = end_text3.get_rect(center=(win_width / 2, win_height - 50*val))

def ShowFPS():
    global win
    global fps_now
    fps_now = math.floor(clock.get_fps())
    current_fps = RenderText("FPS:" + str(fps_now), 20, (255, 255, 255), "MS Gothic", False)
    fps_rect = current_fps.get_rect(topright=(win_width, 0))
    win.blit(current_fps, (fps_rect))

starting = StartingPoint(win, tile_size)
menu = Menu(win, tile_size, win_width, win_height)

start = False
end = False
run = True

frame_pos = 0
inventory_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

            for i in range(len(inventory_keys)):
                if event.key == inventory_keys[i]:
                    frame_pos = i

        if event.type == pygame.MOUSEWHEEL:
            frame_pos -= event.y
            if frame_pos > 8:
                frame_pos = 0
            if frame_pos < 0:
                frame_pos = 8

    time = clock.get_time()
    if not end:
        if not start:
            start, run = menu.update()
        else:
            end = starting.update(win_width, win_height, frame_pos, time)
    else:
        win.fill((0, 0, 0))
        win.blit(text1_background, (text1_background_rect.x, text1_background_rect.y))
        win.blit(end_text, (end_text_rect.x, end_text_rect.y))
        win.blit(end_text2, (end_text2_rect.x, end_text2_rect.y))
        win.blit(end_text3, (end_text3_rect.x, end_text3_rect.y))

    ShowFPS()
    pygame.display.update()
    clock.tick(60)
pygame.quit()