import json

import pygame as pg

from .. import setup
from .. import constants
from ..map_utils import get_map
import threading


class Map:
    def __init__(self):
        self.screen = setup.screen
        self.buttons = pg.sprite.Group()
        rect = self.screen.get_rect()
        self.x = 0
        self.y = 0
        self.loading = True
        self.loader = 10
        self.spn = 0.005
        self.map = get_map(f"ll={constants.start_lon},{constants.start_lat}&spn={self.spn},{self.spn}")
        threading.Thread(target=self.get_map).start()
        self.draw_map()

    def get_map(self):
        while True:
            self.map = get_map(f"ll={constants.start_lon},{constants.start_lat}&spn={self.spn},{self.spn}")

    def draw_map(self):
        self.screen.blit(self.map, (0, 0))

    def update(self, keys, clicks):
        if keys[pg.K_PAGEUP]:
            if self.spn + 0.005 <= 0.18:
                self.spn += 0.005
        if keys[pg.K_PAGEDOWN]:
            if self.spn - 0.005 >= 0.005:
                self.spn -= 0.005
        print(self.spn)
        self.draw_map()
        return False
