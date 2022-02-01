import pygame as pg
import os

from data import setup


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


def draw_text_left(text, size, color, surface, rect):
    font = pg.font.SysFont("Calibri", size)
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = rect.topleft
    surface.blit(textobj, textrect)
    if textrect.width + textrect.x > setup.screen.get_width():
        setup.screen = pg.display.set_mode((textrect.width + textrect.x,
                                            setup.screen.get_height()))
