import pygame as pg
import os


def load_image(name):
    fullname = os.path.join('resources/textures', name)
    image = pg.image.load(fullname)
    return image


def draw_text(text, size, color, surface, rect):
    font = pg.font.SysFont("", size)
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = rect.center
    surface.blit(textobj, textrect)
