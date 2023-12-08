import random
import pygame as pg
import pygame.sprite as sprite
from pygame.locals import *
import pgtools as pgt
import mygame


class Fist(pgt.GameObject):
    def __init__(self, game, *, pos=(0, 0), size=(50, 50), anchor='tl', active=True, visible=True,
                 tcolor=(0, 0, 0), group=None):
        super().__init__(game=game, pos=pos, size=size, anchor=anchor, active=active, visible=visible, tcolor=tcolor,
                         group=group)
        self.game: mygame.MyGame = game
        self.add(game.player_sprites)
        self.activate_events()

        img = pgt.Media.load_image('fist.png', colorkey=-1)
        self.set_image(img)

        self.normal_pos = pos
        self.punch_pos = pgt.Position(pos) + pgt.Position(30, -50)
        self.shrink_box(left=200, right=25)
        self.punching = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.punch()
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            self.punch()

    def punch(self):
        if not self.punching:
            pgt.Media.play_sound("whiff")
            self.pos = self.punch_pos
            self.punching = True
            self.after(0.2, self.unpunch)

    def unpunch(self):
        self.punching = False
        self.pos = self.normal_pos

