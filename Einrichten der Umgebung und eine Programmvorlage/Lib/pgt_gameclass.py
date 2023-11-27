import pygame as pg
from pygame.locals import *
import pygame.sprite as sprite
import os
import math
import random
import pathlib
from pttools import *
import pgtools as pgt


class Function:
    def __init__(self, seconds, func, loops=None, **kwargs):
        self.__func = func
        self.kwargs = kwargs
        self.seconds = seconds
        self.loops = loops
        self.done = False
        self.__next_run = pg.time.get_ticks() + seconds * 1000

    def execute(self):
        if self.done:
            return
        tm = pg.time.get_ticks()
        if tm >= self.__next_run:
            self.__func(**self.kwargs)
            self.__next_run = tm + self.seconds * 1000
            if self.loops is not None:
                self.loops -= 1
                if self.loops <= 0:
                    self.done = True

class Game:
    """Basisklasse für jedes Game"""
    def __init__(self, title=" ", *, width=300, height=200, fps=60, fontsize=30, bgcolor='black'):
        # Konfiguration vorbereiten
        pg.init()
        self._fps = fps
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)

        # Standardverzeichnisse
        self.data = "data"

        self.clock = pg.time.Clock()
        self.functions = []
        self.dt = 0
        self.done = False

        # Standardfont erstellen
        self.font = pg.font.Font(None, fontsize)

        self.bgcolor = bgcolor
        self.background = self.create_background()
        self.background.fill(self.bgcolor)

        # Spritegruppen vorbereiten
        self.visible_sprites = sprite.Group()
        self.player_sprites = sprite.Group()
        self.sprite_groups = [self.visible_sprites]

        # Boxxcolors
        self.rect_color = 'blue'
        self.box_color = 'red'
        self.show_boxes = []

        # Events weitergeben
        self.app_event = TraceVar()

    def __del__(self):
        pg.quit()

    def set_show_boxes(self, *args):
        self.show_boxes = [arg for arg in args]

    def create_background(self):
        background = pg.Surface(self.screen.get_size())
        background.fill(self.bgcolor)
        return background

    def create_group(self):
        group = sprite.Group()
        self.sprite_groups.append(group)

    def remove_group(self, group):
        self.sprite_groups.remove(group)

    def create_text(self, text, *, font=None, antialias=False, color='white', background=None):
        if not font: font = self.font
        return font.render(text, antialias, color, background)

    def function(self, seconds, func, *, loops=None, **kwargs):
        t = Function(seconds, func, loops=loops, **kwargs)
        self.functions.append(t)
        return t

    def after(self, seconds, func, **kwargs):
        self.function(seconds, func, loops=1, **kwargs)

    def _handle_event(self, event):
        """Events behandeln"""
        if event.type == pg.QUIT:
            self.done = True
        else:
            self.handle_event(event)
        self.app_event.value = event

    def run_tasks(self):
        for task in self.functions:
            task.execute()
        self.functions = [task for task in self.functions if not task.done]

    def stop(self):
        self.done = True

    def activate(self):
        """Wird direkt vor den Start des Programms aufgerufen"""
        pass

    def handle_event(self, event):
        """Events behandeln"""
        pass

    def update(self, dt):
        for group in self.sprite_groups:
            group.update(self.dt)

    def draw_background(self):
        """Hintergrund zeichnen"""
        self.screen.blit(self.background, (0, 0))

    def draw(self):
        """Elemente in Bildschirm (self.screen) zeichnen"""
        for group in self.sprite_groups:
            group.draw(self.screen)
        for group in self.show_boxes:
            for sprite in group:
                pg.draw.rect(self.screen, color=self.box_color, rect=sprite.hitbox(), width=1)
                pg.draw.rect(self.screen, color=self.rect_color, rect=sprite.rect, width=1)

    def run(self):
        self.activate()
        self.dt = 0
        while not self.done:
            # Events und Eingaben abfragen
            for event in pg.event.get():
                self._handle_event(event)

            # Tasks ausführen
            self.run_tasks()

            # Berechnungen
            self.update(self.dt)

            # Zeichnen
            self.draw_background()
            self.draw()
            pg.display.flip()

            self.dt = self.clock.tick(self._fps) / 1000
