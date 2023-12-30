import random
import pygame as pg
import pygame.sprite as sprite
from pygame.locals import *
import pgtools as pgt
import mygame

class Kaktus(pgt.GameObject):
    def __init__(self, game, pos=(0, 0), size=(50, 50), anchor='tl', active=True, visible=True,
                 tcolor=(0, 0, 0), group=None):
        super().__init__(game=game, pos=pos, size=size, anchor=anchor, active=active, visible=visible, tcolor=tcolor,
                         group=group)
        self.game: mygame.MyGame = game
        self.add(game.other_sprites)
        height = random.randint(50, 300)
        img = pgt.Media.load_image("cactus.png", height=height)
        self.set_image(img)

        # Bewegung nach links
        self.direction.left()
        self.speed = self.game.speed

    def hit(self):
        self.set_image(pg.transform.rotate(self.image, -90))
        self.active = False

    def update(self, dt):
        super().update(dt)
        self.speed = self.game.speed
        if self.rect.right < 0:
            self.game.punkte.value += 1
            self.kill()


