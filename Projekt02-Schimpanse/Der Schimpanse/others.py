import random
import pygame as pg
import pygame.sprite as sprite
from pygame.locals import *
import pgtools as pgt
import mygame

class Chimp(pgt.GameObject):
    def __init__(self, game, *, pos=(0, 0), size=(50, 50), anchor='tl', active=True, visible=True,
                 tcolor=(0, 0, 0), group=None):
        super().__init__(game=game, pos=pos, size=size, anchor=anchor, active=active, visible=visible, tcolor=tcolor,
                         group=group)
        self.game: mygame.MyGame = game

        img = pgt.Media.load_image('chimp.png', colorkey=-1)
        self.set_image(img)
        self.original = img

        self.speed = 200
        self.direction = pgt.Direction(1)
        self.rotation = 0
        self.change_anchor('c')  # Die Rotation erfolgt um das Zentrum

    def update(self, dt):
        super().update(dt)
        if self.rotation:
            img = pg.transform.rotate(self.original, self.rotation)
            self.set_image(img)
            self.rotation += 12
            if self.rotation > 360:
                self.set_image(self.original)
                self.rotation = 0
        if self.rect.right < 0 or self.rect.left > pgt.get_width():
            self.direction *= -1
            self.image = pg.transform.flip(self.image, True, False)

    def spin(self):
        if not self.rotation:
            self.original = self.image  # Zustand vor Rotation speichern
            pgt.Media.play_sound('punch')
            self.rotation = 12




