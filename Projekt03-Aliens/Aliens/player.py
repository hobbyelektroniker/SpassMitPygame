import random
import pygame as pg
import pygame.sprite as sprite
from pygame.locals import *
import pgtools as pgt
import mygame


class Raumschiff(pgt.GameObject):
    def __init__(self, game, *, pos=(0, 0), size=(50, 50), anchor='tl', active=True, visible=True,
                 tcolor=(0, 0, 0), group=None):
        super().__init__(game=game, pos=pos, size=size, anchor=anchor, active=active, visible=visible, tcolor=tcolor,
                         group=group)
        self.game: mygame.MyGame = game
        self.add(game.player_sprites)

        img = pgt.Media.load_image('bgbattleship.png', height=100)
        img = pg.transform.rotate(img, -90)
        self.set_image(img)

        self.speed = 400
        self.keyboard_move(left=pg.K_LEFT, right=pg.K_RIGHT, up=pg.K_UP, down=pg.K_DOWN)
        self.constraints(top=0, bottom=pgt.get_height(), left=0, right=pgt.get_width() * 3 // 4)



