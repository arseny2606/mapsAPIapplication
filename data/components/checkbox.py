import pygame as pg
from .. import setup
from .. import utils


class CheckBox(pg.sprite.Sprite):
    def __init__(self, group, text, rect, checked=False):
        super().__init__(group)
        self.screen = setup.screen
        self.chk_image = utils.load_image("checkbox/checkbox.png")
        self.chk_hover_image = utils.load_image("checkbox/checkbox_hover.png")
        self.chk_checked_image = utils.load_image("checkbox/checkbox_checked.png")
        self.chk_hover_checked_image = utils.load_image("checkbox/checkbox_hover_checked.png")
        self.image = self.chk_image
        self.rect = self.image.get_rect()
        self.rect.center = rect.center
        self.center = self.rect.copy()
        self.rect.x += 100
        self.text = text
        self.old_time = 0.0
        self.time = pg.time.get_ticks()
        self.checked = checked

    def update(self, clicks):
        self.time = pg.time.get_ticks()
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if self.checked:
                self.image = self.chk_hover_checked_image
            else:
                self.image = self.chk_hover_image
        else:
            if self.checked:
                self.image = self.chk_checked_image
            else:
                self.image = self.chk_image
        utils.draw_text(self.text, 30, "white", self.screen, self.center)
        if self.rect.collidepoint(pg.mouse.get_pos()) and clicks[0] and self.old_time + 120 < self.time:
            self.old_time = self.time
            self.checked = not self.checked
            return self.text, self.checked
        return None
