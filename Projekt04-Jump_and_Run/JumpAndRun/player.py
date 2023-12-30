import random
import pygame as pg
import pygame.sprite as sprite
from pygame.locals import *
import pgtools as pgt
import mygame


class Spieler(pgt.AnimatedGameObject):
    def __init__(self, game, pos=(0, 0), size=(50, 50), anchor='tl', active=True, visible=True,
                 tcolor=(0, 0, 0), group=None):
        super().__init__(game=game, pos=pos, size=size, anchor=anchor, active=active, visible=visible, tcolor=tcolor,
                         group=group)
        self.game: mygame.MyGame = game
        self.add(game.player_sprites)
        self.activate_events()

        self.load_animation("run__*.png")
        self.mass = 1
        self.start_pos = self.pos

    def update(self, dt):
        super().update(dt)
        self.fps = self.game.speed / 10
        if not self.animating and not self.gravity_move():
            self.start_animating()

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if self.gravity_move():
                    self.impulse = 25
                    self.start_animating(0.5)
                else:
                    self.impulse = 350
                    self.stop_animating()

    def hit(self):
        self.pos = self.start_pos
        self.set_image(pg.transform.rotate(self.image, -90))
        self.active = False


