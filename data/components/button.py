import pygame as pg
from .. import setup
from .. import utils


class Button(pg.sprite.Sprite):
    def __init__(self, group, text, rect):
        super().__init__(group)
        self.screen = setup.screen
        self.btn_image = utils.load_image("button/button.png")
        self.btn_hover_image = utils.load_image("button/button_hover.png")
        self.image = pg.transform.scale(self.btn_image, (rect.width, rect.height))
        self.rect = self.image.get_rect()
        self.rect.center = rect.center
        self.text = text

    def update(self, clicks):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.image = pg.transform.scale(self.btn_hover_image,
                                            (self.rect.width, self.rect.height))
        else:
            self.image = pg.transform.scale(self.btn_image, (self.rect.width, self.rect.height))
        utils.draw_text(self.text, 30, "white", self.screen, self.rect)
        if self.rect.collidepoint(pg.mouse.get_pos()) and clicks[0]:
            return self.text
        return False
