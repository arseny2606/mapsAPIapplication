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
        self.x = 0
        self.y = 0
        self.z = 17
        self.running = True
        self.map = get_map(f"ll={constants.start_lon},{constants.start_lat}&z={int(self.z)}")
        threading.Thread(target=self.get_map).start()
        self.draw_map()

    def get_map(self):
        while self.running:
            self.map = get_map(f"ll={constants.start_lon},{constants.start_lat}&z={int(self.z)}")

    def draw_map(self):
        self.screen.blit(self.map, (0, 0))

    def update_event(self, event):
        self.running = False

    def update(self, keys, clicks, key_events):
        for event in key_events:
            if event.key == pg.K_PAGEUP:
                if self.z + 1 <= 17:
                    self.z += 1
            elif event.key == pg.K_PAGEDOWN:
                if self.z - 1 >= 0:
                    self.z -= 1
        self.draw_map()
        return False
