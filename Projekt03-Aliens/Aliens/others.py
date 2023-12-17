import random
import pygame as pg
import pygame.sprite as sprite
from pygame.locals import *
import pgtools as pgt
import mygame

class Alien(pgt.GameObject):
    def __init__(self, game, *, pos=(0, 0), size=(50, 50), anchor='tl', active=True, visible=True,
                 tcolor=(0, 0, 0), group=None):
        super().__init__(game=game, pos=pos, size=size, anchor=anchor, active=active, visible=visible, tcolor=tcolor,
                         group=group)
        self.game: mygame.MyGame = game
        self.add(game.other_sprites)
        # self.activate_events()

        img = pgt.Media.load_image('medfighter.png', height=50)
        img = pg.transform.rotate(img, 90)
        self.set_image(img)

        self.constraints(top=0, bottom=pgt.get_height())

        # self.speed = 200
        # self.direction.left()
        self.function(0.5, self.aendere_richtung_geschwindigkeit)

    def aendere_richtung_geschwindigkeit(self):
        self.speed = random.randint(150, 300)
        self.direction.deg = random.randint(130, 230)

