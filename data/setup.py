import pygame as pg
from . import constants

pg.init()
pg.display.set_caption(constants.name)
screen = pg.display.set_mode((constants.width, constants.height))
