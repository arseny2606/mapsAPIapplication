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
        self.z = 17
        self.map = get_map(f"ll={constants.start_lon},{constants.start_lat}&z={int(self.z)}")
        threading.Thread(target=self.get_map).start()
        self.draw_map()

    def get_map(self):
        while True:
            self.map = get_map(f"ll={constants.start_lon},{constants.start_lat}&z={int(self.z)}")

    def draw_map(self):
        self.screen.blit(self.map, (0, 0))

    def update(self, keys, clicks):
        if keys[pg.K_PAGEUP]:
            if self.z + 0.05 <= 17:
                self.z += 0.05
        if keys[pg.K_PAGEDOWN]:
            if self.z - 0.05 >= 0.05:
                self.z -= 0.05

        print(self.z)
        self.draw_map()
        return False
