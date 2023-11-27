import random
import pygame as pg
import pygame.sprite as sprite
from pygame.locals import *
import pgtools as pgt
import mygame

class Gegner(pgt.GameObject):
    def __init__(self, game, *, pos=(0, 0), size=(50, 50), anchor='tl', active=True, visible=True,
                 tcolor=(0, 0, 0), group=None):
        super().__init__(game=game, pos=pos, size=size, anchor=anchor, active=active, visible=visible, tcolor=tcolor,
                         group=group)
        self.game: mygame.MyGame = game
        # self.activate_events()

        # Beispielcode
        radius = pgt.get_width(self.image) // 2
        center = pgt.get_center(self.image)
        pg.draw.circle(self.image, color='green', center=center, radius=radius)


    def set_image(self, image):
        super().set_image(image)

    def update(self, dt):
        super().update(dt)

    def handle_event(self, event):
        # Events müssen mit activate_events aktiviert werden!
        pass

