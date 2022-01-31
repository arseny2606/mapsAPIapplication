import pygame as pg
from .. import setup
from .. import utils


class Button(pg.sprite.Sprite):
    def __init__(self, group, rect):
        super().__init__(group)
        self.screen = setup.screen
        self.btn_image = utils.load_image("mode/map.png")
        self.btn_image = pg.transform.scale(self.btn_image, (100, 100))
        self.btn_image_satellite = utils.load_image("mode/satellite.png")
        self.btn_image_satellite = pg.transform.scale(self.btn_image_satellite, (100, 100))
        self.btn_image_hybrid = utils.load_image("mode/hybrid.png")
        self.btn_image_hybrid = pg.transform.scale(self.btn_image_hybrid, (100, 100))
        self.image = self.btn_image
        self.rect = self.image.get_rect()
        self.rect.x = rect[0]
        self.rect.y = rect[1]
        self.mode = "map"
        self.text = "map"
        self.time = pg.time.get_ticks()
        self.old_time = 0.0

    def update(self, clicks):
        self.text = {"map": "map", "sat": "satellite", "sat,skl": "hybrid"}[self.mode]
        txt_rect = self.rect.copy()
        txt_rect.y += 70
        utils.draw_text(self.text, 30, "white", self.screen, txt_rect)
        pg.draw.rect(self.screen, "blue", self.rect, 2)
        self.time = pg.time.get_ticks()
        if self.rect.collidepoint(pg.mouse.get_pos()) and clicks[0] and self.old_time + 120 < self.time:
            if self.mode == "map":
                self.mode = "sat"
                self.image = self.btn_image_satellite
            elif self.mode == "sat":
                self.mode = "sat,skl"
                self.image = self.btn_image_hybrid
            elif self.mode == "sat,skl":
                self.mode = "map"
                self.image = self.btn_image
            self.old_time = self.time
            return self.mode
        return False
