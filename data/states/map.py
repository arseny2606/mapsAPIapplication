import json
import math

import pygame as pg

from .. import setup
from .. import constants
from ..components import button
from ..map_utils import get_map
import threading


class Map:
    def __init__(self):
        self.screen = setup.screen
        self.buttons = pg.sprite.Group()
        self.lat = constants.start_lat
        self.lon = constants.start_lon
        self.z = 17
        self.running = True
        self.mode = "map"
        self.map = get_map(f"ll={self.lon},{self.lat}&z={int(self.z)}", map_type=self.mode)
        self.buttons = pg.sprite.Group()
        button.Button(self.buttons, (0, 0))
        threading.Thread(target=self.get_map).start()
        self.draw_map()

    def get_map(self):
        while self.running:
            self.map = get_map(f"ll={self.lon},{self.lat}&z={int(self.z)}", map_type=self.mode)

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
            elif event.key == pg.K_UP:
                self.lat += constants.lat_step * math.pow(2, 13 - self.z)
            elif event.key == pg.K_DOWN:
                self.lat -= constants.lat_step * math.pow(2, 13 - self.z)
            elif event.key == pg.K_RIGHT:
                self.lon += constants.lon_step * math.pow(2, 13 - self.z)
            elif event.key == pg.K_LEFT:
                self.lon -= constants.lon_step * math.pow(2, 13 - self.z)
        while self.lon > 180:
            self.lon -= 360
        while self.lon < -180:
            self.lon += 360
        while self.lat > 85:
            self.lat -= 170
        while self.lat < -85:
            self.lat += 170
        self.draw_map()
        self.buttons.draw(self.screen)
        for i in self.buttons:
            state = i.update(clicks)
            if state:
                self.mode = state
        return False
