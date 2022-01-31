import pygame as pg
from .. import setup, constants
from .. import utils


class InputBox(pg.sprite.Sprite):
    def __init__(self, group, label, rect):
        super().__init__(group)
        self.screen = setup.screen
        self.font = pg.font.SysFont("Arial", 32)
        self.input_box = pg.Rect(100, 100, 140, 32)
        self.color_inactive = pg.Color('lightskyblue3')
        self.color_active = pg.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.rect = self.input_box
        self.rect.center = rect.center
        self.center = self.rect.copy()
        self.rect.x += 150
        self.label = label
        self.text = ""
        self.old_time = 0.0
        self.time = pg.time.get_ticks()
        self.width = 200

    def update(self, clicks, keys, key_events):
        self.time = pg.time.get_ticks()
        utils.draw_text(self.label, 30, "white", self.screen, self.center)
        if self.old_time + 120 < self.time:
            if clicks[0]:
                if self.rect.collidepoint(pg.mouse.get_pos()):
                    self.old_time = self.time
                    self.active = not self.active
                else:
                    self.active = False
                self.color = self.color_active if self.active else self.color_inactive
        for event in key_events:
            if self.active:
                if event.key == pg.K_RETURN:
                    return self.label, self.text
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                    if setup.screen.get_width() > constants.width:
                        setup.screen = pg.display.set_mode(
                            (self.width + self.input_box.x, setup.screen.get_height()))
                else:
                    self.text += event.unicode
        txt_surface = self.font.render(self.text, True, self.color)
        self.width = max(200, txt_surface.get_width() + 10)
        self.input_box.w = self.width
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y))
        pg.draw.rect(self.screen, self.color, self.input_box, 2)
        if self.width + self.input_box.x > setup.screen.get_width():
            setup.screen = pg.display.set_mode((self.width + self.input_box.x,
                                                setup.screen.get_height()))
        return self.label, self.text

    def clear_text(self):
        self.text = ""
        txt_surface = self.font.render(self.text, True, self.color)
        self.width = max(200, txt_surface.get_width() + 10)
        if setup.screen.get_width() > constants.width:
            setup.screen = pg.display.set_mode((constants.width, constants.height))
