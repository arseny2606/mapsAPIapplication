import json

import pygame as pg
from .. import setup
from .. import constants


class Map:
    def __init__(self):
        self.screen = setup.screen
        self.buttons = pg.sprite.Group()
        rect = self.screen.get_rect()
        self.x = 0
        self.y = 0
        self.loading = True
        self.loader = 10

    def update(self, keys, clicks):
        return False