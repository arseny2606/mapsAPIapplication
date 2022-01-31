import pygame as pg
import json

from . import constants
from . import setup
from .states import map


class Control:
    def __init__(self, states):
        self.screen = setup.screen
        self.running = True
        self.clock = pg.time.Clock()
        self.fps = constants.fps
        self.keys = pg.key.get_pressed()
        self.clicks = pg.mouse.get_pressed()
        self.states = states
        self.previous = []
        self.state = self.states["map"]
        if callable(self.state):
            self.state = self.state()
        self.font = pg.font.SysFont("Arial", 25)
        self.fps_text = None

    def event_loop(self):
        key_events = []
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                key_events.append(event)
            if event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.clicks = pg.mouse.get_pressed()
            if event.type == pg.MOUSEBUTTONUP:
                self.clicks = pg.mouse.get_pressed()
        return key_events

    def update(self, key_events):
        self.screen.fill((0, 0, 0))
        state = self.state.update(self.keys, self.clicks)
        if state == "exit":
            self.running = False
        elif state == "back":
            self.state = self.previous[-1]
            if callable(self.state):
                self.state = self.state()
            del self.previous[-1]
        elif state:
            self.previous.append(self.state)
            self.state = self.states[state]
            if callable(self.state):
                self.state = self.state()
        if self.fps_text is not None:
            self.screen.blit(self.fps_text, (10, 0))
        pg.display.update()

    def main(self):
        while self.running:
            key_events = self.event_loop()
            self.update(key_events)
            self.clock.tick(self.fps)


def main():
    states = {"map": map.Map()}
    control = Control(states)
    control.main()
