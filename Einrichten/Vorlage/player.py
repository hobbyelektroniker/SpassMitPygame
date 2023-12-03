import random
import pygame as pg
import pygame.sprite as sprite
from pygame.locals import *
import pgtools as pgt
import mygame


class Spieler(pgt.GameObject):
    def __init__(self, game, *, pos=(0, 0), size=(50, 50), anchor='tl', active=True, visible=True,
                 tcolor=(0, 0, 0), group=None):
        super().__init__(game=game, pos=pos, size=size, anchor=anchor, active=active, visible=visible, tcolor=tcolor,
                         group=group)
        self.game: mygame.MyGame = game
        self.add(game.player_sprites)
        # self.activate_events()

        # Beispielcode
        self.image.fill('blue')
        self.speed = 200
        self.keyboard_move(up=pg.K_UP, down=pg.K_DOWN, left=pg.K_LEFT, right=pg.K_RIGHT)

    def update(self, dt):
        super().update(dt)

    def handle_event(self, event):
        # Events müssen mit activate_events aktiviert werden!
        pass

