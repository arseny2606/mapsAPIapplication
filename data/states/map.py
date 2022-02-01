import json
import math

import pygame as pg

from .. import setup, utils
from .. import constants
from ..components import button, inputbox, picture_button, checkbox
from ..map_utils import get_map, get_coords, get, screen_to_geo, get_address, find, get_spn
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
        self.address = ""
        self.cached_address = ""
        self.additional_params = ""
        self.map = get_map(f"ll={self.lon},{self.lat}&z={int(self.z)}", map_type=self.mode)
        self.zip = False
        self.index = ""
        self.buttons = pg.sprite.Group()
        self.inputboxes = pg.sprite.Group()
        self.checkboxes = pg.sprite.Group()
        picture_button.PictureButton(self.buttons, (10, 460))
        self.search_input = inputbox.InputBox(self.inputboxes, "Введите адрес",
                                              pg.Rect(170, 480, 40, 10))
        button.Button(self.buttons, "Найти", pg.Rect(160, 500, 100, 30))
        button.Button(self.buttons, "Сброс", pg.Rect(160, 550, 100, 30))
        checkbox.CheckBox(self.checkboxes, "Индекс", pg.Rect(160, 650, 100, 30))
        threading.Thread(target=self.get_map).start()
        self.draw_map()

    def get_map(self):
        while self.running:
            try:
                self.map = get_map(f"ll={self.lon},{self.lat}&z={int(self.z)}{self.additional_params}",
                                   map_type=self.mode)
            except Exception:
                self.additional_params = ""
                self.map = get_map(
                    f"ll={self.lon},{self.lat}&z={int(self.z)}{self.additional_params}",
                    map_type=self.mode)

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
        self.checkboxes.draw(self.screen)
        for i in self.inputboxes:
            state = i.update(clicks, keys, key_events)
            if state:
                self.address = state[1]
        for i in self.buttons:
            state = i.update(clicks)
            if state == "Найти":
                self.find_object()
            elif state == "Сброс":
                self.clear_object()
            elif state:
                self.mode = state
        for i in self.checkboxes:
            state = i.update(clicks)
            if state:
                self.zip = state[1]
                if self.zip:
                    try:
                        self.index = \
                            get(self.cached_address)["metaDataProperty"]["GeocoderMetaData"][
                                "Address"][
                                "postal_code"]
                    except KeyError:
                        self.index = ""
                else:
                    self.index = ""
        if self.zip and self.cached_address and self.index:
            utils.draw_text_left(f"{self.index}, {self.cached_address}", 30, "white", self.screen,
                                 pg.Rect(160, 600, 100, 30))
        else:
            utils.draw_text_left(self.cached_address, 30, "white", self.screen,
                                 pg.Rect(160, 600, 100, 30))
        if clicks[0]:
            mouse_pos = pg.mouse.get_pos()
            if mouse_pos[0] <= constants.map_width and mouse_pos[1] <= constants.map_height:
                try:
                    self.additional_params = ""
                    self.cached_address = ""
                    geo_pos = screen_to_geo(self, mouse_pos)
                    self.additional_params = f"&pt={geo_pos[0]},{geo_pos[1]},org"
                    address = get_address(geo_pos)
                    self.cached_address = address
                    try:
                        self.index = get(self.cached_address)["metaDataProperty"]["GeocoderMetaData"] \
                            ["Address"]["postal_code"]
                    except Exception:
                        self.index = ""
                except Exception:
                    self.additional_params = ""
                    self.cached_address = ""
        return False

    def find_object(self):
        address_coords = get_coords(self.address)
        self.cached_address = self.address
        self.lon, self.lat = address_coords
        self.additional_params = f"&pt={self.lon},{self.lat},org"
        self.index = get(self.cached_address)["metaDataProperty"]["GeocoderMetaData"]["Address"][
            "postal_code"]

    def clear_object(self):
        self.additional_params = ""
        self.cached_address = ""
        self.address = ""
        for i in self.inputboxes:
            i.clear_text()
