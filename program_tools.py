import pygame

def RenderText(string, size, color, fonttype = "Arial", bold = True):
    font = pygame.font.SysFont(fonttype, size, bold)
    text = font.render(string, True, color)
    return(text)
