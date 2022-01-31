import json

import pygame as pg

from .. import setup
from .. import constants
from ..map_utils import get_map


class Map:
    def __init__(self):
        self.screen = setup.screen
        self.buttons = pg.sprite.Group()
        rect = self.screen.get_rect()
        self.x = 0
        self.y = 0
        self.loading = True
        self.loader = 10
        self.draw_map()

    def draw_map(self):
        map = get_map(f"ll={constants.start_lon},{constants.start_lat}&spn={0.005},{0.005}")
        self.screen.blit(map, (0, 0))

    def update(self, keys, clicks):
        self.draw_map()
        return False
